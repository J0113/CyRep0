# We are Importing some Modules. These modules are needed make the program work! Make sure to install BZ2 and EasyGUI.
import os
import easygui
import sys
import shutil
import bz2
import hashlib
import re
from pathlib import Path

# Terminal/ CMD cleaner
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
cls()

# For updating the repo, we want to calculate the MD5 Hash
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

# Welcome Screen
easygui.msgbox(msg="Welcome to CyRep0! \nCyRep0 is a free OpenSource Cydia Repo Manager made By @J0113 in Python.", title="Welcome to CyRep0!", ok_button="START!")

# Main Menu
menu = easygui.indexbox(msg="What do you want to do?", title="CyRep0",choices=["New Repo","Repo Manager","Info","Exit"])

# Creating a new Repo
if menu == 0:
	
	# Save Location
	easygui.msgbox(msg="Creating a new Repo!\nPlease create or select a folder.\nIn this folder all the repo file are going to be saved.", title="CyRep0", ok_button="Ok")
	while True:
		try:
			newrepolocation = easygui.diropenbox()
		except ValueError:
			continue
		if newrepolocation is None:
			continue
		else:
			break
	
	# Creating the Release file
	while True:
		try:
			newreponame = easygui.enterbox(msg="How should we call your Repo?", title="CyRep0")
		except ValueError:
			continue
		if newreponame is None:
			continue
		else:
			break
	
	Release = open(newrepolocation + "/Release","w+") 
	Release.write("Origin: " + newreponame + "\nLabel: " + newreponame + "\nSuite: stable\nVersion: 1.0\nCodename: CyRep0\nArchitectures: iphoneos-arm\nComponents: main\nDescription: " + newreponame)
	Release.close() 
	
	
	# Creating the Repo Homepage
	indextemplate = open("indextemplate.html","r") 
	while True:
		try:
			rootindex = easygui.codebox(msg="We are creating a homepage for your repo, don't worry you can always change this later.\nYou may use HTML here, maybe CyRep0 will have a HTML editor later for easier use.\nFor now, edit the template however you like or build your own! Press cancel if you don't want to create a homepage.", title="CyRep0", text=indextemplate)
		except ValueError:
			continue
		if rootindex is None:
			norootindex = easygui.ynbox(msg="You clicked cancel, are you sure that you don't want an homepage?", title="CyRep0")
			if norootindex is True:
				break
			elif norootindex is False:
				continue
			else:
				continue
		else:
			break
	
	if rootindex is None:
		pass
	else:
		Release = open(newrepolocation + "/index.html","w+") 
		Release.write(rootindex)
		Release.close() 
	
	
	# We are going to add an Icon to the Repo
	while True:
		try:
			easygui.msgbox(msg="Now we are going to add an Icon to your Repo! \nMake sure your Icon is an PNG and is either 32x32 pixels or 64x64.", title="CyRep0", ok_button="Ok")
			repoicon = easygui.fileopenbox(default="./*.png" ,filetypes = None ) 
		except ValueError:
			continue
		if repoicon is None:
			defaulticon = easygui.ynbox(msg="You clicked cancel, we are using a default icon than, is that okay?", title="CyRep0")
			if defaulticon is True:
				selectedicon = ("defaulticon.png")
				break
			elif defaulticon is False:
				continue
			else:
				continue
		elif repoicon.endswith('.png'): 
			selectedicon = (repoicon)
			break
		else:
			defaulticon = easygui.indexbox(msg="You selected an invalid type, what do you want to do?", title="CyRep0",choices=["Select another file","Use default Icon"])
			if defaulticon == 0:
				continue
			elif defaulticon == 1:
				selectedicon = ("defaulticon.png")
				break
			else:
				continue
	
	shutil.copyfile(selectedicon, (newrepolocation + "\CydiaIcon.png"))
	
	
	# Copying an Empty Packages List to the Directory so the Repo is seen as a valid repo
	shutil.copyfile("PackagesEmpty.bz2", (newrepolocation + "\Packages.bz2"))
	
	# Creating the Packages and Depiction folder
	os.mkdir(newrepolocation + "\packages\\")
	

	
	# DONE YEEJJJJ
	easygui.msgbox(msg="Congratulations! \nYour Repo has been build (It's saved in: " + newrepolocation + " )!\n\nNow upload your Repo to GithubPages or to any webhost, you can add tweaks anytime you want by starting CyRep0! Make sure to always upload the files after you have made changes.\n\nIf you want to support CyRep0 check out: J0113.github.io/CyRep0!", title="CyRep0!", ok_button="Close!")
	

	
elif menu == 1:

	# Opening a Repo
	easygui.msgbox(msg="Please open the folder were the Repo is located.", title="CyRep0 Repo Manager", ok_button="Ok")
	while True:
		try:
			repolocation = easygui.diropenbox()
			RepoRelease = Path(repolocation + "\Release")
		except ValueError:
			continue
		if repolocation is None:
			stop = easygui.ynbox(msg="You clicked cancel, would you like to quit?", title="CyRep0")
			if stop is True:
				print("Exiting...")
				cls()
				sys.exit()
				exit()
			else:
				continue
		elif RepoRelease.is_file(): 
			break
		else:
			easygui.msgbox(msg="The folder you select is not an valid repo or CyRep0 does not understand this folder. Please select another folder.", title="CyRep0", ok_button="Ok")
			continue
	
	easygui.msgbox(msg="The Repo ( " + repolocation + " ) has been selected!", title="CyRep0 Repo Manager", ok_button="Ok")
	
	
	while True:
		try:
			# Menu of the Package Manger
			managermenu = easygui.choicebox(title="CyRep0", msg="CyRep0 Repo Manger\nMake a Choice", choices=["Add Package","Edit Package","Update Packages List (Needed after you add or edit a package)","\n","Edit Repo Information", "Edit Repo HomePage","\n","Exit"])
		except ValueError:
			continue
		if managermenu == "Add Package":
			
			# Adding a new Package
			easygui.msgbox(msg="Select a .deb file.", title="CyRep0", ok_button="Ok")
			newdeb = easygui.fileopenbox(default="./*.deb" ,filetypes = None ) 
			
			if newdeb is None:
				continue
			elif newdeb.endswith('.deb'):
				
				newname = easygui.enterbox(title="CyRep0", msg="How should we call this package?")
				if newname is None:
					continue
				else:
				
					newversion = easygui.enterbox(title="CyRep0", msg="What version? (Most likely 1.0)")
					newsection = easygui.enterbox(title="CyRep0", msg="What Section does the package need to be placed? (Example: Tweaks or Themes)")
					newdescription = easygui.codebox(msg="Information about this package, will be visable within the Repo.", title="CyRep0")
					newauthor = easygui.enterbox(title="CyRep0", msg="Who made this package?")
					newdepends = easygui.enterbox(title="CyRep0", msg="Does this package Depends on any thing (iOS version or other teak)? Please read website for more information or leave empty!")
					newpackageid = easygui.enterbox(title="CyRep0", msg="Enter the PackageID (bundleIdentifier), make sure that this is the same as specified in the deb, otherwise Cydia will install but not show as installed! (Example: com.developername.tweak)")
					
					os.mkdir(repolocation + "\packages\\" + newname + "\\")
					
					shutil.copyfile(newdeb, (repolocation + "\packages\\" + newname + "\package.deb"))
					
					version = open(repolocation + "\packages\\" + newname + "\\version","w+") 
					version.write(newversion)
					version.close() 
					
					description = open(repolocation + "\packages\\" + newname + "\\description","w+") 
					description.write(newdescription)
					description.close()
					
					section = open(repolocation + "\packages\\" + newname + "\\section","w+") 
					section.write(newsection)
					section.close()
					
					author = open(repolocation + "\packages\\" + newname + "\\author","w+") 
					author.write(newauthor)
					author.close()
					
					PackageID = open(repolocation + "\packages\\" + newname + "\\packageid","w+") 
					PackageID.write(newpackageid)
					PackageID.close()
					
					if newdepends is None:
						continue
					else:
						depends = open(repolocation + "\packages\\" + newname + "\\" + "depends","w+") 
						depends.write(newdepends)
						depends.close()
					
					easygui.msgbox(msg="The package has been added, please select Update Packages List to update your repo!", title="CyRep0 Repo Manager", ok_button="Ok")
					
				
			else:
				easygui.msgbox(msg="Sorry the file you selected is not a .deb file.", title="CyRep0", ok_button="Ok")
			
			
		elif managermenu == "Edit Package":
			
			# Package Editor
			packages = os.listdir(repolocation + "\\packages")
			packagetoedit = easygui.choicebox(title="CyRep0", msg="What Package do you want to edit?", choices=packages)
			
			packageeditorexit = 0
			
			while packageeditorexit < 1:
				packageeditor = easygui.choicebox(title="CyRep0", msg="Package: " + packagetoedit + "\nChoose what you want to edit, or go back by clicking cancel.", choices=["Update DEB file","Change Version","Change Package Description","Change Section","Change Author","Update PackageID","\n","Back to Package Manager"])
			
				if packageeditor == "Change Version":
					newversion = easygui.enterbox(title="CyRep0", msg="What version? (Higher that you are currently using!)")
					version = open(repolocation + "\packages\\" + packagetoedit + "\\version","w+") 
					version.write(newversion)
					version.close() 
					easygui.msgbox(msg="The Version has succesfully been updated!", title="CyRep0", ok_button="Ok")
					
				elif packageeditor == "Change Package Description":
					DescriptionFile = open(repolocation + "\packages\\" + packagetoedit + "\\description","r") 
					DescriptionFile = easygui.codebox(msg="Edit the Repo's Description. This will be visable when installing this tweak in Cydia.", title="CyRep0", text=DescriptionFile)
					Release = open(repolocation + "\packages\\" + packagetoedit + "\description","w+") 
					Release.write(DescriptionFile)
					Release.close() 
					easygui.msgbox(msg="The Package Description has succesfully been updated!", title="CyRep0", ok_button="Ok")
				
				elif packageeditor == "Change Section":
					newsection = easygui.enterbox(title="CyRep0", msg="What Section do you want to Package in? (Example: Tweaks or Themes)")
					section = open(repolocation + "\packages\\" + packagetoedit + "\\section","w+") 
					section.write(newsection)
					section.close() 
					easygui.msgbox(msg="The Section has succesfully been updated!", title="CyRep0", ok_button="Ok")
					
				elif packageeditor == "Change Author":
					newauthor = easygui.enterbox(title="CyRep0", msg="Who should be the new Author?")
					author = open(repolocation + "\packages\\" + packagetoedit + "\\author","w+") 
					author.write(newauthor)
					author.close() 
					easygui.msgbox(msg="The Author has succesfully been updated!", title="CyRep0", ok_button="Ok")
					
				elif packageeditor == "Update PackageID":
					newauthor = easygui.enterbox(title="CyRep0", msg="Enter the new PackageID (bundleIdentifier), make sure that this is the same as specified in the deb, otherwise Cydia will install but not show as installed! (Example: com.developername.tweak)\nIs recommended to not change the PackageID after it has been installed!")
					author = open(repolocation + "\packages\\" + packagetoedit + "\\author","w+") 
					author.write(newauthor)
					author.close() 
					easygui.msgbox(msg="The PackageID has succesfully been updated!", title="CyRep0", ok_button="Ok")
					
				elif packageeditor == "Update DEB file":
					easygui.msgbox(msg="Select a new .deb file.", title="CyRep0", ok_button="Ok")
					debupdate = easygui.fileopenbox(default="./*.deb" ,filetypes = None ) 
					if debupdate.endswith('.deb'):
						shutil.copyfile(debupdate, (repolocation + "\packages\\" + packagetoedit + "\\package.deb"))
						easygui.msgbox(msg="The deb has succesfully been updated!", title="CyRep0", ok_button="Ok")
					else:
						easygui.msgbox(msg="Invalid DEB!", title="CyRep0", ok_button="Ok")
				elif packageeditor == "Back to Package Manager":
					packageeditorexit = 1
				else:
					pass
			
			
		elif managermenu == "Update Packages List (Needed after you add or edit a package)":
			
			# Package Updater
			shouldiupdate = easygui.ynbox(msg="You are about to update the Packages list, this could take a while if you have a lot of packages, please don't close the terminal during this procces!\n\nAre you sure want to start the update?", title="CyRep0")
			
			if shouldiupdate is True:
				print("Updating Packages...\nFinding All Packages...")
				packages = os.listdir(repolocation + "\\packages")
				packagecount = (str(len(packages)))
				print("Found: " + packagecount + " packages!\n Starting now!")
				print("Found all packages, staring now.\n\n\n")
				packageno = 0
				
				PackagesFile = open(repolocation + "\\Packages.temp","w+")
				for package in packages:
					
					with open(repolocation + "\\packages\\" + package + "\\author") as f:
						author = f.readline()
					with open(repolocation + "\\packages\\" + package + "\\depends") as f:
						depends = f.readline()
					with open(repolocation + "\\packages\\" + package + "\\section") as f:
						section = f.readline()
					with open(repolocation + "\\packages\\" + package + "\\version") as f:
						version = f.readline()
					with open(repolocation + "\\packages\\" + package + "\\packageid") as f:
						packageid = f.readline()
					
					PackagesFile.write("\Package: " + packageid)
					PackagesFile.write("\nVersion: " + version)
					PackagesFile.write("\nSection: " + section)
					PackagesFile.write("\nMaintainer: " + author)
					PackagesFile.write("\nDepends: " + depends)
					PackagesFile.write("\nArchitecture: iphoneos-arm")
					PackagesFile.write("\nFilename: ./packages/" + package + "/package.deb")
					
					debsize = Path() / (repolocation + "\\packages\\" + package + "\\package.deb")
					size = debsize.stat().st_size
					PackagesFile.write("\nSize: " + str(size))
					
					debhash = (md5sum(repolocation + "\\packages\\" + package + "\\package.deb"))
					PackagesFile.write("\nMD5sum: " + debhash)
					
					PackagesFile.write("\nDescription: " + package)
					PackagesFile.write("\nName: " + package)
					PackagesFile.write("\nAuthor: " + author)
					PackagesFile.write("\nDepiction: ./packages/" + package + "/index.html\n\n")
					
					packageno = packageno + 1
					packagecurrent = (str(packageno))
					print("[" + packagecurrent + "/" + packagecount + "] " + package)
					
				PackagesFile.close() 
				
				print("\nCompressing to Packages.bz2")
				PackagesBZ2 = open(repolocation + "\\Packages.bz2","wb+") 
				PackagesBZ2.write(bz2.compress(open(repolocation + "\\Packages.temp", 'rb').read()))
				PackagesBZ2.close() 
				print("Cleaning up the Pack.temp")
				os.remove(repolocation + "\\Packages.temp")
				
				print("Everything done!")
				easygui.msgbox(msg="Packages update completed!\n\nThe updated Packages list contains: " + packagecount + " Packages!\nUpload the whole repo to Github Pages or any other webhost!", title="CyRep0", ok_button="Ok")
				cls()
			
			else:
				easygui.msgbox(msg="The update has been canceled.", title="CyRep0", ok_button="Ok")
			
			
		elif managermenu == "Edit Repo Information":
			
			# Release File Editor
			ReleaseFile = open(repolocation + "\Release","r") 
			ReleaseFile = easygui.codebox(msg="Edit the Repo information how ever you want!", title="CyRep0", text=ReleaseFile)
			Release = open(repolocation + "\Release","w+") 
			Release.write(ReleaseFile)
			Release.close() 
			
			
		elif managermenu == "Edit Repo HomePage":
			
			# Index File Editor
			IndexFile = open(repolocation + "\index.html","r") 
			IndexFile = easygui.codebox(msg="Edit the homepage how ever you want!", title="CyRep0", text=IndexFile)
			index = open(repolocation + "\index.html","w+") 
			index.write(IndexFile)
			index.close() 
			
			
		elif managermenu == "Exit":
			
			# Exit
			print("Exiting...")
			cls()
			sys.exit()
			exit()
		else:
			continue
		
		
	
elif menu == 2:

	#Info Menu
	readme = open("readme.txt","r") # To save loadion time, we will load the ReadMe when its needed.
	easygui.textbox(msg="------------------\nWelcome to CyRep0!\n------------------",title="CyRep0",text=readme,codebox=False)
	
	
	
else:
	print("Exiting...")
	cls()
	sys.exit()
	exit()

