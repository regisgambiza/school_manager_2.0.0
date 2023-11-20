#!/bin/bash
for ui_file in $(find src/app/ui -name "*.ui"); do
    pyuic5 -x $ui_file -o ${ui_file%.*}.py
done
