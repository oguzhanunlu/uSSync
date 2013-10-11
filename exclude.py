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
"""
This module (sen tamamlarsin artik :))
"""
import os
import re

class Exclude(object):
    
    def __init__(self, exclude_file):
        self.excluded = self.__read_exclude_file(exclude_file)

    def __read_exclude_file(self, filename):
        if not os.path.exists(filename):
            return []
        lines = []
        with open(filename) as f:
            try:
                for line in f:
                    lines.append(line.strip())
            except:
                pass
        return lines
    
    def get_excluded(self, delimiter='; '):
        return delimiter.join(self.excluded)

    def is_excluded(self, file_or_folder):
        """
        This method determines whether @file_or_folder
        is to be excluded using the exclude file 
        which is similar to a .gitignore file.
        For instance, readme.txt is excluded if *.txt or 
        readme.txt is inside the excluded file. 
        """
        for line in self.excluded:
            if file_or_folder == line:
                return True
            if os.path.basename(file_or_folder) == line:
                return True
            regex = line.replace('.', '\.').replace('?', '.').replace('*', '.*')
            regex = '^' + regex + '$'
            if re.match(regex, file_or_folder):
                return True
        return False
        #return file_or_folder in self.excluded or \
        #        os.path.basename(file_or_folder) in self.excluded



def test(file_or_folder, excluded):
    exclude = Exclude('')
    exclude.excluded = excluded
    return exclude.is_excluded(file_or_folder)

def test_main(args):
    excluded = [
        '*.txt', 'hw?.c', 'README',
    ]
    assert(test('README', excluded) == True)
    assert(test('readme.txt', excluded) == True)
    assert(test('readme', excluded) == False)
    assert(test('README.c', excluded) == False)
    assert(test('hw.c', excluded) == False)
    assert(test('hw2.c', excluded) == True)
    assert(test('hw2.c', excluded) == True)
    assert(test('hw.txt', excluded) == True)
    assert(test('hw12.c', excluded) == False)
    assert(test('hw12.txt', excluded) == True)
    print 'All tests OK'

if __name__ == '__main__':
    import sys
    test_main(sys.argv[1:])
