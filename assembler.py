import os
import shutil
import getpass
import requests
import json
import subprocess
import sys


def if_folders_exist():
    #   -   The function checks if the .themes, .icons ..etc folders are present in the $HOME directory or not
    #   -   If it cannot find them it creates an empty folder.
    
    reqd_folders = [".themes" , ".icons" , ".i3" , ".config" , ".mozilla" , ".fonts"]
    reqd_files = [".bashrc" , ".conkyrc"]
    exist_folders = []
    exist_files = []
    folders = os.popen("find -maxdepth 1").read().split("\n")
    for f in folders:
        f = f[2:]
        #print(f)
        if f in reqd_folders:
            exist_folders.append(f)
        elif f in reqd_files:
            exist_files.append(f)

    #print(exist_folders)
    #print(exist_files)
    
    copy_folders_to_dotfile_folder(exist_folders , exist_files)


def copy_folders_to_dotfile_folder(folders , files):
    #   -   This function copies all the files in the $HOME directory that must be copied to the dotfile dir
    #   -   The dotfile dir is the dir which gets pushed to GitHub
    #   -   Asks the user where to copy the files
    
    dest  = "./dotfiles/"
    
    if not (os.path.isdir(dest)):
        os.system("mkdir dotfiles")

    for F in folders:
        if os.path.exists(dest+F):
            shutil.rmtree(dest+F)
        print("Copying %s...." % str(F)  )
        shutil.copytree(F , dest + F )

    for f in files:
        print("Copying %s...." % str(f)  )
        shutil.copy(f , dest + f )

    print("\n\t\tFiles have been copied!!\n\n")
    push_to_GitHub()    

def copy_wallpapers():
    #   -   This function copies the wallpapers of the user
    #   -   The user will be asked if he has a diffrent folder containg the wallapers
    pass

#-----------------------------------------  GitHub and Vrsion Contolling  ---------------------------------------------

def execute(com):
    proc=subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout_value = proc.communicate()[0]
    print(stdout_value.decode("utf-8"))

def local_database(*argv):
    #   -   Records provided data locally
    
    nixUser = getpass.getuser()

    path = os.path.join("/" , "home" , nixUser)
    #dasspath = os.path.join(path , ".dotasss")
    dasspath = os.path.join(os.getcwd() , ".dotasss")

    #print(dasspath)

    if not os.path.isfile(dasspath):
        with open(dasspath, 'w')as file:
            if(not len(argv)):
                data = {}
            else:
                data = argv
            #file.write(data)
            json.dump(data, file)
    else:
        if(not len(argv)):
            with open(dasspath) as file:
                data = json.load(file)
        else:
            with open(dasspath,'w') as file:
                data = argv
                #file.write(data)
                json.dump(data, file)


    return data

def add_user():
    #   -   Adds a user to the local file dattabase

    data = local_database()

    Username = input("Enter your Username:\t")
    Password = getpass.getpass("Enter your Password:\t")


    payload='{"scopes": ["admin:public_key", "admin:repo_hook", "delete_repo", "repo", "user"], "note": "Dotfiles Assembler"}'
    response=requests.post('https://api.github.com/authorizations',data=payload,auth=(Username, Password))

    if response.status_code==201:
        data[Username]=[response.json()['token'],response.json()['url']]

    #print(response.json())
    
    local_database(data)    

    print("\nUSER ADDED!!\n")


def show_users():
    #   -   Displays the user data recorded in thelocal database

    data = local_database()    
    users=[x for x in data]
    if len(users):
        for i in users:
            print( " -- " + str(next(iter(i))) + "\n")
    else:
        choice = input("No users in the database....Want to add a user? (y/n) \t")
        if choice == 'y':
            add_user()
            

def push_to_GitHub():
    #   -   This function will push the contents of the directory to GitHub
    
    #   --  First a listof the users that have been registred will be shown
    #   --  User then enters his username
    #   --  If his username isnt present then he can add his username
    #   --  The user will be asked to enter the name of the repo and the files will be uploaded to that repo in a new branch
    #   --  The user can then merge it later
    #   --  The user can also add a gitignore later

    data = local_database()
    #print(data[0])
    
    print("\nThe regitred users are:\n")
    show_users()
    print("\n\n")

    ch = input("\nDo you want to add a new user?? [y/n] \t")
    
    if ch == 'y':
        add_user()
    
    username = input("\n Enter your Username:\t")

    data = local_database()

    if username in data[0].keys():
        proname = "dotfiles"
        desc = input('A short description of the repository. \t')
        
        isPrivate = input("Is the repository private? [y/n] \t")
        if isPrivate == 'y':
            privy = True
        else:
            privy = False
            
        headers={"Authorization": "token "+data[0][username][0]}
        
		# proname = proname.strip().replace(' ', '-') #sanitization
		
        payload={"name": proname,"description": desc,"private": privy,"has_issues": True,"has_projects": True,"has_wiki": True}
		
        response=requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(payload))
		
        if response.status_code == 201:
            repo_url = response.json()['clone_url']
            print("Repo created on GitHub @ " + repo_url)
            wd = os.getcwd()
            os.chdir(wd + "/dotfiles")
            command = "git init"
            execute(command)
            command = "git remote add origin "+repo_url
            execute(command)
            command = "git checkout -b mark1"
            execute(command)
            command = "git add . " 
            execute(command)
            commit_msg = input("\nEnter a commit message\n\t")
            command = "git commit -m \" "+commit_msg+" \"" 
            execute(command)
            print("\n\nPushing to GitHub........\n\n")
            command = "git push origin mark1"
            execute(command)
            print("Remote added and Data pushed to remote successfully")
            
        else:
            result = json.loads(response.text)

            if result['errors'][0]['message'] == "name already exists on this account":
                branchName = input("\nEnter a name for the new branch\n\t")
                
                repo_url = "https://github.com/%s/dotfiles.git" % username

                wd = os.getcwd()
                os.chdir(wd + "/dotfiles/")
                command = "git init"
                execute(command)
                command = "git remote add origin "+repo_url
                execute(command)
                command = "git checkout -b "+branchName 
                execute(command)
                command = "git add . " 
                execute(command)
                commit_msg = input("\nEnter a commit message\n\t")
                command = "git commit -m \" "+commit_msg+" \"" 
                execute(command)
                print("\n\nPushing to GitHub........\n\n")
                command = "git push origin "+branchName 
                execute(command)
                print("Remote added and Data pushed to remote successfully")
    else:
        print("\nUser not found, please add a User and run the program again\n\n")
        add_user()


if __name__ == '__main__':
    if_folders_exist()
