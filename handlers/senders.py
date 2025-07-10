import db.places
import db.tasks
import db.teams
from telebot.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
from bot import bot
from constants import BOT_ADMIN_ID
from handlers import teams_dict, tasks_list, TeamState
from handlers.messages import PLAYER_QUEST_END_MESSAGE


async def send_place(team_id: int) -> None:
    """
    Send the place in the current round to all players of the team
    :return:
    """
    team = teams_dict[team_id]
    current_round = team.current_round
    route = team.route
    if current_round >= len(route):
        for player_id in team.members:
            await bot.send_message(chat_id=player_id, text=PLAYER_QUEST_END_MESSAGE)
        team.state = TeamState.DEFAULT
        await db.teams.set_state(team_id=team_id, state=TeamState.DEFAULT)
        await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{team.name} solved all tasks.')
        return
    place_id = route[current_round]
    place = await db.places.get_info(place_id)
    for player_id in team.members:
        text = place.text
        photo_id = place.photo_id
        await bot.send_photo(player_id, photo=photo_id, caption=text)

    teams_dict[team_id].state = TeamState.PLACE
    await db.teams.set_state(team_id=team_id, state=TeamState.PLACE)
    await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{place_id} is sent to members of {team.name}')


async def send_task(team_id: int) -> None:
    """
    Send the task in the current round to all players
    :return:
    """
    team = teams_dict[team_id]
    current_round = team.current_round
    task_id = tasks_list[current_round]
    task = await db.tasks.get_info(task_id)
    for player_id in team.members:
        text = task.text
        await bot.send_message(chat_id=player_id, text=text)
        if task.photo_ids:
            await bot.send_media_group(player_id, [InputMediaPhoto(photo_id) for photo_id in task.photo_ids])
        if task.video_ids:
            await bot.send_media_group(player_id, [InputMediaVideo(video_id) for video_id in task.video_ids])
        if task.audio_ids:
            await bot.send_media_group(player_id, [InputMediaAudio(audio_id) for audio_id in task.audio_ids])

    teams_dict[team_id].state = TeamState.TASK
    await db.teams.set_state(team_id=team_id, state=TeamState.TASK)
    await bot.send_message(chat_id=BOT_ADMIN_ID, text=f'{task_id} is sent to members of {team.name}')
