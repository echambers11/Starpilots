import sys
import pygame

from pathlib import Path
import json

from settings import Settings
from title import Title
from button import Button
from status_bar import StatusBar
from counter import Counter
from timer import Timer
from menu import Menu
from starship import Starship
from enemy import Enemy
from asteroid import Asteroid
from stars import Star




class Game:
    def __init__(self):
        # basic
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Starpilots")

        # sounds
        pygame.mixer.init()
        self.boom = pygame.mixer.Sound(r'sounds/boom.mp3')
        self.boom.set_volume(0.15)
        self.laser = pygame.mixer.Sound(r'sounds/laser.mp3')
        self.laser.set_volume(0.15)
        self.asteroid = pygame.mixer.Sound(r'sounds/asteroid.mp3')
        self.asteroid.set_volume(0.3)
        self.music = pygame.mixer.Sound(r'sounds/music.mp3')
        self.music.set_volume(1.0)
        self.music.play(-1)

        # state
        self.game_active = False
        self.menu_active = True 
        self.campaigning = False
        self.campaign = None

        # display
        self._create_stars()
        self._create_menu()
        self._create_info_screens()
        x = self.settings.screen_width // 2
        y = self.settings.screen_height // 2 + 100
        self.menu_button = Button(self, "Menu", (x, y), 150, 50)

        # highscores
        highscore_path = Path(f'highscores.json')
        strfile = highscore_path.read_text()
        self.highscores = json.loads(strfile)
    

    def _init_new_game(self, map):
        self.game_active = True
        self.menu_active = False
        self.start_time = pygame.time.get_ticks()

        # load map
        map_path = Path(f'maps/{map}.json')
        strfile = map_path.read_text()
        self.map = json.loads(strfile)
        self.map_name = map

        # entities
        self.entities = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # bullets
        self.bullets = pygame.sprite.Group()

        # asteroids
        for asteroid in self.map['asteroids']:
            self.entities.add(Asteroid(self, asteroid['type'], asteroid['pos'], asteroid['angle'],
                                       asteroid['dir'], asteroid['velo'], asteroid['spin'], asteroid['hp']))
        
        # p1
        self.p1_turn = 0
        self.p1_accel = 0
        self.p1 = Starship(self, self.map['p1']['type'], self.map['p1']['pos'], self.map['p1']['angle'], self.map['p1']['dir'],
                           self.map['p1']['velo'], self.map['p1']['spin'], self.map['p1']['hp'], True)
        self.entities.add(self.p1)

        self.health_bar = StatusBar(self, "Health", (self.settings.screen_width - 100, 35), 150, 20, self.p1.hp, self.p1.hp)

        # enemies
        for enemy in self.map['enemies']:
            enemy = Enemy(self, enemy['type'], enemy['pos'], enemy['angle'], enemy['dir'],
                                enemy['velo'], enemy['spin'], enemy['hp'])
            self.entities.add(enemy)
            self.enemies.add(enemy)

        # timer + score
        self.timer = Timer(self, (50, 35), self.start_time)
        self.score_counter = Counter(self, "Score", (70, 70), 0)
        name = map.split('/')[0]
        if name not in self.highscores:
            self.highscores[name] = 0
        self.highscore_counter = Counter(self, "Highscore", (90, 105), self.highscores[name])
    
    '''create entities'''
    def _create_stars(self):
        self.stars = pygame.sprite.Group()
        for x in range(0, self.settings.star_count):
            self.stars.add(Star(self))

    def _create_menu(self):
        # get list of maps
        map_list_path = Path("maps")
        maps = []
        self.maps_folder = []
        for file in map_list_path.iterdir():
            map = file.stem
            maps.append(map)
            self.maps_folder.append(str(file))
        maps.sort()

        # create buttons
        i = 0
        self.map_buttons = []
        for map in maps:
            x = self.settings.screen_width // 2
            y = 290 + i * 60
            button = Button(self, map, (x, y), 200, 50)
            self.map_buttons.append(button)
            i += 1

        # create title
        x = self.settings.screen_width // 2
        y = 130
        self.title = Title(self, "Starpilots", (x, y))

        # create background
        self.background_img = pygame.image.load(f'images/starship_background.png')
        self.background_img = pygame.transform.scale(self.background_img, (810, 830))
        self.background_rect = self.background_img.get_rect()
        self.background_rect.center = (self.settings.screen_width / 2, self.settings.screen_height / 2 + 110)

    def _create_info_screens(self):
        controls_button = Button(self, "Controls", (self.settings.screen_width - 130, self.settings.screen_height - 45), 220, 50)
        tips_button = Button(self, "How To Play", (self.settings.screen_width - 130, self.settings.screen_height - 110), 220, 50)

        self.controls_screen = Menu(self, "Controls", controls_button, self.settings.controls_info)
        self.tips_screen = Menu(self, "How To Play", tips_button, self.settings.tips_info)

    '''main loop'''
    def run(self):
        while True:
            self._update()
            self._check_events()
            if self.game_active:
                self._accl_entities()
                if not self.p1.alive():
                    self.lose()
                elif not self.enemies.sprites():
                    self.win()
            self.clock.tick(60)


    """draw screen"""
    def _update(self):
        # draw background
        self.screen.fill((0, 0, 0))
        for star in self.stars.sprites():
            star.draw_star()

        # draw entities
        if self.game_active:
            self.p1.attack_timer += 3
            self._draw_entities()
            # draw stats
            self.health_bar.draw()
            if self.campaigning:
                self.lvl_counter.draw()
            self.timer.draw(pygame.time.get_ticks())
            self.score_counter.change_stat(self._get_score())
            self.score_counter.draw()
            self.highscore_counter.draw()
            

        # draw menu
        elif self.menu_active:
            self._draw_menu()

        elif self.controls_screen.active:
            self.controls_screen.draw()
        elif self.tips_screen.active:
            self.tips_screen.draw()
        
        # draw menu button
        if not self.menu_active and not self.game_active:
            self.menu_button.draw_button()
            if not self.controls_screen.active and not self.tips_screen.active:
                self.end_txt.draw()
                # draw stats
                self.health_bar.draw()
                if self.campaigning:
                    self.lvl_counter.draw()
                self.timer.draw()
                self.score_counter.draw()
                self.highscore_counter.draw()

        pygame.display.flip()

    def _get_score(self):
        score = self.settings.pts - (self.settings.secs + self.timer.secs)*2
        if score < 0:
            return 0
        else:
            return score

    def _draw_entities(self):
        for entity in self.entities:
            if entity.live:
                entity.update()
            entity.draw()
        for bullet in self.bullets:
            bullet.update(self.entities)
            bullet.draw_bullet()

    def _draw_menu(self):
        self.screen.blit(self.background_img, self.background_rect)
        self.title.draw()
        for button in self.map_buttons:
            button.draw_button()
        self.controls_screen.button.draw_button()
        self.tips_screen.button.draw_button()

    
    """events"""
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.end_game()
                self.menu_active = True
            
            # check for in game events
            if self.game_active and self.p1.live:
                if event.type == pygame.KEYDOWN:
                    self._check_keydown(event)
                if event.type == pygame.KEYUP:
                    self._check_keyup(event)

            # check for menu + end events
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._check_mousedown()

    def _check_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.p1_turn = self.settings.ship_turn
        elif event.key == pygame.K_RIGHT:
            self.p1_turn = -self.settings.ship_turn
        elif event.key == pygame.K_UP:
            self.p1.accl = True
            self.p1_accel = self.settings.ship_accel
        elif event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
            self.p1.shoot()
    
    def _check_keyup(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.p1_turn = 0
        elif event.key == pygame.K_UP:
            self.p1.accl = False
            self.p1_accel = 0
    
    def _check_mousedown(self):
        pos = pygame.mouse.get_pos()

        if self.menu_active:
            for button in self.map_buttons:
                if button.is_pressed(pos):
                    # if file do map
                    if f"maps/{button.txt}.json" in self.maps_folder:
                        self._init_new_game(button.txt)
                    # if folder do campaign
                    else:
                        # get maps in campaign
                        campaign_path = Path(f"maps/{button.txt}")
                        self.campaign_folder = []
                        for file in campaign_path.iterdir():
                            map = file.stem
                            self.campaign_folder.append(map)
                        self.campaign_folder.sort()

                        # run campaign
                        self.campaigning = True
                        self.campaign = button.txt
                        self.lvl = 0
                        self.lvl_counter = Counter(self, "level", (self.settings.screen_width - 65, 70), self.lvl+1)
                        self._init_new_game(f"{self.campaign}/{self.campaign_folder[self.lvl]}")
            # controls button
            if self.controls_screen.button.is_pressed(pos):
                self.menu_active = False
                self.controls_screen.active = True
            # tips button
            if self.tips_screen.button.is_pressed(pos):
                self.menu_active = False
                self.tips_screen.active = True
                        
        elif not self.game_active:
            if self.menu_button.is_pressed(pos):
                self.menu_active = True
                self.controls_screen.active = False
                self.tips_screen.active = False
                self.settings.pts = 0
    
    '''move player'''
    def _accl_entities(self):
        self.p1.turn(self.p1_turn)
        self.p1.acclerate(self.p1_accel)
        if self.p1.hp != self.health_bar.stat:
            self.health_bar.change_stat(self.p1.hp)


    '''end game'''
    def win(self):
        # next lvl if in campaign
        if self.campaigning:
            self.lvl += 1
            self.lvl_counter.change_stat(self.lvl+1)
            if self.lvl < len(self.campaign_folder):
                if self.health_bar.stat < 0:
                    self.health_bar.stat = 0
                self.settings.hp += self.health_bar.stat
                self.settings.secs += self.timer.secs
                self._init_new_game(f"{self.campaign}/{self.campaign_folder[self.lvl]}")
                return None

        # otherwise create win screen
        self.campaigning = False
        self.campaign = None

        x = self.settings.screen_width // 2
        y = self.settings.screen_height // 2
        new_high = self._update_highscore()
        if new_high:
            self.end_txt = Title(self, "New Highscore!", (x, y))
        else:
            self.end_txt = Title(self, "You Win!", (x, y))
        self.end_game()
    
    def lose(self):
        # create lose screen
        self.campaigning = False
        self.campaign = None

        x = self.settings.screen_width // 2
        y = self.settings.screen_height // 2
        self.end_txt = Title(self, "You Lose!", (x, y))
        self.end_game()

    def end_game(self):
        self.settings.secs = 0
        self.game_active = False
        self.menu_active = False
        self.entities.empty()
        self.enemies.empty()
        self.bullets.empty()
    
    def _update_highscore(self):
        score = self._get_score()
        self.score_counter.change_stat(score)
        if score > self.highscore_counter.stat:
            self.highscore_counter.change_stat(score)
            name = self.map_name.split('/')[0]
            highscore_path = Path(f'highscores.json')
            self.highscores[name] = score
            strfile = json.dumps(self.highscores, indent=4)
            highscore_path.write_text(strfile)
            return True
        return False




if __name__ == '__main__':
    game = Game()
    game.run()


'''
Things to add:
- highscores when win
- types of enemies/bullets
'''