from copy import deepcopy
import pygame
from search import create_initial_node, Search
import sokoPuzzle
from threading import Timer
import time
from sys import exit



class Sokoban():

    def __init__(self):
        pygame.init()

        self.level = 0
        self.game_is_solved = False

        self.load_images()
        self.new_game()

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode(
            (window_width, window_height + self.scale))
        self.game_font = pygame.font.SysFont("Arial", 15)

        pygame.display.set_caption("Sokoban")

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ["floor", "wall", "target", "box", "player", "done", "target_player"]:
            self.images.append(pygame.image.load("assets/" + name + ".png"))

    def new_game(self):
        if (self.game_is_solved):
            self.level = 0
            self.game_is_solved = False

        maps = [[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 2, 0, 3, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 0, 1, 4, 0, 1, 1, 1, 1, 1, 1],   # LEVEL 1
                 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 6, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],   # LEVEL 2
                 [1, 1, 1, 1, 1, 0, 0, 3, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 0, 0, 3, 4, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 0, 0, 0, 1, 3, 0, 1, 1, 1, 1, 1, 1, 1],   # LEVEL 3
                 [1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 0, 5, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 3, 1, 3, 0, 1, 1, 1, 1, 1, 1, 1],   # LEVEL 4
                 [1, 1, 1, 1, 1, 0, 2, 4, 2, 0, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 0, 4, 0, 0, 2, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],   # LEVEL 5
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 0, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 2, 0, 1, 0, 4, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 0, 0, 1, 3, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 2, 0, 0, 3, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 0, 0, 1, 3, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 2, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1],   # LEVEL 6
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 2, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 3, 3, 3, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],   # LEVEL 7
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 2, 2, 2, 5, 3, 4, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],   # LEVEL 8
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 2, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0, 3, 0, 3, 3, 0, 0, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 3, 4, 1, 1, 1, 1, 1],   # LEVEL 9
                 [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]]

        self.map = maps[self.level] #self.level
        self.moves = 0

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def draw_window(self):
        self.window.fill((255, 255, 255))

        game_text = self.game_font.render(
            "Moves: " + str(self.moves), True, (0, 0, 255))
        self.window.blit(game_text, (10, self.height * self.scale + 10))

        game_text = self.game_font.render(
            "Level: "+str(self.level+1), True, (0, 0, 255))
        self.window.blit(game_text, (80, self.height * self.scale + 10))
        
        game_text = self.game_font.render(
            "SPACE BAR: auto play", True, (0, 0, 255))
        self.window.blit(game_text, (150, self.height * self.scale + 10))

        game_text = self.game_font.render("F2 = new try", True, (0, 0, 255))
        self.window.blit(game_text, (320, self.height * self.scale + 10))

        game_text = self.game_font.render("Esc = exit game", True, (0, 0, 255))
        self.window.blit(game_text, (420, self.height * self.scale + 10))

        for y in range(self.height):
            for x in range(self.width):
                square = self.map[y][x]
                self.window.blit(
                    self.images[square], (x * self.scale, y * self.scale))

        if self.all_game_solved():
            game_text = self.game_font.render(
                "Congratulations, you solved the game! F2 = NEW GAME", True, (0, 0, 255))
            game_text_x = self.scale * self.width / 2 - game_text.get_width() / 2
            game_text_y = self.scale * self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0), (game_text_x,
                                                      game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))

        pygame.display.flip()

    #if event.key == pygame.K_RETURN: 
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.solver()
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def find_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [4, 6]:
                    return (y, x)

    def move(self, move_y, move_x):
        if self.all_game_solved():
            return
        robot_old_y, robot_old_x = self.find_robot()
        robot_new_y = robot_old_y + move_y
        robot_new_x = robot_old_x + move_x

        if self.map[robot_new_y][robot_new_x] == 1:
            return

        if self.map[robot_new_y][robot_new_x] in [3, 5]:
            box_new_y = robot_new_y + move_y
            box_new_x = robot_new_x + move_x

            if self.map[box_new_y][box_new_x] in [1, 3, 5]:
                return

            self.map[robot_new_y][robot_new_x] -= 3
            self.map[box_new_y][box_new_x] += 3

        self.map[robot_old_y][robot_old_x] -= 4
        self.map[robot_new_y][robot_new_x] += 4
        self.moves += 1

    def all_game_solved(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [2, 6]:
                    return False
        if self.level != len(self.map):
            self.level += 1
            self.new_game()
        elif self.level == len(self.map):
            self.game_is_solved = True
            return True

    def solver(self): 
       dictionnary = {
        0:' ',
        1:'O',  
        2:'S',
        3:'B',
        4:'R',
        5: '*',  
        6: '.',
        7: 'D'
       }
       board = deepcopy(self.map)
    
       for i in range (len(board)):
            for j in range (len(board[0])):
                board[i][j] = dictionnary[board[i][j]]
      
       
       initial_node = create_initial_node(board)
       goalNode, num_steps = Search.A(initial_node, heuristic=3)
       moves = goalNode.moves
       
       for move in moves:
           
            if move == 'U':
                self.move(-1, 0)
                self.draw_window()
                time.sleep(0.2)
                
            if move =='L':
                self.move(0, -1)
                self.draw_window()
                time.sleep(0.2)
                
            if move == 'R': 
                self.move(0, 1)
                self.draw_window()
                time.sleep(0.2)
                
            if move == 'D':
                self.move(1, 0)
                self.draw_window()
                time.sleep(0.2)


if __name__ == "__main__":
    Sokoban()