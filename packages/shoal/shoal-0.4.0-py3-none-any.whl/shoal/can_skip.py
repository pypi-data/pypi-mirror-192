"""Support can-skip logic from Make."""

from pathlib import Path

from beartype import beartype
from beartype.typing import List


@beartype
def can_skip(*, prerequisites: List[Path], targets: List[Path]) -> bool:
    """Generic make-style task skipping logic based on file `mtime`.

    Example use with Invoke, but can be used anywhere:

    ```py
    @task
    def test(ctx: Context) -> None:
        if can_skip(prerequisites=[*Path('src').rglob('*.py')], targets=[Path('.coverage.xml')]):
            return  # Exit early

        ...  # Task code
    ```

    """
    ts_prerequisites = [pth.getmtime() for pth in prerequisites]
    if not ts_prerequisites:
        raise ValueError('Required files do not exist', prerequisites)

    # TODO: Triple check this logic (https://stackoverflow.com/a/22960700/3219667)
    ts_targets = [pth.getmtime() for pth in targets]
    if ts_targets and max(ts_prerequisites) >= min(ts_targets):
        logger.info('Skipping because targets are newer', targets=targets)
        return False
    return True
