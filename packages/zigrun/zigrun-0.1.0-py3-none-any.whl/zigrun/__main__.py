import sys
from enum import Enum
from pathlib import Path

import click
import cloup

from . import ZigError, ZigRunner, ZigToolchain


class CodeKind(Enum):
    EXPR = "expression"
    STMT = "statement"

    def __str__(self) -> str:
        return self.value


@cloup.command()
@cloup.option_group(
    "Input kind",
    cloup.option(
        "--expr",
        "is_expr",
        flag_value="expr",
        is_flag=True,
        help="Evaluate an expression",
    ),
    cloup.option(
        "--stmt",
        "is_stmt",
        flag_value="stmt",
        is_flag=True,
        help="Evaluate statement(s)",
    ),
    constraint=(
        cloup.constraints.mutually_exclusive
        & cloup.constraints.If(
            cloup.constraints.IsSet("stdin"), then=cloup.constraints.require_one
        )
    ).rephrased(help="Mutually exclusive, and required if --stdin is set"),
)
@cloup.option_group(
    "Input source",
    cloup.option("--stdin", is_flag=True, help="Read input from stdin"),
    cloup.option(
        "--eval", "-e", "eval_expression", help="Execute the specified expression"
    ),
    cloup.option(
        "--exec", "-c", "exec_statement", help="Execute the specified statement"
    ),
    constraint=cloup.constraints.require_one,
)
@cloup.option("--zig", 'zig_bin', type=cloup.file_path(exists=True), help="The zig binary to use")
def zigrun(
    eval_expression: str,
    exec_statement: str,
    stdin: bool,
    zig_bin: Path | None,
    is_expr: bool,
    is_stmt: bool,
) -> None:
    kind: CodeKind | None
    if is_expr:
        kind = CodeKind.EXPR
    elif is_stmt:
        kind = CodeKind.STMT
    else:
            kind = None
    code: str | None = None

    def expect_kind(expected: CodeKind) -> None:
        nonlocal kind
        if kind is None:
            kind = expected
        elif kind == expected:
            pass
        else:
            raise click.ClickException(f"Expected a {expected}, got a {kind}")


    if stdin:
        assert kind is not None  # checked by cloup
        code = sys.stdin.read()
    elif eval_expression is not None:
        expect_kind(CodeKind.EXPR)
        code = eval_expression
    elif exec_statement is not None:
        expect_kind(CodeKind.STMT)
        code = exec_statement
    else:
        raise AssertionError
    assert kind is not None
    assert code is not None

    try:
        if zig_bin is not None:
            toolchain = ZigToolchain(name="custom", zig_bin=zig_bin)
        else:
            toolchain = ZigToolchain.from_env()

        runner = ZigRunner()
        match kind:
            case CodeKind.EXPR:
                runner.run_expr(toolchain, code)
            case CodeKind.STMT:
                runner.run_statements(toolchain, code.splitlines())
            case _:
                raise AssertionError   
    except ZigError as e:
        raise click.ClickException(str(e))

if __name__ == "__main__":
    zigrun()
