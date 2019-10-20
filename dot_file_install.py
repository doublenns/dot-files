#!/usr/bin/env python3
import os
import sys
import shutil
import distutils
import requests
import svn.remote


def check_dotlocations(users_homedir, dotlocations):
    '''
    Function to check if dotfiles already exist
    '''
    existing_files = []
    for dotlocation in dotlocations:
        if os.path.exists(f"{users_homedir}/.{dotlocation}"):
            existing_files.append("." + dotlocation)
    if existing_files:
        return existing_files
    return False


def download_file(download_url, dest):
    '''
    Function to download file from URL
    '''
    response = requests.get(download_url)
    if response:
        with open(dest, "wb") as f:
            f.write(response.content)


def download_dir(download_url, dest):
    '''
    Function to download project subdirectory from Github
    '''
    remote = svn.remote.RemoteClient(download_url)
    remote.export(dest)


def deploy_dotfiles(users_homedir, dotfiles, dotdirs):
    '''
    Function deploys the dotfiles into the current user's home dir..
    1st checks to see if can copy the files from cloned repo, in the running
    script's directory. If not, downloads the files from GitHub repo.
    '''
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    gitrepo_raw_url = "https://raw.githubusercontent.com/doublenns/dot-files/master/"
    gitrepo_svn_url = "https://github.com/doublenns/dot-files/trunk/"

    for dotfile in dotfiles:
        # If dotfile is in calling script's path (cloned git repo)
        dotfile_full_path = f"{script_dirname}/{dotfile}"
        if os.path.isfile(dotfile_full_path):
            shutil.copy(dotfile_full_path, f"{users_homedir}/.{dotfile}")
        # If dotfile NOT in script's path (downloaded/executed single file)
        else:
            dotfile_url = gitrepo_raw_url + dotfile
            dest_file = f"{users_homedir}/.{dotfile}"
            download_file(dotfile_url, dest_file)

    for dotdir in dotdirs:
        # If dotdir is in calling script's path (cloned git repo)
        dotdir_full_path = f"{script_dirname}/{dotdir}"
        if os.path.isdir(dotdir_full_path):
            distutils.dir_util.copy_tree(dotdir_full_path, f"{users_homedir}/.{dotdir}")
            # print("Copied " + dotdir_full_path)
        # If dotdir NOT in script's path (downloaded/executed single file)
        else:
            dotdir_url = gitrepo_svn_url + dotdir
            dest_dir = f"{users_homedir}/.{dotdir}"
            download_dir(dotdir_url, dest_dir)


def main():
    '''
    Script's main function
    '''
    users_homedir = os.path.expanduser("~")

    # Manually insert which dotfiles want to be managed here
    dotfiles = ("bash_profile", "gitconfig")
    dotdirs = ("vim", )

    dotlocations = dotfiles + dotdirs
    dot_conflict = check_dotlocations(users_homedir, dotlocations)
    if dot_conflict:
        dot_conflict_str = ", ".join(dot_conflict)
        print(f"You already have these files in your home directory: {dot_conflict_str}")
        choice = input("This script will overwrite existing dotfiles. Proceed? [y/N] ")
        if choice.lower() != "y":
            sys.exit(1)

    deploy_dotfiles(users_homedir, dotfiles, dotdirs)


if __name__ == "__main__":
    main()
    sys.exit(0)
