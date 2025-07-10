DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS audios;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS answers;


-- Table: tasks
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY CHECK(id != ''),
    text TEXT NOT NULL,
    answer TEXT NOT NULL,
    points INTEGER NOT NULL
);

-- Table: photos
-- References: task_id (table: tasks)
CREATE TABLE IF NOT EXISTS photos (
    id TEXT PRIMARY KEY CHECK(id != ''),
    task_id TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id)
);

-- Table: videos
-- References: task_id (table: tasks)
CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY CHECK(id != ''),
    task_id TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id)
);

-- Table: audios
-- References: task_id (table: tasks)
CREATE TABLE IF NOT EXISTS audios (
    id TEXT PRIMARY KEY CHECK(id != ''),
    task_id TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id)
);

-- Table: places
CREATE TABLE IF NOT EXISTS places (
    id TEXT PRIMARY KEY CHECK(id != ''),
    text TEXT NOT NULL,
    password TEXT NOT NULL,
    photo_id TEXT NOT NULL
);

-- Table: teams
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    route TEXT DEFAULT '',
    current_round INT DEFAULT 0,
    state TEXT DEFAULT 'default'
);
-- Adding 2 teams into the teams table
INSERT INTO teams (name) VALUES ('Team 1');
INSERT INTO teams (name) VALUES ('Team 2');

-- Table: players
-- References: team_id (table: teams)
CREATE TABLE IF NOT EXISTS players (
    telegram_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    team_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams (id)
);

-- Table: answers
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    task_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    points INTEGER,
    FOREIGN KEY (task_id) REFERENCES tasks (id),
    FOREIGN KEY (team_id) REFERENCES teams (id)
);