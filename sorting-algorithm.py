import random
import pygame

pygame.init()

class DrawInformation:
    # defines colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    # sets background color to white
    BACKGROUND_COLOR = WHITE
    # creates gradient colors for bars
    GRADIENTS = [
        (0, 0, 0),
        (32, 32, 32),
        (64, 64, 64)
    ]
    # leaves empty space on the sides and top
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2
        # self.start_y = self.TOP_PAD // 2


# draws the general screen
def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)
    pygame.display.update()

# draws the actual bars that get sorted
def draw_list(draw_info):
    lst = draw_info.lst
    for i, val in enumerate(lst):
        # bars are drawn from top left -> bottom right
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        # Changes bar within the 3 colors
        color = draw_info.GRADIENTS[i % 3]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

# creates a random list
def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


# main body of program
def main():
    clock = pygame.time.Clock()
    n = 25
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    # Loops that handles events
    run = True
    while run:
        # Clock that regulates how many loops run per second
        clock.tick(60)
        # Updates the display
        draw(draw_info)
        # Handling of events
        for event in pygame.event.get():
            # Quit button
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            # Pressing "r" key resets bars
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)

    pygame.quit()

if __name__ == "__main__":
    main()
