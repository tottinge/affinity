#!/bin/bash -x


DAYS=${1:-30}

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

python display_nodes.py > groups_by_file.log
python display_edges.py > groups_by_linkage.log

# need to run bayes here as well...
