import pygame, itertools


WHITE = (255, 255, 255)
RED = (128, 0, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
YELLOW = (255,255,0)
ICE_BLUE = (240,248,255)
SEA_GREEN = (46,139,87)


class Box(object):
    state = 0

    def __init__(self, x, y, size, board):
        """
        Box where the x's and o's are drawn. This is the Box constructor

        Args:
            :param x: x coordinate
            :param y: y coordinate
            :param size: size of the board
            :param board: the board you're working on
            :type x: int
            :type y: int
            :type size: int
            :type board: int
        """
        self.size = size
        self.line_width = int(self.size / 20) if self.size > 40 else 1
        self.radius = (self.size / 2) - (self.size / 8)
        self.rect = pygame.Rect(x, y, size, size)
        self.board = board
    
    def draw_x_or_o(self, isX: bool, surface):
        """
        Draws X equivalent or O equivalent

        Args:
            :param isX:  Takes the parameter of the isX as a boolean and draws X or O
            :type isX: boolean

        Returns:
            :return: Nothing
        """
        if isX :
            effect = pygame.mixer.Sound("hadouken1.wav")
            effect.play()
            img = pygame.image.load("ryu_punch.png").convert_alpha()
            surface.blit(img, (self.rect.centerx - self.radius-5, self.rect.centery - self.radius-5))
#            pygame.draw.line(self.board.surface, RED, (self.rect.centerx - self.radius, self.rect.centery - self.radius), (self.rect.centerx + self.radius, self.rect.centery + self.radius), self.line_width)
#            pygame.draw.line(self.board.surface, RED, (self.rect.centerx - self.radius, self.rect.centery + self.radius), (self.rect.centerx + self.radius, self.rect.centery - self.radius), self.line_width)
        else:
            effect = pygame.mixer.Sound("tigerblow.wav")
            effect.play()
            img = pygame.image.load("sagat_kick.png").convert_alpha()
            surface.blit(img, (self.rect.centerx - self.radius-5, self.rect.centery - self.radius-5))
           # pygame.draw.circle(self.board.surface, BLUE, (int(self.rect.centerx), int(self.rect.centery)), int(self.radius), int(self.line_width))


class Board(object):
    turn = 1

    def __init__(self, grid_size=3, box_size=200, border=20, line_width=5):
        """
        Board Constructor

        Args:
            :param grid_size: grid size
            :param box_size: box size
            :param border: border size
            :param line_width: line width
            :type grid_size: int
            :type box_size: int
            :type border: int
            :type line_width: int
        """
        self.grid_size = grid_size
        self.box_size = box_size
        self.border = border
        self.line_width = line_width
        surface_size = (self.grid_size * self.box_size) + (self.border * 2) + (self.line_width * (self.grid_size - 1))
        self.surface = pygame.display.set_mode((surface_size, surface_size), 0, 32)
        self.game_over = False
        self.setup()
        
    def setup(self):
        """
        Sets the word Tic Tac Toe as the caption

        Returns:
            :return: Nothing
        """
        pygame.display.set_caption('Tic Tac Toe - Christmas edition')

        self.surface.fill(GREEN)
        self.draw_lines()
        self.initialize_boxes()
        self.game_over = False
        self.turn = 1
        pygame.mixer.music.load('streetfighter_1.wav')
        pygame.mixer.music.play(-1)
        self.calculate_winners()

    def draw_lines(self):
        """
        Draws the tic tac toe grid

        Returns:
            :return: Nothing
        """
        for i in range(1, self.grid_size):
            start_position = ((self.box_size * i) + (self.line_width * (i - 1))) + self.border
            width = self.surface.get_width() - (2 * self.border)
            pygame.draw.rect(self.surface, WHITE, (start_position, self.border, self.line_width, width))
            pygame.draw.rect(self.surface, WHITE, (self.border, start_position, width, self.line_width))
    
    def initialize_boxes(self):
        """
        This initializes all the boxes of the tic tac toe grid to be empty

        Returns:
            :return: Nothing
        """
        self.boxes = []
        
        top_left_numbers = []
        for i in range(0, self.grid_size):
            num = ((i * self.box_size) + self.border + (i *self.line_width))
            top_left_numbers.append(num)
        
        box_coordinates = list(itertools.product(top_left_numbers, repeat=2))
        for x, y in box_coordinates:
            self.boxes.append(Box(x, y, self.box_size, self))
    
    def get_box_at_pixel(self, x, y):
        """
        Get box at the particular pixel

        Args:
            :param x:  the X coordinate on screen
            :param y:  the Y coordinate on screen
            :type x: int
            :type y: int

        Returns:
            :return:  Nothing
        """
        for index, box in enumerate(self.boxes):
            if box.rect.collidepoint(x, y):
                return box
        return None
    
    def process_click(self, x, y):
        """
        Processes the click at a particular x, y, differentiates between while ingame or gameover state

        Args:
            :param x:  the X coordinate on screen
            :param y:  the Y coordinate on screen
            :type x: int
            :type y: int

        Returns:
            :return:  Nothing
        """
        # game over logic
        if self.game_over:
            self.process_click_gameover(x, y)
        else:
            self.process_click_ingame(x, y)

    def process_click_ingame(self, x, y):
        """
        Processes the click while you are in game

        Args:
            :param x:  the X coordinate on screen
            :param y:  the Y coordinate on screen
            :type x: int
            :type y: int

        Returns:
            :return:  Nothing
        """
        box = self.get_box_at_pixel(x, y)
        if box is not None and not self.game_over:
            self.play_turn(box)
            self.check_game_over()

    def process_click_gameover(self, x, y):
        """
        Processes the game when you choose if you continue to play again or quit the game (GameOver state)

        Args:
            :param x: the X coordinate on screen
            :param y: the Y coordinate on screen
            :type x: int
            :type y: int

        Returns:
            :return Nothing
        """
        surface_size = self.surface.get_height()
        if x < (surface_size / 2.5) and (surface_size / 2.5 ) < y < surface_size:
            self.setup()
        elif (surface_size / 2.5 ) < x < surface_size and (surface_size / 2.5) < y < surface_size:
            pygame.quit()

    def play_turn(self, box):
        """
        This is playing of the turn while ingame

        Args:
            :param box: The box object on the Tic Tac Toe screen
            :type box: Type Box Object tha

        Returns:
            :return: Nothing
        """
        if box.state != 0:
            return
        self.display_player_turn()
        if self.turn == 1:
            box.draw_x_or_o(True, self.surface)
            box.state = 1
            self.turn = 2
        elif self.turn == 2:
            box.draw_x_or_o(False, self.surface)
            box.state = 2
            self.turn = 1
        return

    def display_player_turn(self):
        """
        Displays the player's turn at the top of the screen

        Returns:
            :return:  Nothing
        """

        surface_size = self.surface.get_height()
        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 11))
        text = 'Player %s Turn' % self.turn

        text = font.render(text, True, WHITE, GREEN)
        rect = text.get_rect()
        rect.center = (surface_size / 2, surface_size /12)
        self.surface.blit(text, rect)

    def calculate_winners(self):
        """
        Calculates the winners of the game

        Returns:
            :return:  Nothing
        """
        self.winning_combinations = []
        indices = [x for x in range(0, self.grid_size * self.grid_size)]
        
        # Vertical combinations
        self.winning_combinations += ([tuple(indices[i:i+self.grid_size]) for i in range(0, len(indices), self.grid_size)])
        
        # Horizontal combinations
        self.winning_combinations += [tuple([indices[x] for x in range(y, len(indices), self.grid_size)]) for y in range(0, self.grid_size)]
        
        # Diagonal combinations
        self.winning_combinations.append(tuple(x for x in range(0, len(indices), self.grid_size + 1)))
        self.winning_combinations.append(tuple(x for x in range(self.grid_size - 1, len(indices), self.grid_size - 1)))
    
    def check_for_winner(self):
        """
        Checks for the winner

        Returns:
            :return: returns the winner (either Player 1 or two)
            :rtype winner: int
        """
        winner = 0
        for combination in self.winning_combinations:
            states = []
            for index in combination:
                states.append(self.boxes[index].state)
            if all(x == 1 for x in states):
                winner = 1
            if all(x == 2 for x in states):
                winner = 2
        return winner
    
    def check_game_over(self):
        """
        Checks if the game is over and sets the flag for game over or not

        Returns:
            :return:  Nothing
        """
        winner = self.check_for_winner()
        if winner:
            self.game_over = True
        elif all(box.state in [1, 2] for box in self.boxes):
            self.game_over = True
        if self.game_over:
            self.display_game_over(winner)

    def display_game_over(self, winner):
        """
        Displays if the game is over and prompts if you want the player to play again or quit

        Args:
            :param winner:
            :type winner: int

        Returns:
            :return: Nothing
        """
        surface_size = self.surface.get_height()
        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 8))
        if winner:
            text = 'Player %s wins!' % winner
        else:
            text = 'Draw!'
        text = font.render(text, True, BLACK, GREEN)
        rect = text.get_rect()

        rect.center = (surface_size / 2, surface_size / 4)
        self.surface.blit(text, rect)
        # prompt to play again

        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 12))
        text1 = "Continue?"
        text1 = font.render(text1, True, BLACK, GREEN)
        rect1 = text1.get_rect()
        rect1.center = (surface_size / 2, surface_size / 2)
        self.surface.blit(text1, rect1)

        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 12))
        text2 = "YES?"
        text2 = font.render(text2, True, BLACK, GREEN)
        rect2 = text2.get_rect()
        rect2.center = (surface_size / 4, surface_size * 0.75)
        self.surface.blit(text2, rect2)

        font = pygame.font.Font('freesansbold.ttf', int(surface_size / 12))
        text3 = "NO?"
        text3 = font.render(text3, True, BLACK, GREEN)
        rect3 = text3.get_rect()
        rect3.center = (surface_size * 0.75, surface_size * 0.75)
        self.surface.blit(text3, rect3)




