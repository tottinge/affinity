import os
import fileinput
import os

# check out costs of stashing dirs and giving surrogate IDs
dirs = {}
files={}
paths={}
for line in fileinput.input():
    if not "/" in line:
        continue
    dirpart,filepart = os.path.split(line)
    pathid = dirs.setdefault(dirpart, len(dirs))
    fileid = files.setdefault(filepart, len(files))
    paths[(pathid,fileid)] = 0
    print pathid, fileid, line

print "unique dirs:", len(dirs)
print "unique filenames:", len(files)
print "unique paths:", len(paths)



