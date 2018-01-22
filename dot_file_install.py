#!/usr/bin/env python

import os
import sys
import shutil
if sys.version_info[0] == 2:
    import urllib2
elif sys.version_info[0] == 3:
    import urllib.request
    import urllib.error #import URLError, HTTPError
else:
    print("Python version isn'2 2 or 3. Don't know how to proceed. Exiting")
    sys.exit(1)


def check_dotfiles(users_homedir, dotfiles):
    for dotfile in dotfiles:
        if os.path.isfile( "{}/.{}".format(users_homedir, dotfile) ):
            return True
    return False


def download_file(download_url, dest):
    '''
    Function to download file from URL
    '''
    # Needs better error handling here. Only works now based on order
    # of error that occurs
    try:
        urllib.request.urlretrieve(download_url, dest)
    except NameError: # Fails because Python2 instead of 3
        try:
            response = urllib2.urlopen(download_url)
            with open(dest, "w") as dotfile:
                dotfile.write(response.read())
        except urllib2.HTTPError, e:
            print("Unable to download {} from GitHub. Error code: {}".format(
                download_url, e.code))
        except urllib2.URLError,e:
            print("Unable to download {} from GitHub. Reasone: {}".format(
                download_url, e.reason))
    # Python3 but fails because of HTTP/URL issues
    except urllib.error.HTTPError as e:
        print("Unable to download {} from GitHub. Error code: {}".format(
            download_url, e.code))
    except urllib.error.URLError as e:
        print("Unable to download {} from GitHub. Reasone: {}".format(
            download_url, e.reason))



def deploy_dotfiles(users_homedir, dotfiles):
    '''
    Function deploys the dotfiles into the current user's home dir..
    1st checks to see if can copy the files from cloned repo, in the running
    script's directory. If not, downloads the files from GitHub repo.
    '''

    script_dirname = os.path.dirname(os.path.abspath(__file__))
    gitrepo_raw_url = "https://raw.githubusercontent.com/doublenns/dot-files/master/"

    for dotfile in dotfiles:
        # If dotfile is in calling script's path (cloned git repo)
        dotfile_full_path = "{}/{}".format(script_dirname, dotfile)
        if os.path.isfile( dotfile_full_path ):
            shutil.copy(dotfile_full_path, "{}/.{}".format(users_homedir, dotfile))
            print("Copied " + dotfile_full_path)
        # If dotfile NOT in script's path (downloaded/executed single file)
        else:
            dotfile_url = gitrepo_raw_url + dotfile
            dest = "{}/.{}".format(users_homedir, dotfile)
            download_file(dotfile_url, dest)


def main():
    users_homedir = os.path.expanduser("~")
    dotfiles = ("vimrc",
                    "bash_profile",
                    "gitconfig",
                    "poop")

    if check_dotfiles(users_homedir, dotfiles):
        global input
        #try: input = raw_input
        #except NameError: pass
        if hasattr(__builtins__, 'raw_input'):
            input = raw_input
        choice = input("This script will overwrite existing dotfiles. Proceed? [y/N]")
        if choice.lower() != "y":
            sys.exit(1)

    deploy_dotfiles(users_homedir, dotfiles)


if __name__ == "__main__":
    main()
    sys.exit(0)
