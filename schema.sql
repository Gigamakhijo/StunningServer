CREATE TABLE "USERS"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "email" TEXT NOT NULL,
    "username" TEXT,
    "hashed_password" TEXT NOT NULL,
    "state_comment" TEXT
);

CREATE TABLE "FOLLOW_REQUEST"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "target_username" TEXT NOT NULL,
    "following_state" INTEGER NOT NULL,
);

CREATE TABLE "MATE_RELATIONSHIP"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "first_username" TEXT NOT NULL,
    "second_username" TEXT NOT NULL,   
)