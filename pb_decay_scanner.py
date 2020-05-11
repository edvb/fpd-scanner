import re
import time

from utils import *


def get_decay(lhe_path='./workdir/madgraph/events.lhe', id='2000002'):
    """
    Get decay for particle id in lhe file
    """
    with open(lhe_path, 'r+') as lhe_file:
        lhe_text = lhe_file.read()
        decay_line = re.findall(f"DECAY {id}.*$", lhe_text, re.MULTILINE)[0].split()
        decay = decay_line[2]
    return decay


def get_pb(lhe_path='./workdir/madgraph/events.lhe'):
    """
    Get Integrated Weight(pb) from lhe file.
    """
    with open(lhe_path, 'r+') as lhe_file:
        lhe_text = lhe_file.read()
        pb_line = re.findall(f"Integrated weight.*$", lhe_text, re.MULTILINE)[0].split()
        pb = pb_line[-1]

    return pb


def save_stats(point, decay, pb, save_path='./results.txt'):
    """
    Save stats as table.
    """
    with open(save_path, 'a+') as save_file:
        save_file.write(f"{point} {decay} {pb}\n")


def run_pb_decay(mChi, mPhi):
    """
    Run one workflow to find pb and decay
    """
    input_point = f'({mChi}, {mPhi})'

    print(f'{input_point:<10}: Generating Param Card')
    path, _ = make_param_card(mChi, mPhi)

    print(f'{input_point:<10}: Adding Param Card to Input')
    set_param_card(path)

    print(f'{input_point:<10}: Executing Workflow')
    run_flow(wf='madgraph_simple.yml')
    print(f'{input_point:<10}: Workflow Finished')

    decay = get_decay()
    print(f'{input_point:<10}: Decay is {decay}')

    pb = get_pb()
    print(f'{input_point:<10}: Cross-section(pb) is {pb}')

    save_stats(input_point, decay, pb)
    print(f'{input_point:<10}: Saved Stats\n\n')


def scan_pb_decay(input_points):
    for i in range(0, len(input_points)):
        mChi, mPhi = input_points[i]

        run_pb_decay(mChi, mPhi)

        print(f'{i / len(input_points) * 100}% done at {time.time()}.')


def main():
    scan_pb_decay(INPUT_POINTS[1:])


if __name__ == '__main__':
    main()
