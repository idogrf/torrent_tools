import os
import io
import subprocess

FLEXGET_PATH = os.getenv('FLEXGET_PATH')


def send_to_transmission(params):
    p = subprocess.Popen(['transmission-remote', '--authenv'] + params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()

    output = output.decode("utf-8")
    err = err.decode("utf-8")

    return f'{output}\n{err}'


def execute_flexget_rss_update():
    print('executing flextget script')
    current_wd = os.getcwdb()
    os.chdir(FLEXGET_PATH)
    p = subprocess.Popen(['flexget', 'execute'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    os.chdir(current_wd)
    output = output.decode("utf-8")
    err = err.decode("utf-8")

    response = _parse_flexget_response(output, err)

    return response


def _parse_flexget_response(output, err):
    if len(err) > 0:
        return f'Error: {err}'

    buf = io.StringIO(output)
    lines = buf.readlines()

    accepted = []
    for line in lines:
        if 'Download_TV_Shows' in line and 'ACCEPTED' in line:
            parsed_line = line.split('ACCEPTED: ')[1]
            parsed_line = parsed_line.split('`')[1]
            accepted.append(parsed_line)

    if len(accepted) == 0:
        return 'No new torrents downloaded.'
    else:
        return 'New torrents downloaded: \n - ' + '\n - '.join(accepted)
