import random
import pygame

pygame.init()

class DrawInformation:
    # defines colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
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
    FONT = pygame.font.SysFont('ebgaramondvariablefontwght', 20)
    LARGE_FONT = pygame.font.SysFont('ebgaramondvariablefontwght', 25)

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
        self.block_height = int((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2
        # self.start_y = self.TOP_PAD // 2


# draws the general screen
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLUE)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    

    controls = draw_info.FONT.render("R - reset | SPACE - start sorting | A - ascending | D - descending | U - ↑ speed | L - ↓ speed", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))
    
    sorting = draw_info.FONT.render("B - bubble sort | I - insertion sort | S  - selection sort | Q - quick sort | M - merge sort | B - bogo sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))
    
    draw_list(draw_info)
    pygame.display.update()

# draws the actual bars that get sorted
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i, val in enumerate(lst):
        # bars are drawn from top left -> bottom right
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        # Changes bar within the 3 colors
        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()

# creates a random list
def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

# bubble sort
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.RED, j + 1: draw_info.GREEN}, True)
                yield True
    return lst

# insertion sort
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.RED, i: draw_info.GREEN}, True)
            yield True
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
    sorting = False
    ascending = True
    # default is bubble sort and ascending
    sorting_algo = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None
    speed = 8

    while run:
        # Clock that regulates how many loops run per second
        clock.tick(speed)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        # Handling of event s
        for event in pygame.event.get():
            # Quit button
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            # pressing "r" key resets bars
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_u:
                speed += 2
            elif event.key == pygame.K_l:
                if speed > 2:
                    speed -= 2
            # pressing "space" key sorts
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info, ascending)
            # pressing "a" key ascends
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            # pressing "d" key descends
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            # pressing "i" key descends
            elif event.key == pygame.K_i and not sorting:
                sorting_algo = insertion_sort
                sorting_algo_name = "Insertion Sort"
            # pressing "b" key descends
            elif event.key == pygame.K_b and not sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"


    pygame.quit()

if __name__ == "__main__":
    main()
