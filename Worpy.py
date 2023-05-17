from Crypto.Random import random
import cv2
import numpy as np
import string
import os
import beaupy
from pystyle import Colors, Colorate
import textwrap



def banner():
    banner = """
             ▄▀▀▄    ▄▀▀▄  ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▄ ▀▀▄
            █   █    ▐  █ █      █ █   █   █ █   █   █ █   ▀▄ ▄▀
            ▐  █        █ █      █ ▐  █▀▀█▀  ▐  █▀▀▀▀  ▐     █
              █   ▄    █  ▀▄    ▄▀  ▄▀    █     █            █
               ▀▄▀ ▀▄ ▄▀    ▀▀▀▀   █     █    ▄▀           ▄▀
                     ▀             ▐     ▐   █             █
                                             ▐             ▐

        Made by Ori#6338 | @therealOri_ | https://github.com/therealOri
    """
    colored_banner = Colorate.Horizontal(Colors.purple_to_blue, banner, 1)
    return colored_banner





def clear():
    os.system("clear||cls")


def generate_string():
    alphabet = string.ascii_letters + string.digits
    rnd_string = ''.join(random.choice(alphabet) for i in range(12))
    return rnd_string



# Function to generate a random word search grid
def generate_grid(size):
    grid = [['_' for _ in range(size)] for _ in range(size)]
    return grid



# Function to place a word in the grid
def place_word(grid, word, existing_words):
    width = len(grid)
    height = len(grid[0])
    word = word.upper()
    word = random.choice([word, word[::-1]])  # has a chance to make the word reversed.

    while True:
        direction = random.choice([[1, 0], [0, 1], [1, 1]])  # 1,0 = left to right | 0,1 = right to left | 1,1 = diagonal
        xstart = width if direction[0] == 0 else width - len(word) - 1
        ystart = height if direction[1] == 0 else height - len(word) - 1

        x = random.randrange(0, xstart)
        y = random.randrange(0, ystart)

        intersects = False
        for c in range(len(word)):
            if grid[x + direction[0] * c][y + direction[1] * c] != '_' and grid[x + direction[0] * c][y + direction[1] * c] != word[c]:
                intersects = True
                break

        if not intersects:
            break

    for c in range(len(word)):
        grid[x + direction[0] * c][y + direction[1] * c] = word[c]

    existing_words.append(word)
    return grid



def fill_grid_random(grid):
    alphabet = string.ascii_letters.upper()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '_':
                grid[i][j] = random.choice(alphabet)
    return grid




def main(words: list, grid_size=11):
    grid = generate_grid(grid_size)
    existing_words = []

    for word in words:
        placed = False
        while not placed:
            placed = place_word(grid, word, existing_words)

    # After words have been placed, fill the grid with random letters.
    grid = fill_grid_random(grid)


    cell_size = 50
    image_size = grid_size * cell_size
    header_height = 100
    footer_height = 100
    total_height = image_size + header_height + footer_height
    image = np.ones((total_height, image_size, 3), dtype=np.uint8) * 255

    # Header & Letters
    header_text = "Worpy"
    header_font = cv2.FONT_HERSHEY_SIMPLEX
    header_font_scale = 1
    header_font_thickness = 2
    (header_text_width, header_text_height), _ = cv2.getTextSize(header_text, header_font, header_font_scale, header_font_thickness)
    header_text_offset_x = int((image_size - header_text_width) / 2)
    header_text_offset_y = int(header_height / 2) + int(header_text_height / 2)
    cv2.putText(image, header_text, (header_text_offset_x, header_text_offset_y), header_font, header_font_scale, (0, 0, 0), header_font_thickness, cv2.LINE_AA)


    # Footer for words to find
    footer_font = cv2.FONT_HERSHEY_SIMPLEX
    footer_font_scale = 0.7
    footer_font_thickness = 1
    footer_text = "Words to find: " + ", ".join(words)
    footer_text_lines = textwrap.wrap(footer_text, width=50)
    footer_text_offset_x = 10
    footer_text_offset_y = total_height - 40
    line_height = int(footer_font_scale * 35)


    for i, line in enumerate(footer_text_lines):
        line_y = footer_text_offset_y + i * line_height
        cv2.putText(image, line, (footer_text_offset_x, line_y), footer_font, footer_font_scale, (0, 0, 0), footer_font_thickness, cv2.LINE_AA)

    # Draw the grid lines on the image
    for i in range(header_height, total_height - footer_height + 1, cell_size):
        cv2.line(image, (0, i), (image_size, i), (0, 0, 0), 1)
    for i in range(0, image_size, cell_size):
        cv2.line(image, (i, header_height), (i, total_height - footer_height), (0, 0, 0), 1)

    for i in range(grid_size):
        for j in range(grid_size):
            letter = grid[i][j]
            (text_width, text_height) = cv2.getTextSize(letter.lower(), header_font, header_font_scale, header_font_thickness)[0]
            text_offset_x = int((cell_size - text_width) / 2)
            text_offset_y = int((cell_size + text_height) / 2)
            cv2.putText(image, letter, (j * cell_size + text_offset_x, i * cell_size + header_height + text_offset_y), header_font, header_font_scale, (0, 0, 0), header_font_thickness)

    cv2.imwrite(f"{generate_string()}.png", image)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    clear()
    while True:
        main_options = ["Create?", "Exit?"]
        print(f'{banner()}\n\nWhat would you like to do?\n-----------------------------------------------------------\n')
        main_option = beaupy.select(main_options, cursor_style="#ffa533")

        if not main_option:
            gcm.clear()
            exit("Keyboard Interuption Detected!\nGoodbye! <3")

        if main_options[0] in main_option:
            clear()
            flag=0
            while flag == 0:
                size = beaupy.prompt("How big do you want the grid? - (11 = 11x11)")
                if not size:
                    flag=1
                    clear()
                    break

                if flag == 0:
                    try:
                        size = int(size)
                    except Exception as e:
                        input(f'Value given is not an integer/number.\n{e}\n\nPress "enter" to continue...')
                        clear()
                        continue

                    if size < 10:
                        clear()
                        input('Grid can not be less than 10 (10x10)\n\nPress "enter" to continue..')
                        clear()
                        continue

                    break

            if flag == 1:
                clear()
                continue

            if beaupy.confirm("Want to use the default list of words?"):
                word_list = ["baloons", "party", "cake", "events", "summer", "pool", "music", "games"]
                main(word_list, size)
                clear()
                input(f'Game of word search has been made! Words to find are: {word_list}\n\nPress "enter" to continue...')
                clear()
                continue
            else:
                word_list = beaupy.prompt("What words do you want to use? - (python, butter, waffles, html)").split(", ")
                main(word_list, size)
                clear()
                input(f'Game of word search has been made! Words to find are: {word_list}\n\nPress "enter" to continue...')
                clear()
                continue

        if main_options[1] in main_option:
            clear()
            exit("Goodbye! <3")





