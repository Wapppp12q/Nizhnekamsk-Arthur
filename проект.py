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


class Font:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)


class Player(pygame.sprite.Sprite):
    player_image = load_image('venv/data/people.png')
    player_image = pygame.transform.scale(player_image, (100, 110))
    player_image.set_colorkey('white')

    def __init__(self, screen, people_group, platform_group, earth_group):
        pygame.sprite.Sprite.__init__(self)
        self.people_group = people_group
        self.platform_group = platform_group
        self.earth_group = earth_group
        self.screen = screen
        self.fps = 60
        self.game_over_flag = True
        self.speed = 500
        self.height_jump = 250
        self.clock = pygame.time.Clock()
        self.vy = 40
        self.max_height = 0
        self.point = Point(self.screen)
        self.play = Play(self.screen)
        self.music = Music(self.screen)

        self.image = Player.player_image
        self.rect = self.image.get_rect()
        self.rect.x = 250 - self.image.get_width() / 2
        self.rect.y = 980 - self.image.get_height()

    def update(self, left, turbo, right, *args):
        if self.rect.y > self.max_height:
            self.max_height = self.rect.y
        if turbo:
            self.image = pygame.transform.flip(Player.player_image, True, False)
            self.rect.x -= self.speed / self.fps
        if left:
            self.image = pygame.transform.flip(Player.player_image, True, False)
            self.rect.x -= (self.speed - 300) / self.fps / 2
        if right:
            self.image = Player.player_image
            self.rect.x += self.speed / self.fps
        if self.rect.x < 0 - self.image.get_width():
            self.rect.x = 500
        if self.rect.x > 500:
            self.rect.x = 0 - self.image.get_width()
        if self.rect.y > 1000:
            self.play.check_game_over()
        self.rect.y -= self.vy
        if 40 >= self.vy and not (pygame.sprite.groupcollide(self.people_group, self.earth_group, False, False)
                                  or pygame.sprite.groupcollide(self.people_group, self.platform_group, False, False)):
            self.vy -= 4
        elif (pygame.sprite.groupcollide(self.people_group, self.earth_group, False, False)
              or pygame.sprite.groupcollide(self.people_group, self.platform_group, False, False)):
            self.vy = 40
            self.music.landing_mp()
        else:
            self.vy = 40
        self.point.sum_point(self.max_height)


class Earth(pygame.sprite.Sprite):
    earth_im = load_image('venv/data/earth.jfif')
    earth_im.set_colorkey('white')
    earth_im = pygame.transform.scale(earth_im, (560, 100))

    def __init__(self):
        super().__init__()
        self.image = Earth.earth_im
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = 1030 - self.image.get_height()


class ReliablePlatform(pygame.sprite.Sprite):
    platform = load_image('venv/data/platform.png')

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ReliablePlatform.platform
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(x - 10, x + 10)
        self.rect.y = y * 150

    def update(self):
        pass


class Platforms(pygame.sprite.Sprite):
    platform = load_image('venv/data/platform.png')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Platforms.platform
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 500 - self.image.get_width())
        self.rect.y = random.randrange(0, 900)

    def update(self):
        pass


class Point(Font):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.point = 0

    def sum_point(self, max_height):
        self.point += max_height

    def draw_point_val(self):
        text_point = self.font.render(str(self.point), True, '#808080')
        self.screen.blit(text_point, (10, 10))


class Music(Font):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.val = 1

    def music(self, file):
        landing = pygame.mixer.Sound(file)
        landing.set_volume(self.val)
        if file == "venv/data/landing.mp3":
            landing.play(maxtime=1000)
        else:
            landing.play()

    def difference(self):
        if self.val >= 0.1:
            self.val -= 0.1
        self.music("venv/data/landing.mp3")

    def sum_val(self):
        if self.val < 1:
            self.val += 0.1
        self.music("venv/data/landing.mp3")

    def draw_procents(self):
        val = int(self.val * 100)
        text_val = self.font.render(str(val) + '%', True, '#808080')
        self.screen.blit(text_val, (490 - text_val.get_width(), 10))

    def landing_mp(self):
        self.music("venv/data/landing.mp3")

    def game_over_music(self):
        self.music('venv/data/game_over.mp3')


class Play(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.w = 500
        self.h = 1000
        self.speed = 200
        self.fps = 60
        self.screen = screen
        self.fps = 60
        self.font = pygame.font.Font(None, 50)
        self.clock = pygame.time.Clock()

        self.game_over_flag = False
        self.game_over_im = pygame.image.load('venv/data/game_over.png')
        self.game_over_im.set_colorkey('white')
        self.game_over_im = pygame.transform.scale(self.game_over_im, (500, 300))
        self.rect_game_over = self.game_over_im.get_rect(center=(0 - self.game_over_im.get_width() / 2,
                                                                 500))

    def draw(self):
        if self.game_over_flag:
            while self.rect_game_over.x < 0:
                self.clock.tick(self.fps)
                self.rect_game_over.x += self.speed / self.fps
                self.screen.blit(self.game_over_im, self.rect_game_over)
                pygame.display.flip()
            else:
                self.game_over_flag = False
                end_screen()
        pygame.display.flip()

    def check_game_over(self):
        self.game_over_flag = True
        self.game_over()
        self.draw()

    def game_over(self):
        Music(self.screen).game_over_music()


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

    begin_im = load_image('venv/data/begin.png')
    begin_im = pygame.transform.scale(begin_im, (500, 1000))
    begin_rect = begin_im.get_rect()
    begin_rect.x = 0
    begin_rect.y = 0
    screen.blit(begin_im, begin_rect)

    arrow = load_image('venv/data/arrow.png')
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

    fon_im = load_image("venv/data/fon.png")
    fon_im = pygame.transform.scale(fon_im, (w, h))
    fon_rect = fon_im.get_rect()
    fon_rect.x = 0
    fon_rect.y = 0

    count_platform = 0
    fps = 60
    clock = pygame.time.Clock()
    earth_group = pygame.sprite.Group()
    people_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()

    time_click = 0
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
####################################################################################################################
                        music = Music(screen)
                        point = Point(screen)
                        play = Play(screen)
                        for i in range(5):
                            platform_group.add(ReliablePlatform(random.randrange(0, 500-200), i))
                        for i in range(count_platform):
                            platform_group.add(Platforms())
                        #earth_group.add(Earth())
                        people_group.add(Player(screen, people_group, platform_group, earth_group))
                        player = Player(screen, people_group, platform_group, earth_group)
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
                        time_click = 0
                    if event.key == pygame.K_DOWN:
                        music_difference = True
                        draw_music = True
                        time_click = 0
                if event.type == pygame.KEYUP:
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
        if main_motion:
            play.draw()
            screen.blit(fon_im, fon_rect)
            earth_group.draw(screen)
            platform_group.draw(screen)
            people_group.draw(screen)
            point.draw_point_val()
            pygame.display.flip()
            if draw_music:
                time_click += 1/fps
                if time_click > 2.5:
                    draw_music = False
            if music_sum_val:
                music.sum_val()
                music_sum_val = False
            if music_difference:
                music.difference()
                music_difference = False
            if draw_music:
                music.draw_procents()
            people_group.update(left, left_turbo, right)
            platform_group.update()
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
