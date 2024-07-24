USE summer2024team4;
CREATE TABLE board (
    boardID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    timeDate DATETIME NOT NULL,
    active BOOLEAN NOT NULL,
    messageCount INT DEFAULT 0,
    voteCount INT DEFAULT 0
);