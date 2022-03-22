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


class Point(Font):
    def __init__(self, screen):
        Font.__init__(self)
        self.screen = screen
        self.point = 0

    def sum_point(self, m_height):
        self.point = m_height
        self.draw_point_val()

    def draw_point_val(self):
        text_point = self.font.render(str(self.point), True, '#808080')
        self.screen.blit(text_point, (10, 10))


class Music(Font):
    def __init__(self, screen):
        Font.__init__(self)
        self.screen = screen

    def play_music(self, file):
        landing = pygame.mixer.Sound(file)
        landing.set_volume(val)
        if file == "venv/data/landing.mp3":
            landing.play(maxtime=1000)
        else:
            landing.play()

    def draw_proc(self):
        text_val = int(val * 100)
        text_val = self.font.render(str(text_val) + '%', True, '#808080')
        self.screen.blit(text_val, (490 - text_val.get_width(), 10))

    def landing_mp(self):
        self.play_music("venv/data/landing.mp3")

    def game_over_music(self):
        self.play_music('venv/data/game_over.mp3')


class Player(Music, Point, pygame.sprite.Sprite):
    player_image = load_image('venv/data/people.png')
    player_image = pygame.transform.scale(player_image, (60, 70))
    player_image.set_colorkey('white')

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        Music.__init__(self, screen)
        Point.__init__(self, screen)
        self.play = Play(screen)
        self.max_height = 0

        self.screen = screen
        self.fps = 60
        self.speed = 500
        self.clock = pygame.time.Clock()
        self.vy = 28
        self.collide_flag = True
        self.camera = False

        self.image = Player.player_image
        self.rect = self.image.get_rect()
        self.rect.x = 250 - self.image.get_width() / 2
        for earth in earth_group:
            self.rect.y = earth.rect[1] - self.image.get_height()
            self.height_zero = earth.rect[1] - self.image.get_height()

    def update(self, left, turbo, right):
        self.sum_point(self.max_height)
        self.collide_flag = True
        self.camera = False
        if self.rect.y >= 500 and self.rect.y - self.vy < 500:
            self.rect.y = 500
            self.camera = True
            group_changes(self.vy - (self.rect.y - 500))
            self.max_height += self.vy
        if not self.camera:
            if self.height_zero - self.rect.y > self.max_height * 100:
                self.max_height = int((self.height_zero - self.rect.y) / 100)
        if not self.camera:
            self.rect.y -= self.vy

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

        for earth in earth_group:
            if ((pygame.sprite.groupcollide(people_group, earth_group, False, False) and
                 self.vy <= 0 and
                 self.rect.y + self.image.get_height() <= earth.rect[1] + earth.rect[3] / 2) or
                    (
                            self.rect.y + self.image.get_height() < earth.rect[1] < self.rect.y - self.vy
                    )):
                self.vy = 28
                self.landing_mp()
                self.collide_flag = False
                break
        for platform in platform_group:
            if ((pygame.sprite.groupcollide(people_group, platform_group, False, False) and
                    self.vy <= 0 and
                    self.rect.y + self.image.get_height() <= platform.rect[1] + platform.rect[3] / 2 ) or
                    (
                     self.rect.y + self.image.get_height() < platform.rect[1] < self.rect.y - self.vy
                    )):
                self.vy = 28
                self.landing_mp()
                self.collide_flag = False
                break
        for relib in reliable_group:
            if ((pygame.sprite.groupcollide(people_group, reliable_group, False, False) and
                    self.vy <= 0 and
                    self.rect.y + self.image.get_height() <= relib.rect[1] + relib.rect[3] / 2) or
                    (
                     self.rect.y + self.image.get_height() < relib.rect[1] < self.rect.y - self.vy
                    )):
                self.vy = 28
                self.landing_mp()
                self.collide_flag = False
                break
        if self.collide_flag:
            self.vy -= 2


class Earth(pygame.sprite.Sprite):
    earth_im = load_image('venv/data/earth.jfif')
    earth_im.set_colorkey('white')
    earth_im = pygame.transform.scale(earth_im, (560, 100))

    def __init__(self):
        super().__init__()
        self.image = Earth.earth_im
        self.rect = self.image.get_rect()
        self.rect.x = -31
        self.rect.y = 1030 - self.image.get_height()


class ReliablePlatform(pygame.sprite.Sprite):
    platform = load_image('venv/data/platform.png')
    platform.set_colorkey('white')
    platform = pygame.transform.scale(platform, (65, 17))

    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ReliablePlatform.platform
        self.rect = self.image.get_rect()
        pos_x = random.randrange(x_pos_relib - 100, x_pos_relib + 100)
        if pos_x < 0:
            self.rect.x = 0 - pos_x
        elif pos_x > 500:
            self.rect.x = 500 - self.image.get_width()
        else:
            self.rect.x = pos_x
        if y < 100:
            self.rect.y = y * 190
        else:
            self.rect.y = y


class Platforms(pygame.sprite.Sprite):
    platform = load_image('venv/data/platform.png')
    platform.set_colorkey('white')
    platform = pygame.transform.scale(platform, (65, 17))

    def __init__(self, first=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = Platforms.platform
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 500 - self.image.get_width())
        if first:
            self.rect.y = random.randrange(-1000, 900)
        else:
            self.rect.y = random.randrange(-1000, 0 - self.image.get_height())


class Play(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 200
        self.screen = screen
        self.fps = 60
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
                self.rect_game_over.x += self.speed * 1.95 / self.fps
                self.screen.blit(self.game_over_im, self.rect_game_over)
                pygame.display.flip()
            end_screen(self.screen)

    def check_game_over(self):
        self.game_over_flag = True
        self.game_over()
        self.draw()

    def game_over(self):
        Music(self.screen).game_over_music()


def group_changes(height):
    relib_empty = []
    platform_empty = []
    for earth in earth_group:
        earth.rect[1] += height
        if earth.rect[1] > 1000:
            earth_group.remove(earth)
    for platform in platform_group:
        platform.rect[1] += height
        platform_empty.append(platform.rect[1])
        if platform.rect[1] > 1000:
            platform_group.remove(platform)
    min_rect_plat = min(platform_empty)
    if min_rect_plat >= 0:
        for i in range(8):
            platform_group.add(Platforms(False))
    for reliable in reliable_group:
        reliable.rect[1] += height
        if reliable.rect[1] > 1000:
            reliable_group.remove(reliable)
            if len(reliable_group) == 4:
                for reliable2 in reliable_group:
                    relib_empty.append(reliable2.rect[1])
                min_rect_relib = min(relib_empty)
                if min_rect_relib >= 0:
                    reliable_group.add(ReliablePlatform(min_rect_relib - 190))


def end_screen(screen):
    fps = 60
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((500, 1000))
    switch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 650), (300, 50)),
                                          text='Начать заново',
                                          manager=manager)
    pygame.display.flip()

    while True:
        time_delta = clock.tick(fps) / 1000
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch:
                        manager = 0
                        earth_group.empty()
                        people_group.empty()
                        platform_group.empty()
                        reliable_group.empty()
                        start_screen()
            manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(screen)
            pygame.display.flip()


def start_screen():
    global x_pos_relib
    global count_reliable_platform
    global earth_group
    global platform_group
    global people_group
    global reliable_group
    global val
    global pathh
    global count_platform

    pygame.init()
    pygame.mixer.init()
    w, h = 500, 1000
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption('Jumper')

    begin_im = load_image(pathh + 'begin.png')
    begin_im = pygame.transform.scale(begin_im, (500, 1000))
    begin_rect = begin_im.get_rect()
    begin_rect.x = 0
    begin_rect.y = 0
    screen.blit(begin_im, begin_rect)

    arrow = load_image(pathh + 'arrow.png')
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

    text_left_right = font.render('Нажимать для движения в стороны', True, 'black')
    text_up_down = font.render('Нажимать для изменения звука', True, 'black')
    text_space = font.render('Пробел или левой клавишей', True, 'black')
    text_space2 = font.render('Нажимать для паузы', True, 'black')

    screen.blit(text_left_right, (30, 300))
    screen.blit(text_up_down, (50, 850))
    screen.blit(text_space, (90, 350))
    screen.blit(text_space2, (130, 380))

    manager = pygame_gui.UIManager((500, 1000))
    switch = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 450), (300, 100)),
                                          text='Начать игру',
                                          manager=manager)
    pygame.display.flip()

    fon_im = load_image(pathh + "fon.png")
    fon_im = pygame.transform.scale(fon_im, (w, h))
    fon_rect = fon_im.get_rect()
    fon_rect.x = 0
    fon_rect.y = 0

    fps = 60
    clock = pygame.time.Clock()

    time_click = 0
    pause = False
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
                        #########################################################
                        play = Play(screen)
                        for y in range(-1, count_reliable_platform):
                            reliable_group.add(ReliablePlatform(y))
                        for count_rel in range(count_platform):
                            platform_group.add(Platforms())
                        earth_group.add(Earth())
                        people_group.add(Player(screen))
                        player = Player(screen)
                        main_motion = True
            if main_motion:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not pause:
                        pause = True
                    else:
                        pause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not pause:
                            pause = True
                        else:
                            pause = False
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
            if not pause:
                screen.blit(fon_im, fon_rect)
                earth_group.draw(screen)
                platform_group.draw(screen)
                reliable_group.draw(screen)
                people_group.draw(screen)
                if draw_music:
                    time_click += 1 / fps
                    if time_click > 2.5:
                        draw_music = False
                if music_sum_val:
                    if val < 1:
                        val = round(val + 0.1, 1)
                    music_sum_val = False
                if music_difference:
                    if val > 0:
                        val = round(val - 0.1, 1)
                    music_difference = False
                if draw_music:
                    player.draw_proc()
                pygame.display.flip()

                reliable_group.update()
                people_group.update(left, left_turbo, right)
                platform_group.update()
                pygame.display.flip()
            else:
                pygame.draw.polygon(screen, 'gray', ((230, 480), (270, 500), (230, 520)))
        pygame.display.flip()


if __name__ == '__main__':
    earth_group = pygame.sprite.Group()
    people_group = pygame.sprite.Group()
    platform_group = pygame.sprite.Group()
    reliable_group = pygame.sprite.Group()
    count_reliable_platform = 5
    count_platform = 16
    x_pos_relib = random.randrange(0, 500)
    val = 1
    pathh = 'venv/data/'
    start_screen()
