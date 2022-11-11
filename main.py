import sys
import pygame

pygame.init()  # Initialize. Do this first!

grid = [[None, None, None],
        [None, None, None],
        [None, None, None]]

x_turn = True
clicked_last_frame = False

black = 0, 0, 0  # Color black
white = 255, 255, 255  # Color white

screen_size = 600, 700  # Screen size

large_font = pygame.font.SysFont(None, 300)  # Default font

x_text = large_font.render('X', True, black)
o_text = large_font.render('O', True, black)

small_font = pygame.font.SysFont(None, 75)


def draw_board(screen, grid):
    # Draw a dividing line between the top and the game board
    pygame.draw.line(screen, black, (0, 100), (600, 100), 5)

    # Draw the horizontal grid lines
    pygame.draw.line(screen, black, (0, 300), (600, 300), 5)
    pygame.draw.line(screen, black, (0, 500), (600, 500), 5)
    pygame.draw.line(screen, black, (0, 700), (600, 700), 5)

    # Draw the vertical grid lines
    pygame.draw.line(screen, black, (200, 700), (200, 100), 5)
    pygame.draw.line(screen, black, (400, 700), (400, 100), 5)

    for y in range(3):  # Loop through each row of the board
        for x in range(3):  # Loop through each position of the row
            if grid[y][x] == "X":
                # Calculate the position for the X
                position_x = (x + 1) * 200 - x_text.get_rect().right - 30
                position_y = (y + 1) * 200 - x_text.get_rect().centery + 10

                # Put the X onto the screen
                screen.blit(x_text, (position_x, position_y))

            elif grid[y][x] == "O":
                # Calculate the position for the O
                position_x = (x + 1) * 200 - o_text.get_rect().right - 20
                position_y = (y + 1) * 200 - o_text.get_rect().centery + 10

                # Put the O onto the screen
                screen.blit(o_text, (position_x, position_y))


# Draw the player won bar
def draw_won_bar(screen, message):
    message = small_font.render(message, True, black)
    screen.blit(message, (20, 30))

# Checks if the player pressed the retry button


def retry_pressed(screen, clicked_this_frame):
    rect = pygame.draw.rect(screen, black, [380, 15, 200, 70])
    retry_text = small_font.render("Retry", True, white)
    screen.blit(retry_text, (410, 28))
    if clicked_this_frame and rect.collidepoint(pygame.mouse.get_pos()):
        return True
    else:
        return False


# Function to check if a player won
def check_for_win(grid):
    for y in range(3):
        if grid[y][0] == grid[y][1] == grid[y][2] != None:
            return grid[y][0]
    for x in range(3):
        if grid[0][x] == grid[1][x] == grid[2][x] != None:
            return grid[0][x]
    if grid[0][0] == grid[1][1] == grid[2][2] != None:
        return grid[0][0]
    if grid[0][2] == grid[1][1] == grid[2][0] != None:
        return grid[0][2]
    return None


# Create the screen and set its size to the size
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Tic Tac Toe")  # Set the title of the window

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)  # Fill the screen with white

    # Get the left mouse button state (0 is mouse left)
    click = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position

    # If we don't check if the button was pressed this frame and not pressed the previous frame, it will think we cl
    if click and not clicked_last_frame:
        clicked_this_frame = True
    else:
        clicked_this_frame = False

    clicked_last_frame = click

    # If the player presses the restart button, restart the game
    if retry_pressed(screen, clicked_this_frame):
        grid = [[None, None, None],
                [None, None, None],
                [None, None, None]]
        x_turn = True

    # Check if any player won
    winner = check_for_win(grid)

    # Someone has won
    if winner != None:
        draw_won_bar(screen, f"Player {winner} Won")
    # No player has won, check if the player has clicked
    elif clicked_this_frame:
        # Checking if the mouse y is greater than 100 because the board starts over y = 100
        if mouse_y > 100:
            # Convert the mouse position to tic tac toe board coordinates
            grid_x = mouse_x // 200
            grid_y = (mouse_y - 100) // 200

            # Make sure the location the player clicks on is empty
            if grid[grid_y][grid_x] == None:
                if x_turn:
                    grid[grid_y][grid_x] = "X"
                else:
                    grid[grid_y][grid_x] = "O"
                x_turn = not x_turn

    draw_board(screen, grid)
    pygame.display.flip()  # Updates the display
