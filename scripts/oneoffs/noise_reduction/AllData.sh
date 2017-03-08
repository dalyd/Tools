#/usr/bin/env bash

# Download and process all results from a multi patch

PATCH_FILE=${1}
DSI_PATH=${DSI_PATH:-/Users/daviddaly/mongosrc/dsi-repos/master}
echo "Patch File is " $PATCH_FILE
echo "DSI PATH is " $DSI_PATH
python $DSI_PATH/analysis/multi_analysis.py -C $PATCH_FILE --json-array --out flat.json
python $DSI_PATH/analysis/multi_analysis.py -C $PATCH_FILE --json --out agg.json
python $DSI_PATH/analysis/multi_graphs.py --json --input agg.json
