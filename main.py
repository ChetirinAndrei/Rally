import pygame as pg

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)

pg.init()
pg.display.set_caption('Need For Speed Carbon')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()

bg_image = pg.image.load('Image/road.jpg')
bg_image_rect = bg_image.get_rect(topleft=(0, 0))
bg_image_2_rect = bg_image.get_rect(topleft=(0, -HEIGHT))


def bg():
    pg.draw.line(screen, GREEN, (20, 0), (20, 600), 40) 
    pg.draw.line(screen, GREEN, (780, 0), (780, 600), 40)
    for xx in range(10):
        for yy in range(10):
            pg.draw.line(
                screen, WHITE,
                (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)


class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('Image/car4.png')


car4 = Car()
car4_image = car4.image
car4_w, car4_h = car4.image.get_width(), car4.image.get_height()
car4.x, car4.y = (WIDTH - car4_w) // 2, (HEIGHT - car4_h) // 2

game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

    car4.y -= 1
    if car4.y < -car4_h:
        car4.y = HEIGHT

        bg_image_rect.y += 1
        if bg_image_rect.y > HEIGHT:
            bg_image_rect.y = 0
        bg_image_2_rect.y += 1
        if bg_image_2_rect.y > 0:
            bg_image_2_rect.y = -HEIGHT

    screen.fill(GREY)
    # bg()
    for i in range(2):
        screen.blit(bg_image, bg_image_rect if i == 0 else bg_image_2_rect)
    #screen.blit(car4_image, (car4.x, car4.y))
    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Need For Speed Carbon     FPS: {int(clock.get_fps())}')

# pg.image.save(screen, 'road.jpg')
