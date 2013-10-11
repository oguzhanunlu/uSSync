# This file is part of uSSync. 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2013 Erdal Sivri, Oguzhan Unlu
# README 
# to see this code working well, it is needed to create a config file, namely sampleconfig.conf, and put these lines into 
# it:
# /home/yourusername/Desktop # please change username part
# /home/yourusername/Documents # please change username part

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
# if creating folder option used, uncomment the line below
#os.system("rm -rf well")
