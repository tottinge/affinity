#!/bin/bash -e
# Run a full (standard) analysis of the code in the repository.
# Default period is 30 days.
# 
# Creates db file, log files, etc in current directory.
# Filenames contain the number of days used in the file.

DAYS=${1:-30}
export EVENTS_DB_NAME=events.${DAYS}.$(date +%F).sqlite.db
FILESUFFIX=${DAYS}days.csv

echo "Gathering mercurial records"
for repo in jdcorefs GSD vtcorefs
do
    hg log -R ~/${repo}/ -r "date(-${DAYS}) and ! merge()" --style=matchable.style  | 
        python hg2csv.py ${repo} > ${repo}.${FILESUFFIX} &
done
wait

echo "creating database (${EVENTS_DB_NAME})"
python import_data.py *.${FILESUFFIX} 2>toobig.log &
python howmanyfiles.py *.${FILESUFFIX}  &
wait 

echo "Correlating edges"
./get_edges.sh

echo "Conducting analysis"
echo -e "\tgroups_by_file.${DAYS}.log"
python display_nodes.py > groups_by_file.${DAYS}.log

echo  -e "\tgroups_by_linkage.${DAYS}.log"
python display_edges.py > groups_by_linkage.${DAYS}.log

echo  -e "\tspanning_edges.${DAYS}.log"
python display_spanning_edges.py > spanning_edges.${DAYS}.log

echo  -e "\tpath_correlation.${DAYS}.log"
python display_path_correlation.py > path_correlation.${DAYS}.log


echo ""
echo Database is ${EVENTS_DB_NAME}
# need to run bayes here as well...
