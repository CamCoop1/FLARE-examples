#!/usr/bin/bash
#SBATCH --output=/remote/nas00-1/users/charris/phd/fcc/FLARE-examples/analysis/studies/large_mc_batch_example/logs/MCProductionWrapperDependency/stdout
#SBATCH --error=/remote/nas00-1/users/charris/phd/fcc/FLARE-examples/analysis/studies/large_mc_batch_example/logs/MCProductionWrapperDependency/stderr
#SBATCH --mem=5GB
exec /remote/nas00-1/users/charris/phd/fcc/FLARE-examples/analysis/studies/large_mc_batch_example/MCProductionWrapperDependency/executable_wrapper.sh