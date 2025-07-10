"""
Messages, used in the Quest bot
"""

# Admins messages
NEW_TASK_MESSAGE = "Task adding mode acitvated"
NEW_PLACE_MESSAGE = "Place adding mode activated"
WRONG_TASK_FORMAT_ERROR_MESSAGE = "Wrong task format"
WRONG_PLACE_FORMAT_ERROR_MESSAGE = "Wrong place format"
TASK_ADDED_MESSAGE = "Task description is successfully added"
PLACE_ADDED_MESSAGE = "Place is successfully added"
PHOTO_ADDED_MESSAGE = "Photo is successfully added to the task"
VIDEO_ADDED_MESSAGE = "Video is successfully added to the task"
AUDIO_ADDED_MESSAGE = "Audio is successfully added to the task"
END_TASK_MESSAGE = "Task addition mode deactivated"
DELETE_TASK_MESSAGE = "Task deleted"
DELETE_PLACE_MESSAGE = "Place deleted"
SET_ROUTE_MESSAGE = "Route is set for the team"
SET_SCORE_MESSAGE = "Score is set for the task"
QUEST_ALREADY_STARTED_MESSAGE = "Quest have already started"
UNBLOCKED_ALREADY_MESSAGE = "Sending tasks have already unblocked"
HELP_MESSAGE = """
List of the possible commands:
<b>/вжух</b> - start the Quest

<b>/newtask</b> - activate the task adding mode.
In task adding mode you can add description of the task by sending the text message formatted as:

<b>ID</b>: <i>task_id</i>
<b>Text</b>: <i>Please solve this equation x + 2 = 5</i>
<b>Answer</b>: <i>3</i>
<b>Points</b>: <i>10</i>

After you send this message, you can also add some photos, videos and audios to newly created task.
<b>/endtask</b> - deactivate the task adding mode. Use this command when you have added all you want to the task. 
<b>/delete task_id</b> - delete the task with task_id
<b>/newplace</b> - activate the place adding mode
In place adding mode you can add description of the place by sending the text message formatted as:

<b>ID</b>: <i>place_id</i>
<b>Text</b>: <i>some text</i>
<b>Password</b>: <i>something</i>

<b>/route N</b> - get the sequence of places for the team N (1 or 2)
<b>/route N task1 task2 ...</b> - set the sequence of places for the team N
<b>/score task_id N</b> - set the score for solution of the task with task_id
<b>/teamname N Name of the team</b> - set the name for the team N
<b>/results</b> - show the leaderboard
<b>/finish</b> - finish theQuest
<b>/help</b> - show this message
"""


# Players messages
PLAYER_MAIN_MENU_MESSAGE = "Приветствую на квесте, выбери команду"
PLAYER_TEAM_CHOICE_MESSAGE = "Ты теперь в команде"
# PLAYER_PLACE_MESSAGE = "Отправляйтесь сюда за ключом!"
PLAYER_WRONG_PASSWORD_MESSAGE = "Неправильный ключ. Попробуй еще раз."
PLAYER_ANSWER_SENDED_MESSAGE = "Ответ на задание отправлен! Оценка будет прислана чуть позже"
PLAYER_QUEST_END_MESSAGE = "Время первой части ВТУПИ вышло. Результаты будут чуть позже. Отправляйтесь на точку сбора"
