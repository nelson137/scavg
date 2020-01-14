#!/bin/bash

pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null

    . ./venv/bin/activate

    python3 ./t.py

popd >/dev/null
