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

## Importing Custom Data

To add your own data to the music database using HeidiSQL, follow these steps:

1. **Open HeidiSQL**:
   - Launch HeidiSQL and connect to your MariaDB server where the music database is set up.

2. **Select the Database**:
   - In the left panel, locate and select the music database created with `musicdb.sql`.

3. **Navigate to the Target Table**:
   - Choose the table you want to add data to (e.g., `Songs`, `Albums`, `Artists`, `Genres`, `Users`, etc.).

4. **Import Data**:
   - **Option 1: Manual Entry**:
     - Right-click on the table and select “Open Table.”
     - In the table view, click on the last row to manually enter new records, filling in each column as needed.

   - **Option 2: Import from CSV**:
     - Prepare your data in a CSV file with columns matching the structure of the table.
     - Right-click on the table and select “Import CSV file.”
     - In the import dialog, select your CSV file and configure the delimiter and column mappings as necessary.
     - Click “Import” to load the data into the table.

5. **Verify Data Import**:
   - After importing, run a quick query on the table (e.g., `SELECT * FROM Songs`) to verify that the new data is accessible.

6. **Using Custom Data with the Application**:
   - Once your data is added to the tables, run the application using `python3 musicdb.py`. Your custom entries will now be available for use within the app.
