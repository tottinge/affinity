#!/bin/bash -v
DAYS=90
FILESUFFIX=${DAYS}days.csv

for repo in jdcorefs GSD vtcorefs
do
    hg log -R ~/${repo}/ -r "date(-${DAYS}) and ! merge()" --style=matchable.style  | 
        python hg2csv.py ${repo} > ${repo}.${FILESUFFIX} &
done

wait

python import_data.py *.${FILESUFFIX} 2>toobig.log &
python howmanyfiles.py *.${FILESUFFIX}  &

wait 

./get_edges.sh
python analyze_graph.py > groups.log

# need to run bayes here as well...
