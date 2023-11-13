"""test."""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from time import time

import tomllib as toml
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
    added:               Mapped[datetime] = mapped_column(default=datetime.now)
    modified:            Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    file_path:           Mapped[str] = mapped_column(unique=True, index=True)
    release_year:        Mapped[int] = mapped_column(nullable=True)

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
    season:              Mapped[str] = mapped_column(nullable=True)

    subtitle:            Mapped[bool] = mapped_column(default=False)
    artwork:             Mapped[bool] = mapped_column(default=False)


def find_media_files(search_dirs: list[str], extensions: list[str]) -> set[Path]:
    """
    Find media files with the given extensions in the specified directories.

    Args:
        search_dirs (list[str]): list of directories to search for media files.
        extensions (list[str]): list of file extensions to search for.

    Returns:
        Set[Path]: Set of Path objects representing the found media files.
    """
    logging.info("Searching for media files")
    files = set()
    for search_dir in search_dirs:
        search_path = Path(search_dir)

        for file_extensions in extensions:
            logging.debug(f"Searching for {file_extensions}")
            files.update(search_path.rglob(file_extensions))

    return files


def get_media_info(
    file_path: Path,
    search_dir: str,
) -> dict[str, str | bool | int | float | None]:
    """
    Returns a dictionary containing information about a media file.

    Args:
        file_path (Path): The path to the media file.

    Returns:
        dict[str, str | bool | int | float | None]:
        A dictionary containing the following keys:
            - file_path
            - media_type
            - frame_count
            - stream_size
            - video_codec
            - frame_rate
            - file_size
            - duration
            - file_name
            - file_extension
            - bit_rate
            - audio_stream_count
            - audio_codec
            - audio_language
            - video_format
            - series_name (if media_type is TV)
            - season (if media_type is TV)
            - release_year
    """

    media_info = MediaInfo.parse(file_path)
    track = media_info.tracks[0]

    complete_name = track.complete_name
    media_type = complete_name.replace(search_dir, "").split("/")[0]

    if media_type in ("4K", "Movies"):
        release_year = int(file_path.stem.split("-")[-1])
        series_name = None
        season = None

    if media_type == "TV":
        series_info = complete_name.replace(f"{search_dir}TV/", "").split("/")
        release_year = int(series_info[0].split("-")[-1])
        series_name = series_info[0].replace(f"-{release_year}", "")
        season = series_info[1]

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
        "season": season,
        "release_year": release_year,
    }


def add_batched_media(file_group: list[Path], db_session: DB_Session) -> None:
    """
    Add a batch of media files to the database.

    Args:
        file_group (list[Path]): A list of file paths to media files.
        db_session (Session): A SQLAlchemy database session.

    Returns:
        None
    """
    batched_start_time = time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        test2 = [executor.submit(get_media_info, file_path, "/ZFS/Storage/Plex/") for file_path in file_group]
        test = [future.result() for future in as_completed(test2)]
    db_session.execute(insert(Media), test)
    logging.info("Committing to database")
    db_session.commit()
    batched_end_time = time()
    logging.info(f"Batched took {batched_end_time - batched_start_time} seconds")


def batched(iterable, batched_size):
    """
    Splits an iterable into batches of a specified size.

    Args:
        iterable: The iterable to be batched.
        batched_size: The size of each batch.

    Yields:
        A batch of the specified size from the iterable.
    """
    iterable_len = len(iterable)
    for ndx in range(0, iterable_len, batched_size):
        yield iterable[ndx : min(ndx + batched_size, iterable_len)]


def add_media(files: list[Path], db_session: DB_Session) -> None:
    """
    Adds a list of media files to the database.

    Args:
        files (list[Path]): A list of Path objects representing the media files to be added.
        db_session (DB_Session): An instance of the database session to use for adding the media files.

    Returns:
        None
    """
    logging.info(f"Adding {len(files)} files to database")
    # TODO replace with batched when 2.12 is released
    file_groups = batched(files, batched_size=100)
    for file_group in file_groups:
        add_batched_media(file_group=file_group, db_session=db_session)


def remove_existing_files(files: list[Path], db_session: DB_Session) -> list[Path]:
    """
    Removes existing files from the given list of files based on their file names
    that already exist in the database.

    Args:
        files (list[Path]): A list of Path objects representing files to be scanned.
        db_session (Session): A SQLAlchemy session object to interact with the database.

    Returns:
        list[Path]: A list of Path objects representing files that do not exist in the database.
    """
    logging.info("Removing existing files")

    db_paths = db_session.execute(select(Media.file_name)).scalars().all()

    return [file for file in files if file.name not in db_paths]


def main() -> None:
    """
    Main function that scans for media files in specified directories,
    removes existing files from the database, and adds new files to the database.
    """
    start_time = time()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s-%(name)s-%(levelname)s-%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting Media Scanner")

    config_path = Path("secret.toml")
    with config_path.open("rb") as config_file:
        config = toml.load(config_file)

    engine_url = URL.create(
        "postgresql",
        username=config["database"]["username"],
        password=config["database"]["password"],
        host=config["database"]["host"],
        port=config["database"].get("port", 5432),
        database=config["database"]["database"],
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
