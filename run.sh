# rm -rf workdir
WORKFLOW=${1:-workflows/workflow.yml}
WORKDIR=${2:-workdir}
yadage-run $WORKDIR $WORKFLOW inputs/input.yml -d initdir=$PWD/inputs
