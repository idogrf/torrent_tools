import os
import sys
from transcode_media.transcode_operations import convert_subtitles, convert_audio

sys.path.append('/home/pi/projects/repositories/telegram_bots')
from telegram_subscribers_update import UpdaterBot


def run(media_dir):
    updater_bot = UpdaterBot()

    converted_audio_files = convert_audio(media_dir)
    converted_subtitles_files = convert_subtitles(media_dir)

    if (len(converted_audio_files) > 0) or (len(converted_subtitles_files) > 0):
        updater_bot.update_subscribers('The following files has been converted - ')
        updater_bot.update_subscribers(converted_audio_files + converted_subtitles_files)


if __name__ == '__main__':

    media_dir = os.getenv('MEDIA_PATH')

    run(media_dir=media_dir)