from . import teams_dict, tasks_list

__all__ = [
    'get_leaderboard'
]

TITLE = '<b>Таблица результатов</b>'
HEADER = '|          <b>Команда</b>          |  А  |  B  |  <b>Σ</b>  |'
TOTAL_WIDTH = 33
TEAM_WIDTH = 30
SCORE_WIDTH = 5


def get_leaderboard() -> str:
    rows = []
    separator = ''.join('-' for i in range(TOTAL_WIDTH))
    rows.append(f'.{TITLE:^45}')
    rows.append('')
    rows.append(HEADER)
    rows.append(separator)
    for team in teams_dict.values():
        name = team.name[:15]
        scores = ['–' for i in range(4)]
        for i, score in enumerate(team.scores):
            scores[i] = score
        a, b, c, d = scores
        total = sum(team.scores)
        row = f'|<b>{name:^{TEAM_WIDTH}}</b>|{a:^{SCORE_WIDTH}}|{b:^{SCORE_WIDTH}}|<b>{total:^{SCORE_WIDTH + 1}}</b>|'
        rows.append(row)
    # rows.append(separator)
    leaderboard = '\n'.join(rows)
    return leaderboard
