import sys
import mariadb as mdb

# function to determine if a string is a float because python doesn't have that apparently
def is_float(string):
    try:
        float(string)
    except ValueError:
        return False
    return True

# important global variables
exit_app = False
logout = False
user_id = None
username = ""
password = ""
# initial setup of database connection
try:
    conn = mdb.connect(
        user=sys.argv[1] if len(sys.argv) >= 2 else "root",
        password=sys.argv[2] if len(sys.argv) >= 3 else "1234",
        host=sys.argv[3] if len(sys.argv) >= 4 else "127.0.0.1",
        port=int(sys.argv[4]) if len(sys.argv) >= 5 else 3306,
        database=sys.argv[5] if len(sys.argv) >= 6 else "musicdb"
    )
except mdb.Error as e:
    print(f"Error connecting to Database: {e}")
    print("Make sure correct arguments were provided.")
    sys.exit(1)
except ValueError:
    print("Please enter the port value as an integer (eg. \"3306\")")
    sys.exit(1)

cur = conn.cursor()


# function definitions (main code at end of file)
# Handles login for existing users
def login():
    global cur
    global username
    global password
    global user_id
    cur.execute("SELECT * FROM user WHERE Username=?", (username,))
    results = cur.fetchall()
    if len(results) != 1:
        print("Invalid Username")
        return False
    
    for uid, db_uname, db_upass in results:
        if db_uname != username:
            print("Oh no, big problem with SQL query (this shouldn't happen!) 44")
            return False
        if db_upass != password:
            print("Incorrect Password")
            return False
        else:
            user_id = uid
            return True
    
    return False


# allows for creation of a new user
def create_user():
    global cur
    global username
    global password
    global user_id
    cur.execute("SELECT * FROM user WHERE Username=?", (username,))
    results = cur.fetchall()
    if len(results) > 0:
        print("Username taken")
        return False
    
    cur.execute("SELECT MAX(Account_id) FROM user")
    results = cur.fetchall()

    if len(results) < 1:
        max_id = 0
    elif results[0][0] is int and results[0][0] >= 1:
        max_id = results[0][0]
    else:
        print("Oh no, big problem with SQL query (this shouldn't happen!) 79")
        return False

    try:
        cur.execute("INSERT INTO user (Account_id,Username,User_Password) VALUES (?, ?, ?)",
                    (max_id+1, username, password))
    except mdb.Error as e:
        print(f"SQL error: {e}")
        return False
    
    user_id = max_id+1
    return True


# Lets the user search for songs
def search_song():
    global cur
    global user_id
    while True:
        print("Select a song search option: ")
        song_menu_options = ("1", "2", "3", "4", "5", "6", "7", "E")
        print("1. Search by Song name")
        print("2. Search by Album name")
        print("3. Search by Artist name")
        print("4. Search by Genre")
        print("5. List by number of reviews")
        print("6. List by average rating")
        print("7. List all you have reviewed")
        print("E. Back to main menu")
        song_menu_input = input("Select an option: ")
        while song_menu_input.capitalize() not in song_menu_options:
            song_menu_input = input("Invalid option, please try again: ")
        
        match song_menu_input:
            case "1":
                song_name = input("Enter song name: ")
                cur.execute("SELECT * FROM song WHERE UPPER(Song_Name)=?",
                            (song_name.capitalize(),))
            case "2":
                album_name = input("Enter album name: ")
                cur.execute("SELECT * FROM song WHERE UPPER(Album_Name)=?",
                            (album_name.capitalize(),))
            case "3":
                artist_name = input("Enter artist name: ")
                cur.execute("SELECT * FROM song WHERE UPPER(Artist_Name)=?",
                            (artist_name.capitalize(),))
            case "4":
                genre_name = input("Enter a genre: ")
                cur.execute("SELECT S.*\
                            FROM song AS S, song_in_genre AS G\
                            WHERE S.Song_Name=G.Song_Name AND S.Album_Name=G.Album_Name AND S.Artist_Name=G.Artist_Name AND UPPER(G.Genre_Name)=?",
                            (genre_name.capitalize(),))
            case "5":
                min_review_num = input("Enter minimum number of reviews (default: 0): ")
                while not min_review_num == "" and not min_review_num.isdigit():
                    min_review_num = input("Invalid number, please try again: ")
                if min_review_num == "":
                    min_review_num = "0"
                cur.execute("SELECT S.*\
                            FROM song AS S, review AS R\
                            WHERE S.Song_Name=R.Song_Name AND S.Album_Name=R.Album_Name AND S.Artist_Name=R.Artist_Name\
                            GROUP BY S.Song_Name, S.Album_Name, S.Artist_Name\
                            HAVING COUNT(R.*)>=?\
                            ORDER BY COUNT(R.*) DESC",
                            (int(min_review_num),))
            case "6":
                min_avg_stars = input("Enter minimum average stars (default: 1.0): ")
                while not min_avg_stars == "" and is_float(min_avg_stars):
                    min_avg_stars = input("Invalid number, please try again: ")
                if min_avg_stars == "":
                    min_avg_stars = "1.0"
                cur.execute("SELECT S.*\
                            FROM song AS S, review AS R\
                            WHERE S.Song_Name=R.Song_Name AND S.Album_Name=R.Album_Name AND S.Artist_Name=R.Artist_Name\
                            GROUP BY S.Song_Name, S.Album_Name, S.Artist_Name\
                            HAVING AVG(R.Stars)>=?\
                            ORDER BY AVG(R.Stars) DESC",
                            (float(min_avg_stars)))
            case "7":
                cur.execute("SELECT S.*\
                            FROM song AS S, review AS R\
                            WHERE S.Song_Name=R.Song_Name AND S.Album_Name=R.Album_Name AND S.Artist_Name=R.Artist_Name AND R.Account_id=?",
                            (user_id,))
            case "E":
                return
        song_results = cur.fetchall()
        song_selection = select_song(song_results=song_results)
        if song_selection == "E":
            continue
        if song_selection == "NoneFound":
            continue
        interact_song(song_tuple=song_results[int(song_selection)])
        return


# song selection code
def select_song(song_results):
    global cur
    global user_id
    if song_results is not list or len(song_results) == 0:
        return "NoneFound"
    print("Select a song by number:")
    print("Format:Select_Num. Song_Name, Album_Name, Artist_Name, Track_Length, Review Count, Average Stars\n")
    for idx, (s_n, al_n, ar_n, tl) in enumerate(song_results):
        cur.execute("SELECT AVG(Stars),COUNT(*) FROM review WHERE Song_Name=?, Album_Name=?, Artist_Name=?",
                    (str(s_n), str(al_n), str(ar_n)))
        stars_results = cur.fetchall()
        print(f"{idx}. {s_n}, {al_n}, {ar_n}, {tl}, ", end="")
        print(f"{stars_results[0][1]}, ", end="")
        if int(stars_results[0][1]) < 1:
            print(f"{str(stars_results[0][0])[:3] if len(str(stars_results[0][0])) > 2 else str(stars_results[0][0])[0]+'.0'}")
        else:
            print("0.0")
    print("E. Abort Song selection")
    selection = input("Pick a number to select a song: ")
    while not (selection.isdigit() and int(selection) < len(song_results)) and selection != "E":
        selection = input("Invalid input.\nSelect one of the songs listed by number or E to exit: ")
    
    return selection


# interact with a song once selected
def interact_song(song_tuple):
    global cur
    global user_id


# main code of program
if __name__ == "__main__":
    print("Welcome to MusicDB!\n")

    while not exit_app:
        exit_app = False
        logout = False
        menu_options = ("1", "2", "E")
        print("1. Log in (existing user)")
        print("2. Create an account (new user)")
        print("E. Exit MusicDB :(")
        menu_input = input("Select an option: ")
        while menu_input.capitalize() not in menu_options:
            menu_input = input("Invalid option, please try again: ")

        match menu_input:
            case "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                while not login():
                    yn_input = input("Invalid input, try again (y/N)? ")
                    if yn_input.capitalize() in ("N", ""):
                        logout = True
                        break
                    elif yn_input.capitalize() == "Y":
                        username = input("Enter username: ")
                        password = input("Enter password: ")
            case "2":
                username = input("Make a username (<= 40 characters): ")
                password = input("Make a password (<= 40 characters): ")
                while not create_user():
                    yn_input = input("Invalid input, try again (y/N)? ")
                    if yn_input.capitalize() in ("N", ""):
                        logout = True
                        break
                    elif yn_input.capitalize() == "Y":
                        username = input("Enter username: ")
                        password = input("Enter password: ")
            case "E":
                exit_app = True
                break
        if logout:
            continue # return to login/create user menu

        while not logout and not exit_app:
            print(f"\nLogged into MusicDB as: {username}")

            menu_options = ("1", "2", "3", "4", "5", "6", "7", "8", "L", "E")
            print("1. Search for a Song")
            print("2. Search for an Album")
            print("3. Search for an Artist")
            print("4. Search for a User")
            print("5. Add a Song")
            print("6. Add an Album")
            print("7. Add an Artist")
            print("8. Account details")
            print("L. Logout")
            print("E. Exit MusicDB :(")
            menu_input = input("Select an option: ")
            while menu_input.capitalize() not in menu_options:
                menu_input = input("Invalid option, please try again: ")
            
            match menu_input:
                case "1":
                    pass
                case "2":
                    pass
                case "3":
                    pass
                case "4":
                    pass
                case "5":
                    pass
                case "6":
                    pass
                case "7":
                    pass
                case "8":
                    pass
                case "L":
                    logout = True
                case "E":
                    exit_app = True
        if logout:
            continue # return to login/create user menu
        if exit_app:
            break # break out of application loop
    
    print("Goodbye!\n")

conn.commit()

conn.close()