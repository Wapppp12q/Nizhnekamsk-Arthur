import os
import sys
import pygame
import pygame_gui
import random


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    return image


class Sprite(pygame.sprite.Sprite):
     def __init__(self, group):
         super().__init__(group)


class Player(Sprite):
    player_image = load_image('data/people.png')

    def __init__(self, group):
        Sprite.__init__(self, group)
        self.game_over_flag = True
        self.speed = 120
        self.height_jump = 80
        self.clock = pygame.time.Clock()
        self.draw_music = False

        self.people = Player.player_image
        self.rect = self.people.get_rect()
        self.rect.x = 250 - self.people.get_width() / 2
        self.rect.y = 1000 - self.people.get_height()

    def jump(self, image, draw_music=False):
        self.draw_music = draw_music
        if self.rect.y < 0:
            self.game_over_flag = True

    def left(self, turbo=False, draw_music=False):
        image = pygame.transform.flip(self.people, True, False)
        if turbo:
            self.rect.x -= self.speed / self.fps
        else:
            self.rect.x -= self.speed / 2 / self.fps
        if self.rect.x < 0 - self.people.get_width():
            self.rect.x = 500 - self.people.get_width()
        self.jump(image, draw_music)

    def right(self, draw_music):
        self.rect.x += self.speed / self.fps
        if self.rect.x > 500:
            self.rect.x = 0
        self.jump(self.people, draw_music)


class Platforms(Sprite):
    platform = load_image('data/platform.png')

    def __init__(self, group):
        Sprite.__init__(self, group)
        self.platform_im = Platforms.platform
        self.begin_platfoms_im = pygame.transform.scale(self.platform_im, (490, 20))
        self.begin_platfoms_im.set_colorkey('white')
        self.begin_platform_rect = self.begin_platfoms_im.get_rect()
        self.begin_platform_rect.x = 5
        self.begin_platform_rect.y = 980
        self.platforms()

    def platforms(self):
        pass


class Point:
    def __init__(self):
        self.point = 0

    def sum_point(self, max_height):
        self.point += max_height

    def draw_point_val(self):
        text_point = self.font.render(str(self.point), True, '#808080')
        self.screen.blit(text_point, (10, 10))


class Music:
    def __init__(self):
        self.val = 1

    def music(self, file):
        landing = pygame.mixer.Sound(file)
        landing.set_volume(self.val)
        if file == "data/landing.mp3":
            landing.play(maxtime=1000)
        else:
            landing.play()

    def difference(self):
        if self.val >= 0.1:
            self.val -= 0.1
        self.music("data/landing.mp3")

    def sum_val(self):
        if self.val < 1:
            self.val += 0.1
        self.music("data/landing.mp3")

    def draw_procents(self):
        val = int(self.val * 100)
        text_val = self.font.render(str(val) + '%', True, '#808080')
        self.screen.blit(text_val, (490 - text_val.get_width(), 10))

    def game_over_music(self):
        self.music('data/game_over.mp3')


class Play(Music, Platforms, Point, Player):
    def __init__(self, screen, people_group, platform_group):
        Music.__init__(self)
        Point.__init__(self)
        Player.__init__(self, people_group)
        Platforms.__init__(self, platform_group)
        self.w = 500
        self.h = 1000
        self.screen = screen
        self.fps = 60
        self.font = pygame.font.Font(None, 50)
        self.fon_im = load_image("data/fon.png")
        self.fon_im = pygame.transform.scale(self.fon_im, (self.w, self.h))
        self.fon_rect = self.fon_im.get_rect()
        self.fon_rect.x = 0
        self.fon_rect.y = 0

        self.game_over_im = pygame.image.load('data/game_over.png')
        self.game_over_im = pygame.transform.scale(self.game_over_im, (500, 200))
        self.rect_game_over = self.game_over_im.get_rect(center=(0 - self.game_over_im.get_width() / 2,
                                                                 500))
        self.game_over()
        self.image

    def draw(self):
        self.screen.blit(self.fon_im, self.fon_rect)
        self.draw_point_val()
        if self.draw_music:
            self.draw_procents()
        if self.game_over_flag:
            if self.rect_game_over.x < 0:
                self.rect_game_over.x += 200 / 60
                self.screen.blit(self.game_over_im, self.rect_game_over)
            else:
                self.game_over_flag = False
                end_screen()
        pygame.display.flip()

    def check_game_over(self):
        if self.game_over_flag:
            self.game_over()

    def game_over(self):
        self.game_over_music()


def end_screen():
    manager = pygame_gui.UIManager((500, 1000))
    switch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 650), (300, 50)),
                                          text='Начать заново',
                                          manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch:
                        start_screen()


def start_screen():
    pygame.init()
    pygame.mixer.init()
    w, h = 500, 1000
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption('Jumper')

    begin_im = load_image('data/begin.png')
    begin_im = pygame.transform.scale(begin_im, (500, 1000))
    begin_rect = begin_im.get_rect()
    begin_rect.x = 0
    begin_rect.y = 0
    screen.blit(begin_im, begin_rect)

    arrow = load_image('data/arrow.png')
    arrow.set_colorkey('white')
    arrow_down = pygame.transform.scale(arrow, (100, 100))
    arrow_down = pygame.transform.rotate(arrow_down, 90)
    down_rect = arrow.get_rect()
    down_rect.x = 200
    down_rect.y = 700
    screen.blit(arrow_down, down_rect)

    arrow_up = pygame.transform.scale(arrow, (100, 100))
    arrow_up = pygame.transform.rotate(arrow_up, 270)
    up_rect = arrow.get_rect()
    up_rect.x = 200
    up_rect.y = 600
    screen.blit(arrow_up, up_rect)

    arrow_right = pygame.transform.scale(arrow, (100, 100))
    arrow_right = pygame.transform.rotate(arrow_right, 180)
    rect_right = arrow.get_rect()
    rect_right.x = 240
    rect_right.y = 150
    screen.blit(arrow_right, rect_right)

    arrow_left = pygame.transform.scale(arrow, (100, 100))
    rect_left = arrow.get_rect()
    rect_left.x = 140
    rect_left.y = 150
    screen.blit(arrow_left, rect_left)

    font = pygame.font.Font(None, 35)

    text_left_right = font.render('Нажимать, для движения в стороны', True, 'black')
    text_up_down = font.render('Нажимать, для изменения звука', True, 'black')

    screen.blit(text_left_right, (30, 300))
    screen.blit(text_up_down, (50, 850))

    manager = pygame_gui.UIManager((500, 1000))
    switch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 450), (300, 100)),
                                          text='Начать игру',
                                          manager=manager)
    pygame.display.flip()

    fps = 60
    clock = pygame.time.Clock()
    people_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()

    left = True
    left_turbo = False
    right = False
    draw_music = False
    main_motion = False
    music_sum_val = False
    music_difference = False
    while True:
        time_delta = clock.tick(fps) / 1000.0
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch:
                        manager = 0
                        screen = pygame.display.set_mode((w, h))
                        pygame.display.set_caption('Jumper')

                        play = Play(screen, people_group, platform_group)
                        main_motion = True
            if main_motion:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        right = True
                        left = False
                        left_turbo = False
                    if event.key == pygame.K_LEFT:
                        right = False
                        left = False
                        left_turbo = True
                    if event.key == pygame.K_UP:
                        music_sum_val = True
                        draw_music = True
                    if event.key == pygame.K_DOWN:
                        music_difference = True
                        draw_music = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        music_difference = False
                        time_click = 0
                    if event.key == pygame.K_UP:
                        music_sum_val = False
                        time_click = 0
                    if event.key == pygame.K_RIGHT:
                        right = False
                        left_turbo = False
                        left = True
                    if event.key == pygame.K_LEFT:
                        right = False
                        left = True
                        left_turbo = False
            if manager != 0:
                manager.process_events(event)
                manager.update(time_delta)
                manager.draw_ui(screen)
        if manager == 0:
            if left:
                play.left(draw_music=draw_music)
            if left_turbo:
                play.left(True, draw_music=draw_music)
            if right:
                play.right(draw_music=draw_music)
            if draw_music:
                time_click += 1/fps
                if time_click > 2.5:
                    draw_music = False
            if music_sum_val:
                play.sum_val()
            if music_difference:
                play.difference()
            play
            play.check_game_over()
            platform_group.draw(screen)
            people_group.draw(screen)
        pygame.display.flip()


start_screen()