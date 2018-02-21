# Project Notes
Josh Lau, Matt Phillips / TCSS 455 Machine Learning / Martine de Cock / Jan 11 2018

*Usage*

tcss455 -i [input directory] -o [output directory]

Trains averages and popularity on our basic training data.
Then, assigns each user from the input directory data based upon those.
Finally, writes users as XML to the output directory, each as its own file.

Overview

Text - given status updates
JPEG - given profile picture
Relational "likes" - given ids for pages like by the user

Predict gender (M / F) as binary classification
Age (xx-24) as multi-class classification
Personality traits (OCEAN) percentages as regression problems 

You can use any course to predict any output
For teams of two, take away one source, and add again later if time allows.

Jan 18 Submission

Find the maximum occurring gender and age, and predict that for each result.
For personality, you should find the average among all users for each personality traint and predict it for all users.
You must meet the baseline, but in future updates you must beat the baseline.

Virtual machine notes

For an output directory: /output
In output directory, output valid XML files in a the format on page 3.
The id in the output XML schema is the user's id. You can use any XML output engine.
Each XML output should be in a file [id].xml

Using manage_vc

In the command prompt, execute "manage_vc.exe" to gain access to the Ubuntu VM.

SSHing into the VM

You may SSH into the VM via cssgate.
1. SSH into cssgate via Putty for Windows.
2. Grep the teams from /etc/hosts to discover the IP for your VM.
3. SSH into the VM with the IP address listed for your team as it-admin. (We're team 6.)
   - Retrieve the it-admin password from manage_vc.exe -> "Reveal password"

Installing packages on the VM

- Run sudo to command as an administrator, you'll need your password.
- "sudo apt-get" is used for installation in the Linux package manager.
- We must install packages so that other users can run it. DO NOT INSTALL ANYTHING AS ITUSER, INSTALL AS ITADMIN.
- Switch users by using the "su" command. Password for ituser is the same as itadmin.
- Running "exit" pops off the latest user switch.
- Data is underneat ~/data

Basic workflows

- Create output folder with:
cd ~
mkdir output
- As ituser, get rid of the output file with rm -rf ~/output
- Run the following as itadmin to make sure you've installed everything correctly and test your program:
tcss455 -i /data/public-test-data/ -o ~/output.

-rwxrwxr-x Read Write Execute

Our script should have permsisions to execute as listed above, check chmod for this.

#!/bin/bash

This must go in the top of the tcss455 file put in ~. This tells it to interpret the contents as bash.
