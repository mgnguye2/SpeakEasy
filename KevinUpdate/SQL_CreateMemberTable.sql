USE summer2024team4;
CREATE TABLE member (
    memberID INT PRIMARY KEY NOT NULL,
    active BOOLEAN NOT NULL,
    password VARCHAR(255) NOT NULL CHECK (LENGTH(password) >= 5),
    admin BOOLEAN NOT NULL,
    votes INT
);

