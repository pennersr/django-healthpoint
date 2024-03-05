r"""
      ___           ___       __   __         ___
|__| |__   /\  |     |  |__| |__) /  \ | |\ |  |
|  | |___ /~~\ |___  |  |  | |    \__/ | | \|  |

"""  # noqa
VERSION = (1, 0, 0, "final", 0)

__title__ = "django-healthpoint"
__version_info__ = VERSION
__version__ = ".".join(map(str, VERSION[:3])) + (
    "-{}{}".format(VERSION[3], VERSION[4] or "") if VERSION[3] != "final" else ""
)
__author__ = "Raymond Penners"
__license__ = "MIT"
__copyright__ = "Copyright 2018-2024 Raymond Penners and contributors"
