#Создай собственный Шутер!
from pygame import *
from random import *
from time import time as timer
mixer.init()
font.init()
 
#переменные
FPS = 60
run = True
finish = False
clock = time.Clock()
h = 700
w = 500
lost = 0
score = 0
num_fire = 0
rel_time = False

#создание классов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_w,player_h, player_speed):
        super().__init__()
        self.w = player_w
        self.h = player_h
        self.image = transform.scale(image.load(player_image),(player_w,player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)
        fire.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(5,630)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


#создание окна игры
window = display.set_mode((h, w))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(h,w))

player = Player('rocket.png', 320, 410, 65, 85, 10)

#создание групп
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(5,630),0,75,55, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(5,630),0,65,65,randint(1,4))
    asteroids.add(asteroid) 
#подключение фоновой музыки
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)

win = font2.render('YOU WIN!',True,(255,225,0))
lose = font2.render('YOU LOSE!', True, (255,0,0))
wait = font1.render('Wait,reload',True,(255,0,0))


#игровой цикл
while run:
    #условие завершения игры
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()


    
    if finish != True:
        window.blit(background,(0,0))
        sprites_list = sprite.groupcollide(bullets, monsters, True, True)
        for s in sprites_list:
            score += 1
            monster = Enemy('ufo.png',randint(5,630),0,75,55, randint(1,8))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters,False)or sprite.spritecollide(player,asteroids,False) or lost >= 3:
            finish = True
            window.blit(lose,(230, 225))
        if score >= 10:
            finish = True
            window.blit(win, (230, 225))

        #отображение фона
        
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        text_lost = font1.render('Пропущено:'+ str(lost),True,(255,255,255))
        text_score = font1.render('Счет:'+ str(score),True, (255,255,255))
        window.blit(text_score,(5,15))
        window.blit(text_lost,(5,45))
        bullets.draw(window)
        #перезарядка
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <3:
                window.blit(wait,(310,460))
            else:
                num_fire = 0
                rel_time = False

        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()

    clock.tick(FPS)
    display.update()        