# StockAPI
This set of scripts is mainly for testing Git in a fun context. 
This text is mainly to understand the process of git and branches.

I have a main and a developer branch in the StockAPI project

When I update a file and want to update the my working branch (e.g. developer) then I write

>git add .\README.md

to add/stage the file for updating

>git commit -m "commit text"

to give a bit of descriptive text for the update

>git push https://github.com/Jkallehauge/StockAPI 

to push it to the remote repository

>git checkout main

then we are working directly on the main branch

>git checkout developer

then we are working on the developer branch

If I want to merge all changes in my developer branch into the main then first I stage/add and the commit the changes as above. 

The I switch to my target branch for example main
>git checkout main

then I merge the source (Developer) branch into this
>git merge Developer

finaliy I update the remote repository
>git push https://github.com/Jkallehauge/StockAPI

And then the Developer branch has been merged into the main branch







