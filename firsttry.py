import os 

# creating a folder, namely well, containing a file, namely gogogo.py, to be resynchronized
#os.mkdir('well')
#os.chdir('well')
#os.system("touch gogogo.py")

# to show folder structure of directory containing our sample well folder
#os.chdir('../')
#os.system("ls -R")

# reading synchronization paths from a config file
f = open('sampleconfig.conf',"r")
lines = f.readlines()
# resynchronization 
for x in lines:
    os.system("rsync -avz " + x[:-1] + " /home/blacksimit/Documents/joke")

f.close()
# to see whether synchronization is done or not
os.chdir('joke')
os.system("ls -R")
os.system("rm -rf well")
