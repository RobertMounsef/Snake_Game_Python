###########################################################################
# Additional function(s) to complement the colorama package
###########################################################################

import colorama,sys
import os

size = os.get_terminal_size()

def print_at(row,col,text=""):
    ''' put the cursor at row/col, where 0,0 is the top-left corner of your screen '''

    global size    
    if row < 0 or col < 0 or row + 1 > size.lines  or col + 1 > size.columns : 
        row = max(min(row,size.lines),0)
        col = max(min(col,size.columns),0)
        text = ""

    print(colorama.Cursor.POS(col+1,row+1),end="")
    print (text,end="")
    sys.stdout.flush()
