#!/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#   Copyright (C) 2023 Eyetu Kingsley
#
#   Synapse is a terminal-based file manager that helps 
#   users manage and organize their files and directories.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


import curses
from curses import wrapper
import math
import os
import socket

pair1 = (4, -1, 0)
pair2 = (6, -1, 131072)
text_win_height = 1
username = os.getlogin()
hostname = socket.gethostname()
# from pygments import highlight
# from pygments.lexers import PythonLexer
# from pygments.formatters import TerminalFormatter

# Let there be 3 windows
# Window 1 shows the contents of the previous directory
# Window 2 displays the contents of the current directory
# Window 3 displays the contents of the currently selected directory in the second window (or the contents of the file if it's a file that is selected)

# These values manage the scroll location of window 1 and window 2
win2_scroll = 0
win3_scroll = 0
rotate = True

def convert_bytes(size):
    """ Convert bytes to KB, or MB or GB"""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            if type(size) == float:
                if size.is_integer():
                    return "%d %s" % (size, x)
                else:
                    return "%3.1f %s" % (size, x)
            elif type(size) == int:
                return "%d %s" % (size, x)
        size /= 1024.0
    return size

def expand_str(str, end_str, final_len):
    """ Expand the file name string up to the maximum width of the pad """
    str_maxlength = math.floor(final_len-len(end_str) * 4.0/5.0)
    if len(str) > str_maxlength:
        split_str = str.split(".")
        if len(split_str) > 1:
            name = '.'.join(split_str[:-1])
            extension = split_str[-1]
        else:
            name = ''.join(split_str[0])
            extension = ''
        max_name = str_maxlength - len(extension) - 10
        name = name[:max_name] + '~'
        if str.find('.') == -1:
            str = name
        else:
            str = name + "." + extension
    padding = final_len - len(str) - 3
    return " " + str + end_str.rjust(padding, ' ') + " "

def arrange_folder(folder, items):
    """Arranges the contents of a directory by putting the folders first, and the files next. The folders and files are separately sorted by name and combined"""
    folders = []
    files = []
    for file in items:
        path = folder + '/' + file
        if os.path.isdir(path):
            folders.append(file)
        else:
            files.append(file)
    
    folders.sort()
    files.sort()
    arrangement = folders + files
    return arrangement

def main(screen):
    def refresh_win2(down=True, scroll=False):
        # Prevent scrolling if at the end of the menu
        if selected_option == len(current_files) - 1 and len(current_files) > curses.LINES - 2:
            global win2_scroll
            if win2_scroll == 0 or selected_option >= math.floor(curses.LINES / 2):
                win2_scroll = (len(current_files) - (curses.LINES - 1)) + 3
            window2.refresh(win2_scroll, 0, 1, window1Width, curses.LINES - 3, curses.COLS - 1)
        elif selected_option >= math.floor(curses.LINES / 2):
            # Rotate prevents the pad from scrolling twice at once
            global rotate
            stop_scrolling = False
            if selected_option >= (len(current_files) - (curses.LINES / 2) + 3):
                stop_scrolling = True
            # Revert scrolling to original state when the highlighted item loops back to the start
            if win2_scroll >= math.floor(curses.LINES / 2) and selected_option <= math.floor(curses.LINES / 2):
                win2_scroll = 0
            # Go up if the up signal is received, and vice-versa
            if rotate and not stop_scrolling and scroll:
                if down:
                    win2_scroll += 1
                else:
                    win2_scroll -= 1
            rotate = not rotate
            # Update the screen to scroll
            window2.refresh(win2_scroll, 0, 1, window1Width, curses.LINES - 3, curses.COLS - 1)
        else:
            # Udate the screen normally if scrolling is not needed
            window2.refresh(0, 0, 1, window1Width, curses.LINES - 3, curses.COLS - 1)

    def display_content(window, file, windowHeight):
        """Displays the contents of a file in the chosen window."""
        y_coord = 0
        try:
            with open(file) as file:
                try:
                    lines = file.readlines()
                except UnicodeDecodeError:
                    lines = []
            for line in lines:
                y_coord += 1
                if y_coord <= windowHeight - 2: # curses.LINES - 2
                    window.addstr(y_coord, 0, line)
        except PermissionError:
            screen.addstr(curses.LINES-1, 1, "Run this program as root to access your root directories", curses.color_pair(3) + curses.A_BOLD + curses.A_STANDOUT)

    def display_window(window, windowHeight, windowWidth, window_dir, window_data, selector):
        # Displays the contents of a directory in the chosen window with color styles
        y_coord = 3
        for i, option in enumerate(window_data):
            y_coord += 1
            file_path = window_dir + '/' + option
            if not os.path.islink(file_path):
                file_size = os.path.getsize(file_path)
            else:
                sym_path = os.readlink(file_path)
                try:
                    file_size = os.stat(file_path).st_size
                except FileNotFoundError:
                    try:
                        file_size = os.stat(sym_path).st_size
                    except FileNotFoundError:
                        file_size = 4096
            
            # Specify file as a non directory
            file_is_dir = False

            # If the file is a directory, specify file as a directory and let the output state the number of items in the file
            if os.path.isdir(file_path):
                file_is_dir = True
                try:
                    append_str = str(len(os.listdir(file_path)))
                except PermissionError:
                    screen.addstr(curses.LINES-1, 1, "Run this program as root to access your root directories", curses.color_pair(3) + curses.A_BOLD + curses.A_STANDOUT)
            else:
                append_str = convert_bytes(file_size)
            if y_coord <= windowHeight: # curses.LINES - 2
                if i == selector:
                    color_scheme = get_color_scheme(option, file_is_dir, highlight=True)
                    properties = color_scheme + curses.A_BOLD
                    window.addstr(y_coord, 0, expand_str(option, append_str, windowWidth), properties)
                else:
                    color_scheme = get_color_scheme(option, file_is_dir, highlight=False)
                    properties = color_scheme
                    if file_is_dir:
                        properties = color_scheme + curses.A_BOLD
                    window.addstr(y_coord, 0, expand_str(option, append_str, windowWidth), properties)
            else:
                pass
    
    
    curses.curs_set(0)
    curses.cbreak()

    # Tell the terminal to use the default colors (to allow using the white background) 
    curses.use_default_colors()
    curses.start_color()

    # Initialize all color pairs to be used in the program
    # curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) # Sets up color pair #1, it does black text with white background 
    curses.init_pair(2,curses.COLOR_BLUE, -1)
    curses.init_pair(3,curses.COLOR_RED, -1)
    curses.init_pair(4,curses.COLOR_YELLOW, -1)
    curses.init_pair(5,curses.COLOR_GREEN, -1)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_GREEN)
    h = curses.color_pair(1)
    folder_color = curses.color_pair(2) # Color pair for a normal folder option
    compressed_color = curses.color_pair(3) # Color pair for a normal compressed file option
    image_color = curses.color_pair(4) # Color pair for a normal image file option
    document_color = curses.color_pair(5) # Color pair for a normal document option
    highlight_folder_color = curses.color_pair(6) # Color pair for a highlighted folder option
    highlight_compressed_color = curses.color_pair(7) # Color pair for a highlighted compressed file option
    highlight_image_color = curses.color_pair(8) # Color pair for a highlighted image file option
    highlight_document_color = curses.color_pair(9) # Color pair for a highlighted document option
    n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

    def get_color_scheme(file_name, is_dir=False, highlight=False):
        """Receive a file name and determine the color pair to use for it based on the extension, whether it's a folder, and whether or not it is an highlighted option"""
        if highlight:
            color_scheme = curses.A_REVERSE
            if is_dir:
                color_scheme = highlight_folder_color
            elif(file_name.endswith(('.html', '.pdf', '.css', '.js', '.docx', '.txt'))):
                color_scheme = highlight_document_color
            elif(file_name.endswith(('.zip', '.rar', '.7z'))):
                color_scheme = highlight_compressed_color
            elif(file_name.endswith(('.png', '.svg', '.jpg', 'jpeg', 'ico'))):
                color_scheme = highlight_image_color
        else:
            color_scheme = curses.A_NORMAL
            if is_dir:
                color_scheme = folder_color
            elif(file_name.endswith(('.html', '.pdf', '.css', '.js', '.docx', '.txt'))):
                color_scheme = document_color
            elif(file_name.endswith(('.zip', '.rar', '.7z'))):
                color_scheme = compressed_color
            elif(file_name.endswith(('.png', '.svg', '.jpg', 'jpeg', 'ico'))):
                color_scheme = image_color
        
        return color_scheme


    # Create the first window (the window that shows the previous files)
    window1Width = math.floor(curses.COLS * 3.0/12.0)
    window1Height = 20000
    window1 = curses.newpad(window1Height, window1Width)

    # Create the second window (the window that shows the current directory and it's content)
    window2Width = math.floor(curses.COLS * 4.0/12.0)
    window2Height = 20000
    window2 = curses.newpad(window2Height, window2Width)

    # Create the third window (the window that shows the next directory files or the contents of a readable document)
    window3Width = math.floor(curses.COLS * 5.0/12.0)
    window3Height = 20000
    window3 = curses.newpad(window3Height, window3Width)

    screen.refresh()

    current_dir = os.getcwd()
    previous_dir = os.path.dirname(current_dir)
    selected_option = 0  # Keep track of the selected main menu option (the current directory)

    # current_dir is the current directory (the directory you're in at the moment), previous_dir is the parent directory (the previous folder you accessed) and future_dir is the future directory (directory of the selected option)
    while True:
        # Collect and arrange the list of files in the current directory
        current_files = arrange_folder(current_dir, os.listdir(current_dir))

        if previous_dir == None:
            # If we're at the root directory, don't show the previous files
            previous_files = []
        else:
            # Otherwise, collect and arrange the list of files in the previous directory
            previous_files = arrange_folder(previous_dir, os.listdir(previous_dir))

        # Get the path of the next directory by joining the path of the current directory with a slash, followed by the selected directory in the terminal menu
        slash = '/'
        # If we're at the root directory on Linux, there's no need to add a slash
        if previous_dir == None:
            slash = ''
        future_dir = current_dir + slash + current_files[selected_option]

        # If the next directory is actually a directory, arrange the files for display
        if os.path.isdir(future_dir):
            future_files = arrange_folder(future_dir, os.listdir(future_dir))
        else:
            # Otherwise, specify it as empty (having no files)
            future_files = []

        selected_suboption = 0  # Keep track of the selected option in window 3 (the next directory)
        preselected_option = 0  # Keep track of the previously selected option in window 1 (the previous directory)

        # If there are previous files to show, split the path of the current directory by the '/'
        if len(previous_files) > 0:
            split_path = current_dir.split('/')
            # If we're not at the root directory, make the selected option of the previous directory to be the current directory (identified by the name which is at the end of the path)
            if split_path[-1] != '':
                preselected_option = previous_files.index(split_path[-1])

        # Erase all windows anytime changes are made to properly show changes
        window2.erase()
        window3.erase()
        window1.erase()

		# Print the main menu options
        # window1.addstr(1, 2, f'Previous Directory: {previous_dir}')
        # window2.addstr(1, 2, f'Current Directory: {current_dir}')
        display_window(window2, window2Height, window2Width, current_dir, current_files, selected_option)        
        refresh_win2()

        # window3.addstr(1, 1, f'Next Directory: {future_dir}')
        # Print the children of the currently selected menu option on the third window if the selected option is a folder
        if os.path.isdir(future_dir):
            display_window(window3, window3Height, window3Width, future_dir, future_files, selected_suboption)
        # If the selected option is a file, display it's contents on the third window
        else:
            display_content(window3, future_dir, window3Height)
        window3.refresh(0, 0, 1, window1Width+window2Width, curses.LINES - 3, curses.COLS - 1)

        # Display the files in the previous directory on the first window
        display_window(window1, window1Height, window1Width, previous_dir, previous_files, preselected_option)
        window1.refresh(0, 0, 1, 0, curses.LINES - 3, curses.COLS - 2)

        
        topmost_text = f"{username}@{hostname}"
        currdir_path = current_dir + "/"
        # Show the user's hostname and username like the normal terminal would
        screen.addstr(0, 1, topmost_text, curses.color_pair(5)+curses.A_BOLD)
        # Add the current directory text one space after the text showing the username and host name
        screen.addstr(0, len(topmost_text)+2, currdir_path, curses.color_pair(2)+curses.A_BOLD)
        # Update the name of the current file/folder selected in the default color
        screen.addstr(0, len(topmost_text)+len(currdir_path)+2, current_files[selected_option], curses.A_BOLD)
        # Calculate the length of all the text added and the length of the remaining screen
        screen.refresh()


        # Get user input
        key = screen.getch()

        # Move the highlighted menu entry up if the down key is pressed
        if key == curses.KEY_UP or key == 38:
            if selected_option > 0:
                selected_option -= 1
            else:
                selected_option = len(current_files) - 1

            # update the future directory to be the current highlighted option
            file = current_dir + '/' + current_files[selected_option]
            if os.path.isdir(file):
                future_dir = file
            
            # Update the current folder
            total_length = len(topmost_text) + len(currdir_path) + len(current_files[selected_option]) + 2
            remaining_screen = curses.COLS - total_length
            # Add 3 to balance out some kinks in the expand_str code
            padding_space = expand_str('', '', remaining_screen+3)
            screen.addstr(0, total_length, padding_space)

            # window2.addstr(curses.LINES - 1, 1, "Up Key works")
            # Refresh the second window to properly reflect changes
            refresh_win2(False, scroll=True)
            
        # Move the highlighted menu entry down if the down key is pressed
        elif (key == curses.KEY_DOWN or key == 40):
            if selected_option < len(current_files) - 1:
                selected_option += 1
            else:
                selected_option = 0
                
            # Update the current folder
            total_length = len(topmost_text) + len(currdir_path) + len(current_files[selected_option]) + 2
            remaining_screen = curses.COLS - total_length
            # Add 3 to balance out some kinks in the expand_str code
            padding_space = expand_str('', '', remaining_screen+3)
            screen.addstr(0, total_length, padding_space)

            # window2.addstr(15, 1, "Down Key Works")
            refresh_win2(True, scroll=True)

        # Navigate up and down through the submenu options
        elif (key == curses.KEY_LEFT) or (key == 37) or (key == curses.KEY_BACKSPACE) or (key == 8):
            # If the previous directory isn't the root folder, go back by 1 folder
            if previous_dir != None:
                # Get the name of the previous directory and set the current directory to be the previous one
                prev_dir_name = previous_dir.split('/')[-1]
                current_dir = previous_dir
                # If the name of the previous directory is empty, we're in the root directory else make the previous directory the one before the current directory
                if prev_dir_name == "":
                    previous_dir = None
                else:
                    previous_dir = os.path.dirname(current_dir)

                # Once the user goes back, the selected option will be the folder that they just came out from
                selected_option = preselected_option

                # Scroll to the currently selected option
                global win2_scroll
                win2_scroll = math.floor(selected_option - (curses.LINES / 2) + 3)
                if not win2_scroll >= 0:
                    win2_scroll = 0

            refresh_win2()
        elif (key == curses.KEY_RIGHT) or (key == 39) or (key == curses.KEY_ENTER) or (key == 10) or (key == 13):
            # If the next directory is a folder and it has at least 1 content, move into it
            if os.path.isdir(future_dir) and len(os.listdir(future_dir)) > 0:
                previous_dir = current_dir
                current_dir = future_dir
                selected_option = 0
            refresh_win2()
        
        # If the backspace key is pressed twice, quit the program
        elif key == 27:
            second_key = screen.getch()
            if second_key == 27:
                break

def run():
    wrapper(main)