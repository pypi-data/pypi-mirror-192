import os
import shutil

class DirectoryConfig:
    def renameArchive(directoryOld, directoryNew, startWithName, newName):
        directoryList = os.listdir(directoryOld)
        archives = [a1 for a1 in directoryList if a1.startswith(startWithName)]
        archive  = archives.pop()
        try:
            os.remove(directoryNew + '\\' + newName)
        except:
            pass
        
        shutil.copy(directoryOld + '\\' + archive, directoryNew + '\\' + newName)