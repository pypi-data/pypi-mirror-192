from __future__ import annotations

import sys
from typing import TYPE_CHECKING


# TODO: use try/except ImportError when https://github.com/python/mypy/issues/1393 is fixed
if sys.version_info < (3, 10):
    # compatibility for python <3.10
    import importlib_metadata as metadata
else:
    from importlib import metadata

if TYPE_CHECKING:
    from collections.abc import Callable

# Ensures we don't get a [no-untyped-call] error when using importlib_metadata.
# See: https://mypy.readthedocs.io/en/stable/error_code_list2.html#check-that-no-untyped-functions-are-called-no-untyped-call  # noqa
get_version: Callable[[str], str] = metadata.version

__version__ = get_version("science_book")
