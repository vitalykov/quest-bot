import aiosqlite
from constants import DB_FILE

__all__ = [
    'add_photo',
    'add_audio',
    'add_video',
    'get_photos',
    'get_audios',
    'get_videos',
    'delete_photos',
    'delete_audios',
    'delete_videos',
    'delete_media'
]


async def add_photo(photo_id: str, task_id: str) -> None:
    """
    Add photo with photo_id to the existing task with task_id
    :param photo_id: id of the photo in the telegram server
    :param task_id: id of the task in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO photos (id, task_id) VALUES (?, ?)', (photo_id, task_id))
        await db.commit()


async def add_video(video_id: str, task_id: str) -> None:
    """
    Add video with video_id to the existing task with task_id
    :param video_id: id of the video in the telegram server
    :param task_id: id of the task in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO videos (id, task_id) VALUES (?, ?)', (video_id, task_id))
        await db.commit()


async def add_audio(audio_id: str, task_id: str) -> None:
    """
    Add audio with audio_id to the existing task with task_id
    :param audio_id: id of the audio in the telegram server
    :param task_id: id of the task in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT INTO audios (id, task_id) VALUES (?, ?)', (audio_id, task_id))
        await db.commit()


async def get_photos(task_id: str) -> list[str]:
    """
    Get the list of photos related to the specific task
    :param task_id: id of the task in the database
    :return: list of ids of the photos in the telegram server
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT id FROM photos WHERE task_id = ?', (task_id, )) as cursor:
            photo_ids = [row[0] async for row in cursor]
    return photo_ids


async def get_videos(task_id: str) -> list[str]:
    """
    Get the list of videos related to the specific task
    :param task_id: id of the task in the database
    :return: list of ids of the videos in the telegram server
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT id FROM videos WHERE task_id = ?', (task_id, )) as cursor:
            video_ids = [row[0] async for row in cursor]
    return video_ids


async def get_audios(task_id: str) -> list[str]:
    """
    Get the list of audios related to the specific task
    :param task_id: id of the task in the database
    :return: list of ids of the audios in the telegram server
    """
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT id FROM audios WHERE task_id = ?', (task_id, )) as cursor:
            audio_ids = [row[0] async for row in cursor]
    return audio_ids


async def delete_photos(task_id: str) -> None:
    """
    Delete photos from the databsase related to the task_id
    :param task_id: id of the task in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM photos WHERE task_id = ?', (task_id, ));
        await db.commit()


async def delete_videos(task_id: str) -> None:
    """
    Delete videos from the databsase related to the task_id
    :param task_id: id of the task in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM videos WHERE task_id = ?', (task_id, ));
        await db.commit()


async def delete_audios(task_id: str) -> None:
    """
    Delete audios from the databsase related to the task_id
    :param task_id: id of the task in the database
    :return:
    """
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('DELETE FROM audios WHERE task_id = ?', (task_id, ));
        await db.commit()


async def delete_media(task_id: str) -> None:
    """
    Delete media files from the database related to the task_id
    :param task_id: id of the task
    :return:
    """
    await delete_photos(task_id)
    await delete_videos(task_id)
    await delete_audios(task_id)
