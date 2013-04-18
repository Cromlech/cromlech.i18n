# -*- coding: utf-8 -*-

import logging
import os
from os.path import join
from stat import ST_MTIME

CAN_COMPILE = True
try:
    import polib
except ImportError:
    CAN_COMPILE = False


def compile_mo_file(pofile):
    """Creates or updates a mo file in the locales folder.
    """
    if not CAN_COMPILE:
        logging.critical(
            "Unable to compile messages: Python `polib` library missing.")
        return

    base, ext = os.path.splitext(pofile)
    mofile = base + '.mo'

    po_mtime = 0
    try:
        po_mtime = os.stat(pofile)[ST_MTIME]
    except (IOError, OSError):
        return

    mo_mtime = 0
    if os.path.exists(mofile):
        # Update mo file?
        try:
            mo_mtime = os.stat(mofile)[ST_MTIME]
        except (IOError, OSError):
            return

    if po_mtime > mo_mtime:
        try:
            po = polib.pofile(pofile)
            po.save_as_mofile(mofile)
            return mofile
        except (IOError, OSError):
            logging.warn('Error while compiling %s' % pofile)
