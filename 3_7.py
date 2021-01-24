import pygame
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[[w, h, 'black', 0] for w in range(width)] for h in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, def_screen):
        for height in range(self.height):
            for width in range(self.width):
                if self.board[height][width][2] != 'black':
                    pygame.draw.rect(def_screen,
                                     self.board[height][width][2],
                                     (width * self.cell_size + self.left, self.top + height * self.cell_size,
                                      self.cell_size, self.cell_size),
                                     )
                pygame.draw.rect(def_screen,
                                 'white',
                                 (width * self.cell_size + self.left, self.top + height * self.cell_size,
                                  self.cell_size, self.cell_size),
                                 1)

    def click_handler(self, position):
        x_pos, y_pos = position
        x_pos = (x_pos - self.left) // self.cell_size
        y_pos = (y_pos - self.top) // self.cell_size
        if x_pos in range(self.width) and y_pos in range(self.height):
            return x_pos, y_pos


class Tetris(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.spin = 0
        self.score = 0
        self.act_figure = self.random_figure()
        self.stop_status = True
        self.x = 4
        self.y = 1
        self.active_pos = [4, 0, 'r', 0]
        self.texts = []
        self.figures = {'z': {0: [(0, 0), (-1, -1), (0, -1), (1, 0)],
                              1: [(1, 0), (0, 0), (1, -1), (0, 1)],
                              2: [(0, 1), (-1, 0), (0, 0), (1, 1)],
                              3: [(-1, 0), (0, 0), (0, -1), (-1, 1)],
                              'color': 'violet'
                              },
                        '-z': {0: [(0, 0), (1, -1), (0, -1), (-1, 0)],
                               1: [(1, 0), (1, 1), (0, 0), (0, -1)],
                               2: [(0, 0), (-1, 1), (0, 1), (1, 0)],
                               3: [(-1, 0), (-1, -1), (0, 1), (0, 0)],
                               'color': 'red'
                               },
                        't': {0: [(0, 0), (-1, 0), (0, 1), (1, 0)],
                              1: [(0, 0), (-1, 0), (0, 1), (0, -1)],
                              2: [(0, 0), (-1, 0), (0, -1), (1, 0)],
                              3: [(0, -1), (1, 0), (0, 1), (0, 0)],
                              'color': 'blue'
                              },
                        'l': {0: [(0, 0), (-1, 0), (1, 0), (2, 0)],
                              1: [(0, 0), (0, -1), (0, -2), (0, 1)],
                              2: [(-1, -1), (0, -1), (2, -1), (1, -1)],
                              3: [(1, 0), (1, -1), (1, -2), (1, 1)],
                              'color': 'lightblue'
                              },
                        'r': {1: [(0, 0), (0, -1), (1, -1), (0, 1)],
                              2: [(0, 0), (-1, 0), (1, 0), (1, 1)],
                              3: [(0, 0), (0, 1), (0, -1), (-1, 1)],
                              0: [(0, 0), (-1, -1), (-1, 0), (1, 0)],
                              'color': 'green'
                              },
                        'g': {3: [(0, 0), (-1, -1), (0, -1), (0, 1)],
                              0: [(0, 0), (1, -1), (1, 0), (-1, 0)],
                              1: [(0, 0), (1, 1), (0, 1), (0, -1)],
                              2: [(0, 0), (-1, 1), (-1, 0), (1, 0)],
                              'color': 'orange'
                              },
                        'rect': {0: [(0, 0), (1, 0), (0, 1), (1, 1)],
                                 1: [(0, 0), (1, 0), (0, 1), (1, 1)],
                                 2: [(0, 0), (1, 0), (0, 1), (1, 1)],
                                 3: [(0, 0), (1, 0), (0, 1), (1, 1)],
                                 'color': 'yellow'
                                 }}

    def random_figure(self):
        r = random.randrange(7)
        slow = ['z', '-z', 't', 'l', 'r', 'g', 'rect']
        new_figure = slow[r]
        return new_figure

    def next_move(self):
        self.set_pict()
        self.check_down()
        self.y += 1

    def flank_spin(self):
        for i in self.figures[self.act_figure][self.spin]:
            if self.x + i[0] not in range(self.width):
                return False
            elif self.y + i[1] not in range(self.height):
                return False
            elif self.board[self.y + i[1]][self.x + i[0]][3]:
                return False
        return True

    def cleaner(self):
        for height in range(self.height):
            for width in range(self.width):
                if not self.board[height][width][3]:
                    self.board[height][width][2] = 'black'

    def check_down(self):
        x, y, f, g = self.x, self.y, self.act_figure, self.spin
        for i in self.figures[f][g]:
            if y + 1 + i[1] not in range(self.height):
                self.stop_figure()
                break
            check = self.board[y + 1 + i[1]][x + i[0]]
            if check[3]:
                self.stop_figure()
                break

    def stop_figure(self):
        x, y, f, s = self.x, self.y, self.act_figure, self.spin
        for rex in self.figures[f][s]:
            self.board[y + rex[1]][x + rex[0]][3] = 1
            self.board[y + rex[1]][x + rex[0]][2] = self.figures[self.act_figure]['color']
        if y - 1 == 1:
            self.stop_status = False
        self.chek_row()
        self.x, self.y, self.act_figure, self.spin = 4, 1, self.random_figure(), 0

    def set_pict(self):
        self.cleaner()
        x, y, f, g = self.x, self.y, self.act_figure, self.spin
        for i in self.figures[f][g]:
            x, y = self.x + i[0], self.y + i[1]
            self.board[y][x][2] = self.figures[self.act_figure]['color']

    def chek_row(self):
        bufer = 0
        coord = []
        for i in range(self.height):
            if len(list(filter(lambda x: x[-1], self.board[i]))) == self.width:
                bufer += 1
                coord.append(i)
        slow = {1: ['Crash!', 70, 100, 100], 2: ['Big crash', 80, 100, 300], 3: ['Woow!!!', 90, 100, 500],
                4: ['АААА, ЧТО ТУТ ПРОИСХОДИТ?!?!', 120, 100, 1000]}
        if bufer:
            self.score += slow[bufer][3]
            self.texts.append(slow[bufer][:3])
        for der in coord:
            self.row_down(der)
        print(self.score)

    def row_down(self, y):
        for crew in range(y, 0, -1):
            for j in range(self.width):
                self.board[crew][j] = self.board[crew - 1][j][:]


pygame.init()
screen = pygame.display.set_mode((600, 600))
game = Tetris(9, 15)
running = True
MYEVENTTYPE = pygame.USEREVENT + 1
clock = pygame.time.Clock()
fps = 30
timer_num = 100000
pygame.time.set_timer(MYEVENTTYPE, timer_num)
font = pygame.font.Font(None, 50)
game.set_pict()
game.render(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.x -= 1
                if not game.flank_spin():
                    game.x += 1
            elif event.key == pygame.K_RIGHT:
                game.x += 1
                if not game.flank_spin():
                    game.x -= 1
            elif event.key == pygame.K_UP:
                game.spin += 1
                game.spin %= 4
                if not game.flank_spin():
                    game.spin -= 1
                    game.spin %= 4
            elif event.key == pygame.K_DOWN:
                game.next_move()
                pygame.time.set_timer(MYEVENTTYPE, timer_num)
            game.set_pict()
        if event.type == MYEVENTTYPE and game.stop_status:
            game.next_move()
        if event.type == pygame.QUIT:
            running = False
        elif not game.stop_status:
            game.stop_status = False
    screen.fill((0, 0, 0))
    text = font.render(f"Вы проиграли! Ваш счёт: {game.score}", True, (100, 255, 100))
    score_text = font.render(f'Ваш счёт: {game.score}', True, (255, 0, 255, 255))
    if not game.stop_status:
        screen.blit(text, (10, 470))
    screen.blit(score_text, (300, 10))
    game.render(screen)
    if game.texts:
        deleters = []
        for k in range(len(game.texts)):
            font_text = pygame.font.Font(None, game.texts[k][1])
            front = font_text.render(game.texts[k][0], True,
                                     (random.randrange(256), random.randrange(256), random.randrange(256)))
            screen.blit(front, (game.texts[k][2], 100))
            if game.texts[k][1] >= 4:
                game.texts[k][1] -= 3
                game.texts[k][2] += 2
            else:
                deleters.append(k)
        for i in deleters:
            del game.texts[i]
    pygame.display.flip()
    clock.tick(fps)
