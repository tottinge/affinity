import numpy
import csv

def digestable(input):
    return (line for line in input if len(line) < 131072)

sample = []
with open("GSD.90day.csv") as infile:
    with open("GSD.90day.big", "w") as big:
        reader=csv.reader(digestable(infile))
        for row in reader:
            num,src,user,dt,branch,tickets,files = row
            count = len(files.split(','))
            if count > 206:
                big.write("%s:%d:%s:%s:%s\n" %(num,count,branch,user,str(tickets)))
            sample.append(count)
        
print "mean:",numpy.mean(sample)
print "std:", numpy.std(sample)
print "max:", max(sample)
print "min:", min(sample)
percentiles = [90,95,99]
print "percentile:\n", "".join(map(lambda x: "\t%d percentile = %d files\n" %(int(x[0]),int(x[1])), zip(percentiles, numpy.percentile(sample,percentiles))))
