import os
import shelve
import tempfile

class SqueezePath(object):

    def __init__(self):
        self.invert = None
        self.squeezefile = tempfile.mktemp(prefix="squeeze") 
        self.uniques = shelve.open(self.squeezefile)

    def cleanup(self):
        self.uniques.close()
        os.unlink(self.squeezefile)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.cleanup()

    def encode(self, target):
        dirpart,filepart = os.path.split(target)
        d = self.uniques.setdefault(dirpart, len(self.uniques))
        f = self.uniques.setdefault(filepart, len(self.uniques))
        self.invert = None
        return "%d/%d" % (d,f)

    def decode(self, code):
        self.get_invert()
        dcode,fcode = map(int, code.split("/"))
        result = os.path.join(self.invert[dcode],self.invert[fcode])
        return result

    def get_invert(self):
        if not self.invert:
            self.invert = dict( (v,k) for (k,v) in self.uniques.iteritems())

