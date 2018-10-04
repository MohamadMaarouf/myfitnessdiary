# CSC-330---GearGrinders
This repo will house our project and all files associated with it.

# Flask structure we are working with

  |  
  |-InternREQ (project's root level)  
  |-.git (This file is hidden by defualt and is better left untouched. It was created using "git init" and controls everything git)  
  |-flaskr.py (For routing and other python functions if we need to add more python files they go in this level of the project)  
  |-static  
  |---| Any resources (i.e. image files, .css files, and anything you are not sure where to put, probably goes here)   
  |-templates  
  |---| All html files and files that can be considered a route in flask  
  |  
  
# Steps for working with a repo  
    
  1) Make sure you have git installed on what ever machine you wish to use. If you do not have git go here: [https://git-scm.com] and download.  
  
  2) Set git up by typing the following commands in the command line:   
            git config --global user.name "Enter Username Here"  
            git config --global user.email johndoe@example.com  
     These steps are required so we know who is adding what and, git usually won't allow you to push files without this step.  
       
  2.5) Test your variabels by typing  
            git config --list  
    
# Getting the repo on local machine  
    1) Open up the command line  
    2) cd into the folder you want to store this repo
    3) On Github go to https://github.com/Conlonc2/CSC-330-GearGrinders and fork this repository  
    4) Next, go to your newly forked repository and click on "clone or download" and copy the clone link  
    5) Now in the open command line type "git clone "Paste the repo link you just copied in step 4 here!". Press enter  
    6) Make sure the folder is now on your computer and start hacking away!  
    
 # Adding changes to github  
    1) Make edits to the project  
    2) git add < enter files that have been updated and need to be staged >  
    3) git commit -m "Enter message that tells us what you did"  
    4) git push <REMOTE NAME> <BRANCH NAME>  
      
# Wrapping it up  
  After following these steps you should have a local version of this project and be able to create pull requests so we can merge your   edits with the main project. If you have any questions still please feel free to ask.  
