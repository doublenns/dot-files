#!/usr/bin/env python

import os
import sys
import shutil
import urllib


def check_dotfiles(users_homedir, dotfiles):
    for dotfile in dotfiles:
        if os.path.isfile( "{}/.{}".format(users_homedir, dotfile) ):
            return True
    return False


def copy_dotfiles(users_homedir, dotfiles):
    pass


def main():
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    users_homedir = os.path.expanduser("~")
    dotfiles = ("vimrc",
                    "bash_profile",
                    "poop")
    gitrepo_raw_url = "https://raw.githubusercontent.com/doublenns/dot-files/master/"

    if check_dotfiles(users_homedir, dotfiles):
        global input
        #try: input = raw_input
        #except NameError: pass
        if hasattr(__builtins__, 'raw_input'):
            input = raw_input
        choice = input("This script will overwrite existing dotfiles. Proceed? [y/N]")
        if choice.lower() != "y":
            sys.exit(1)

    for dotfile in dotfiles:
        # If dotfile is in calling script's path (cloned git repo)
        dotfile_full_path = "{}/{}".format(script_dirname, dotfile)
        if os.path.isfile( dotfile_full_path ):
            shutil.copy(dotfile_full_path, "{}/.{}".format(users_homedir, dotfile))
        # If dotfile NOT in script's path (downloaded/executed single file)
        else:
            dotfile_url = gitrepo_raw_url + dotfile
            urllib.urlretrieve(dotfile_url, "{}/.{}".format(users_homedir, dotfile))


if __name__ == "__main__":
    main()
    sys.exit(0)
