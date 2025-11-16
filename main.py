# streamlit run C:\Users\shayn\Python\Knives2\knives.py

# IMPORTS
import streamlit as st
import hashlib
from target import *
from datetime import datetime


# SESSION STATE VARIABLES
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'targets' not in st.session_state:
    st.session_state.targets = []
if 'reload' not in st.session_state:
    st.session_state.reload = True
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'target' not in st.session_state:
    st.session_state.target = None
if 'datetime' not in st.session_state:
    st.session_state.datetime = None
if 'history' not in st.session_state:
    st.session_state.history = []
# Set page config to scale to screen size
st.set_page_config(layout="wide")

# Hash Password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Does User Name Exist?
def username_exists(username, filename='users.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                stored_username = line.strip().split(',')[0]
                if stored_username.lower() == username.lower():
                    return True  # username already exists
        return False  # username available
    except FileNotFoundError:
        print("    File not found.")

# Create Account
def create_account(username, password, filename='users.txt'):
    if not username_exists(username, filename):
        hashed_password = hash_password(password)
        with open(filename, 'a') as file:
            file.write(f'{username},{hashed_password}\n')
        return True  # account created successfully
    else:
        return False  # username already exists

# Log In
def login_auth(username, password, filename='users.txt'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(',')
                if stored_username == username:
                    hashed_password = hash_password(password)
                    if hashed_password == stored_hashed_password:
                        return True  # login successful
                    else:
                        return False  # incorrect password
        return False  # username does not exist
    except FileNotFoundError:
        return False  # file does not exist

def sign_in(username,password):
    if username_exists(username):
        if login_auth(username, password):
            st.session_state.page = "Play"
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.targets = load_targets(username)
        else:
            st.error("Incorrect password")
    else:
        st.error("Username not found")

def sign_up(username, password, confirm_password):
    if not username_exists(username):
        if password == confirm_password:
            create_account(username, password)
            change_page("play")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Passwords do not match.")
    else:
        st.error("Username taken.")

# Change Page
def change_page(page):
    st.session_state.page = page
def change_page_play():
    st.session_state.page = "play"
def change_page_targets():
    st.session_state.page = "targets"
def change_page_stats():
    st.session_state.page = "stats"
def change_page_sign_up():
    st.session_state.page = "sign_up"

# HOME
def home_page(info="Home"):
    st.title(info)
    username = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    st.button("Sign In", on_click=sign_in, args=[username, password])
    st.button("Sign Up",on_click=change_page_sign_up)


# SIGN UP
def sign_up_page():
    st.title("Sign Up")
    username = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Re-Enter Password", type="password")
    st.button("Submit", on_click=sign_up, args=[username, password, confirm_password])

# # # PLAY # # #

def play(game):
    current_date_time = datetime.now()
    st.session_state.datetime = current_date_time.strftime("%b-%d-%Y %H:%M")
    st.session_state.playing = True
    st.session_state.target = "Shane's"

def generate_scoreboard(rounds, throws_per_round):
    scoreboard = []
    for round in range(rounds):
        r = []
        for throw in range(throws_per_round[round]):
            r.append(0)
        scoreboard.append(r)
    scoreboard.append([0])
    return scoreboard

def submit_score(scoreboard):
    filename='game_data.json'
    game_data = {
            'user': st.session_state.username,
            'date': st.session_state.datetime,
            'game' : "game_name",
            'knives' : "knife_type",
            'target': st.session_state.target,
            'scoreboard': scoreboard
    }
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data.append(game_data)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        print("Game Data saved.")
    # END GAME
    st.session_state.playing = False
    st.session_state.target = None

def show_current_game():
    scoreboard = generate_scoreboard(3, [3,3,3])
    total = 0
    for r in range(3):
        st.write(f"ROUND {r+1}")
        col1, col2, col3 = st.columns(3)
        for t in range(3):
            if t == 0 :
                scoreboard[r][t] = col1.text_input(f"(R{r+1}) Throw {t + 1}")
            elif t == 1 :
                scoreboard[r][t] = col2.text_input(f"(R{r+1}) Throw {t + 1}")
            else :
                scoreboard[r][t] = col3.text_input(f"(R{r+1}) Throw {t + 1}")
            try:
                total += int(scoreboard[r][t])
            except :
                pass
    st.write(f"TOTAL : {total}")
    scoreboard[-1]=[total]
    st.button(f"Submit Score", on_click=submit_score, args=[scoreboard])

def play_page():
    #nav()
    st.title("Play")
    if not st.session_state.playing:
        # Show Game List, Play Buttons with Titles
        st.button("Shane's Bullseye 10 feet", on_click=play, args=["game_name"])
    if st.session_state.playing:
        show_current_game()

# # # TARGET # # #

def create_target(size, rings, target_name, shape):
    username = st.session_state.username
    while len(size) > int(rings): size.pop()
    target = Target(username, target_name, shape, rings, size)
    ### STILL NEEDS A CHECK IF EXISTS FUNCTION
    save_target(target)
    st.session_state.targets = load_targets(username)
    st.session_state.checkbox_state = False

def del_tar(t_name):
    username = st.session_state.username
    delete_target(username, t_name)
    st.session_state.targets = load_targets(username)

def target_page():
    #nav()
    st.title("Targets")


    # Load Targets
    st.session_state.targets = load_targets(st.session_state.username)

    # Show existing targets
    for target in st.session_state.targets:
        if st.checkbox(f"{target.name}"):
            st.write(f"Shape : {target.shape}")
            st.write(f"Number of Rings : {target.num_rings}")
            st.write(f"Size of Rings : {target.ring_size}")
            # Delete Target
            st.button(f"Delete {target.name}", on_click=del_tar, args=[target.name])

    # Add new target
    add_target = st.checkbox("Add Target", key="checkbox_state")
    if add_target:
        target_name = st.text_input("Target Name")
        shape = st.radio("Shape", ("Square", "Circle"))
        rings = st.slider("Number of Rings", 1, 10, 1)
        size = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        st.write("From center out, enter the width of each ring (inches)")
        for x in range(int(rings)):
            size[x] = st.slider(f"Width of Ring {x}", 1.0, 48.0, step=0.5)
        create_button = st.button("Create Target", on_click=create_target, args=[size,rings, target_name, shape])
        if create_button:
            add_target.value = False



# # # STAT # # #

def load_history(user_name):
    filename = 'game_data.json'
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    # Filter targets by user name
    user_games = [game for game in data if game['user'] == user_name]
    # Convert target data to Target objects
    # targets = [Target(
    #     user=target['user'],
    #     name=target['name'],
    #     shape=target['shape'],
    #     num=target['num_rings'],
    #     size=target['ring_size']
    # ) for target in user_games]
    return user_games

def stat_page():
    #nav()
    st.title("Stats")

    # Load History
    st.session_state.history = load_history(st.session_state.username)

    # Show existing targets
    # for game in st.session_state.history:
    #     if st.checkbox(f"{game["date"]}"):
    #         st.write(f"Game : {game['game']}")
    #         st.write(f"Target : {game['target']}")
    #         st.write(f"Knives : {game['knives']}")
    #         if st.checkbox(f"Score : {game['scoreboard'][-1][0]}"):
    #             for x in range(len(game['scoreboard'])-1):
    #                 mod = "st"
    #                 if x+1 == 2 : mod = "nd"
    #                 elif x+1 == 3 : mod = "rd"
    #                 elif x+1 > 3 : mod = "th"
    #                 st.write(f"{x+1}{mod} Round :: ( {" - ".join(game['scoreboard'][x])} )")
    for game in st.session_state.history:
        if st.checkbox(f"{game["date"]}"):
            tab = "&nbsp;" * 8
            st.write(f"{tab}{tab}Game : {game['game']}")
            st.write(f"{tab}{tab}Target : {game['target']}")
            st.write(f"{tab}{tab}Knives : {game['knives']}")
            st.write(f"{tab}{tab}Score : {game['scoreboard'][-1][0]}")
            for x in range(len(game['scoreboard']) - 1):
                st.write(f"{tab}{tab}{tab}( { " - ".join(game['scoreboard'][x]) } )")





# NAV BAR
# def nav():
#     col1, col2, col3 = st.columns(3)
#     col1.button('Play', on_click=change_page_play)
#     col2.button('Targets', on_click=change_page_targets)
#     col3.button('Stats', on_click=change_page_stats)
def nav():
    with st.sidebar:
        st.session_state.page = st.radio("Navigation", ("Play", "Targets", "Stats"))

# # Render pages
def main():
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "sign_up":
        sign_up_page()
    else :
        nav()
        if st.session_state.page == "Play":
            play_page()
        elif st.session_state.page == 'Targets':
            target_page()
        elif st.session_state.page == 'Stats':
            stat_page()
        else:
            home_page("Error")

if __name__ == '__main__':
    main()