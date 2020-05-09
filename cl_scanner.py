import datetime
import shutil
from pathlib import Path
import yaml

from utils import *


def transfer_output(input_point, input_path='./workdir/madanalysis5/ANALYSIS', output_path='./outputs'):
    """
    Transfer information in madanalysis5 output folder to ./outputs
    """
    input_path, output_path = Path(input_path), Path(output_path)
    folder_path = output_path / 'folders' / f'ANALYSIS-{input_point}'
    summary_path = folder_path / 'Output' / 'SAF' / 'CLs_output_summary.dat'

    if input_path.exists():
        shutil.move(input_path, folder_path)
        shutil.copy(summary_path, output_path / 'summaries' / f'summary-{input_point}.txt')
    else:
        print(f'{input_point:<10}: Missing workflow folder, moving on')


def run_cl(mChi, mPhi):
    """
    One run to produce confidence limit output from ma5
    """
    input_point = f'({mChi}, {mPhi})'

    print(f'{input_point:<10}: Generating Param Card')
    path, _ = make_param_card(mChi, mPhi)

    print(f'{input_point:<10}: Adding Param Card to Input')
    set_param_card(path)

    print(f'{input_point:<10}: Executing Workflow')
    run_flow(wf='fullma5.yml')
    print(f'{input_point:<10}: Workflow Finished')

    transfer_output(input_point)
    print(f'{input_point:<10}: Transferred Output')


def scan_cl(input_points):
    """
    Get madanalysis5 output folder for each input point.
    """

    last_time = datetime.datetime.now()
    total_hours = 0
    for i in range(0, len(input_points)):
        mChi, mPhi = input_points[i]

        current_hour = datetime.datetime.now().hour
        total_hours += current_hour - last_time
        last_time = current_hour

        print(f'{int(i / len(input_points)) * 100}% done at {total_hours}.')
        run_cl(mChi, mPhi)


def main():
    scan_cl(INPUT_POINTS)


if __name__ == '__main__':
    # main()
    run_cl(10, 100)
    '''
./bin/ma5 -R -s {ma5_card}
cp -r ANALYSIS_0 {output_folder}
    '''
