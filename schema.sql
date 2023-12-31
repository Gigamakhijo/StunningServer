CREATE TABLE IF NOT EXISTS "USERS"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "username" TEXT,
    "hashed_password" TEXT NOT NULL,
    "state_comment" TEXT
);

CREATE TABLE IF NOT EXISTS "FOLLOW_REQUEST"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "target_username" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "MATE"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "first_username" TEXT NOT NULL,
    "second_username" TEXT NOT NULL 
);