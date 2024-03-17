# =============================================================================
# GetChar.py
# - currently only works on Linux/MAC
# - will be updated to work on Windows in the next release
# =============================================================================
import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select

'''
A simple wrapper around terminal control functions

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Sandy Bultena 2021

'''

# ================================================================================
# return the terminal size
# ================================================================================
def terminal_rows_cols():
    ''' returns a tuple, (rows, cols) of the current terminal window size '''
    size = os.get_terminal_size()
    return (size.lines, size.columns)

# ================================================================================
# get single character from user
# ... this is a blocking method, i.e. your code waits until a user has entered
#     a key
# ================================================================================
def get_char():
    ''' 
    gets a single char that the user has typed on the keyboard. 
    NOTE: the arrow keys will return a string 'Down', 'Up', 'Right', 'Left'
          the enter key will return a string 'Enter'
          Because of the stdin.flush() command, other special keys may not
          return the correct thing.  Too bad.
    Ctrl-C will kill the program
    '''
    kb = KBHit()

    sys.stdout.flush()
    try: 
        char = kb.getch()
        if ord(char) == 3:
            raise KeyboardInterrupt

        # windows arrows
        elif ord(char) == 0 and os.name =='nt':
            next1 = kb.getch()
            if (ord(next1) == 72): char = "Up"
            elif (ord(next1) == 77): char = "Right"
            elif (ord(next1) == 80): char = "Down"
            elif (ord(next1) == 75): char = "Left"
            else: raise ValueError

        # mac arrows
        elif ord(char) == 27 and os.name !='nt':
            next1, next2 = kb.getch(), kb.getch()
            if (ord(next1) == 91 and ord(next2) == 66): char = "Down"
            elif (ord(next1) == 91 and ord(next2) == 67): char = "Right"
            elif (ord(next1) == 91 and ord(next2) == 68): char = "Left"
            elif (ord(next1) == 91 and ord(next2) == 65): char = "Up"
            else: raise ValueError

        # enter key
        elif ord(char) == 13: char = "Enter"

        # get rid of any outstanding characters
        sys.stdin.flush()

    # user requested quiting
    except KeyboardInterrupt:
        print ("Quiting program upon user request")
        quit()

    # always reset the terminal
    finally:
        kb.set_normal_term()

    # flush stdout (otherwise won't print to screen in non-buffer mode
    sys.stdout.flush()

    # return the char (or character description)
    return char

# ================================================================================
# get all the characters the user has typed since the last time you asked
# ... this is a NON-blocking method, i.e. your code does not wait
# Inspired by 'jedie' answer at
# https://stackoverflow.com/questions/2408560/non-blocking-console-input
# ================================================================================
import sys
import threading
import time
import queue
input_queue = None

def get_char_non_blocking():
    ''' get character, but don't wait for it 
    Note: if 'setup_non_blocking_input()' has not already been called, it will be 
    called from this function '''
    global input_queue
    if input_queue is None:
        _setup_non_blocking_input()
    if not input_queue.empty():
        return input_queue.get() 
    
def _setup_non_blocking_input():
    ''' setup for non blocking input.  used in conjuction with 'get_chars_non_blocking()' '''
    global input_queue
    global input_thread
    input_queue = queue.Queue()
    input_thread = threading.Thread(target=_add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

def _add_input(input_queue):
    while True:
        input_queue.put(get_char())


##############################################################################
# https://stackoverflow.com/questions/2408560/non-blocking-console-input
# The following was
# made by Simon D. Levy, part of a compilation of software he has written 
# and released under the Gnu Lesser General Public License.
# https://simondlevy.academic.wlu.edu/files/software/kbhit.py
##############################################################################


'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''

import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select

class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


# Test    
if __name__ == "__main__":

    last_update = time.time()
    while True:
        if time.time()-last_update>5.0:
            sys.stdout.write(".")
            last_update = time.time()

            x=get_char_non_blocking()
            if x :
                print ("\ninput:", x)

        sys.stdout.flush()


    # never gets here because of the test above
    kb = KBHit()

    print('Hit any key, or ESC to exit')

    while True:

        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27: # ESC
                break
            print(c)
 
    kb.set_normal_term()



