#!/bin/bash

if ! command -v python &> /dev/null
then
    echo "python not found, (python-is-python3 not installed?)"
else
    python -m zxvcv.cmdutil.pvenv.remove ${@:1}
fi
