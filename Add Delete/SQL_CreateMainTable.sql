USE summer2024team4;
CREATE TABLE main (
    messageID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    timeDate DATETIME NOT NULL,
    memberID INT NOT NULL,
    boardID INT NOT NULL,
    vote INT,
    active BOOLEAN NOT NULL,
    message TEXT,
    FOREIGN KEY (memberID) REFERENCES member(memberID),
    FOREIGN KEY (boardID) REFERENCES board(boardID)
);