import os
import sys
def GetFileNameWithoutExtension(filename):
    name= os.path.basename(filename).split('.')[0]
    return name