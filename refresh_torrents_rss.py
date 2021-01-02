from torrent_tools.data_operations import delete_small_dirs
from torrent_tools.torrent_operations import refresh_rss_torrents


if __name__ == '__main__':
    refresh_rss_torrents()
    delete_small_dirs()
