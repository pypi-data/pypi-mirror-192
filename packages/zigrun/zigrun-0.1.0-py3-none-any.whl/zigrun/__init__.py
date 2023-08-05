from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import KW_ONLY, dataclass, field
from pathlib import Path
from typing import Any

import jinja2

from ._version import __version__


@dataclass
class ZigToolchain:
    name: str
    zig_bin: Path = field(kw_only=True)
    version: str = field(init=False)

    def __post_init__(self) -> None:
        assert isinstance(self.zig_bin, Path)
        if not os.access(self.zig_bin, os.X_OK | os.F_OK | os.R_OK):
            raise ZigToolchainError(
                f"Unable to access binary {self.zig_bin}", toolchain=self
            )
        self.version = "?"
        self.version = self.capture_stdout("version").rstrip()

    @staticmethod
    def from_env() -> ZigToolchain:
        if (custom_zig := os.getenv("ZIGRUN_ZIG")) is not None:
            return ZigToolchain(name="$ZIGRUN_ZIG", zig_bin=Path(custom_zig))
        elif (system_zig := shutil.which("zig")) is not None:
            return ZigToolchain(name="system", zig_bin=Path(system_zig))
        else:
            raise ZigToolchainError("Unable to find `zig` command", toolchain=None)

    def capture_stdout(self, *cmd: str | Path, **kwargs: Any) -> str:
        return self.direct_run(*cmd, stdout=subprocess.PIPE).stdout

    def direct_run(
        self, *cmd: str | Path, **kwargs: Any
    ) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run([self.zig_bin, *cmd], encoding="UTF-8", check=True, **kwargs)
        except subprocess.CalledProcessError:
            res = ["Unable to execute `zig"]
            if cmd:
                res.append(" ")
                res.append(str(cmd[0]))
            res.append("`")
            raise ZigToolchainError("".join(res), toolchain=self)

    def __str__(self) -> str:
        return f"zig {self.version} ({self.name})"


class ZigError(RuntimeError):
    pass


class ZigToolchainError(ZigError):
    toolchain: ZigToolchain | None

    def __init__(self, msg: str, *, toolchain: ZigToolchain | None):
        if toolchain is not None:
            msg += f" with {toolchain}"
        super().__init__(msg)
        self.toolchain = toolchain


class ZigRunner:
    environment: jinja2.Environment
    _mainfile_template: jinja2.Template

    def __init__(self) -> None:
        self.environment = jinja2.Environment(
            loader=jinja2.PackageLoader("zigrun"), autoescape=False
        )
        self._mainfile_template = self.environment.get_template("main.zig.jinja2")

    def run_expr(self, toolchain: ZigToolchain, expr: str) -> None:
        self._run(toolchain, ctx={"zig_expression": expr}, code_kind="expression")

    def run_statements(self, toolchain: ZigToolchain, expr: list[str]) -> None:
        self._run(toolchain, ctx={"zig_statements": expr}, code_kind="statements")

    def _run(
        self, toolchain: ZigToolchain, *, ctx: dict[str, object], code_kind: str
    ) -> None:
        with tempfile.NamedTemporaryFile(
            mode='w+',
            prefix="main", suffix=".zig", encoding="utf-8"
        ) as f:
            self._mainfile_template.stream(ctx).dump(f)
            f.flush()
            try:
                toolchain.direct_run("run", f.name)
            except ZigToolchainError as e:
                raise ZigRunError(f"Unable to run {code_kind}", toolchain=e.toolchain)


class ZigRunError(ZigToolchainError):
    pass
