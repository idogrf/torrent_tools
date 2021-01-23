import os
from transcode_media.transcode_operations import convert_subtitles, convert_audio


def run(media_dir):
    convert_audio(media_dir)
    convert_subtitles(media_dir)


if __name__ == '__main__':

    media_dir = os.getenv('MEDIA_PATH')

    run(media_dir=media_dir)