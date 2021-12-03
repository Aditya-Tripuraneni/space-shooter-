"""Author: Aditya Neel Tripuraneni
   Date: 09/19/21
   Finish Date: 11/06/21
   Worked on approximately once a week
   Program Description: Play as a spaceship and shoot the enemy square.
"""
import pygame

pygame.init()
WIDTH, HEIGHT = 750, 750
MAX_COOL_DOWN = 15

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square fighter")
run = True

# COLOURS
PINK = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (32, 87, 110)
PURPLE = (221, 160, 221)
FUCHSIA = (255, 0, 255)
NAVYBLUE = (0, 0, 128)

# IMAGES
background = pygame.image.load("Images/assets/background.png")
spaceship_player_one = pygame.image.load("Images/assets/pixel_ship_yellow.png")
spaceship_player_one = pygame.transform.rotate(spaceship_player_one, 270)

spaceship_player_two = pygame.image.load("Images/assets/pixel_ship_yellow.png")
spaceship_player_two = pygame.transform.rotate(spaceship_player_two, 90)

# MUSIC
pygame.mixer.music.load("Images/assets/backgroundMusic.mp3")
pygame.mixer.music.play(-1)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
player_one_text = myfont.render('Player 1', True, PURPLE)
player_two_text = myfont.render('Player 2 ', True, YELLOW)

# SFX
laser_sfx = pygame.mixer.Sound("Images/assets/sf_laser_15.wav")
hit_sfx = pygame.mixer.Sound("Images/assets/hitSFX.wav")


class Player:
    def __init__(self, x, y, width, height, colour, current_cooldown=0, jump_count=10, velocity=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.current_cool_down = current_cooldown
        self.jump_count = jump_count
        self.velocity = float(velocity)
        self.current_health = 100
        self.game_over = False
        self.hitbox = (self.x - 5, self.y - 5, 110, 100)

    def draw_character(self, win):
        self.hitbox = (self.x - 5, self.y - 5, 90, 100)
        win.blit(spaceship_player_one, (player_one.x + 5, player_one.y))
        win.blit(spaceship_player_two, (player_two.x - 10, player_two.y))

    def draw_health_bar(self, win, colour, x, y, width, height):
        pygame.draw.rect(win, colour, (x, y, width, height))  # Red health bar
        self.green_health = pygame.draw.rect(win, GREEN, (x, y, self.current_health, height))

    def can_shoot(self):
        if self.current_cool_down > MAX_COOL_DOWN:
            self.current_cool_down = 0
            return True  # allows shooting
        return False  # no shooting


def detect_collision(green_bullets, pink_bullets):
    # green bullets
    for green_bullet in green_bullets:
        green_bullet_collide_target = pygame.Rect.colliderect(green_bullet.bullet, player_two.hitbox)
        if green_bullet_collide_target:
            player_two.current_health -= 10
            green_bullets.remove(green_bullet)
            hit_sfx.play()

    for pink_bullet in pink_bullets:
        pink_bullet_collide_target = pygame.Rect.colliderect(pink_bullet.bullet, player_one.hitbox)
        if pink_bullet_collide_target:
            player_one.current_health -= 10
            pink_bullets.remove(pink_bullet)
            hit_sfx.play()


class Bullet:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.velocity = 8

    def draw(self, window):
        self.bullet = pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))

    def draw_special_attack(self, window):
        self.laser = pygame.draw.rect(window, self.colour, (self.x , self.y, self.width, self.height))


def handle_bullets():
    for bullet in bullets_one:
        if 750 > bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets_one.pop(bullets_one.index(bullet))

    for bullet2 in bullets_two:
        if 750 > bullet2.x > 0:
            bullet2.x -= bullet2.velocity
        else:
            bullets_two.pop(bullets_two.index(bullet2))

    for laser in lasers_one:
        if 750 > laser.x > 0:
            laser.x += laser.velocity
        else:
            lasers_one.pop(lasers_one.index(laser))

    for laser2 in lasers_two:
        if 750 > laser2.x > 0:
            laser2.x -= laser2.velocity
        else:
            lasers_two.pop(lasers_two.index(laser2))


def detect_game_over():
    if player_one.current_health == 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Player 2 wins!', True, TEAL, PURPLE)
        window.blit(text, (250, 250))
        player_one.game_over = True
    if player_two.current_health == 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Player 1 wins!', True, TEAL, PURPLE)
        window.blit(text, (250, 250))
        player_two.game_over = True


player_one = Player(50, 500, 100, 100, YELLOW, velocity=10)
player_two = Player(600, 500, 100, 100, RED, velocity=10)

# Bullet holders
bullets_one = []
bullets_two = []
lasers_one = []
lasers_two = []


def redraw_game_window(window):
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    window.blit(player_one_text, (0, 12))
    window.blit(player_two_text, (635, 12))
    player_one.draw_character(window)
    player_two.draw_character(window)
    player_one.draw_health_bar(window, RED, 0, 0, 100, 20)
    player_two.draw_health_bar(window, RED, 650, 0, 100, 20)
    for bullet in bullets_one:
        bullet.draw(window)
    for bullet2 in bullets_two:
        bullet2.draw(window)

    for laser in lasers_one:
        laser.draw(window)
    for laser2 in lasers_two:
        laser2.draw(window)
    pygame.display.update()




def game_commands():
    handle_bullets()
    detect_collision(bullets_one, bullets_two)
    detect_game_over()


clock = pygame.time.Clock()

while run:
    pygame.time.delay(50)
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    player_one.current_cool_down += 1
    player_two.current_cool_down += 1
    if keys[pygame.K_w] and player_one.y > 45:
        player_one.y -= player_one.velocity
    if keys[pygame.K_s] and player_one.y < 630:
        player_one.y += player_one.velocity
    if keys[pygame.K_UP] and player_two.y > 45:
        player_two.y -= player_two.velocity
    if keys[pygame.K_DOWN] and player_two.y < 630:
        player_two.y += player_two.velocity
    if keys[pygame.K_d] and player_one.can_shoot() and len(bullets_one) < 6:
        bullet_one = Bullet(player_one.x + (player_one.width // 2), player_one.y + (player_one.height // 2), 30, 10,
                            GREEN)
        laser_sfx.play()

        bullets_one.append(bullet_one)

    if keys[pygame.K_LEFT] and player_two.can_shoot() and len(bullets_two) < 6:
        bullet_two = Bullet(player_two.x + (player_two.width // 2), player_two.y + (player_two.height // 2), 30, 10,
                            PINK)
        bullets_two.append(bullet_two)
        laser_sfx.play()
    #special attack
    if keys[pygame.K_e] and not keys[pygame.K_d] and len(lasers_one) < 1:
        laser_one = Bullet(player_one.x + (player_one.width // 2), player_one.y + (player_one.height // 2), 400, 50,
                            BLUE)
        lasers_one.append(laser_one)

    if keys[pygame.K_RCTRL] and not keys[pygame.K_LEFT] and len(lasers_two) <1:
        laser_two = Bullet(player_two.x - 400, player_two.y + (player_two.height // 2), 400, 50,
                            YELLOW)
        lasers_two.append(laser_two)

    if player_one.game_over or player_two.game_over:
        pygame.time.delay(5000)
        run = False
    redraw_game_window(window)
    game_commands()
    pygame.display.update()
    clock.tick(120)

pygame.quit()

"""TO DO:
-------------------------------------------------
   - shooting lasers
-------------------------------------------------
   """

"""
Accomplished: Bullets work!
              Collision added!  
              Health bar added!
              Game over detection added! 
              Pictures
              Hit box for picture of spaceship
              SFX
              Music 
              charge attack

"""
