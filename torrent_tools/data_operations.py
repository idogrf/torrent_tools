import os
import psutil
import shutil

MEDIA_PATH = os.getenv('MEDIA_PATH')
ROOT_PATH = os.getenv('ROOT_PATH')
TV_SHOWS_PATH = os.getenv('TV_SHOWS_PATH')


def _get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def get_free_root_space():
    return psutil.disk_usage(ROOT_PATH).free / (2 ** 30)


def get_free_media_space():
    return psutil.disk_usage(MEDIA_PATH).free / (2 ** 30)


def delete_small_dirs():
    deleted_dirs = []
    for dirpath, dirnames, filenames in os.walk(TV_SHOWS_PATH):
        if len(dirnames) == 0:
            dir_size = _get_size(dirpath) / (2 ** 30)
            if dir_size < 0.01:
                print(f'Deleting small dir - {dirpath}')
                shutil.rmtree(dirpath)
                deleted_dirs.append(dirpath)
    if len(deleted_dirs) == 0:
        return 'Found no empty dirs'
    else:
        return 'Deleted dirs: \n - ' + '\n - '.join(deleted_dirs)
