import pygame,sys
from pygame.math import Vector2
import random
from openpyxl import load_workbook

cell_size = 40
cell_num = 20


class Apple:
    def __init__(self,screen):
        '''zmienne owocow'''
        self.screen = screen
        self.apple_img = pygame.image.load('venv/resources/apple.png').convert_alpha()
        self.banana_img = pygame.image.load('venv/resources/banana.png').convert_alpha()
        self.cherry_img = pygame.image.load('venv/resources/cherry.png').convert_alpha()
        self.grape_img = pygame.image.load('venv/resources/grape-kopia.png').convert_alpha()
        self.orange_img = pygame.image.load('venv/resources/orange.png').convert_alpha()
        self.strawberry_img = pygame.image.load('venv/resources/strawberry-kopia.png').convert_alpha()
        self.randomize()
        self.change_Fruit()

    def draw_Fruit(self):
        '''rysowanie owocow'''
        self.fruit = pygame.Rect(int(self.position.x* cell_size),int(self.position.y*cell_size),cell_size,cell_size)
        self.screen.blit(self.choice,self.fruit)

    def randomize(self):
        '''wybieranie losowego miejsca dla owoca'''
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.position = Vector2(self.x, self.y)

    def change_Fruit(self):
        '''wybiranie losowego img dla owoca'''
        self.img = [self.apple_img, self.banana_img, self.cherry_img, self.strawberry_img,self.grape_img,self.orange_img]
        self.choice = random.choice(self.img)


class Snake:
    def __init__(self,screen,mode):
        '''zmienne dla weza'''
        self.mode = mode
        self.screen = screen
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.body_lenght = int(len(self.body)*10)
        self.direction = Vector2(0,0)
        self.new_block = False

    def draw_snake(self):
        '''rysowanie weza'''
        for block in self.body:
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)
            block = pygame.Rect(x_position,y_position,cell_size,cell_size)
            pygame.draw.rect(self.screen,(184,111,122),block)
        pygame.display.flip()

    def move_snake(self):
        '''porusznie cialem weza'''
        if not self.direction == [0,0]:
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]

    def add_block(self):
        '''zwiekszanie weza o jeden blok'''
        self.new_block = True
        self.body_lenght +=10

    def reset(self):
        '''resetowanie weza do  ustawien poczatkowych'''
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

    def move_left(self):
        '''Poruszanie sie w lewo'''
        self.direction = Vector2(-1, 0)

    def move_right(self):
        '''Poruszanie sie w prawo'''
        self.direction = Vector2(1, 0)

    def move_up(self):
        '''Poruszanie sie w gore'''
        self.direction = Vector2(0, -1)

    def move_down(self):
        '''Poruszanie sie w dol'''
        self.direction = Vector2(0, 1)


class Main:
    def __init__(self,mode):
        '''zmienne dla glownego okna gry'''
        pygame.init()
        self.rock_list = []
        for i in range(0, 15):
            x1 = random.randint(0, cell_num - 1)
            y1 = random.randint(0, cell_num - 1)
            self.rock_position = Vector2(x1,y1)
            self.rock_list.append([x1, y1])
        self.mode = mode
        self.screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font(None, 25)
        self.screen_update = pygame.USEREVENT
        pygame.time.set_timer(self.screen_update, 150)
        self.rock_img = pygame.image.load('venv/resources/cobble.png').convert_alpha()
        self.snake = Snake(self.screen,self.mode)
        self.apple = Apple(self.screen)

    def update(self):
        '''update gry'''
        self.snake.move_snake()
        self.check_collsion()
        self.check_fail()

        if self.mode == 0:
            self.level_easy()
        elif self.mode == 1:
            self.level_medium()
        elif self.mode == 2:
            self.level_hard()

    def draw_elem(self):
        '''rysowanie wszystkich elementow'''
        self.apple.draw_Fruit()
        self.snake.draw_snake()
        self.draw_score()
        if self.mode == 2:
            self.draw_rock()

    def rock_collision(self):
        for rock in self.rock_list:
            if rock == self.snake.body[0]:
                print("rock")
                self.game_over()

    def draw_rock(self):
        '''rysowanie przeszkod'''
        for rock in self.rock_list:
            rock = pygame.Rect(rock[0] * cell_size, rock[1] * cell_size, cell_size, cell_size)
            self.screen.blit(self.rock_img, rock)

    def check_collsion(self):
        '''sprawdzanie czy nie zaszla kolicja'''
        if self.apple.position == self.snake.body[0]:
            self.apple.randomize()
            self.apple.change_Fruit()
            self.snake.add_block()
            print("colision")

        for block in self.snake.body[1:]:
            if block == self.apple.position:
                self.apple.randomize()

        for rock in self.rock_list:
            if rock == self.apple.position:
                self.apple.randomize()

    def level_easy(self):
        '''poziom trudnosci latwy: waz wchodza w sciane pojawia sie po drugiej stronie'''
        if not self.snake.direction == [0, 0]:
            x = self.snake.direction.x
            y = self.snake.direction.y
            head_x = self.snake.body[0][0]
            head_y = self.snake.body[0][1]

            if self.mode == 0:
                if head_x >= 20:
                    head_x = 0

                if head_x < 0:
                    head_x = 20

                if head_y >= 20:
                    head_y = 0

                if head_y < 0:
                    head_y = 20
                print(self.snake.body[0])
                self.snake.body[0] = Vector2(head_x, head_y)
                body_copy = self.snake.body[:-1]
                body_copy.insert(0, body_copy[0] + self.snake.direction)

    def level_medium(self):
        '''poziom trudnosci sredni: waz wchodza w sciane umiera'''
        if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
            print("border")
            self.game_over()

    def level_hard(self):
        '''poziom trudnosci latwy: waz wchodza w sciane umiera + dolozone sa przeszkody jesli waz w nie wejdzie umiera'''
        self.level_medium()
        self.rock_collision()

    def check_fail(self):
        '''sprawdza czy waz nie wejdzie w siebie'''
        if not self.snake.direction == [0,0]:
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    print("snake")
                    self.game_over()

    def game_over(self):
        '''przegrana resetuje gre'''
        self.load_to_file()
        print("koniec")
        self.snake.reset()

    def load_to_file(self):
        workbook_name = 'score.xlsx'
        wb = load_workbook(workbook_name)
        page = wb.active
        data = [self.snake.body_lenght]
        page.append(data)
        wb.save(filename=workbook_name)

    def game_over_mes(self):
        '''funkcja wypisania wiadomosci z wynikiem i mozliwosciami gry dalej lub wyjscia'''
        self.screen.fill((196, 180, 77))
        font = pygame.font.SysFont('arial', 30)
        line = font.render(f"Score: {str(len(self.snake.body*10))}",True,(255,255,255))
        self.screen.blit(line,(200,300))
        line2 = font.render(f"To play again press ENTER. To exit press ESCAPE:",True,(255,255,255))
        self.screen.blit(line2, (200, 350))
        pygame.display.flip()

    def draw_score(self):
        '''rysowanie wyniku'''
        score_text = str(len(self.snake.body)*10)
        score_surface = self.game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_num - 60)
        score_y = int(cell_size * cell_num - 40)
        score_rect = score_surface.get_rect(center=(score_x,score_y))
        self.screen.blit(score_surface,score_rect)

    def run(self):
        '''funkcja odpalajaca gre'''
        pause = False
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.screen_update and not pause:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        pause = False
                    if event.key == pygame.K_RETURN:
                        pause = True

                    if not pause:
                        if event.key == pygame.K_UP:
                            if self.snake.direction.y != 1:
                                self.snake.move_up()
                        if event.key == pygame.K_DOWN:
                            if self.snake.direction.y != -1:
                                self.snake.move_down()
                        if event.key == pygame.K_LEFT:
                            if self.snake.direction.x != 1:
                                self.snake.move_left()
                        if event.key == pygame.K_RIGHT:
                            if self.snake.direction.x != -1:
                                self.snake.move_right()

            self.screen.fill((175, 215, 70))
            self.draw_elem()
            pygame.display.update()
            self.clock.tick(60)
