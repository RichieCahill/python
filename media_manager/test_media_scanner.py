from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from sqlalchemy.orm import Session as DB_Session

from media_scanner import (
    add_batched_media,
    add_media,
    batched,
    find_media_files,
    get_media_info,
    remove_existing_files,
)


def test_add_batched_media():
    db_session = MagicMock(spec=DB_Session)

    file_group = [Path("/test/path/Movies/file1"), Path("/test/path/Movies/file2")]

    with patch(
        "media_scanner.get_media_info",
        return_value={"title": "Test Title", "duration": 3600},
    ) as media_info_mock:
        add_batched_media(file_group, db_session)

        media_info_mock.assert_any_call(
            Path("/test/path/Movies/file1"), "/ZFS/Storage/Plex/"
        )
        media_info_mock.assert_any_call(
            Path("/test/path/Movies/file2"), "/ZFS/Storage/Plex/"
        )

        db_session.execute.assert_called_once()
        db_session.commit.assert_called_once()


def test_find_media_files(tmp_path):
    [
        (tmp_path / file).touch()
        for file in [
            "test.mp4",
            "test.mkv",
            "test.avi",
            "test.txt",
            "test.jpg",
            "test.png",
        ]
    ]

    search_dirs = [
        str(tmp_path),
    ]

    media_files = find_media_files(search_dirs, extensions=["*.mp4", "*.mkv", "*.avi"])

    assert media_files == {
        tmp_path / "test.mp4",
        tmp_path / "test.mkv",
        tmp_path / "test.avi",
    }


def test_find_media_files_multy_dir(tmp_path):
    [
        (tmp_path / file).touch()
        for file in [
            "test.mp4",
            "test.mkv",
            "test.avi",
            "test.txt",
            "test.jpg",
            "test.png",
        ]
    ]

    dir1 = tmp_path / "dir1"
    dir1.mkdir()
    [
        (dir1 / file).touch()
        for file in [
            "test1.mp4",
            "test1.mkv",
            "test1.avi",
            "test1.txt",
            "test1.jpg",
            "test1.png",
        ]
    ]

    dir2 = tmp_path / "dir2"
    dir2.mkdir()
    [
        (dir2 / file).touch()
        for file in [
            "test2.mp4",
            "test2.mkv",
            "test2.avi",
            "test2.txt",
            "test2.jpg",
            "test2.png",
        ]
    ]

    search_dirs = [
        str(dir1),
        str(dir2),
    ]

    media_files = find_media_files(search_dirs, extensions=["*.mp4", "*.mkv", "*.avi"])

    assert media_files == {
        dir1 / "test1.mp4",
        dir1 / "test1.mkv",
        dir1 / "test1.avi",
        dir2 / "test2.mp4",
        dir2 / "test2.mkv",
        dir2 / "test2.avi",
    }


def test_batched():
    iterable = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    batched_size = 3
    expected_output = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    assert list(batched(iterable, batched_size)) == expected_output

    iterable = [1, 2, 3, 4, 5]
    batched_size = 2
    expected_output = [[1, 2], [3, 4], [5]]
    assert list(batched(iterable, batched_size)) == expected_output

    iterable = [1]
    batched_size = 1
    expected_output = [[1]]
    assert list(batched(iterable, batched_size)) == expected_output

    iterable = []
    batched_size = 1
    expected_output = []
    assert list(batched(iterable, batched_size)) == expected_output


def test_remove_existing_files():
    files = [
        Path("file1.mp4"),
        Path("file2.mkv"),
        Path("file3.avi"),
        Path("file4.txt"),
        Path("file5.jpg"),
        Path("file6.png"),
    ]

    db_session = Mock()

    db_session.execute.return_value.scalars.return_value.all.return_value = [
        "file1.mp4",
        "file3.avi",
        "file5.jpg",
    ]

    result = remove_existing_files(files, db_session)

    assert result == [
        Path("file2.mkv"),
        Path("file4.txt"),
        Path("file6.png"),
    ]


def test_add_media():
    files = [
        Path("file1.mp4"),
        Path("file2.mkv"),
        Path("file3.avi"),
        Path("file4.txt"),
        Path("file5.jpg"),
        Path("file6.png"),
    ]

    db_session = MagicMock(spec=DB_Session)

    with patch("media_scanner.add_batched_media") as mock_add_batched_media:
        add_media(files, db_session)

        mock_add_batched_media.assert_called_once_with(
            file_group=files, db_session=db_session
        )


def test_add_media_150_files():
    files = [Path("file.mp4") for _ in range(150)]

    db_session = MagicMock(spec=DB_Session)

    with patch("media_scanner.add_batched_media") as mock_add_batched_media:
        add_media(files, db_session)

        mock_add_batched_media.expected_calls(
            call(
                file_group=[Path("file.mp4") for _ in range(100)],
                db_session=db_session,
            ),
            call(
                file_group=[Path("file.mp4") for _ in range(50)],
                db_session=db_session,
            ),
        )


def test_get_media_info_movies():
    with patch("media_scanner.MediaInfo.parse") as mock_parse:
        mock_track = mock_parse.return_value.tracks[0]
        mock_track.complete_name = "/test/path/Movies/media-1234.mp4"
        mock_track.frame_count = 100
        mock_track.stream_size = 1000000
        mock_track.codecs_video = "h264"
        mock_track.frame_rate = 30.0
        mock_track.file_size = 100000000
        mock_track.duration = 3600
        mock_track.file_extension = ".mp4"
        mock_track.overall_bit_rate = 128000
        mock_track.count_of_audio_streams = 1
        mock_track.audio_codecs = "aac"
        mock_track.audio_language_list = ["en"]
        mock_track.format = "MPEG-4"

        media_info = get_media_info(
            file_path=Path("/test/path/Movies/media-1234.mp4"),
            search_dir="/test/path/",
        )

    assert media_info == {
        "file_path": "/test/path/Movies/media-1234.mp4",
        "media_type": "Movies",
        "frame_count": 100,
        "stream_size": 1000000,
        "video_codec": "h264",
        "frame_rate": 30.0,
        "file_size": 100000000,
        "duration": 3600,
        "file_name": "media-1234.mp4",
        "file_extension": ".mp4",
        "bit_rate": 128000,
        "audio_stream_count": 1,
        "audio_codec": "aac",
        "audio_language": ["en"],
        "video_format": "MPEG-4",
        "series_name": None,
        "season": None,
        "release_year": 1234,
    }


def test_get_media_info_tv():
    with patch("media_scanner.MediaInfo.parse") as mock_parse:
        mock_track = mock_parse.return_value.tracks[0]
        mock_track.complete_name = "/test/path/TV/show-1234/Season_01/media.mp4"
        mock_track.frame_count = 100
        mock_track.stream_size = 1000000
        mock_track.codecs_video = "h264"
        mock_track.frame_rate = 30.0
        mock_track.file_size = 100000000
        mock_track.duration = 3600
        mock_track.file_extension = ".mp4"
        mock_track.overall_bit_rate = 128000
        mock_track.count_of_audio_streams = 1
        mock_track.audio_codecs = "aac"
        mock_track.audio_language_list = ["en"]
        mock_track.format = "MPEG-4"

        media_info = get_media_info(
            file_path=Path("/test/path/TV/show-1234/Season_01/media.mp4"),
            search_dir="/test/path/",
        )

    assert media_info == {
        "file_path": "/test/path/TV/show-1234/Season_01/media.mp4",
        "media_type": "TV",
        "frame_count": 100,
        "stream_size": 1000000,
        "video_codec": "h264",
        "frame_rate": 30.0,
        "file_size": 100000000,
        "duration": 3600,
        "file_name": "media.mp4",
        "file_extension": ".mp4",
        "bit_rate": 128000,
        "audio_stream_count": 1,
        "audio_codec": "aac",
        "audio_language": ["en"],
        "video_format": "MPEG-4",
        "series_name": "show",
        "season": "Season_01",
        "release_year": 1234,
    }
