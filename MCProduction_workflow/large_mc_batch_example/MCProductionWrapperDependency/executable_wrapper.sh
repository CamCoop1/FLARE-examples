#!/bin/bash
set -e
cd /remote/nas00-1/users/charris/phd/fcc/FLARE-examples/analysis/studies/large_mc_batch_example
echo 'Working in the folder:'; pwd
echo 'Current environment:'; env
echo 'Will now execute the program'
exec /remote/nas00-1/users/charris/phd/fcc/FLARE-examples/.venv/bin/python3 /remote/nas00-1/users/charris/phd/fcc/FLARE-examples/analysis/studies/large_mc_batch_example/tasks.py --batch-runner --task-id MCProductionWrapperDependency__99914b932b --version 1000_large_batch/run3 --cwd /remote/nas00-1/users/charris/phd/fcc/FLARE-examples/analysis/studies/large_mc_batch_example --mcprod True