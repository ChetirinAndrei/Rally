import pygame as pg
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)
block = True

pg.init()
pg.display.set_caption('Need For Speed Carbon')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()
car_accident = 0
block = False
life = 3
time = 0
'''
bg_image = pg.image.load('Image/road.jpg')
bg_image_rect = bg_image.get_rect(topleft=(0, 0))
bg_image_2_rect = bg_image.get_rect(topleft=(0, -HEIGHT))
'''
cars = [pg.image.load('Image/car1.png'), pg.image.load('Image/car3.png'), pg.image.load('Image/car2.png')]
font = pg.font.Font(None, 32)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('Image/car4.png')
        self.orig_image = self.image
        self.angle = 0
        self.speed = 2
        self.acceleration = 0.02
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(self.x, self.y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.velocity
        self.rect.center = self.position

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.angle -= 1
            if self.angle < -25:
                self.angle = -25
        elif keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.angle += 1
            if self.angle > 25:
                self.angle = 25
        else:
            self.velocity.x = 0
            if self.angle < 0:
                self.angle += 1
            elif self.angle > 0:
                self.angle -= 1
        if keys[pg.K_UP]:
            self.velocity.y -= self.acceleration
            if self.velocity.y < -self.speed:
                self.velocity.y = -self.speed
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.acceleration
            if self.velocity.y > self.speed:
                self.velocity.y = self.speed
        else:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration
                if self.velocity.y > 0:
                    self.velocity.y = 0
            elif self.velocity.y < 0:
                self.velocity.y -= self.acceleration
                if self.velocity < 0:
                    self.velocity.y = 0
        if self.rect.left < 38:
            self.rect.left = 40
            self.angle -= .1
            if self.angle >= 0:
                self.angle = 0


class Road(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(screen.get_size())
        self.image.fill(GREY)
        pg.draw.line(screen, GREEN, (20, 0), (20, 600), 40)
        pg.draw.line(screen, GREEN, (780, 0), (780, 600), 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, WHITE,
                    (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                    (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.transform.flip(img, False, True)
        self.speed = random.randint(2, 3)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0

            list_x.remove(self.rect.centerx)
            while True:
                self.rect.centerx = random.randrange(80, WIDTH, 80)
                if self.rect.centerx in list_x:
                    continue
                else:
                    list_x.append(self.rect.centerx)
                    self.speed = random.randint(2, 3)
                    break


all_sprite = pg.sprite.Group()
cars_group = pg.sprite.Group()
for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT))

list_x = []
n = 0
while n < 6:
    x = random.randrange(80, WIDTH, 80)
    if x in list_x:
        continue
    else:
        list_x.append(x)
        cars_group.add(Car(x, -cars[0].get_height(), cars[n] if n < len(cars) else random.choice(cars)))
        n += 1
player = Player()
all_sprite.add(player)

game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                #if c.collidepoint(e.pos)
                block = False

    if pg.sprite.spritecollideany(player, cars_group):
        if block is False:
            player.position[0] += 50 * random.randrange(-1, 2, 2,)
            player.angle = 50 * random.randrange(-1, 2, 2)
            car_accident += 1
            #life -= 1
            block = True
            print(car_accident)
            if life <= 0:
                game = False
    else:
        block = False
    '''
    car4.y -= 1
    if car4.y < -car4_h:
        car4.y = HEIGHT

        bg_image_rect.y += 1
        if bg_image_rect.y > HEIGHT:
            bg_image_rect.y = 0
        bg_image_2_rect.y += 1
        if bg_image_2_rect.y > 0:
            bg_image_2_rect.y = -HEIGHT

    #screen.fill(GREY)
    bg()
    for i in range(2):
        #screen.blit(bg_image, bg_image_rect if i == 0 else bg_image_2_rect)
    #screen.blit(car4_image, (car4.x, car4.y))
    '''
    all_sprite.update()
    all_sprite.draw(screen)
    screen.blit(font.render(f'кол-во аварий = {car_accident}', True, GREEN), (50, 10))
    '''screen.blit(font.render)'''

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Need For Speed Carbon     FPS: {int(clock.get_fps())}')

# pg.image.save(screen, 'Image/road.jpg')
