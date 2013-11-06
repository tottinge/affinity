#!/bin/bash -ex
# Run a full (standard) analysis of the code in the repository.
# Default period is 30 days.
# 
# Creates db file, log files, etc in current directory.
# Filenames contain the number of days used in the file.

DAYS=${1:-30}
SQUELCH=${2:-6}
MIN_GROUP=${3:-4}
FILESUFFIX=${DAYS}days.xml
REPOSITORIES=$(cat repositories.config)
echo "Days:${DAYS}, Squelch:${SQUELCH}, Min group:${MIN_GROUP}"

export OUT_DIR=EVENTS.${DAYS}.$(date +%F)
if [ -d ${OUT_DIR} ] ; then
    echo "${OUT_DIR} exists. Drop it and try again"
    exit 1
fi
mkdir -p ${OUT_DIR}


echo "Gathering and converting mercurial records"
for repo in ${REPOSITORIES}
do
    shortname=$(basename ${repo})
    hg log -R ${repo} -r "date(-${DAYS}) and ! merge()" --style=matchable.style  | 
    python hg2nx.py ${shortname} > ${OUT_DIR}/${shortname}.${FILESUFFIX} || 
        echo "Failed for ${repo}"  & 
done
wait

echo "Combining the individual graphs"
python combine_graphs.py ${OUT_DIR}/*.${FILESUFFIX} > ${OUT_DIR}/combined.xml


#echo "Conducting analysis"
#python display_nodes.py ${SQUELCH} ${MIN_GROUP} > ${OUT_DIR}/groups_by_file.${DAYS}.txt
#python display_edges.py ${SQUELCH} ${MIN_GROUP} > ${OUT_DIR}/groups_by_linkage.${DAYS}.txt
#python display_spanning_edges.py ${SQUELCH} ${MIN_GROUP} > ${OUT_DIR}/spanning_edges.${DAYS}.txt
#python display_path_correlation.py ${SQUELCH} ${MIN_GROUP} > ${OUT_DIR}/path_correlation.${DAYS}.txt
#python display_connectors.py ${SQUELCH} ${MIN_GROUP} > ${OUT_DIR}/connectors.${DAYS}.txt

echo "done"
