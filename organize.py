def make_xsec_s95(summaries_path='./outputs/summaries', results_path='./results.txt', output_path='./organized.txt'):
    output_str = f'{"(mChi, mPhi)":20} {"xsec":20} {"s95(exp)":20} {"s95(obs)":20}\n'

    with open(results_path) as results_file:
        results = results_file.readlines()
        for result in results:
            result = result.split()
            mChi, mPhi = result[0][1:-1], result[1][:-1]
            xsec = result[-1]
            with open(f'{summaries_path}/summary-({mChi}, {mPhi}).txt') as summary_file:
                summary = summary_file.readlines()[1:-1]
                summary = [i.split() for i in summary if i.strip()]

                get_sig95exp = lambda x: x[3]
                get_sig95obs = lambda x: x[4]
                best_sr = min(summary, key=get_sig95exp)

                s95exp, sig95obs = get_sig95exp(best_sr), get_sig95obs(best_sr)

            output_str += f'{f"({mChi}, {mPhi})":20} {xsec:20} {s95exp:20} {sig95obs}\n'

    print(output_str)

    with open(output_path, 'w+') as output_file:
        output_file.write(output_str)

    return output_str


if __name__ == '__main__':
    make_xsec_s95()
