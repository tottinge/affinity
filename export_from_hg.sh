#!/bin/bash -v

for repo in jdcorefs GSD vtcorefs
do
        hg log -R ~/${repo}/ -r "date(-90) and ! merge()" --style=matchable.style  | python matchable.py ${repo} > ${repo}.90days.csv &
done

wait

python import_data.py *.90days.csv 2>toobig.log &

python howmanyfiles.py *.csv  &

wait 

./get_edges.sh
python build_groups.py >groups.log
