# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import subprocess
import sys
from shutil import rmtree

from decouple import config
from git import Repo

from .. import *
from ..dB._core import HELP
from ..loader import Loader
from . import *
from .utils import load_addons


def _after_load(loader, module, plugin_name=""):
    if not module or plugin_name.startswith("_"):
        return
    from strings import get_help

    if doc_ := get_help(plugin_name) or module.__doc__:
        try:
            doc = doc_.format(i=HNDLR)
        except Exception as er:
            loader._logger.exception(er)
            loader._logger.info(f"Error in {plugin_name}: {module}")
            return
        if loader.key in HELP.keys():
            update_cmd = HELP[loader.key]
            try:
                update_cmd.update({plugin_name: doc})
            except BaseException as er:
                loader._logger.exception(er)
        else:
            try:
                HELP.update({loader.key: {plugin_name: doc}})
            except BaseException as em:
                loader._logger.exception(em)


def load_other_plugins(addons=None, pmbot=None, manager=None, vcbot=None):

    # for official
    _exclude = udB.get_key("EXCLUDE_OFFICIAL") or config("EXCLUDE_OFFICIAL", None)
    _exclude = _exclude.split() if _exclude else []

    # "INCLUDE_ONLY" was added to reduce Big List in "EXCLUDE_OFFICIAL" Plugin
    _in_only = udB.get_key("INCLUDE_ONLY") or config("INCLUDE_ONLY", None)
    _in_only = _in_only.split() if _in_only else []
    Loader().load(include=_in_only, exclude=_exclude, after_load=_after_load)

  # vc bot
    if vcbot and not vcClient._bot:
        try:
            import pytgcalls  # ignore: pylint

            if os.path.exists("vcbot"):
                if os.path.exists("vcbot/.git"):
                    subprocess.run("cd vcbot && git pull", shell=True)
                else:
                    rmtree("vcbot")
            if not os.path.exists("vcbot"):
                subprocess.run(
                    "git clone https://github.com/TeamUltroid/VcBot vcbot", shell=True
                )
            try:
                if not os.path.exists("vcbot/downloads"):
                    os.mkdir("vcbot/downloads")
                Loader(path="vcbot", key="VCBot").load(after_load=_after_load)
            except FileNotFoundError as e:
                LOGS.error(f"{e} Skipping VCBot Installation.")
        except ModuleNotFoundError:
            LOGS.error("'pytgcalls' not installed!\nSkipping loading of VCBOT.")
            
