#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from id3 import fill_tags
from retrieve import retrieve_file


def _get_filepath(song, extension, config):
    format_dict = {
        'song': song.name,
        'album': song.album_name,
        'artist': song.artist,
        'playlist': config.get('playlist', '')
    }

    directory = config['directory'].format(**format_dict)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = config['filename'].format(**format_dict) + extension
    filepath = os.path.join(directory, filename)
    return filepath


def download_lyric(song, config):
    filepath = _get_filepath(song, '.lrc', config)
    if os.path.exists(filepath):
        return

    with open(filepath, 'w') as file:
        file.write(song.lyric.encode('UTF-8'))


def download_audio(song, config):
    filepath = _get_filepath(song, '.mp3', config)
    if os.path.exists(filepath):
        return

    quality = config['quality']
    if quality == 'normal':
        remote_url = song.default_mp3_url
    else:
        remote_url = getattr(song, quality + '_quality_mp3_url')
        if remote_url is None:
            remote_url = song.default_mp3_url

    local_url = filepath + '.part'
    retrieve_file(remote_url, local_url, filepath)
    fill_tags(local_url, song, config)
    os.rename(local_url, filepath)


def download_song(song, config):
    config['song'] = song.name
    download_audio(song, config)
    if config['lyric'] and song.lyric:
        download_lyric(song, config)


def download_songs(songs, config):
    for song in songs:
        download_song(song, config)


def download_album(album, config):
    config['album'] = album.name
    download_songs(album.songs, config)


def download_albums(albums, config):
    for album in albums:
        download_album(album, config)


def download_playlist(playlist, config):
    config['playlist'] = playlist.name
    download_songs(playlist.songs, config)


def download_playlists(playlists, config):
    for playlist in playlists:
        download_playlist(playlist, config)


def download_artist(artist, config):
    config['artist'] = artist.name
    download_albums(artist.albums, config)


def download_artists(artists, config):
    for artist in artists:
        download_artist(artist, config)
