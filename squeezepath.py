import os

class SqueezePath(object):

    def __init__(self):
        self.uniques = {}
        self.invert = None

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

