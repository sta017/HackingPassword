#Hacking V7   - Suraj Tamrakar (part of assignment in Python programming and problem solving
# course offered by U of Alberta in coursera.
#In this graphical password guessing game, 
# a list of password is displayed and the player is allowed multiple attemtps.
# For each entry, a hint is diplayed on the right, indicating how many letters
# match. On entering the correct password or running out of attempts,
# corresponding outcome is displayed with a prompt to end the game. 

from uagame import Window
from time import sleep
from random import randint, choice

def main():
    # setting location and attempts as global variable here, because we call it multiple times.
    location =[0,0]
    attempts = 4
    #hint_location= [0,0]
    window = create_window()
    
    display_header(window, location, attempts)
    password = display_pwd_list(window,location) 
    guess = get_guess(window, password, attempts, location)
    prompt_end(window,password, guess, location)
     
#create a window
def create_window():
    window = Window('Hacking', 500,500)
    window.set_font_name=('couriernew')
    window.set_font_size(18)
    window.set_font_color('green')
    window.set_bg_color('black')
    return window

def display_header(window, location, attempts):           
    #the output of create_window() becomes the input accessible here.
    # location= [0,0] removed line_x = 0,  line_y = 0 
    # Displays first two line in the screen
    head_line = ['DEBUG MODE', str(attempts) + ' ATTEMPT(S) LEFT']
    
    for item in head_line:
        display_line(window, item, location, line_space =1)
        
    return attempts

def display_line(window,string,location, line_space):                       
    # generalizing the repeated lines with this function.
    #line_x, line_y = location[0,0]
    #Displayed a string in the window and update the  location
    #- window is the Window to display in
    # - string is the str to display in
    # - location is a tuple containing the int x and int y coords
    # of where the strin should be displayed and it should be 
    # updated to one 'line' below the top left corner of the 
    # displayed string.
    delay = 0.1                 # delay time in seconds
    string_height = window.get_font_height()
    window.draw_string(string, location[0],location[1])         # replacing 1st argument with 'string'     
    window.update()
    sleep(delay)
    location[1] += line_space *string_height

def space(window, location, line_space):
    #Adds a blank space in between lines
    # - linespace is number of line gaps desired.
    string_height= window.get_font_height()
    location[1] += line_space*string_height

def display_pwd_list(window, location):
    #display password list
    # - pwd is assisgned a desired/RANDOM password from the list.
    list= ['PROVIDE', 'SETTING', 'CANTINA','CUTTING','HUNTERS','SURVIVE',
           'HEARING', 'HUNTING','REALIZE','NOTHING', 'OVERLAP', 'FINDING','PUTTING']
    
    space(window, location, 1)         #Adding a gap between header and the pwd list.
    embed_size = 13
    for item in list:
        embeded_pwd = embed_password(item, embed_size)
        display_line(window, embeded_pwd, location, line_space =1)
        
    pwd = list[choice(range(0,len(list)))]      #choice == random.choice,  randomly selects pwd.               
    return pwd

def embed_password(password, size):
    #Returns pasword embedded with random symbols
    fill = '!@#$%^*()-+=~[]{}'
    embedding = ''
    password_size = len(password)
    split_index = randint(0, size - password_size)
    for index in range(0, split_index):
        #concatenate random char to embedded password
        embedding = embedding + choice(fill)
    embedding += password
    if len(embedding) <= size:
        for index in range(len(embedding), size):
            #concatenate random char to embedded password
            embedding = embedding + choice(fill)
        
    return embedding

def get_guess(window, password, attempts, location):
    #prompt for guess   
    string_height = window.get_font_height()
    hint_location= [window.get_width()//2, 0]
    location[1] += string_height
    guess = None
    while attempts != 0 and guess != password:
        #get next guess
           # displaying attempts left
        window.draw_string(str(attempts), location[0], string_height)
        
        #check warning
        guess = window.input_string('ENTER PASSWORD >', location[0], location[1])
        match_word(window,hint_location, password, guess)
        location[1] += string_height
        attempts -= 1
        check_warning(window, attempts)
    return guess 
 
def check_warning(window, attempts): 
    #checks the remaining attempts to decide if the Warning for last attempt
    # should be displayed. 
    if attempts == 1:
        warning_msg = '*** LOCKOUT WARNING ***'
        warning_width = window.get_width()- window.get_string_width(warning_msg)
        warning_height = window.get_height() - window.get_font_height()          # gives the height of the last line.
        window.draw_string(warning_msg, warning_width , warning_height)
       

def prompt_end(window, password, guess,location, delay = 0.1):
    window.clear() 
    value = 0       #INITIALIZING value for index number in the dictionary.
    if guess == password:
        value = 1   
        
    #end game
    #   display outcome
    #      display guess
    #         compute x and y coordinates
    x_space = window.get_width() - window.get_string_width(guess)
    location[0] = x_space // 2
    
    string_height = window.get_font_height()
    outcome_height = 7 * string_height
    y_space = window.get_height() - outcome_height
    location[1] = y_space // 2
    
    display_line(window, guess, location, line_space = 1)
    location[1] += string_height
    prompt_msg(window,location, value)
    
    window.close()
    
def prompt_msg(window, location, value):   
    # Value can be 0 for false and 1 for True.
    # Using the value obtained, appropriate display msg and prompt msg is 
    # taken from the dictionary below.
    # -The prompt msg appears directly below the end of the display msg.
    output_msg= {0: ['LOGIN FAILURE - TERMINAL LOCKED','PLEASE CONTACT AN ADMINISTRATOR'],
                 1: ['EXITING DEBUG MODE',"LOGIN SUCCESSFUL - WELCOME BACK"] }
    prompt = {0:'PRESS ENTER TO EXIT', 1:'PRESS ENTER TO CONTINUE'}
    
    for items in output_msg[value]:
        x_space = window.get_width() - window.get_string_width(items)
        location[0] = x_space // 2    
        display_line(window, items, location, line_space = 2)
        
    #Prompt for an end.
    x_space = window.get_width() - window.get_string_width(prompt[value])
    location[0] = x_space // 2
    window.input_string(prompt[value], location[0], location[1])    
    
def count_letter(string):
    count = 0
    letters = []
    for i in range(len(string)):
        letters.append(string[i])
        count += 1
    
    return count, letters

def match_word(window,hint_location, pwd, word2):
    #Checks input guess and outputs how many letters are in 
    # matching position, despite the length of the guess word. 
    # -
    count, pwd_letter= count_letter(pwd)
    _, check_letter = count_letter(word2)
    match= 0
    label= {0: 'INCORRECT', 1: 'CORRECT'}
    if check_letter == pwd_letter:
        match = count
        value = 1
    else:    
        index = min(count,_)              #  checks letters in the idices of the shortest length word.
        for i in range(index):
            if check_letter[i] == pwd_letter[i]:
                match += 1
        value = 0
        
    label_msg= [str(label[value])+ ' CHOICE' , str(match)+'/'+str(count)+ ' LETTERS IN MATCHED POSITION']
    
    for item in label_msg:
        display_line(window, item, hint_location, line_space =1)
    
    
main()

