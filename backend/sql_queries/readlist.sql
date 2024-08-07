CREATE TABLE IF NOT EXISTS readlist (
    manga_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    total_chps REAL NOT NULL CHECK (total_chps > 0),
    status TEXT NOT NULL,
    genres TEXT NOT NULL,
    poster TEXT NOT NULL UNIQUE,
    session TEXT NOT NULL UNIQUE,
    created_on DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);