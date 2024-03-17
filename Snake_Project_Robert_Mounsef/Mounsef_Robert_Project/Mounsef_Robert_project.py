import colorama
from PrintAt import print_at
import time
import GetChar
from GetChar import get_char
from GetChar import get_char_non_blocking
import random
(MAX_ROW, MAX_COL) = GetChar.terminal_rows_cols()
rows =[2,2,2,2,2,2,2,2,2,2,] 
cols =[2,2,2,2,2,2,2,2,2,2,] 
MID_ROW=MAX_ROW//2
MID_COL=MAX_COL//2
row = 0
col = 0
key = ""
drow = 1 
dcol = 0 
print_at(0,0,colorama.Back.BLACK) 
print_at(0,0,colorama.ansi.clear_screen())
score = 0
game= "Start"
for count in range (0,1):
    random1=random.randint(2,MAX_ROW-2)
    random2=random.randint(2,MAX_COL-2)
    print_at(random1,random2,colorama.ansi.Back.RED)   
    print_at(random1,random2, " ")
while key != 'q' and score != 250 and game !="end": 
    if score == 50 or score== 100 or score == 150:
        level = score/50 +1
        print_at(2,2,colorama.ansi.Back.BLACK)
        print_at(2,2,f"Level {level:.0f}")
        row = 0
        col = 0
        key = ""
        drow = 1 
        dcol = 0    
        cols=[2,2,2,2,2,2,2,2,2,2,]
        rows= [2,2,2,2,2,2,2,2,2,2,]
        time.sleep(3)
        print_at(0,0,colorama.ansi.clear_screen())
    
        if score>= 150:
            while random1== MID_ROW:
                random1=random.randint(2,MAX_ROW-2)
            while random2== MID_COL:
                random2=random.randint(2,MAX_COL-2)
    
        print_at(random1,random2,colorama.ansi.Back.RED)   
        print_at(random1,random2, " ")
        score= score+10
    if score >= 150:#WALLS
        for count in range(5,MAX_ROW-5):
            print_at(count,MID_COL," ")
            print_at(count,MID_COL,colorama.ansi.Back.BLUE)
        for count in range(5, MAX_COL-5):
            print_at(MID_ROW,count," ")
            print_at(MID_ROW,count,colorama.ansi.Back.BLUE)
    if score in range (0,50):
        time.sleep(0.2)
    if score in range (50,260): #Level 2
        time.sleep(0.1)
    if score >= 150:
        if rows[0]== MID_ROW and cols[0] in range (5,MAX_COL-5):
            game="end"
        if rows[0] in range (6,MAX_ROW-5) and cols[0]== MID_COL:
            game="end"
    if rows[0]== random1 and cols[0]== random2:
        score= score+10
        random1=random.randint(2,MAX_ROW-2)
        random2=random.randint(2,MAX_COL-2)
        if score>= 150:
            while random1== MID_ROW:
                random1=random.randint(2,MAX_ROW-2)
            while random2== MID_COL:
                random2=random.randint(2,MAX_COL-2)
        print_at(random1,random2,colorama.ansi.Back.RED)
        print_at(random1,random2, " ")
        if score in range (0,100):
            for count in range (0,4):
                rows.append(tail_row)
                cols.append(tail_col)
        elif score in range (100,260): #level 3
            for count in range (0,10):
                rows.append(tail_row)
                cols.append(tail_col)
    
    if min(rows)== 0:
        game="end"
    elif max(rows)==MAX_ROW:
        game="end"
    elif max(cols)== MAX_COL:
        game="end"
    elif min(cols)<0:
        game="end"
    print_at(rows[0],cols[0],colorama.Back.BLACK)
    print_at(0,0,f"score={score}")
    key = get_char_non_blocking() 
    tail_row = rows.pop()
    tail_col = cols.pop()

    print_at(tail_row, tail_col, colorama.ansi.Back.BLACK) 
    print_at(tail_row,tail_col, " ") 
    print_at(rows[0],cols[0],colorama.Back.WHITE) 
    
    if key == "s":
        drow = 1
        dcol = 0
    elif key == "w":
        drow = -1
        dcol = 0
    elif key == "d":
        drow = 0
        dcol = 1
    elif key == "a":
        drow = 0
        dcol = -1

    row = row + drow  
    col = col + dcol  

    rows.insert(0,row)  
    cols.insert(0,col) 

    print_at(row, col, " ") 
    for count in range (1,len(rows)):
        if rows[0] == rows[count] and cols[0]==cols[count]:
            game="end"
     
print_at(0,0,colorama.Back.BLACK)
print_at(0,0,colorama.ansi.clear_screen())

if score == 250:
    print_at(0,0,"You won!")
else:
    print_at(0,0,f"you lost and your score was {score}")
