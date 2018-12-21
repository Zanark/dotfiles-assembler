import os
import shutil
import getpass
import requests

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
        print(f)
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
        shutil.copytree(F , dest + F )

    for f in files:
        shutil.copyfile(f , dest + f )    

def copy_wallpapers():
    #   -   This function copies the wallpapers of the user
    #   -   The user will be asked if he has a diffrent folder containg the wallapers
    pass

#-----------------------------------------  GitHub and Vrsion Contolling  ---------------------------------------------

def local_database(*argv):
    #   -   Records provided data locally
    
    nixUser = getpass.getuser()

    path = os.path.join("/" , "home" , nixUser)
    dassPath = os.path.join(path , ".dotasss")

    if not os.path.isfile(dassPath):
        with open(dasspath, 'wb')as file:
				if(not len(argv)):
					data = {}
				else:
					data = argv
				file.write(data)				
	else:
		if(not len(argv)):
			with open(dasspath, 'rb') as file:
				data = file.read()				
		else:
			with open(dasspath,'wb') as file:
				data = argv
				file.write(data)

    return data

def add_user():
    #   -   Adds a user to the local file dattabase

    UserName = input("Enter your Username")
    Password = getpass.getpass("Enter your Password")

    if user_name in data.keys():
        print("User already exists")
    else:
        payload='{"scopes": ["admin:public_key", "admin:repo_hook", "delete_repo", "repo", "user"], "note": "Dotfiles Assembler"}'
        response=requests.post('https://api.github.com/authorizations',data=payload,auth=(UserName, Password))

        if response.status_code==201:
            data[user_name]=[response.json()['token'],response.json()['url']]
        
        file_handler(data)    

        print("USER ADDED!!")


def show_users():
    #   -   Displays the user data recorded in thelocal database

    data = local_database()
    
    users=[x for x in data]

		if len(users):
            for i in users:
                print(i)
        else:
            choice = input("No users in the database....Want to add a user? (y/n)")
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

    print("The regitred users are:")
    show_users()

    ch = input("Do you want to add a new user?? [y/n]")
    
    if ch == 'y':
        add_user()
    
    username = input("\n Enter your Username:\t")

    if username in data.keys():
		proname = "dotfiles"
		desc = input('A short description of the repository.')

        isPrivate = input("Is the repository private? [y/n]")
        if isPrivate == 'y':
            privy = True
        else:
            privy = False

		headers={"Authorization": "token "+data[username][0]}
        
		# proname = proname.strip().replace(' ', '-') #sanitization
		
		payload={"name": proname,"description": desc,"private": privy,"has_issues": True,"has_projects": True,"has_wiki": True}
		
		response=requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(payload))
		
		if response.status_code == 201:
			repo_url = response.json()['clone_url']
            print("Dotfiles pushed to GitHub @ " + repo_url)
			command="git remote add origin "+repo_url
			execute(command)
			print("REmote added successfully")

		else:
            print(response.json())
	else:
		print("User not found, please add a User and run the program again")
        add_user()

if_folders_exist()
