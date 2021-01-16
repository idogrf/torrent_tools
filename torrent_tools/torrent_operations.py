from datetime import datetime

from torrent_tools.data_operations import get_free_media_space, get_free_root_space
from torrent_tools.torrent_utils import send_to_transmission, execute_flexget_rss_update


def refresh_rss_torrents():
    print(f'Starting script. Time - {datetime.now()}')

    free_media_space = get_free_media_space()

    if free_media_space > 5:
        return execute_flexget_rss_update()
    else:
        return False, 'Not enough disk space'


def download_torrent(torrent_url, dest_path):
    params = ['--add', torrent_url, '--download-dir', dest_path]
    response = send_to_transmission(params)
    return response


def stop_all_torrents():
    params = ['--torrent', 'all', '--stop']
    response = send_to_transmission(params)
    if 'success' in response:
        return 'Success'
    return response


def start_all_torrents():
    params = ['--torrent', 'all', '--start']
    response = send_to_transmission(params)
    if 'success' in response:
        return 'Success'
    return response


def list_torrents():
    params = ['--list']
    response = send_to_transmission(params)
    return response



