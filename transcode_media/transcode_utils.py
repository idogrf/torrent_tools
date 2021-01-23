import os

from pymediainfo import MediaInfo


def get_all_files(media_dir):
    file_list = []
    for path, subdirs, files in os.walk(media_dir):
        for name in files:
            file_list.append({'filename': name, 'filepath': path})
    return file_list


def get_media_info(path):
    media_info = MediaInfo.parse(path)
    track_types = [track.track_type.lower() for track in media_info.tracks]
    if 'audio' in track_types and 'video' in track_types:
        return media_info
    return None