from time import sleep
import random
from pygame import  *
from pygame.time import  *
from pygame.transform import grayscale

class Bird:
    def __init__(self, x, y):
        self.sprite = image.load('straight_plane.png').convert_alpha()
        width = 64
        height = width * self.sprite.get_height() / self.sprite.get_width()
        self.sprite = transform.scale(self.sprite, (width, height))
        self.rectangle = self.sprite.get_rect(centerx = x, centery=y)
        self.gravity = 0
    def paint(self, surface):
        surface.blit(self.sprite, self.rectangle)
    def jump(self, delta):
        mixer.Channel(0).play(mixer.Sound('whoosh.wav'), maxtime=600)
        self.gravity = -0.5 * delta
    def update(self, delta):
        self.rectangle.top += self.gravity
        self.gravity += 0.025 * delta
        if self.rectangle.bottom < 0:
            self.rectangle.top = 800
        if self.rectangle.top > 800:
            self.rectangle.bottom = 0


            
color = (200, 200, 255)
class Tower:
    def __init__(self):
        self.offset = 9 * 50  * 2
        self.vertical_offset = 300
        self.wide = 200
        self.top_sprite = Surface((100, self.vertical_offset))
        self.bottom_sprite = Surface((100, 16 * 50 - self.vertical_offset - self.wide))
        self.top_sprite.fill(color)
        self.bottom_sprite.fill(color)
        self.top_rectangle = self.top_sprite.get_rect(bottomright=(self.offset, 0))
        self.bottom_rectangle = self.bottom_sprite.get_rect(bottomright=(self.offset, 800))
    def paint(self, surface):
        self.top_rectangle = self.top_sprite.get_rect(topright=(self.offset, 0))
        self.bottom_rectangle = self.bottom_sprite.get_rect(bottomright=(self.offset, 800))
        surface.blit(self.top_sprite, self.top_rectangle)
        surface.blit(self.bottom_sprite, self.bottom_rectangle)
        draw.rect(surface, 'white', self.top_rectangle, width = 3)
        draw.rect(surface, 'white', self.bottom_rectangle, width = 3)
    def update(self, delta):
        self.offset -= 0.2 * delta
        if self.offset < 0:
            self.offset = 9 * 50 + 100
            self.vertical_offset = random.choice([100, 200, 300, 400, 500, 600])
            self.top_sprite = Surface((100, self.vertical_offset))
            self.bottom_sprite = Surface((100, 16 * 50 - self.vertical_offset - self.wide))
            self.top_sprite.fill(color)
            self.bottom_sprite.fill(color)
            self.top_rectangle = self.top_sprite.get_rect(bottomright=(self.offset, 0))
            self.bottom_rectangle = self.bottom_sprite.get_rect(bottomright=(self.offset, 800))

class Game:
    def __enter__(self):
        init()
        display.init()
        display.set_caption('Plane go brr')
        self.f = font.Font('./ProggyClean.ttf', 150)
        self.stage = display.set_mode((9 * 50, 16 * 50))
        self.width, self.height = display.get_window_size()
        self.delta = 0
        self.bird = Bird(self.width / 2, 0)
        self.tower = Tower()
        self.score = 0
        return self

    def __exit__(self, t, v, trace):
        display.quit()
        quit()

    def paint(self):
        self.stage.fill((50, 50, 50))
        textSurf = self.f.render(str(self.score // 60), True, (255, 255, 255))
        textRect = textSurf.get_rect(centerx=self.width/2, centery=self.height/2)
        textSurf.set_alpha(180)
        self.stage.blit(textSurf, textRect)
        self.bird.paint(self.stage)
        self.tower.paint(self.stage)

    def listen(self):
        for e in event.get():
            if e.type == QUIT:
                self.playing = False
            if e.type == KEYUP or e.type == MOUSEBUTTONUP:
                self.bird.jump(self.delta)
        self.bird.update(self.delta)
        self.tower.update(self.delta)
        if (
                self.tower.top_rectangle.colliderect(self.bird.rectangle)
            or
                self.tower.bottom_rectangle.colliderect(self.bird.rectangle)
                ):
            self.playing = False
            sleep(0.5)
        self.score += 1


    def start(self):
        self.playing = True
        clock = Clock()
        while self.playing:
            self.paint()
            display.update()
            self.listen()
            self.delta = clock.tick(60)
    

with Game() as g:
    g.start()
