from random import randint

from pygame import *

# я цей проєкт вже раз п'ятий перевідправляю
# код трохи перероблював, а в останнє виправив
# одну помилку через яку снаряди миготіли періодично
# було дуже цікаво працювати з pygame та над цим проєктом
init()
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

win_width, win_height = 618, 359
FPS = 30
clock = time.Clock()

win = display.set_mode((win_width, win_height))
display.set_caption("Супєрма масівє гамєс: Манкі гамєта")

x_speed, y_speed = 5, 23
gravity = 2
jump_height = y_speed

font = font.SysFont("Elephant", 30)
gameOver_render = font.render(f"Game over", 1, red)
playAgain_render = font.render(f"Play again", 1, red, white)
playAgain_rect = playAgain_render.get_rect(topleft=(win_width//2-playAgain_render.get_width()//2, gameOver_render.get_height()+5))

boomerang_image = image.load("images/boomerang.png").convert_alpha()
banana_image = image.load("images/banana.png").convert_alpha()
size = banana_image.get_size()
new_size = (size[0] // 20, size[1] // 20)
banana_image = transform.scale(banana_image, new_size)
meteorite_image = image.load("images/meteorite.png").convert_alpha()

# додавати нові снаряди досить просто!
# снаряд = [чи снаряд летить вертикально, швидкість, текстура, шкода, очки]
# івент_створення_снаряду = якесь число
# def функція_яка_перезапустить_івент():
#   time.set_timer(івент_створення_вашого_снаряду, період, 1)

boomerang = [False, 5, boomerang_image, 1, -10]
spawn_boomerang = 1
def spawn_boomerang_event():
    time.set_timer(spawn_boomerang, randint(1, 3)*1000, 1)

meteorite = [True, 8, meteorite_image, 1, -5]
spawn_meteorite = 2
def spawn_meteorite_event():
    time.set_timer(spawn_meteorite, randint(2, 3)*900, 1)

banana = [True, 3, banana_image, -1, 10]
spawn_banana = 3
def spawn_banana_event():
    time.set_timer(spawn_banana, randint(10, 15)*1000, 1)

add_score = 42
time.set_timer(add_score, 1000)

# не забудьте потім викликати функцію
spawn_boomerang_event()
spawn_meteorite_event()
spawn_banana_event()

# далі прокрутіть до основного циклу

projectiles_list = []
score = 0
score_render = font.render(f"Score: {score}", 1, red)
health = 5
bg_x = 0
frame = 0
fast = 2
slow = 4
anim_speed = slow
x, y = 50, 200
bg = image.load("images/bg.png").convert_alpha()
player_sprites = []
for i in range(1, 16):
    sprite = image.load(f"images/monkey/{i}.png").convert_alpha()
    size = sprite.get_size()
    new_size = (size[0] // 2, size[1] // 2)
    sprite = transform.scale(sprite, new_size)
    player_sprites.append(sprite)

flipped = False
jumping = False

def flip_player_sprites():
    global player_sprites
    # воно просто перебирає усі елементи списку спрайтів бібізяни та застосовує ефект flip до кожного з них
    player_sprites = [transform.flip(sp, True, False) for sp in player_sprites]

def move():
    global x, y, flipped, frame, player_sprites, jumping, y_speed, anim_speed
    if keys[K_SPACE]:
        jumping = True
    if keys[K_d] and x < win_width - player_sprite.get_width():
        anim_speed = fast
        x += x_speed
        if flipped:
            flip_player_sprites()
            flipped = False
    elif keys[K_a] and x >= 0:
        anim_speed = fast
        x -= x_speed
        if not flipped:
            flip_player_sprites()
            flipped = True
    else:
        anim_speed = slow
        if flipped:
            flip_player_sprites()
            flipped = False
    frame += 1
    if frame >= len(player_sprites)*anim_speed:
        frame = 0
    if jumping:
        y -= y_speed
        y_speed -= gravity
        if y_speed < -jump_height:
            jumping = False
            y_speed = jump_height

def draw():
    global x, y, bg_x, score_render
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x + win_width, 0))
    bg_x -= 3
    if bg_x <= -win_width:
        bg_x = 0
    win.blit(player_sprite, (x, y))
    score_render = font.render(f"Score: {score}", 1, red)
    win.blit(score_render, (win_width-score_render.get_width(), 50))
    health_render = font.render(f"Health: {health}", 1, red)
    win.blit(health_render, (win_width - health_render.get_width(), 0))

def projectile_actions():
    global score, health, x, y
    player_rect = player_sprite.get_rect(topleft=(x, y))
    if projectiles_list:
        for a in projectiles_list.copy():
            vertical, speed, texture, damage, given_score, rectangle = a
            win.blit(texture, rectangle)
            if vertical:
                rectangle.y += speed
                if rectangle.y > win_height:
                    projectiles_list.remove(a)
            else:
                rectangle.x -= speed
                if rectangle.x < 0:
                    projectiles_list.remove(a)
            if rectangle.colliderect(player_rect):
                health -= damage
                score += given_score
                if score <= 0:
                    score = 0
                projectiles_list.remove(a)

def random_coordinates(vertical, p_image):
    p_width = p_image.get_width()
    p_height = p_image.get_height()
    return (randint(0, win_width-p_width), -p_height) if vertical else (win_width+p_width, 225)

def spawn_projectile(projectile):
    projectile = projectile.copy()
    p_image = projectile[2]
    orientation = projectile[0]
    coordinates = random_coordinates(orientation, p_image)
    p_rect = p_image.get_rect(topleft=coordinates)
    projectile.append(p_rect)
    projectiles_list.append(projectile)

# додайте в перебірку ось таке:
# if i.type == івент_створення_снаряду:
#     spawn_projectile(снаряд)
#     функція_яка_перезапустить_івент()

while True:
    clock.tick(FPS)
    for i in event.get():
        if i.type == QUIT:
            quit()
        if i.type == spawn_boomerang:
            spawn_projectile(boomerang)
            spawn_boomerang_event()
        if i.type == spawn_meteorite:
            spawn_projectile(meteorite)
            spawn_meteorite_event()
        if i.type == spawn_banana:
            spawn_projectile(banana)
            spawn_banana_event()
        if i.type == add_score:
            score += 1
    if health > 0:
        keys = key.get_pressed()
        player_sprite = player_sprites[frame // anim_speed]
        move()
        draw()
        projectile_actions()
    else:
        win.fill(black)
        win.blit(score_render, (win_width - score_render.get_width(), 50))
        win.blit(gameOver_render, (win_width//2-gameOver_render.get_width()//2, 0))
        win.blit(playAgain_render, playAgain_rect.topleft)
        mouse_pos = mouse.get_pos()
        if playAgain_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
            score = 0
            health = 5
            projectiles_list.clear()
            jumping = False
            y_speed = jump_height
            x, y = 50, 200
    display.update()