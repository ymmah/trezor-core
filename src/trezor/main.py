import sys

sys.path.append('lib')

from typing import *
from trezor import loop
from trezor import workflow
from trezor import log

log.level = log.DEBUG


def run(default_workflow: Callable[[], Coroutine]) -> None:
    workflow.start_default(default_workflow)
    loop.run_forever()
