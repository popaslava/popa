

from pygame import *
from random import randint

HEIGHT = 700
WIDTH = 1200
FPS = 70

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

window = display.set_mode((WIDTH,HEIGHT))

img_bullet = 'bullet.png'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'

display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(1200,700))   

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            ship.fire()


    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top, 15 ,20 , -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



font.init()
font2 = font.Font(None,36)    

max_lost = 5
number = 9
score = 0
lost = 0
timer = 0
goal =1000

def stats():
    global score
    for monster in monsters:
        for bullet in bullets:
            if monster.rect.colliderect(bullet.rect):
                score += 1

bullets = sprite.Group()

monsters = sprite.Group()
for  i in range(1,6):
    monster = Enemy(img_enemy,randint(80,WIDTH - 80),-40,80,50,randint(1,5))
    monster.add(monsters)

ship = Player(img_hero,5,HEIGHT - 100,80,100,10)

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True, True)
        for c in collides:
            score = score + 1           
            monster  = Enemy(ufo.png,randint(80,win_width - 80),- 40, 80,50,randint(1,5))
            monsers.add(monster)
        if sprite.spritecollide(ship,monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        text = font2.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose,(10,50))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsers:
            m.kill()
        time.delay(3000)
        for i in renge(1,6):
            monster = Enemy(img_enemy,rendint(80, win_width - 80), -40,80,50, randint(1,5))
            monsers.add(monster)
    time.delay(50)
