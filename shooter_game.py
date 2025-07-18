from pygame import *
from random import *

#! ЭТО КРАСНЫЙ
# TODO Это оранжевый
# // Зачёркнутый
# ? ЭТО СИНИЙ
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg') #Звук стрельбы

font.init()
font2 = font.Font(None,36)

font1 = font.Font(None,80)

win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))

img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = 'ufo.png' #Враг 
img_bullet = 'bullet.png'

lost = 0 # Пропущено кораблей
score = 0 #Сбито кораблей
goal = 10 #Столько противников нужно сбить для победы
max_lost = 3 # Проиграли, если пропустим столько

class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)


       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        #Создаём пулю
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost +=1
class Bullet(GameSprite): #класс пули с методом движения вверх
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# Создаём спрайты
ship = Player(img_hero, 5, 400, 80, 100, 10)

monsters = sprite.Group() 
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width-80),-40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group() # Группа для пуль 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна

clock = time.Clock()
while run == True:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
          
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
        



    if finish != True:
        #обновляем фон
        window.blit(background,(0,0))
      
        ship.update()
        monsters.update() 
        #Вызов метода движения пуль вверх
        bullets.update() 
        ship.reset()
        monsters.draw(window)
        #ОТОБРАЖЕНИЕ ГРУППЫ ПУЛЬ
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for c in collides:
            #Этот цикл сработает столько раз, сколько у нас подбито монстров
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width-80),-40, 80, 50, randint(1,5))
            monsters.add(monster)
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        
        if lost >= max_lost or sprite.spritecollide(ship, monsters, False):
            finish = True
            window.blit(lose, (200,200))


        text = font2.render('Счет:' + str(score), True, (255,255,255))
        
        window.blit(text, (10,20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        display.update()
#цикл срабатывает каждые 0.05 секунд
    #time.delay(50)
    clock.tick(50)