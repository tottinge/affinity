import os 
from collections import namedtuple
import fileinput

acceptable_reds = [ ("rgb(%d,%d,%d)" % (r,255-r,100)) for r in range(255) ]
url_prefix = "http://wdxivsgsdci01.jdnet.deere.com/hgweb/hgweb.cgi/GSD/raw-file/tip/"

text_sizes = [
    "xx-small", 
    "x-small",
    "small",
    "medium", 
    "large",
    "x-large",
    "xx-large",
]

html_doc = """<html>
<head>
    <title>SCM Heatmap</title>
    <style type='text/css'>
        body { font-family: sans-serif; color: lightgrey; }
        ul li { display: inline; margin: 2px; }
    </style>
</head>
<body>
  <ul>%s</ul>
</body>
</html>
"""


class Report(object):
    def __init__(self, data):
        self.data = data
        self.most_changed = self._most_changes_for_one_file(data)

    def generate_html(self):
        return html_doc % "\n".join(self._generate_links())

    def _generate_links(self):
        interesting_data = sorted(self.data, reverse=True)[:50]
        interesting_data = sorted(interesting_data, key=lambda x:x[-1])
        for (changes,defects,path) in interesting_data:
            textsize = self._get_size(changes, self.most_changed)
            color = self._get_color(defects,changes)
            yield self._link_styling(path,changes,defects,color,textsize)

    def _get_color(self, n,m):
        color= self._select_by_proportion(n,m, acceptable_reds)
        return color

    def _get_size(self,n,m):
        return self._select_by_proportion(n,m, text_sizes)

    def _select_by_proportion(self, n,m, array):
        percentage = float(n)/m
        extent = len(array)-1
        index = int(percentage * (extent))
        return array[index]

    def _link_styling(self, fullpath, changes, defects, color, size):
        path,filename = os.path.split(fullpath)
        url = url_prefix + fullpath
        style="font-size: %s; color: %s" % (size,color)
        title="%s Changes: %d Defects %d" % (fullpath, changes, defects)
        link = "<li title='%s'><a href='%s' style='%s' >%s</a></li>"  % (
            title,
            url,
            style, 
            filename
        )
        return link

    def _most_changes_for_one_file(self, data):
        return max(changes for (changes,defects,path) in data)

def read_input():
    for line in fileinput.input():
        rawTickets, rawDefects, filename = line.split(",",2)
        record =  int(rawTickets.strip()), int(rawDefects.strip()), filename.strip()
        yield record


if __name__ == "__main__":
    data = [record for record in read_input()]
    report = Report(data)
    print report.generate_html()

   
