# Run this from Jenkins workspace directory

BUILD_ARTIFACTS_DIR=${1:-"/tmp"}

if [ -f multiline.style ]; then
    STYLE_FILE=./multiline.style
else
    STYLE_FILE=GSX/_Tools/HeatMap/multiline.style 
fi

if [ -f heatmap.py ]; then
    RUN_FROM=.
else
    RUN_FROM=GSX/_Tools/HeatMap
fi

hg log -r "date(-60)" --style ${STYLE_FILE} | 
	python ${RUN_FROM}/heatmap.py |
	tee ${BUILD_ARTIFACTS_DIR}/heatmap.csv | 
	python ${RUN_FROM}/Generate.py > ${BUILD_ARTIFACTS_DIR}/heatmap.html

