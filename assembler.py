import os

def if_folders_exist():
    #The function checks if the .themes, .icons ..etc folders are present in the $HOME directory or not
    #If it cannot find them it creates an empty folder.
    
    reqd_folders = [".themes" , ".icons" , ".i3" , ".config" , ".mozilla"]
    reqd_files = [".bashrc" , ".conkyrc"]
    exist_folders = []
    exist_files = []
    folders = os.popen("find -maxdepth 1").read().split("\n")
    #print(folders)
    for f in folders:
        f = f[2:]
        print(f)
        if f in reqd_folders:
            exist_folders.append(f)
        elif f in reqd_files:
            exist_files.append(f)

    #print(exist_folders)
    #print(exist_files)
    
    copy_folders_to_dotfile_folder(exist_folders , exist_files)


def copy_folders_to_dotfile_folder():
    #This function copies all the files in the $HOME directory that must be copied to the dotfile dir
    #The dotfile dir is the dir which gets pushed to GitHub
    
    dest  = "./dotfiles/"
    
    if not (os.path.isdir(dest)):
        os.system("mkdir dotfiles")

    for F in folders:
        shutil.copytree(F , dest + F )

    for f in files:
        shutil.copyfile(f , dest + f )    

def copy_wallpapers():
    #This function copies the wallpapers of the user
    #The user will be asked if he has a diffrent folder containg the wallapers

def push_to_GitHub():
    #This function will push the contents of the directory to GitHub
    #The user will be asked to enter the name of the repo and the files will be uploaded to that repo in a new branch
    #The user can then merge it later
    #The user can also add a gitignore later
    #Will add the functionality of creating a repo from the command line itself later
