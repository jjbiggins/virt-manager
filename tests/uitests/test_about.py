# This work is licensed under the GNU GPLv2 or later.
# See the COPYING file in the top-level directory.

import datetime

from . import lib


###################################
# UI tests for the 'About' dialog #
###################################

def testAbout(app):
    app.root.find("Help", "menu").click()
    app.root.find("About", "menu item").click()
    win = app.root.find_fuzzy("About", "dialog")
    l = win.find_fuzzy("Copyright", "label")

    curyear = datetime.datetime.now().strftime("%Y")
    if curyear not in l.text:
        print(f"Current year={curyear} not in about.ui dialog!")

    win.keyCombo("<ESC>")
    lib.utils.check(lambda: win.visible is False)
