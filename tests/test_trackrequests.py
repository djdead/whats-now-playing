#!/usr/bin/env python3
''' test the trackpoller '''

import asyncio
import logging
import pathlib
import threading

import pytest  # pylint: disable=import-error
import pytest_asyncio  # pylint: disable=import-error

import nowplaying.trackrequests  # pylint: disable=import-error


@pytest_asyncio.fixture
async def trackrequestbootstrap(bootstrap, getroot):  # pylint: disable=redefined-outer-name
    ''' bootstrap a configuration '''
    stopevent = threading.Event()
    config = bootstrap
    config.cparser.setValue('settings/input', 'json')
    playlistpath = pathlib.Path(getroot).joinpath('tests', 'playlists', 'json',
                                                  'test.json')
    config.pluginobjs['inputs']['nowplaying.inputs.json'].load_playlists(
        getroot, playlistpath)
    config.cparser.sync()
    yield nowplaying.trackrequests.Requests(stopevent=stopevent,
                                            config=config,
                                            testmode=True)
    stopevent.set()
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_trackrequest_artisttitlenoquote(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist - title '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', 'artist - title')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_artisttitlenoquotespaces(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist - title '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user', '      artist     -      title    ')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_artisttitlenoquotecomplex(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist - title '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user',
        '      prince and the revolution     -      purple rain    ')
    assert data['artist'] == 'prince and the revolution'
    assert data['title'] == 'purple rain'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_artisttitlequotes(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist - "title" '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', 'artist - "title"')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_artisttitlequotesspaces(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist - "title" '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user', '    artist    -     "title"   ')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_titlequotesartist(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' "title" - artist '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', '"title" - artist')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_titlequotesbyartist(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' title by artist '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', '"title" by artist')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_quotedweirdal(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' weird al is weird '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user',
        '"Weird Al" Yankovic - This Is The Life.')
    assert data['artist'] == '"Weird Al" Yankovic'
    assert data['title'] == 'This Is The Life.'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_quotedchampagne(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' weird al is weird '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user',
        'Evelyn "Champagne" King - "I\'m In Love"')
    assert data['artist'] == 'Evelyn "Champagne" King'
    assert data['title'] == 'I\'m In Love'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_xtcfornigel(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' for part of the title '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user', 'xtc - making plans for nigel')
    assert data['artist'] == 'xtc'
    assert data['title'] == 'making plans for nigel'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_xtcforatnigel(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' for @user test '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request(
        {'displayname': 'test'}, 'user', 'xtc - making plans for @nigel')
    assert data['artist'] == 'xtc'
    assert data['title'] == 'making plans'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_nospace(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist-title '''

    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', 'artist-title')
    assert data['artist'] == 'artist'
    assert data['title'] == 'title'
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'


@pytest.mark.asyncio
async def test_trackrequest_rouletterequest(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist-title '''

    trackrequest = trackrequestbootstrap
    logging.debug(trackrequest.databasefile)
    trackrequest.clear_roulette_artist_dupes()
    trackrequest.config.cparser.setValue('settings/requests', True)
    trackrequest.config.cparser.sync()

    data = await trackrequest.user_roulette_request(
        {
            'displayname': 'test',
            'playlist': 'testlist'
        }, 'user', 'artist-title')
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'

    data = await trackrequest.get_request({
        'artist': 'Nine Inch Nails',
        'title': '15 Ghosts II'
    })
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'
    assert data['requesterimageraw']


@pytest.mark.asyncio
async def test_trackrequest_rouletterequest_normalized(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist-title '''

    trackrequest = trackrequestbootstrap
    logging.debug(trackrequest.databasefile)
    trackrequest.clear_roulette_artist_dupes()
    trackrequest.config.cparser.setValue('settings/requests', True)
    trackrequest.config.cparser.sync()

    data = await trackrequest.user_roulette_request(
        {
            'displayname': 'test',
            'playlist': 'testlist'
        }, 'user', 'artist-title')
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'

    data = await trackrequest.get_request({
        'artist': 'Níne Ínch Näíls',
        'title': '15 Ghosts II'
    })
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'
    assert data['requesterimageraw']


@pytest.mark.asyncio
async def test_trackrequest_getrequest_artist(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist-title '''

    trackrequest = trackrequestbootstrap
    logging.debug(trackrequest.databasefile)
    trackrequest.clear_roulette_artist_dupes()
    trackrequest.config.cparser.setValue('settings/requests', True)
    trackrequest.config.cparser.sync()
    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', 'Nine Inch Nails')
    logging.debug(data)
    assert data['requestartist'] == 'Nine Inch Nails'
    assert not data['requesttitle']

    data = await trackrequest.get_request({
        'artist': 'Níne Ínch Näíls',
        'title': '15 Ghosts II'
    })
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'
    assert data['requesterimageraw']


@pytest.mark.asyncio
async def test_trackrequest_getrequest_title(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist-title '''

    trackrequest = trackrequestbootstrap
    logging.debug(trackrequest.databasefile)
    trackrequest.clear_roulette_artist_dupes()
    trackrequest.config.cparser.setValue('settings/requests', True)
    trackrequest.config.cparser.sync()
    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_track_request({'displayname': 'test'},
                                                 'user', '"15 Ghosts II"')
    logging.debug(data)
    assert not data['requestartist']
    assert data['requesttitle'] == '15 Ghosts II'

    data = await trackrequest.get_request({
        'artist': 'Níne Ínch Näíls',
        'title': '15 Ghosts II'
    })
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'
    assert data['requesterimageraw']


@pytest.mark.asyncio
async def test_trackrequest_getrequest_filename(trackrequestbootstrap):  # pylint: disable=redefined-outer-name
    ''' artist-title '''

    trackrequest = trackrequestbootstrap
    logging.debug(trackrequest.databasefile)
    trackrequest.clear_roulette_artist_dupes()
    trackrequest.config.cparser.setValue('settings/requests', True)
    trackrequest.config.cparser.sync()
    trackrequest = trackrequestbootstrap

    data = await trackrequest.user_roulette_request(
        {
            'displayname': 'test',
            'playlist': 'testlist'
        }, 'user', 'artist-title')

    filename = trackrequest.config.pluginobjs['inputs'][
        'nowplaying.inputs.json'].playlists['testlist'][0]

    data = await trackrequest.get_request({'filename': filename})
    assert data['requester'] == 'user'
    assert data['requestdisplayname'] == 'test'
    assert data['requesterimageraw']