import os

def if_folders_exist():
    #The function checks if the .themes, .icons ..etc folders are present in the $HOME directory or not
    #If it cannot find them it creates an empty folder.

    reqd_folders = [".themes" , ".icons" , ".i3" , ".config"]
    reqd_files = [".bashrc" , ".conkyrc"]
    folders = os.popen("find -maxdepth 1").read().split("\n")


def copy_folders_to_dotfile_folder():
    #This function copies all the files in the $HOME directory that must be copied to the dotfile dir
    #The dotfile dir is the dir which gets pushed to GitHub

def copy_wallpapers():
    #This function copies the wallpapers of the user
    #The user will be asked if he has a diffrent folder containg the wallapers

def push_to_GitHub():
    #This function will push the contents of the directory to GitHub
    #The user will be asked to enter the name of the repo and the files will be uploaded to that repo in a new branch
    #The user can then merge it later
    #The user can also add a gitignore later
    #Will add the functionality of creating a repo from the command line itself later
