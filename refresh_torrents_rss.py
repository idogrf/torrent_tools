import sys

from torrent_tools.data_operations import delete_small_dirs
from torrent_tools.torrent_operations import refresh_rss_torrents

sys.path.append('/home/pi/projects/repositories/telegram_bots')
from telegram_subscribers_update import UpdaterBot

updater_bot = UpdaterBot()
refresh_response = refresh_rss_torrents()
print(refresh_response)
if refresh_response[0]:
    updater_bot.update_subscribers('The following torrents has been downloaded - ')
    updater_bot.update_subscribers(refresh_response[1])
delete_response = delete_small_dirs()
print(delete_response)


