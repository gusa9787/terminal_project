import curses
from curses import wrapper

import pyfiglet
from pyfiglet import figlet_format

import numpy as np
from PIL import Image

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import time
import datetime
import time
import threading
import requests

# Global Variables
getTime = True
lock = threading.Lock()
API_KEY = '6VME7TKN3TU44U6B'

############################################################################################################################################################################
############################################################################################################################################################################

class userInfo:
    def __init__(self):
        self.name = None
        self.email = None
    
    def setName(self, name):
        self.name = name
    
    def setEmail(self, email):
        self.email = email

def slowTextEffect(stdscr, text, height, width, delay=0.0001):
    stdscr.clear()
    x = (width - len(text)) // 2
    y = height // 2

    for i in range(len(text)):
        stdscr.addstr(y, x + i, text[i])
        stdscr.refresh()
        time.sleep(delay)

def getString(stdscr):
    string = ""
    y, x = stdscr.getyx()

    while True:
        key = stdscr.getch()
        if key == ord('\n'):
            break
        elif key in {curses.KEY_BACKSPACE, curses.KEY_DC, 127}:
            if string:
                string = string[:-1]
                stdscr.addstr(y, x, " " * (len(string) + 1))
                stdscr.addstr(y, x, string)
                stdscr.move(y, x + len(string))
        elif 32 <= key <= 126:
            string += chr(key)
            stdscr.addstr(y, x + len(string) - 1, chr(key))

    return string

############################################################################################################################################################################
############################################################################################################################################################################

def Quit(stdscr):
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            return True
        else:
            return False

def YorN(stdscr):
    while True:
        key = stdscr.getch()
        if key == ord('y'):
            return True
        elif key == ord('n'):
            return False

def CUBuff(stdscr, height, width):
    stdscr.clear()
    ascii_art = [
        " .... ... .... ... .... ... ... .... ... ......::::-------::::..................................... ",
        "...........................................::--=+*##%%%%%##*+=--::..................................",
        "........................................:--=#%%@%%%%%%%%%%%%%%%#+--:................................",
        "......................................--=*%%%%%%%%%%%%%%%%%%%%%%%%*=-:..............................",
        "... ........ ... .... ... .... ... .:------------------=#%%%%%%%%%@%*--... ... .... ... .... ... ... ",
        " .... ... .... ... .... ... ... ...:---------------------*%%%%%%%%%%%%------:...................... ",
        "... ........ ... .... ... ........:------============-----*%%%%%%%%%%%@%%%#*==--::..... .... ... ...",
        " .... ... .... ... .... .....:---===----+@%%%%%%%%%%%-----*%%%%%%%%%%%%%%%%%%@%#=--:............... ",
        ".........................:--=*%%%@#=----+%%%%%%%%%%@*----+%@%%%%%%%%%%%%%%%%%%%%@%+--...............",
        "..................::-----=#%%%%%%%*----=#%*------+@%%%%%%%%%=------#%%%%%%%%%%%%%%@%#--..............",
        "..................--+***#%%%%%%%%%*----=@%*------+%%%%%%%%%#=-----+%%%%%%%%@%%%%%%%@#--.............",
        "... ........ ... .:--=+%%%%%%%%%%%+----=%%#+----=#%#++++*%@+----=*%%%%%%%%#-:%%%%%%%%*-:.... ... ... ",
        " .... ... .... ... .:-=%%%%%%%%%@#-----#%%%+----=%@+----+%@+----+%%%%%%%#-..%%%%%%%%%%--........... ",
        "....................:-*%%%%%%%%%%*-----@%%%+----=%@+----+%%=----+%%%%%@#. .*%%%%%%%%%%=:............",
        "....................:-#%%%%%%%%%%*----------------------*@*----=#%%%%%%=  :#%%%%%%%%%%-:............",
        "....................:-*%%%%%%%%%%%*-------------------+%%@*----=%%%%%%@%**%%%%%%%%%%@+-:............",
        "..................:--+%%%%%%%%%%%%%%+=====------====*%%%%%+----=%%%%%%%%%%%%%%%%%%@%+--.............",
        "................:-=*%%%%%%%%%%%%%%%%%%%%@#=----+%%%%%%%%@#=----*%%%%%%%%%%%%%%%%%@%=-:..............",
        "... ........ ...:-*%%%%%%%%%%%%%%%%%%%%%%*-----#%%%%%%%%%*----=%%%%%%%%%%%%%%%%@%*--:.. .... .......",
        "................-=#%%%%%%%%%%%%%%%%%%%%%%#--------------------+%%%%%%%%%%%%%%@%*=-:.................",
        "...............:-+%%%%%%%%#%@@%%%%%%%%%%%%#=----------------+%%%%%%%%%%%%%%%%#=-:...................",
        "..............--*%%%%%%%#----+*#%@@@@@%#*+=--:::::--+******#%%%%%@%*%%%%%@@#=-:.....................",
        ".............--#%%%%%%%%+-:..:-----------::.....:-+%%%%%%%%%%%%@%#=-=#%#+=--:.......................",
        "... ........:-+%%%%%%%%@=-:................ ....-+%%%%%%%%%%%%%#=-::-----..... ............. .......",
        "............-=%%%%%%%%%%--.....................:-+@%%%%%%%%@#=--:...................................",
        "... ........:-*%%%%%%%%#-:.... ... ... .... ...--*%%%%%%%@*---... ... .... ................. .......",
        ".............--#@%%%@%%--:.....................-=*%%%%%%*=-:........................................",
        "..............--*%%%#=--.......................----------:..........................................",
        "...............--+#+--..............................................................................",
        "................:---:...............................................................................",
    ]
    
    start_y = height // 2 - len(ascii_art) // 2
    start_x = width // 2 - max(len(line) for line in ascii_art) // 2

    for i, line in enumerate(ascii_art):
        stdscr.addstr(start_y + i, start_x, line)

def intro(stdscr, height, width):
    curses.curs_set(0)
    text = "Hello!"
    slowTextEffect(stdscr, text, height, width)
    time.sleep(1)
    text = "Welcome to the MEXITEL!"
    slowTextEffect(stdscr, text, height, width)
    time.sleep(1)
    text = "Inspired by the MINITEL, this program was developed to experience how a TUI program works!"
    slowTextEffect(stdscr, text, height, width)
    time.sleep(2)
    text = "Enjoy!"
    slowTextEffect(stdscr, text, height, width)
    time.sleep(1)
    text = "Program developed by Gustavo Sanchez Sanchez Jr, Student at the University of Colorado at Boulder"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    stdscr.refresh()
    time.sleep(3)
    CUBuff(stdscr, height, width)
    stdscr.refresh()
    time.sleep(2)

def getInfo(stdscr, userInfo, height, width):
    stdscr.refresh()
    stdscr.clear()
    curses.curs_set(1)
    text = "Enter your name: "
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    name = getString(stdscr)
    stdscr.clear()
    userInfo.setName(name)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.clear()
    text = "Does this seem correct: " + name + " ?"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    text = "Press 'y' for yes and 'n' for no."
    stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    while YorN(stdscr) == False:
        stdscr.clear()
        curses.curs_set(1)
        text = "Enter your name: "
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        name = getString(stdscr)
        stdscr.clear()
        userInfo.setName(name)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        text = "Does this seem correct: " + userInfo.name + " ?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    stdscr.clear()
    curses.curs_set(1)
    text = "Enter your email: "
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    email = getString(stdscr)
    stdscr.clear()
    userInfo.setEmail(email)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.clear()
    text = "Does this seem correct: " + userInfo.email + " ?"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    text = "Press 'y' for yes and 'n' for no."
    stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    while YorN(stdscr) == False:
        stdscr.clear()
        curses.curs_set(1)
        text = "Enter your email: "
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        email = getString(stdscr)
        stdscr.clear()
        userInfo.setEmail(email)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        text = "Does this seem correct: " + userInfo.email + " ?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    stdscr.clear()
    text = "Logging In ..."
    slowTextEffect(stdscr, text, height, width)

    time.sleep(3)

############################################################################################################################################################################
############################################################################################################################################################################

def displayCurrentTime(stdscr, time_str):
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "Current Date and Time:")
    stdscr.addstr(1, 0, time_str)

def getCurrentTime(stdscr):
    global getTime
    while True:
        with lock:
            if not getTime:
                break
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(1)  
        yield current_time

def time_thread(stdscr):
    global getTime
    current_time_generator = getCurrentTime(stdscr)
    while True:
        with lock:
            if not getTime:
                break
        time_str = next(current_time_generator)
        displayCurrentTime(stdscr, time_str)
        stdscr.refresh()

def print_menu(stdscr, selected_row_idx, menu_options, user):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, option in enumerate(menu_options):
        x = (w - len(option))//2
        y = (h - 10) + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)

    stdscr.attron(curses.A_BOLD)
    text = "Welcome to the MEXITEL, " + user.name
    stdscr.addstr(h//2, (w - len(text)) // 2, text)
    stdscr.attroff(curses.A_BOLD)

    stdscr.refresh()

############################################################################################################################################################################
############################################################################################################################################################################
'''
 def sendEmail(stdscr, receiverEmail, password, subject, body, user):
    message = MIMEMultipart()
    message["From"] = user.email
    message["To"] = receiverEmail
    message["Subject"] = subject
    body = body
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user.email, password)
        server.sendmail(user.email, receiverEmail, message.as_string())
        text = "Email sent successfully!"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        time.sleep(3) '''

def openEmail(stdscr, height, width, user):
    curses.curs_set(1)
    stdscr.clear()
    text = "Enter the receiver email: "
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    receiverEmail = getString(stdscr)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.clear()
    text = "Does this seem correct: " + receiverEmail + " ?"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    text = "Press 'y' for yes and 'n' for no."
    stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    while YorN(stdscr) == False:
        stdscr.clear()
        curses.curs_set(1)
        text = "Enter the receiver email: "
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        receiverEmail = getString(stdscr)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        text = "Does this seem correct: " + receiverEmail + " ?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    stdscr.clear()
    curses.curs_set(1)
    text = "Enter your email password: "
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    password = getString(stdscr)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.clear()
    text = "Does this seem correct: " + password + " ?"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    text = "Press 'y' for yes and 'n' for no."
    stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    while YorN(stdscr) == False:
        stdscr.clear()
        curses.curs_set(1)
        text = "Enter your email password: "
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        password = getString(stdscr)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        text = "Does this seem correct: " + password + " ?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    stdscr.clear()
    curses.curs_set(1)
    text = "Enter the subject of the email: "
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    subject = getString(stdscr)
    curses.curs_set(0)
    stdscr.refresh()
    stdscr.clear()
    text = "Does this seem correct: " + subject + " ?"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    text = "Press 'y' for yes and 'n' for no."
    stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    while YorN(stdscr) == False:
        stdscr.clear()
        curses.curs_set(1)
        text = "Enter the subject of the email: "
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        subject = getString(stdscr)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        text = "Does this seem correct: " + subject + " ?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

    stdscr.clear()
    curses.curs_set(0)
    text = "You will now type up the body of your email."
    slowTextEffect(stdscr, text, height, width)
    time.sleep(3)
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(1)
    stdscr.move(0, 0)
    body = getString(stdscr)

    stdscr.clear()
    curses.curs_set(0)
    text = "Do you accept to send email?"
    stdscr.addstr(height // 2, (width - len(text)) // 2, text)
    text = "Press 'y' for yes and 'n' for no."
    stdscr.addstr(height // 4, (width - len(text)) // 2, text)
    if YorN(stdscr):
        # sendEmail(stdscr, receiverEmail, password, subject, body, user) // Due to privacy issues with Google, this feature no longer works.
        text = "Sending ..."
        slowTextEffect(stdscr, text, height, width)
        time.sleep(5)
        text = "Email sent successfully!"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        stdscr.refresh()
        time.sleep(3)
        return
    else:
        stdscr.clear()
        stdscr.refresh()
        return

phoneBook = {
    "Alice Smith": "123-456-7890",
    "Bob Johnson": "987-654-3210",
    "Charlie Williams": "555-555-5555",
    "David Brown": "111-222-3333",
    "Eve Jones": "444-444-4444",
    "Frank Garcia": "999-999-9999",
    "Grace Martinez": "888-888-8888",
    "Hank Robinson": "777-777-7777",
    "Ivy Clark": "666-666-6666",
    "Jack Rodriguez": "555-555-5555",
    "Kate Lewis": "444-444-4444",
    "Liam Lee": "333-333-3333",
    "Mia Walker": "222-222-2222",
    "Nora Hall": "111-111-1111",
    "Olivia Allen": "000-000-0000",
    "Paul Young": "999-999-9999",
    "Quinn Wright": "888-888-8888",
    "Ryan Scott": "777-777-7777",
    "Sarah King": "666-666-6666",
    "Tom Hill": "555-555-5555",
    "Violet Green": "444-444-4444",
    "William Adams": "333-333-3333",
    "Xavier Baker": "222-222-2222",
    "Yvonne Nelson": "111-111-1111",
    "Zach Roberts": "000-000-0000",
    "Adam White": "999-999-9999",
    "Barbara Thompson": "888-888-8888",
    "Chris Anderson": "777-777-7777",
    "Diana Harris": "666-666-6666",
    "Evan Moore": "555-555-5555",
    "Fiona Carter": "444-444-4444",
    "George Wright": "333-333-3333",
    "Holly Baker": "222-222-2222",
    "Ian King": "111-111-1111",
    "Jenny Hill": "000-000-0000",
    "Kevin Scott": "999-999-9999",
    "Lisa Allen": "888-888-8888",
    "Michael Davis": "777-777-7777",
    "Nancy Green": "666-666-6666",
    "Oscar Evans": "555-555-5555",
    "Pamela Reed": "444-444-4444",
    "Quentin Harris": "333-333-3333",
    "Rachel White": "222-222-2222",
    "Steven Nelson": "111-111-1111",
    "Tina Roberts": "000-000-0000",
    "Ulysses Brown": "999-999-9999",
    "Victoria Davis": "888-888-8888",
    "Walter Adams": "777-777-7777",
    "Xena Smith": "666-666-6666",
    "Yolanda Clark": "555-555-5555",
    "Zoe Johnson": "444-444-4444",
    "Andrew Martinez": "333-333-3333",
    "Bethany Young": "222-222-2222",
    "Carl White": "111-111-1111",
    "Daisy Harris": "000-000-0000",
    "Edward Scott": "999-999-9999",
    "Fiona Thompson": "888-888-8888",
    "Gary Wright": "777-777-7777",
    "Hannah Carter": "666-666-6666",
    "Isaac Evans": "555-555-5555",
    "Jessica Reed": "444-444-4444",
    "Kyle Harris": "333-333-3333",
    "Linda Green": "222-222-2222",
    "Matthew Davis": "111-111-1111",
    "Nina Adams": "000-000-0000",
    "Oliver Smith": "999-999-9999",
    "Penny Clark": "888-888-8888",
    "Quincy Johnson": "777-777-7777",
    "Rachel Martinez": "666-666-6666",
    "Steven Brown": "555-555-5555",
    "Tina Wright": "444-444-4444",
    "Ulysses Thompson": "333-333-3333",
    "Valerie Reed": "222-222-2222",
    "William Harris": "111-111-1111",
    "Xavier Evans": "000-000-0000",
    "Yvonne Carter": "999-999-9999",
    "Zack Smith": "888-888-8888",
    "Allison Davis": "777-777-7777",
    "Brian Clark": "666-666-6666",
    "Cathy Johnson": "555-555-5555",
    "David Martinez": "444-444-4444",
    "Emily Wright": "333-333-3333",
    "Frank Thompson": "222-222-2222",
    "Gina Reed": "111-111-1111",
    "Henry Adams": "000-000-0000",
    "Isabella Harris": "999-999-9999",
    "John Smith": "888-888-8888",
    "Kathy Clark": "777-777-7777",
    "Liam Evans": "666-666-6666",
    "Megan Johnson": "555-555-5555",
    "Nathan Martinez": "444-444-4444",
    "Olivia Wright": "333-333-3333",
    "Peter Thompson": "222-222-2222",
    "Quinn Reed": "111-111-1111",
    "Rachel Adams": "000-000-0000",
    "Samuel Harris": "999-999-9999",
    "Tina Smith": "888-888-8888",
    "Ulysses Carter": "777-777-7777",
    "Victoria Davis": "666-666-6666",
    "Walter Johnson": "555-555-5555",
    "Xena Martinez": "444-444-4444",
    "Yolanda Wright": "333-333-3333",
    "Zachary Thompson": "222-222-2222",
    "Adam Miller": "111-222-3333",
    "Bethany Clark": "222-333-4444",
    "Cameron Davis": "333-444-5555",
    "Diana Thompson": "444-555-6666",
    "Ethan Harris": "555-666-7777",
    "Fiona Wilson": "666-777-8888",
    "George Taylor": "777-888-9999",
    "Hannah Brown": "888-999-0000",
    "Isaac Lee": "999-000-1111",
    "Jessica White": "000-111-2222",
    "Kevin Martinez": "111-222-3333",
    "Linda Rodriguez": "222-333-4444",
    "Michael Smith": "333-444-5555",
    "Natalie Johnson": "444-555-6666",
    "Oscar Garcia": "555-666-7777",
    "Peter Wilson": "666-777-8888",
    "Quincy Lee": "777-888-9999",
    "Rachel Davis": "888-999-0000",
    "Samuel Brown": "999-000-1111",
    "Tina Taylor": "000-111-2222",
    "Ulysses Moore": "111-222-3333",
    "Valerie Harris": "222-333-4444",
    "Wendy Thompson": "333-444-5555",
    "Xavier Wilson": "444-555-6666",
    "Yolanda Rodriguez": "555-666-7777",
    "Zack Miller": "666-777-8888",
    "Adam Clark": "777-888-9999",
    "Bethany Davis": "888-999-0000",
    "Cameron Thompson": "999-000-1111",
    "Diana Garcia": "000-111-2222",
    "Ethan Wilson": "111-222-3333",
    "Fiona Taylor": "222-333-4444",
    "George Moore": "333-444-5555",
    "Hannah Harris": "444-555-6666",
    "Isaac Rodriguez": "555-666-7777",
    "Jessica Miller": "666-777-8888",
    "Kevin Clark": "777-888-9999",
    "Linda Davis": "888-999-0000",
    "Michael Thompson": "999-000-1111",
    "Natalie Wilson": "000-111-2222",
    "Oscar Moore": "111-222-3333",
    "Peter Harris": "222-333-4444",
    "Quincy Rodriguez": "333-444-5555",
    "Rachel Miller": "444-555-6666",
    "Samuel Clark": "555-666-7777",
    "Tina Davis": "666-777-8888",
    "Ulysses Thompson": "777-888-9999",
    "Valerie Wilson": "888-999-0000",
    "Wendy Moore": "999-000-1111",
    "Xavier Harris": "000-111-2222",
    "Yolanda Rodriguez": "111-222-3333",
    "Xavier Harris": "222-333-4444",
    "Jack Thompson": "888-999-0000",
    "Katherine Wilson": "999-000-1111",
    "Liam Harris": "000-111-2222",
    "Megan Rodriguez": "111-222-3333",
    "Nathan Miller": "222-333-4444"
}

def openDirectory(stdscr, height, width):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    global phoneBook

    title = "Telephone Directory"
    num_cols = min(4, w // 30)  
    num_entries = len(phoneBook)
    num_rows = (num_entries + num_cols - 1) // num_cols

    idx = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if idx >= num_entries:
                break
            name, phone = list(phoneBook.items())[idx]
            x = (col * (w // num_cols)) + 8 
            y = row + 1
            stdscr.addstr(y, x, f"{name}: {phone}")
            idx += 1

    text = "Press 'q' to exit directory."
    y = height - 1
    x = width - len(text) - 1
    stdscr.addstr(y, x, text)
    stdscr.refresh()

    while (Quit(stdscr) == False):
        continue

def getStockPrice(symbol):
    global API_KEY
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'

    try:
        response = requests.get(url)
        data = response.json()
        if 'Global Quote' in data:
            price = data['Global Quote']['05. price'] + '.'
            return price
        else:
            return "Stock symbol not found or API limit exceeded."
    except Exception as e:
        return f"Error: {e}."

def openStocks(stdscr, height, width):
    
    while(True):
        curses.curs_set(1)
        stdscr.clear()
        text = "Enter the stock symbol you are looking for (MUST BE CAPITALIZED): "
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        symbol = getString(stdscr)
        curses.curs_set(0)
        stdscr.refresh()
        stdscr.clear()
        text = "Does this seem correct: " + symbol + " ?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

        while YorN(stdscr) == False:
            curses.curs_set(1)
            stdscr.clear()
            text = "Enter the stock symbol you are looking for (MUST BE CAPITALIZED): "
            stdscr.addstr(height // 2, (width - len(text)) // 2, text)
            receiverEmail = getString(stdscr)
            curses.curs_set(0)
            stdscr.refresh()
            stdscr.clear()
            text = "Does this seem correct: " + symbol + " ?"
            stdscr.addstr(height // 2, (width - len(text)) // 2, text)
            text = "Press 'y' for yes and 'n' for no."
            stdscr.addstr(height // 4, (width - len(text)) // 2, text)

        price = getStockPrice(symbol)
        curses.curs_set(0)
        text = "The current price of " + symbol + " is " + price
        slowTextEffect(stdscr, text, height, width)
        time.sleep(3)
        stdscr.clear()
        stdscr.refresh()
        text = "Would you like to continue?"
        stdscr.addstr(height // 2, (width - len(text)) // 2, text)
        text = "Press 'y' for yes and 'n' for no."
        stdscr.addstr(height // 4, (width - len(text)) // 2, text)

        if (YorN(stdscr)) == False:
            return

def quitProgram(stdscr, height, width):
    stdscr.clear()
    text = "Thank you for using our service. Come back soon!"
    slowTextEffect(stdscr, text, height, width)
    time.sleep(3)
    CUBuff(stdscr, height, width)
    stdscr.refresh()
    time.sleep(2)

############################################################################################################################################################################
############################################################################################################################################################################

def main(stdscr):
    height, width = stdscr.getmaxyx()

    # Make program introduction
    intro(stdscr, height, width)

    # Get user info to then utilize in program functionalities.
    user = userInfo()
    getInfo(stdscr, user, height, width)

    # Print menu
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0

    # Define menu options (Main Program)
    menu_options = ["E-Mail", "Stocks", "Telephone Directory", "Quit"]

    # Threads for Homepage Tools
    global getTime
    time_thread_handle = threading.Thread(target=time_thread, args=(stdscr,), daemon=True)
    time_thread_handle.start()

    while True:
        stdscr.clear()
        print_menu(stdscr, current_row, menu_options, user)
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.clear()

            if menu_options[current_row] == "E-Mail":
                getTime = False
                time_thread_handle.join()
                openEmail(stdscr, height, width, user)
                getTime = True
                curses.curs_set(0)
                time_thread_handle = threading.Thread(target=time_thread, args=(stdscr,), daemon=True)
                time_thread_handle.start()
                continue

            elif menu_options[current_row] == "Stocks":
                getTime = False
                time_thread_handle.join()
                openStocks(stdscr, height, width)
                getTime = True
                curses.curs_set(0)
                time_thread_handle = threading.Thread(target=time_thread, args=(stdscr,), daemon=True)
                time_thread_handle.start()
                continue

            elif menu_options[current_row] == "Telephone Directory":
                getTime = False
                time_thread_handle.join()
                openDirectory(stdscr, height, width)
                getTime = True
                curses.curs_set(0)
                time_thread_handle = threading.Thread(target=time_thread, args=(stdscr,), daemon=True)
                time_thread_handle.start()
                continue

            elif menu_options[current_row] == "Quit":
                getTime = False
                time_thread_handle.join()
                quitProgram(stdscr, height, width)
                return 0

            stdscr.refresh()
            stdscr.getch()
            break

wrapper(main)