#!/bin/bash -e
# Run a full (standard) analysis of the code in the repository.
# Default period is 30 days.
# 
# Creates db file, log files, etc in current directory.
# Filenames contain the number of days used in the file.

DAYS=${1:-30}
export OUT_DIR=EVENTS.${DAYS}.$(date +%F)
if [ -d ${OUT_DIR} ] ; then
    echo "${OUT_DIR} exists. Drop it and try again"
    exit 1
fi
mkdir -p ${OUT_DIR}

export EVENTS_DB_NAME=${OUT_DIR}/events.sqlite.db
FILESUFFIX=${DAYS}days.csv


echo "Gathering mercurial records"
for repo in jdcorefs GSD vtcorefs
do
    hg log -R ~/${repo}/ -r "date(-${DAYS}) and ! merge()" --style=matchable.style  | 
        python hg2csv.py ${repo} > ${OUT_DIR}/${repo}.${FILESUFFIX} &
done
wait

echo "creating database (${EVENTS_DB_NAME})"
python import_data.py ${OUT_DIR}/*.${FILESUFFIX} 2>toobig.log &
python howmanyfiles.py ${OUT_DIR}/*.${FILESUFFIX}  &
wait 

echo "Correlating edges"
./get_edges.sh


echo "Conducting analysis"
python display_nodes.py > ${OUT_DIR}/groups_by_file.${DAYS}.log
python display_edges.py > ${OUT_DIR}/groups_by_linkage.${DAYS}.log
python display_spanning_edges.py > ${OUT_DIR}/spanning_edges.${DAYS}.log
python display_path_correlation.py > ${OUT_DIR}/path_correlation.${DAYS}.log


echo ""
echo Database is ${EVENTS_DB_NAME}
# need to run bayes here as well...
