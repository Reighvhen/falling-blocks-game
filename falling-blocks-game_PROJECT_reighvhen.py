# Made by Reigh Vhen Dimailig 


#   Note:This is made using Spyder 6 IDE 
#        Please run this on an EXTERNAL TERMINAL otherwise it won't work in the regular Ipython console

#   1.) Go to the 'Run' menu
# 	2.) Click configuration per file
# 	3.) Change by selecting external terminal instead of the regular Ipython console, in the 'Run this file in' section.
# 	4.) Click 'Ok' to save the change.


#   - Copyright Notice - 
#   This project is inspired by the original Tetris game, which is a trademark of The Tetris Company. 
#   All rights to the original Tetris game, including its gameplay, mechanics, and trademarks, belong its original creator and The Tetris Company.
#   This code is a personal project created for educational and non-commercial purposes, and it is not associated with or endorsed by The Tetris Company.

import matplotlib.pyplot as plt
import random
from matplotlib.patches import Rectangle

#   Finally, this is it!!

# Constants for grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Block shapes and colors
BLOCKS = {
    'O': {'shape': [(0, 0), (1, 0), (0, 1), (1, 1)], 'color': 'red'},    # Square block (O)
    'I': {'shape': [(0, 0), (1, 0), (2, 0), (3, 0)], 'color': 'green'},  # Line block (I)
    'L': {'shape': [(0, 0), (1, 0), (2, 0), (2, 1)], 'color': 'blue'},   # L block
    'T': {'shape': [(0, 0), (1, 0), (2, 0), (1, 1)], 'color': 'purple'}, # T block
    'S': {'shape': [(0, 0), (1, 0), (1, 1), (2, 1)], 'color': 'orange'}  # S block
}

def draw_grid(ax):
    ax.set_xlim(0, GRID_WIDTH)
    ax.set_ylim(0, GRID_HEIGHT)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    
    for x in range(GRID_WIDTH + 1):
        start_point = [x,0] #start of the vertical line @ (x,0)
        end_point = [x, GRID_HEIGHT] # End of the vertical line @ (x, GRID_HEIGHT)
        
        #plot the verical lines
        ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='white', linewidth = 0.5)
        
    for y in range(GRID_HEIGHT + 1):
        start_point = [0,y] #start of the horizontal line @ (x,0)
        end_point = [GRID_WIDTH, y] # End of the horizontal line @ (GRID_WIDTH, y)
        
        #plot the horizonatl lines
        ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='white', linewidth = 0.5)

def draw_block(ax, block_shape, start_x, start_y, color):
    
    # Draw the current block at the specified position
    for dx, dy in block_shape:
        
        #calculate the position of the block's square (where they start on the grid - bottom left corner, like a point of origin?)
        x_position = start_x + dx #move left or right
        y_position = start_y + dy #move up or down
        
        #create a rectangle at the calculated position
        rect = Rectangle((x_position, y_position), 1, 1, facecolor=color, edgecolor='white')
                      # (bottom-left corner of the rectangle), (1x1 square), (color of the block (inside the rectangle)), (border color of the block)
        
        #add the rectangle to the plot
        ax.add_patch(rect)

# allows for the rotation of the block
def rotate_block(block_shape):
    
    # for each (dx, dy) in block_shape, we return a new rotated coordinates (-dy, dx)
    rotated_block = [(-dy, dx) for dx, dy in block_shape]
    
    return rotated_block


def check_collision(block_shape, start_x, start_y, placed_blocks):
        
    # Empty set to store the (x, y) positions, this allow us to know that there are blocks occupying the grid cells at positions (x,y)
    # Also help in preventing blocks to overlap
    placed_positions = set()

    for block in placed_blocks:
        # Access the x-coordinate (first value) from the block
        px = block[0]

        # Access the y-coordinate (second value) from the block
        py = block[1]

        # Add the (px, py) position to the set
        placed_positions.add((px, py))
            
    # block_shape contains the relative coordinates of the block's segments
    for dx, dy in block_shape:
        
        # Calculate the block's actual position on the grid
        x = start_x + dx
        y = start_y + dy
        
        # Ensure the block is within the grid boundaries:
        # - x must be between 0 and GRID_WIDTH - 1
        # - y must be non-negative (blocks can't fall below 0)
        # Collision with grid edges
        if x < 0 or x >= GRID_WIDTH or y < 0:
            return True 
        
        # Check if the block collides with placed blocks
        if (x, y) in placed_positions:
            return True # Collision with another block detected, don't move
        
    return False # No collisions, you can move

# Clear completed lines and shift blocks down
def clear_lines(placed_blocks):
    
    # Create an empty dictionary to know how many blocks are in each row
    row_counts = {}
    
    # Go through each placed block and count how many blocks are in each row (y-value)
    for block in placed_blocks: 
        x = block[0]  # x-coordinate
        y = block[1]  # y-coordinate
        color = block[2] 
        
        if y in row_counts: 
            row_counts[y] += 1  # If the row is already in the dictionary, add 1
        else: 
            row_counts[y] = 1  # If the row is not in the dictionary, start counting from 1
            
   
    #Find all rows that are full (have exactly GRID_WIDTH blocks)
    full_rows = []
    
    for row in row_counts:  # Loop over the row (y-coordinate)
        count = row_counts[row]  # Access the count directly by using the row (y-coordinate)
        if count == GRID_WIDTH:  # If the row is full
            full_rows.append(row)  # Add the row to the list of full rows
    
    # If there are no full rows, return the original placed blocks and 0 (no lines cleared)
    if not full_rows:
        return placed_blocks, 0  # No rows cleared
    
    
    # Create a new set of blocks by removing the blocks in the completed rows
    new_blocks = set()  # This will store the blocks after they've been moved down.

    for (x, y, color) in placed_blocks:
        if y not in full_rows:  # If the block is not in a full row, keep it.
            # Move the block down based on how many rows are cleared above it.
            rows_above = 0
            for r in full_rows:
                if r < y:
                    rows_above += 1  
    
            new_y = y - rows_above  # Shift the block down by that many rows.
            new_blocks.add((x, new_y, color))
    # Return the new blocks and the number of cleared rows
    return new_blocks, len(full_rows)

# Create the overall window
fig = plt.figure(figsize=(6, 12))  # This creates the whole figure with size 6x12 inches

# Step 2: Create the drawing area inside the figure
ax = fig.add_subplot(111)  # This creates one subplot (axes) inside the figure, 111 = (1 row and 1 column of plots)

# Set the background color of the figure and the plot to black
fig.patch.set_facecolor('black')  # Make the background of the whole figure black
ax.set_facecolor('black')         # Make the background of the plot area black

keyboard_input = None  # No key pressed

# Handle keyboard input
def on_key(event):
    global keyboard_input
    
    # event.key - gets the key that was pressed by the user, which is then stores the the variable keyboard_input
    keyboard_input = event.key

def run_game():
    """Main loop for the block-falling game."""
    global keyboard_input
    placed_blocks = set()  # Initialize set to keep track of placed blocks.
    score = 0  # Initialize score.
    high_score = 0  # Initialize high score.
    game_active = False  # Track if the game is active.

    # Connect key press events for control.
    fig.canvas.mpl_connect('key_press_event', on_key)

    while True:
        if not game_active:  # Check if the game is active.
            ax.clear()  # Clear the axis for a fresh display.
            draw_grid(ax)  # Draw the grid.
            
            
            # Display the "Press SPACE to Start" message.
            # Place the message at the center of the screen
            ax.text(
                GRID_WIDTH / 2,  # X-coordinate: half of the grid width (centered horizontally)
                GRID_HEIGHT / 2,  # Y-coordinate: half of the grid height (centered vertically)
                "Press the \n SPACEBAR \n to Start",  # The message to display
                color='white',  # The color of the text
                fontsize=24,  # The size of the text
                ha='center',  # Horizontal alignment: 'center' means it's aligned to the center
                va='center',  # Vertical alignment: 'center' means it's aligned to the center
                fontweight='bold'  # Makes the text bold
                )
            
            plt.draw()  # Update the display.

            # Wait for the player to press SPACE.
            while keyboard_input != ' ':
                plt.pause(0.1)  # Pause to allow for key press.
            game_active = True  # Set the game to active.
            keyboard_input = None  # Reset keyboard input.
            placed_blocks = set()  # Clear placed blocks from previous game.
            score = 0  # Reset score.

        # Select a random block.
        block_label = random.choice(list(BLOCKS.keys()))  # Select random block from BLOCKS.
        current_block = BLOCKS[block_label]['shape']  # Get block shape.
        current_color = BLOCKS[block_label]['color']  # Get block color.
        x, y = (GRID_WIDTH // 2) - 1, GRID_HEIGHT - 1  # Starting position for the block.

        # Check for game over before placing the block.
        if check_collision(current_block, x, y, placed_blocks):  # Check if collision occurs.
            game_active = False  # Game over condition.
            ax.clear()  # Clear the axis for game over display.
            draw_grid(ax)  # Draw the grid again.

            # Display game over message.
            # "GAME OVER" message 
            ax.text(
                GRID_WIDTH / 2,  # X-coordinate: center of the grid horizontally
                GRID_HEIGHT / 2,  # Y-coordinate: center of the grid vertically
                "GAME OVER",  # Text message to display
                color='white',  # Text color
                fontsize=24,  # Font size: larger for emphasis
                ha='center',  # Horizontal alignment: centered at the X-coordinate
                va='center',  # Vertical alignment: centered at the Y-coordinate
                fontweight='bold'  # Bold text for emphasis
            )
            
            
            #Final score
            ax.text(
                GRID_WIDTH / 2,  # X-coordinate: horizontally centered on the grid
                (GRID_HEIGHT / 2) - 2,  # Y-coordinate: slightly below the center (2 units down)
                "Final Score: " + str(score),  # Displays "Final Score: [score value]"
                color='white',  # Text color
                fontsize=16,  # Font size: moderate for readability but smaller than the title
                ha='center',  # Horizontal alignment: center-aligns the text
                va='center'  # Vertical alignment: center-aligns the text
            )

            # Update high score if necessary.
            if score > high_score:  # Check if current score is higher than high score.
                high_score = score  # Update high score.
            ax.text(
                GRID_WIDTH / 2,  # X-coordinate: horizontally centered on the grid (middle of the screen)
                (GRID_HEIGHT / 2) - 4,  # Y-coordinate: slightly below the previous message (4 units down)
                "High Score: " + str(high_score), # Displays "High Score: [high_score value]"
                color='white',  # Text color is white
                fontsize=16,  # Font size: 16, smaller than the "GAME OVER" text
                ha='center',  # Horizontal alignment: center-aligns the text
                va='center'  # Vertical alignment: center-aligns the text
            )
            
            ax.text(
                GRID_WIDTH / 2,  # X-coordinate: horizontally centered on the grid (middle of the screen)
                (GRID_HEIGHT / 2) - 6,  # Y-coordinate: a little lower than the previous line (6 units down)
                "Press SPACE to Retry",  # Static text telling the player to press SPACE to restart
                color='white',  # Text color is white
                fontsize=16,  # Font size: same as the high score text for consistency
                ha='center',  # Horizontal alignment: center-aligns the text
                va='center'  # Vertical alignment: center-aligns the text
            )
            plt.draw()  # Update the display.

            # Wait for player to press SPACE to retry.
            while keyboard_input != ' ':
                plt.pause(0.1)  # Pause to check for key press.
            keyboard_input = None  # Reset keyboard input.
            continue  # Restart the game loop.

        # Game loop for moving the block.
        while True:  # Continue until block is placed.
            ax.clear()  # Clear the axis for a fresh display.
            ax.set_title("Score: %d  High Score: %d" % (score, high_score),
                         color='white', 
                         fontsize=16)
            draw_grid(ax)  # Draw the grid.

            # Draw all blocks that have already been placed on the grid.
            for block in placed_blocks:
                # Access the x-coordinate (horizontal position) of the block
                px = block[0]
            
                # Access the y-coordinate (vertical position) of the block
                py = block[1]
            
                # Access the color of the block (third value in the block)
                color = block[2]
            
                # Now, we will draw the block at its (px, py) position with its color
                draw_block(ax, [(0, 0)], px, py, color)  
                # (0,0) = where our block starts

            # Draw the current falling block.
            draw_block(ax, current_block, x, y, current_color)  # Draw the current block.
            plt.pause(0.2)  # Pause to create animation effect.

            # current_block = contains the list of coordinates (relative positions) that make up the block
            # (x/y) (+-) 1 = move one left/right/down
            # placed_blocks = represents all the blocks that is currently on the grid

            # Check if the player wants to move the block left
            if keyboard_input == 'left':
                # Check if there is no collision when moving left
                if not check_collision(current_block, x - 1, y, placed_blocks):
                    x -= 1  # Move the block left if no collision
            
            # Check if the player wants to move the block right
            elif keyboard_input == 'right':
                # Check if there is no collision when moving right
                if not check_collision(current_block, x + 1, y, placed_blocks):
                    x += 1  # Move the block right if no collision
            
            # Check if the player wants to move the block down
            elif keyboard_input == 'down':
                # Check if there is no collision when moving down
                if not check_collision(current_block, x, y - 1, placed_blocks):
                    y -= 1  # Move the block down if no collision
                    
                    
            elif keyboard_input == 'up':  # Rotate block.
                if block_label not in ['Square', 'O']:  # Only rotate if the block is not a square or 'O'.
                    rotated_block = rotate_block(current_block)  # Attempt to rotate the block.
                    if not check_collision(rotated_block, x, y, placed_blocks):  # Check for collision.
                        current_block = rotated_block  # rotate if valid
                        
            keyboard_input = None  # Reset input to avoid repetition.

            # Move the block down automatically (every frame).
            if not check_collision(current_block, x, y - 1, placed_blocks):
                y -= 1  # Move the block down one space.
            else:
                # If the block can't move down because of collision, place it on the grid.
                for dx, dy in current_block:
                    
                    # Calculate the new position (new_x, new_y) for the block and get the color of the current block
                    new_x = x + dx
                    new_y = y + dy
                    color = current_color
                    
                    blocK = (new_x, new_y, color)
                    
                    # Add the tuple to the placed_blocks set
                    placed_blocks.add(blocK)

                break  # Exit the loop to spawn a new block.

        # Clear completed lines and update the score.
        result = clear_lines(placed_blocks)
        placed_blocks = result[0]
        lines_cleared = result[1]
        score += lines_cleared * 100  # Update the score based on how many lines were popped, 1 row = 100 points!!.

plt.show(block=False)  # Keep the plot open without blocking the program.
run_game()  # Start the game.





