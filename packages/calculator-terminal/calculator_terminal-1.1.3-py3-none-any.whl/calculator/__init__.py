"""
Calculator In Terminal
~~~~~~~~~~~~~~~~~~~~

Una calculadora funcional en tus manos.

:copyright: (c) 2023-presente Developer Anonymous
:license: Apache, mira LICENSE para más detalles.
"""

__title__ = 'calculator'
__author__ = 'Developer Anonymous'
__license__ = 'Apache'
__copyright__ = 'Copyright 2023-presentado Developer Anonymous'
__version__ = '1.1.0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from .calculator import *

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int

version_info: VersionInfo = VersionInfo(major=1, minor=1, micro=0, releaselevel='beta', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo