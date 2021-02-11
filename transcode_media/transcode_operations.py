import os
import subprocess

import ffmpeg

from torrent_tools.data_operations import get_free_media_space
from transcode_media.transcode_utils import get_all_files, get_media_info


def convert_subtitles(media_dir):
    file_list = get_all_files(media_dir)
    files_with_no_valid_subtitles = []
    for file in file_list:
        media_info = get_media_info(os.path.join(file['filepath'], file['filename']))
        if media_info is not None:
            print(f"Checking subtitles for - {file['filename']}")
        else:
            continue
        subtitles_tracks = [track for track in media_info.tracks if track.track_type == 'Text']
        if len(subtitles_tracks) == 0:
            continue
        valid_subtitles_channels = [sub_track.channel_s for sub_track in subtitles_tracks if
                                    sub_track.format.lower() not in ['ass', 'pgs']]
        has_valid_subtitles_track = len(valid_subtitles_channels) >= 1
        if not has_valid_subtitles_track:
            print(f"No valid subtitles track - {file['filename']}")
            files_with_no_valid_subtitles.append(file)

    if len(files_with_no_valid_subtitles) == 0:
        print('No files found for subtitles conversion\n')
        return [], []
    print('\n')

    converted_files = []
    cant_convert = []
    for file in files_with_no_valid_subtitles:
        file_path = os.path.join(file['filepath'], file['filename'])

        filename_parts = file['filename'].split('.')
        new_filename = '.'.join(filename_parts[:-1]) + '.srt'

        if os.path.exists(os.path.join(file['filepath'], new_filename)):
            print(f"Skipping {new_filename} - File already exists")
            continue

        print(f'Converting Subtitles for - {file["filename"]}')

        cmd = f"ffmpeg -txt_format srt -i {file_path} {os.path.join(file['filepath'], new_filename)}"
        args = cmd.split(' ')
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        output = output.decode("utf-8")
        err = err.decode("utf-8")

        print(output)
        print(err)
        if len(err) > 0:
            cant_convert.append(file["filename"])
        converted_files.append(new_filename)

    return converted_files, cant_convert


def convert_audio(media_dir):
    file_list = get_all_files(media_dir)
    files_with_no_valid_audio = []
    for file in file_list:
        media_info = get_media_info(os.path.join(file['filepath'], file['filename']))
        if media_info is not None:
            print(f"Checking audio for - {file['filename']}")
        else:
            continue

        audio_tracks = [track for track in media_info.tracks if track.track_type == 'Audio']
        audio_tracks = [audio_track for audio_track in audio_tracks if audio_track.format not in ['DTS']]
        audio_tracks = [audio_track for audio_track in audio_tracks if audio_track.channel_s <= 6]
        has_valid_audio_track = len(audio_tracks) >= 1
        if not has_valid_audio_track:
            print(f"No valid audio track - {file['filename']}")
            files_with_no_valid_audio.append(file)

    if len(files_with_no_valid_audio) == 0:
        print('No files found for audio conversion\n')
        return [],[]
    print('\n')

    converted_files = []
    cant_convert = []
    for file in files_with_no_valid_audio:
        file_path = os.path.join(file['filepath'], file['filename'])
        free_space = get_free_media_space()
        file_size = os.path.getsize(file_path) / (2 ** 30)
        if file_size > free_space:
            cant_convert.append(file['filename'])
            print(f"Cannot convert file {file['filename']} not enough disk space")
            continue

        stream = ffmpeg.input(file_path)
        filename_parts = file['filename'].split('.')
        filename_parts[-2] = f'{filename_parts[-2]}_converted'
        new_filename = '.'.join(filename_parts)
        stream = ffmpeg.output(stream, os.path.join(file['filepath'], new_filename), acodec='eac3', vcodec='copy')
        print(f'Converting Audio for - {file["filename"]}')
        ffmpeg.run(stream)
        os.remove(file_path)
        converted_files.append(new_filename)

    return converted_files, cant_convert
