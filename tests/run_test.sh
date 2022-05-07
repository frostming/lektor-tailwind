#!/bin/bash

set -eo pipefail

if ! which realpath > /dev/null; then
    realpath() {
        OURPWD=$PWD
        cd "$(dirname "$1")"
        LINK=$(readlink "$(basename "$1")")
        while [ "$LINK" ]; do
            cd "$(dirname "$LINK")"
            LINK=$(readlink "$(basename "$1")")
        done
        REALPATH="$PWD/$(basename "$1")"
        cd "$OURPWD"
        echo "$REALPATH"
    }
fi

project_root=$(dirname "$(dirname "$(realpath "$0")")")
copy_files=("setup.py" "setup.cfg" "lektor_tailwind.py" "README.md" "LICENSE")
cd "$(pwd)/example"

rm -fr packages
mkdir -p packages/tailwind

echo "[INFO] Copy plugin files"
set -x
for file in "${copy_files[@]}"; do
    cp "${project_root}/${file}" packages/tailwind/
done
set +x

echo "[INFO] Initialize plugin"
lektor plugin reinstall > /dev/null 2>&1
lektor plugin list|grep tailwind

echo "[INFO] Test server"
lektor server -p 9527 > /dev/null 2>&1 &
sleep 1
pgrep tailwindcss && echo "Tailwind is running"
pkill -f "lektor server"

echo "[INFO] Test build"
lektor build
grep -q "/*! tailwindcss" _build/static/style.css && echo "Tailwind is built in to style.css"
echo "[INFO] All tests passed!"
