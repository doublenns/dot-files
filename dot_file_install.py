#!/usr/bin/env python
import os
import sys
import shutil
import distutils
from distutils import dir_util
if sys.version_info[0] == 2:
    import urllib2
elif sys.version_info[0] == 3:
    import urllib.request
    import urllib.error
else:
    print("Python version isn'2 2 or 3. Don't know how to proceed. Exiting")
    sys.exit(1)


def run_shell_cmd(cmd, *shell):
    # Might want to use a "try" or call.check in case Command fails
    if "shell" in shell.lower():
        process = subprocess.Popen(cmd,
                stdout=subprocess.PIPE, shell=True)
    else:
        process = subprocess.Popen(cmd.split(),
                stdout=subprocess.PIPE)
    output = process.communicate()[0]
    rc = process.returncode
    return output, rc


def check_dotlocations(users_homedir, dotlocations):
    '''
    Function to check if dotfiles already exist
    '''
    for dotlocation in dotlocations:
        if os.path.exists("{}/.{}".format(users_homedir, dotlocation)):
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
    except NameError:  # Fails because Python2 instead of 3
        try:
            response = urllib2.urlopen(download_url)
            with open(dest, "w") as dotfile:
                dotfile.write(response.read())
        except urllib2.HTTPError as e:
            print("Unable to download {} from GitHub. Error code: {}".format(
                download_url, e.code))
        except urllib2.URLError as e:
            print("Unable to download {} from GitHub. Reasone: {}".format(
                download_url, e.reason))
    # Python3 but fails because of HTTP/URL issues
    except urllib.error.HTTPError as e:
        print("Unable to download {} from GitHub. Error code: {}".format(
            download_url, e.code))
    except urllib.error.URLError as e:
        print("Unable to download {} from GitHub. Reasone: {}".format(
            download_url, e.reason))


def download_dir(download_url, dest):
    '''
    Function to download project subdirectory from Github
    '''
    run_shell_cmd("svn export " + download_url + " " + dest)


def deploy_dotfiles(users_homedir, dotfiles, dotdirs):
    '''
    Function deploys the dotfiles into the current user's home dir..
    1st checks to see if can copy the files from cloned repo, in the running
    script's directory. If not, downloads the files from GitHub repo.
    '''
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    gitrepo_raw_url = "https://raw.githubusercontent.com/doublenns/dot-files/master/"
    gitrepo_svn_url= "https://raw.githubusercontent.com/doublenns/dot-files/trunk/"

    for dotfile in dotfiles:
        # If dotfile is in calling script's path (cloned git repo)
        dotfile_full_path = "{}/{}".format(script_dirname, dotfile)
        if os.path.isfile(dotfile_full_path):
            shutil.copy(dotfile_full_path, "{}/.{}".format(users_homedir, dotfile))
            # print("Copied " + dotfile_full_path)
        # If dotfile NOT in script's path (downloaded/executed single file)
        else:
            dotfile_url = gitrepo_raw_url + dotfile
            dest = "{}/.{}".format(users_homedir, dotfile)
            download_file(dotfile_url, dest)

    for dotdir in dotdirs:
        # If dotdir is in calling script's path (cloned git repo)
        dotdir_full_path = "{}/{}".format(script_dirname, dotdir)
        if os.path.isdir(dotdir_full_path):
            distutils.dir_util.copy_tree(dotdir_full_path, "{}/.{}".format(users_homedir, dotdir))
            # print("Copied " + dotdir_full_path)
        # If dotdir NOT in script's path (downloaded/executed single file)
        else:
            dotdir_url = gitrepo_svn_url + dotfile
            dest = "{}/.{}".format(users_homedir, dotdir)
            download_dir(dotdir_url, dest)


def main():
    '''
    Script's main function
    '''
    users_homedir = os.path.expanduser("~")

    # Manually insert which dotfiles want to be managed here
    dotfiles = ("bash_profile"
                , "gitconfig"
                # , "dotfile_that_doesnt_exist"
                )
    dotdirs = ("vim"
                # , "dotdir_that_doesnt_exist"
                )

    dotlocations = dotfiles + dotdirs
    if check_dotlocations(users_homedir, dotlocations):
        global input
        # try: input = raw_input
        # except NameError: pass
        if hasattr(__builtins__, 'raw_input'):
            input = raw_input
        choice = input("This script will overwrite existing dotfiles. Proceed? [y/N]")
        if choice.lower() != "y":
            sys.exit(1)

    deploy_dotfiles(users_homedir, dotfiles, dotdirs)


if __name__ == "__main__":
    main()
    sys.exit(0)
