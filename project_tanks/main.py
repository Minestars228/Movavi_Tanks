import random
import time
import pygame
import settings

pygame.init()
pygame.mixer.init()

score = 0
space = 0
live = 3

last_spawn = 0
spawn_time = 1
def spawn_enemy():
    global last_spawn
    now = time.time()
    if now - spawn_time > last_spawn:
        last_spawn = now
        e = pygame.sprite.Sprite(all_sprites, enemyes)
        img = pygame.transform.rotate(enemy_img, -90)
        e.image = img
        e.rect = img.get_rect()
        e.rect.x = settings.SCREEN_WIDTH + 50
        e.rect.y = random.randint(0, settings.SCREEN_HEIGHT - e.rect.height)

def move_enemy():
    for e in enemyes:
        e.rect.x -= 5
        if e.rect.bottom < 0:
            e.kill()

def check_collide_aliens():
    for e in enemyes:
        if pygame.sprite.collide_rect(player , e):
            return e
    return None

def MOVE_PLAYER():
    speed = settings.PLAYER_MOVE_SPEED
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.rect.top > 0:
        player.rect.y -= speed
    if keys[pygame.K_s] and player.rect.bottom < settings.SCREEN_HEIGHT:
        player.rect.y += speed
last_shot = 0
def SHOT():
    global last_shot
    now = time.time()
    if now - settings.RELOAD > last_shot:
        shot_sound.play()
        last_shot = now
        bullet = pygame.sprite.Sprite(bullets, all_sprites)
        bullet.image = bullet_img
        bullet.rect: pygame.Rect = bullet.image.get_rect()
        bullet.rect.centery = player.rect.centery
        bullet.rect.centerx = player.rect.centerx

def move_bullet():
    speed = settings.BULLET_MOVE_SPEED
    for b in bullets:
        b.rect.x += speed
        if b.rect.bottom >= settings.SCREEN_WIDTH:
            b.kill()

def check_collide_shot():
    for e in enemyes:
        for b in bullets:
            if pygame.sprite.collide_rect(e, b):
                b.kill()
                return e
    return None

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # версия с полноэкранным режимом
screen = pygame.display.set_mode(settings.SCREEN_SIZE)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemyes = pygame.sprite.Group()

player_img = pygame.image.load("./project_tanks/images/tank_blue.png")
player_img = pygame.transform.rotate(player_img, 90)

enemy_img = pygame.image.load("./project_tanks/images/tank_red.png")

bg_img = pygame.image.load("./project_tanks/images/bg.png")

bullet_img = pygame.image.load("./project_tanks/images/bullet.png")
bullet_img = pygame.transform.rotate(bullet_img, -90)

player = pygame.sprite.Sprite(all_sprites)
player.image = player_img 
player.rect = player_img.get_rect()
player.rect.left = 30
player.rect.centery = settings.SCREEN_HEIGHT // 2

m = pygame.sprite.Sprite(all_sprites, enemyes)
m.image = pygame.image.load("./project_tanks/images/tank_red.png")
m.rect = m.image.get_rect()
m.rect.left = 5000

pygame.mixer.music.load("./project_tanks/sounds/tank_move.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops = -1)
shot_sound = pygame.mixer.Sound('./project_tanks/sounds/fire.wav')
shot_sound.set_volume(0.2)
GameOver_sound = pygame.mixer.Sound('./project_tanks/sounds/game_over.wav')

boom_sound = pygame.mixer.Sound('./project_tanks/sounds/boom.wav')


font_object = pygame.font.SysFont('Arial' , 24)
font_object_big = pygame.font.SysFont('Arial' , 124)

font_object_1 = pygame.font.SysFont('Arial', 50)
text = font_object_1.render(f"Счет: {score}", False, 'white')

font_object_2 = pygame.font.SysFont('Arial', 200)
GameOver = font_object_2.render(f"Game Over", False, 'white')

font_object_3 = pygame.font.SysFont('Arial', 50)
lives = font_object_3.render(f"Жизни: {live}", False, 'white')

font_object_4 = pygame.font.SysFont('Arial', 30)
GameOver2 = font_object_4.render(f"Нажмите 'R' для того чтобы начать заново", False, 'white')

bg_x = 0

clock = pygame.time.Clock()
game_end = False
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                SHOT()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space += 1
            if event.key == pygame.K_e:
                if score >= 15:
                    live += 1
                    score -= 15
            if event.key == pygame.K_r:
                for e in enemyes:
                    e.rect.x += 5000
                game_end = False
                live = 3
                score = 0  
                pygame.display.update()
    if live <= 0:
        game_end = True
    if not game_end:
        if space % 2 == 0:
            screen.blit(bg_img, (bg_x , 0))
            bg_x -= 1.5
            if bg_x + bg_img.get_width() <= settings.SCREEN_WIDTH:
                bg_x = 0

            lives = font_object_3.render(f"Жизни: {live}", False, 'white')

            screen.blit(text , (10 , 0))
            screen.blit(lives , (10 , 60))

            all_sprites.draw(screen)

            MOVE_PLAYER()
            move_bullet()
            move_enemy()
            spawn_enemy()
            m = check_collide_aliens()
            l = check_collide_shot()
            if m:
                boom_sound.play()
                m.rect.centery = 5000
                live -= 1
            if l:
                boom_sound.play()
                l.rect.centery = 5000
                score += 5
    else:
        pygame.mixer.music.stop()
        GameOver_sound.play()
        screen.fill('black')
        screen.blit(GameOver , (175 , 100))
        screen.blit(GameOver2 , (350 , 600))

    pygame.display.update()
    font_object = pygame.font.SysFont('Arial', 50)
    text = font_object.render(f"Счет: {score}", False, 'white')
    clock.tick(60)

pygame.quit()
