# Music Relational Database

## Introduction
This project is a Python and SQL-based music relational database application designed to manage and query data related to music, including songs, albums, artists, genres, user interactions, and more. Built with a focus on efficient relational data storage, it allows users to perform operations such as adding and retrieving information about songs, albums, and user interactions.

## Features
Stores and organizes comprehensive music data: songs, albums, artists, genres, user comments, and liked songs.
Supports user interaction tracking, such as liked songs and comments.
Allows retrieval of related songs and genres for a personalized experience.
Built with Python and SQL, leveraging the mariadb library for database management.

# Requirements

**Operating System:** Windows

**Python Library:** mariadb

**Database Management Tool:** HeidiSQL

## Installation

1. **Download Files:** Download musicdb.py and musicdb.sql.
   
2. **Install Requirements:**
   
- Install the mariadb library:
```bash
pip install mariadb
```
- Download and install HeidiSQL.
  
3. **Set Up Database:**

- Open HeidiSQL and connect to your MariaDB server.
- Import musicdb.sql to set up the database structure and initial data.
- Follow the HeidiSQL prompts to complete the database configuration.
  
## Usage
To run the program, open a console and enter:
```bash
python3 musicdb.py
```
2. Once the program is running, you will be prompted to login or create a new account. Then follow the given prompts to use the application.

## Database Structure

**Tables:**

- Songs: Stores song details such as title, duration, and album.
- Albums: Contains album-specific information.
- Artists: Manages artist data.
- Genres: Categorizes songs by genre.
- Users: Tracks user information and activity.
- Liked_Songs: Logs user-favorited songs.
- Comments: Stores user comments on songs.
- Related_Songs: Records relationships between songs and genres.
