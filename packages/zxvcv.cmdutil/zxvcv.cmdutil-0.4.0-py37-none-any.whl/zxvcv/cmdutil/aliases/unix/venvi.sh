#!/bin/bash

if [[ $1 == --help || $1 == "" || $2 == "" ]]; then
    echo "Initialize python virtual env"
    echo "usage venvi [--help] pyver args"
    echo ""
    echo "arguments:"
    echo "  --help      show brief help message"
    echo "  pyver       python version which should beused to create virtual environment"
    echo "  args        arguments for python script what will create virtual environment"
else
    if ! command -v python$1 &> /dev/null
    then
        echo "python$1 not found, 'type venvi --help' to display help page"
    else
        python$1 -m zxvcv.cmdutil.pvenv.initialize ${@:2}
    fi
fi
