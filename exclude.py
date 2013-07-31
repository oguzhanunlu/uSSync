"""
This module (sen tamamlarsin artik :))
"""
import os

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
        # [erdal] bu .gitignore'un yaptigi isi yapacak
        # eger arguman olarak verilen @file_or_folder
        # "exclude_file" ile arguman verilen dosyanin
        # icinde geciyorsa True, degilse False return edecek. 
        # dosyanin satirlari self.excluded listesinin icinde
        # olacak. *.txt, *.c v.b. ifadelere destek vermesi lazim. 
        # simdilik sadece dosya ismine gore tam dogru calismayan
        # bir satir yazdim. relative/absolute olma durumlarina
        # gore uygun bir sey yazmak gerekiyor. 
        return file_or_folder in self.excluded or \
                os.path.basename(file_or_folder) in self.excluded

