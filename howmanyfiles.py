import sys
import numpy
import csv
import fileinput

def digestable(input):
    return (line for line in input if len(line) < 131072)

sample = []
for row in csv.reader(digestable(fileinput.input())):
    num,src,user,dt,branch,tickets,files = row
    count = len(files.split(','))
    if count > 206:
        continue
    sample.append(count)

print "mean:",numpy.mean(sample)
print "std:", numpy.std(sample)
print "max:", max(sample)
print "min:", min(sample)
percentiles = [90,95,99,99.9]
print "percentile:\n", "".join(map(lambda x: "\t%.2f percentile = %d files\n" %(float(x[0]),int(x[1])), zip(percentiles, numpy.percentile(sample,percentiles))))
