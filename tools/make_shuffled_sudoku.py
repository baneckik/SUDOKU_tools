from PIL import Image, ImageDraw, ImageFont
import random
import math


def randomize_sudoku(sudoku, seed=123):
    random.seed(seed)
    
    # shuffling the digits
    digits = list(range(1, 10))
    digits_new = list(range(1, 10))
    random.shuffle(digits_new)
    digits_new_dict = dict(zip(digits, digits_new))
    sudoku_new = [0 if digit==0 else digits_new_dict[digit] for digit in sudoku]
    
    # shuffling boxes
    # box columns
    box_cols = [[[sudoku_new[i*3+j*9+k] for k in range(3)] for j in range(9)] for i in range(3)]
    random.shuffle(box_cols)
    sudoku_new = [box_cols[(i//3)%3][i//9][i%3] for i in range(81)] 
    # box rows
    box_rows = [[[sudoku_new[i*27+j*9+k] for k in range(9)] for j in range(3)] for i in range(3)]
    random.shuffle(box_rows)
    sudoku_new = [box_rows[i//27][(i//9)%3][i%9] for i in range(81)]
    
    # shuffling lines
    # columns
    columns = [[sudoku_new[i+j*9] for j in range(9)] for i in range(9)]
    col1, col2, col3 = columns[:3], columns[3:6], columns[6:]
    random.shuffle(col1)
    random.shuffle(col2)
    random.shuffle(col3)
    columns_new = col1+col2+col3
    sudoku_new = [columns_new[i%9][i//9] for i in range(81)]
    # rows
    rows = [[sudoku_new[i*9+j] for j in range(9)] for i in range(9)]
    row1, row2, row3 = rows[:3], rows[3:6], rows[6:]
    random.shuffle(row1)
    random.shuffle(row2)
    random.shuffle(row3)
    rows_new = row1+row2+row3
    sudoku_new = [rows_new[i//9][i%9] for i in range(81)]
    
    # transposition:
    if random.randint(0, 1)==0:
        for i in range(1, 9):
            for j in range(i+1, 9):
                sudoku_new[i*9+j], sudoku_new[j*9+i] = sudoku_new[j*9+i], sudoku_new[i*9+j]
    
    return sudoku_new

def draw_sudoku(img, sudoku, x, y, seed=None):
    square_size = 110
    main_line_width = 8
    small_line_width = 4
    
    draw = ImageDraw.Draw(img)
    
    # main lines:
    for i in range(4):
        # vertical:
        draw.line(xy=(x+i*3*square_size, y-3, x+i*3*square_size, y+9*square_size+main_line_width/2), 
              fill=(0, 0, 0), width = main_line_width)
        # horizontal:
        draw.line(xy=(x, y+i*3*square_size, x+9*square_size+main_line_width/2, y+i*3*square_size), 
              fill=(0, 0, 0), width = main_line_width)
    
    # small lines:
    for i in range(9):
        if i%3 != 0:
            # vertical:
            draw.line(xy=(x+i*square_size, y, x+i*square_size, y+9*square_size), 
                  fill=(0, 0, 0), width = small_line_width)
            # horizontal:
            draw.line(xy=(x, y+i*square_size, x+9*square_size, y+i*square_size), 
                  fill=(0, 0, 0), width = small_line_width)
    
    # digits:
    myFont = ImageFont.truetype('Keyboard.ttf', 65)
    for i, digit in enumerate(sudoku):
        if digit != 0 and digit != "0":
            draw.text(xy=(x+(i%9)*square_size + square_size*0.3, y+(i//9)*square_size+square_size*0.1), 
                  text=str(digit), font=myFont, fill=(0, 0, 0))
            
    # drawing seed information:
    if not math.isnan(seed):
        myFont = ImageFont.truetype('Keyboard.ttf', 30)
        draw.text(xy=(x, y-50), text="seed "+str(seed), font=myFont, fill=(0, 0, 0))

if __name__ == "__main__":
    output_file_name = "sudoku_test_00.png"
    img = Image.new(mode = "RGB", size = (2400, 3500), color = (255, 255, 255))
    
    sudoku_path = "../example_sudoku/example_sudoku.txt"
    with open(sudoku_path) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if not line.startswith("#") and len(line.strip())==9]
        sudoku = [int(digit) for line in lines for digit in line] 
    
    #seeds = [1]*6
    seeds = [random.randint(0, 1000000) for i in range(6)]
    
    for i in range(6):
        sudoku_rand = randomize_sudoku(sudoku, seeds[i])
        x = (i%2)*1150+130
        y = (i//2)*1100+200
        draw_sudoku(img, sudoku_rand, x, y, seed=seeds[i])
    
    img.save(output_file_name)
    
    
    
    
    