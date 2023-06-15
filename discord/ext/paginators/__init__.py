from typing import Literal, NamedTuple

from .callbacks import *
from .codeblocks import *
from .controller import *
from .paginators import *
from .types import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


__version_info__: VersionInfo = VersionInfo(major=0, minor=2, micro=0, releaselevel="alpha", serial=0)
__version__: str = "0.2.0a0"

__title__: str = "discord-ext-paginators"
__url__: str = "https://github.com/Axelancerr/discord-ext-paginators"

__author__: str = "Aaron Hennessey (Axelancerr)"
__email__: str = "axelancerr@gmail.com"

__license__: str = "MIT"
__copyright__: str = "Copyright (c), 2023-present, Aaron Hennessey (Axelancerr)"
