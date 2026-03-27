#!/bin/bash
# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mkzip2.sh
#
#--------1---------2---------3---------4---------5---------6---------7--------#
set -e
OUT=ccocr.zip
rm -f "$OUT"

# log/, output/ 以下をソートして最後のフォルダを取得
LAST_LOG=$(ls -d log/*/ 2>/dev/null | sort | tail -1)
LAST_OUT=$(ls -d output/*/ 2>/dev/null | sort | tail -1)

zip -r "$OUT" \
    code/jobs/ \
    code/m/ \
    code/main.py \
    code/mymail.ps1 \
    CURRENT_TASK/

# poppler はカラフォルダとして追加
zip "$OUT" code/poppler/

# 最後の log フォルダを追加
if [ -n "$LAST_LOG" ]; then
    # log/LAST/flsk/static/spic はカラフォルダとして追加（除外して後から追加）
    zip -r "$OUT" "$LAST_LOG" --exclude "${LAST_LOG}flsk/static/spic/*"
    zip "$OUT" "${LAST_LOG}flsk/static/spic/"
else
    echo "warning: no folders found under log/"
fi

# 最後の output フォルダを追加
if [ -n "$LAST_OUT" ]; then
    zip -r "$OUT" "$LAST_OUT"
else
    echo "warning: no folders found under output/"
fi

echo "created: $OUT"



exit


set -e
OUT=ccocr.zip
rm -f "$OUT"

# log/ 以下をソートして最後のフォルダを取得
LAST_LOG=$(ls -d log/*/ 2>/dev/null | sort | tail -1)

zip -r "$OUT" \
    code/jobs/ \
    code/m/ \
    code/main.py \
    code/mymail.ps1 \
    CURRENT_TASK/
# poppler はカラフォルダとして追加
zip "$OUT" code/poppler/

# 最後の log フォルダを追加
if [ -n "$LAST_LOG" ]; then
    zip -r "$OUT" "$LAST_LOG"
else
    echo "warning: no folders found under log/"
fi

echo "created: $OUT"
