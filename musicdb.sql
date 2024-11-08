CREATE DATABASE IF NOT EXISTS musicdb;

USE musicdb;

CREATE TABLE IF NOT EXISTS User (
  Account_id INT,
  Username VARCHAR(40) NOT NULL,
  User_Password VARCHAR(40) NOT NULL,
  PRIMARY KEY (Account_id)
);

CREATE TABLE IF NOT EXISTS Artist (
  Artist_Name VARCHAR(40),
  PRIMARY KEY (Artist_Name)
);

CREATE TABLE IF NOT EXISTS Tours (
  Artist_Name VARCHAR(40),
  Tour_Date DATE,
  Tour_Location VARCHAR(60),
  PRIMARY KEY (Artist_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Artist(Artist_Name)
);

CREATE TABLE IF NOT EXISTS Follows (
  Artist_Name VARCHAR(40),
  Account_id INT,
  PRIMARY KEY (Artist_Name, Account_id),
  FOREIGN KEY (Artist_Name) REFERENCES Artist(Artist_Name),
  FOREIGN KEY (Account_id) REFERENCES User(Account_id)
);

CREATE TABLE IF NOT EXISTS Friends (
  Account_id INT,
  Friend_id INT,
  PRIMARY KEY (Account_id, Friend_id),
  FOREIGN KEY (Account_id) REFERENCES User(Account_id),
  FOREIGN KEY (Friend_id) REFERENCES User(Account_id)
);

CREATE TABLE IF NOT EXISTS Album (
  Album_Name VARCHAR(40),
  Artist_Name VARCHAR(40),
  Release_Date DATE NOT NULL,
  Cover_Art VARCHAR(180),
  PRIMARY KEY (Album_Name, Artist_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Artist(Artist_Name)
);

CREATE TABLE IF NOT EXISTS Song (
  Song_Name VARCHAR(40),
  Album_Name VARCHAR(40),
  Artist_Name VARCHAR(40),
  Track_Length INT NOT NULL,
  PRIMARY KEY (Song_Name, Album_Name, Artist_Name),
  FOREIGN KEY (Album_Name) REFERENCES Album(Album_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Album(Artist_Name)
);

CREATE TABLE IF NOT EXISTS Genre (
  Genre_Name VARCHAR(40) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Similar_Genres (
  Genre_Name VARCHAR(40),
  Similar_Name VARCHAR(40),
  PRIMARY KEY (Genre_Name, Similar_Name),
  FOREIGN KEY (Genre_Name) REFERENCES Genre(Genre_Name),
  FOREIGN KEY (Similar_Name) REFERENCES Genre(Genre_Name)
);

CREATE TABLE IF NOT EXISTS Review (
  Review_id INT,
  Account_id INT,
  Stars INT NOT NULL CHECK (Stars > 0 AND Stars < 6),
  Song_Name VARCHAR(40),
  Album_Name VARCHAR(40),
  Artist_Name VARCHAR(40),
  review_txt VARCHAR(255),
  PRIMARY KEY (Review_id, Account_id),
  FOREIGN KEY (Account_id) REFERENCES User(Account_id),
  FOREIGN KEY (Song_Name) REFERENCES Song(Song_Name),
  FOREIGN KEY (Album_Name) REFERENCES Song(Album_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Song(Artist_Name)
);

CREATE TABLE IF NOT EXISTS Reaction (
  Account_id INT,
  Review_id INT,
  Poster_id INT,
  is_like BOOLEAN,
  PRIMARY KEY (Account_id, Review_id, Poster_id),
  FOREIGN KEY (Account_id) REFERENCES User(Account_id),
  FOREIGN KEY (Review_id) REFERENCES Review(Review_id),
  FOREIGN KEY (Poster_id) REFERENCES Review(Account_id)
);

CREATE TABLE IF NOT EXISTS Artist_In_Genre (
  Artist_Name VARCHAR(40),
  Genre_Name VARCHAR(40),
  PRIMARY KEY (Artist_Name, Genre_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Artist(Artist_Name),
  FOREIGN KEY (Genre_Name) REFERENCES Genre(Genre_Name)
);

CREATE TABLE IF NOT EXISTS Song_In_Genre (
  Song_Name VARCHAR(40),
  Album_Name VARCHAR(40),
  Artist_Name VARCHAR(40),
  Genre_Name VARCHAR(40),
  PRIMARY KEY (Song_Name, Album_Name, Artist_Name, Genre_Name),
  FOREIGN KEY (Song_Name) REFERENCES Song(Song_Name),
  FOREIGN KEY (Album_Name) REFERENCES Song(Album_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Song(Artist_Name),
  FOREIGN KEY (Genre_Name) REFERENCES Genre(Genre_Name)
);

CREATE TABLE IF NOT EXISTS Album_In_Genre (
  Album_Name VARCHAR(40),
  Artist_Name VARCHAR(40),
  Genre_Name VARCHAR(40),
  PRIMARY KEY (Album_Name, Artist_Name, Genre_Name),
  FOREIGN KEY (Album_Name) REFERENCES Album(Album_Name),
  FOREIGN KEY (Artist_Name) REFERENCES Album(Artist_Name)
);