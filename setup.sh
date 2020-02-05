#!/bin/bash

set -e

pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null

    # Create the venv if not exists
    [ -d ./venv ] || python3 -m venv ./venv
    # Activate the venv
    . ./venv/bin/activate

    # Install python3 modules
    pip3 install -r ./requirements.txt >/dev/null

    # Make sure apt dependencies are installed
    apt_deps=( sqlite3 )
    for dep in "${apt_deps[@]}"; do
        dpkg -s "$dep" >/dev/null 2>&1 || echo "Missing apt dependency: $dep" >&2
    done

popd >/dev/null
