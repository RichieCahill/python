"""test."""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import time

from pymediainfo import MediaInfo
from sqlalchemy import URL, MetaData, create_engine, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session as DB_Session
from sqlalchemy.types import BigInteger


class MediaManager(DeclarativeBase):
    metadata = MetaData(schema="media_manager")


class Media(MediaManager):
    # fmt: off
    __tablename__ = "media"
    __table_args__ = {}

    id:                  Mapped[int] = mapped_column(primary_key=True)
    file_path:           Mapped[str] = mapped_column(unique=True, index=True)

    audio_codec:         Mapped[str] = mapped_column(nullable=True)
    audio_language:      Mapped[str] = mapped_column(nullable=True)
    audio_stream_count:  Mapped[str] = mapped_column(nullable=True)
    bit_rate:            Mapped[int] = mapped_column(nullable=True)
    file_name:           Mapped[str] = mapped_column(nullable=True)
    duration:            Mapped[int] = mapped_column(nullable=True)
    file_extension:      Mapped[str] = mapped_column(nullable=True)
    file_size:           Mapped[int] = mapped_column(BigInteger)
    frame_count:         Mapped[str] = mapped_column(nullable=True)
    frame_rate:          Mapped[str] = mapped_column(nullable=True)
    media_type:          Mapped[str] = mapped_column(nullable=True)
    stream_size:         Mapped[int] = mapped_column(nullable=True)
    video_codec:         Mapped[str]
    video_format:        Mapped[str] = mapped_column(nullable=True)

    series_name:         Mapped[str] = mapped_column(nullable=True)
    session:             Mapped[str] = mapped_column(nullable=True)


def find_media_files(search_dirs: list[str], extensions: list[str]) -> set[Path]:
    logging.info("Searching for media files")
    files = set()
    for search_dir in search_dirs:
        search_path = Path(search_dir)

        for file_extensions in extensions:
            logging.debug(f"Searching for {file_extensions}")
            files.update(search_path.rglob(file_extensions))

    return files


def get_media_info(file_path: str) -> dict:
    search_dir = "/ZFS/Storage/Plex/"
    media_info = MediaInfo.parse(file_path)
    track = media_info.tracks[0]
    series_name = None
    session = None
    complete_name = track.complete_name
    media_type = complete_name.replace(search_dir, "").split("/")[0]
    if media_type == "TV":
        series_info = complete_name.replace(f"{search_dir}TV/", "").split("/")
        series_name = series_info[0]
        session = series_info[1]

    return {
        "file_path": track.complete_name,
        "media_type": media_type,
        "frame_count": track.frame_count,
        "stream_size": track.stream_size,
        "video_codec": track.codecs_video,
        "frame_rate": track.frame_rate,
        "file_size": track.file_size,
        "duration": track.duration,
        "file_name": file_path.name,
        "file_extension": track.file_extension,
        "bit_rate": track.overall_bit_rate,
        "audio_stream_count": track.count_of_audio_streams,
        "audio_codec": track.audio_codecs,
        "audio_language": track.audio_language_list,
        "video_format": track.format,
        "series_name": series_name,
        "session": session,
    }


def add_batched_media(file_group: list[Path], db_session: DB_Session) -> None:
    batched_start_time = time()
    with ThreadPoolExecutor(max_workers=100) as executor:
        test2 = [executor.submit(get_media_info, file_path) for file_path in file_group]
        test = [future.result() for future in as_completed(test2)]
    db_session.execute(insert(Media), test)
    logging.info("Committing to database")
    db_session.commit()
    batched_end_time = time()
    logging.info(f"Batched took {batched_end_time - batched_start_time} seconds")


def batched(iterable, batched_size):
    iterable_len = len(iterable)
    for ndx in range(0, iterable_len, batched_size):
        yield iterable[ndx : min(ndx + batched_size, iterable_len)]


# 121mb ram
# 2023-11-05 16:36:21-root-INFO-Finished in 1267.9497802257538 seconds
# 2023-11-06 02:17:26-root-INFO-Finished in 473.0883719921112 seconds
# 2023-11-06 03:44:58-root-INFO-Finished in 388.3023223876953 seconds
# 2023-11-11 19:55:46-root-INFO-Finished in 734.7975401878357 seconds batch size 1
# 2023-11-11 02:06:23-root-INFO-Finished in 892.5836849212646 seconds batch size 100
# 2023-11-11 02:57:31-root-INFO-Finished in 1085.956045627594 seconds batch size 1000

# 2023-11-11 20:05:02-root-INFO-Finished in 66.27891302108765 seconds batch size 1000
# with 100 workers scaning media


def add_media(files: list[Path], db_session: DB_Session) -> None:
    logging.info(f"Adding {len(files)} files to database")
    # TODO replace with batched when 2.12 is released
    file_groups = batched(files, batched_size=1)
    for file_group in file_groups:
        add_batched_media(file_group=file_group, db_session=db_session)


def remove_existing_files(files: list[Path], db_session: DB_Session) -> list[Path]:
    logging.info("Removing existing files")

    db_paths = db_session.execute(select(Media.file_name)).scalars().all()

    return [file for file in files if file.name not in db_paths]


def main() -> None:
    """main."""

    start_time = time()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting Media Scanner")



    engine_url = URL.create(
        "postgresql",
        username=username,
        password=password,
        host=host,
        port=5432,
        database=database,
    )
    logging.debug(f"engine_url {engine_url}")
    engine = create_engine(engine_url)
    MediaManager.metadata.create_all(engine)

    files = find_media_files(
        search_dirs=[
            "/ZFS/Storage/Plex/4K/",
            "/ZFS/Storage/Plex/TV/",
            "/ZFS/Storage/Plex/Movies/",
        ],
        extensions=["*.mp4", "*.mkv", "*.avi", "*.m4v", "*.mov"],
    )

    with DB_Session(engine) as db_session:
        files = remove_existing_files(files, db_session)

        add_media(files, db_session)

    end_time = time()
    logging.info(f"Finished in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
