"""Extend Invoke for Calcipy."""

import sys
from pathlib import Path

from beartype.typing import Any, Callable
from beartype import beartype
from beartype.typing import List
from invoke import Task, Collection, Config, Context, Program
from functools import wraps
from contextlib import suppress
import logging
from ._log import configure_logger
from invoke import task as invoke_task
from pydantic import BaseModel
from ._log import get_logger

logger = get_logger()


class GlobalTaskOptions(BaseModel):
    """Global Task Options."""

    file_args: List[Path]
    verbose: int

class _ShoalProgram(Program):
    """Customized version of Invoke's `Program`."""

    def print_help(self) -> None:
        """Extend print_help with shoal-specific global configuration.

        https://github.com/pyinvoke/invoke/blob/0bcee75e4a26ad33b13831719c00340ca12af2f0/invoke/program.py#L657-L667

        """
        super().print_help()
        print('Global Task Options:')  # noqa: T201
        print('')  # noqa: T201
        self.print_columns([
            ('*file_args', 'List of Paths available globally to all tasks'),
            ('verbose', 'Globally configure logger verbosity (-vvv for most verbose)'),
        ])
        print('')  # noqa: T201


@beartype
def start_program(pkg_name: str, pkg_version: str, module) -> None:
    """Run the customized Invoke Program.

    FYI: recommendation is to extend the `core_args` method, but this won't parse positional arguments:
    https://docs.pyinvoke.org/en/stable/concepts/library.html#modifying-core-parser-arguments

    """
    # Manipulate 'sys.argv' to hide arguments that invoke can't parse
    file_argv: List[Path] = []
    verbose_argv: int = 1
    sys_argv: List[str] = []
    last_argv = ''
    for argv in sys.argv:
        if not last_argv.startswith('-') and Path(argv).is_file():
            file_argv.append(Path(argv))
        elif argv in {'-v', '-vv', '-vvv', '--verbose'}:
            verbose_argv = argv.count('v')
        else:
            sys_argv.append(argv)
        last_argv = argv
    sys.argv = sys_argv

    class ShoalConfig(Config):

        gto: GlobalTaskOptions = GlobalTaskOptions(file_args=file_argv, verbose=verbose_argv)

    _ShoalProgram(
        name=pkg_name,
        version=pkg_version,
        namespace=Collection.from_module(module),
        config_class=ShoalConfig,
    ).run()


@beartype
def task(*task_args, **task_kwargs) -> Callable[[Any], Task]:
    """Wrapper to accept arguments for an invoke task."""
    @beartype
    def wrapper(func) -> Task:
        """Wraps the decorated task."""
        @invoke_task(*task_args, **task_kwargs)
        @beartype
        @wraps(func)
        def inner(ctx: Context, *args, **kwargs) -> Task:
            """Configure logging, then run actual task."""
            verbose = 2
            with suppress(AttributeError):
                verbose = ctx.config.gto.verbose
            log_lookup = {3: logging.NOTSET, 2: logging.DEBUG, 1: logging.INFO, 0: logging.WARNING}
            raw_log_level = log_lookup.get(verbose)
            configure_logger(log_level=logging.ERROR if raw_log_level is None else raw_log_level)

            print('')  # noqa: T201
            logger.info(f'Running {func.__name__}', summary=func.__doc__)
            logger.debug('Task arguments', args=args, kwargs=kwargs)

            return func(ctx, *args, **kwargs)
        return inner
    return wrapper
