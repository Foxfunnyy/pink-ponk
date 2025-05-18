from pygame import *
from random import randint
font.init()

RED = (255, 100, 100)
BLUE = (100, 100, 255)
window = display.set_mode((600, 600))


clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, pos, size, speedd):
        super().__init__()
        self.image = Surface(size, SRCALPHA)
        self.rect = self.image.get_rect()
        self.speed = speedd
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, pos, size, speedd, color, k_up, k_down):
        super().__init__(pos, size, speedd)
        self.image.fill(color)
        self.k_up = k_up
        self.k_down = k_down
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[self.k_up] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[self.k_down] and self.rect.y  < 600 - self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, pos, size, speedd, color):
        super().__init__(pos, size, speedd)
        draw.ellipse(self.image, color, Rect(0, 0, size[0], size[1]))
        self.dir_x = -1
        self.dir_y = 1
    def update(self):
        if self.rect.y < 0:
            self.dir_y = 1     
        elif self.rect.y > 600 - self.rect.height:
            self.dir_y = -1
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
    def reset(self):
        self.rect.x = 300 - self.rect.width/2
        self.rect.y = 300 - self.rect.height/2
        self.dir_x = 1 - 2*randint(0,1)
        self.dir_y = 1 - 2*randint(0,1)




player1 = Player((100, 100), (32, 64), 5, RED, K_w, K_s)
player2 = Player((500, 100), (32, 64), 5, BLUE, K_UP, K_DOWN)
ball = Ball((300, 300), (42, 42), 2, (255, 255, 255))

ball.reset()

counterfont = font.SysFont('verdana', 30)
def draw_counter(value, x, y):
    img = counterfont.render(value, True, (255, 255, 255))
    window.blit(img,(x, y))

score1 = 0
score2 = 0

resultfont = font.SysFont('verdana', 50)
def draw_result(value, x, y, color):
    img = resultfont.render(value, True, color)
    window.blit(img,(x, y))



gameover = False

finish = False


while not gameover:
    for e in event.get():
        if e.type == QUIT:
            gameover = True

    if not finish:
        if sprite.collide_rect(player1, ball):
            ball.dir_x = 1
        if sprite.collide_rect(player2, ball):
            ball.dir_x = -1
        if ball.rect.x < 0:
            score2 += 1
            ball.reset()
        elif ball.rect.x > 600 - ball.rect.width:
            score1 += 1
            ball.reset()      
        player1.update()
        player2.update()
        ball.update()
        if score1 >= 3 or score2 >= 3:
            finish = True

    window.fill((10, 10, 10))

    player1.draw()
    player2.draw()
    ball.draw()

    draw_counter(str(score1), 280, 5)
    draw_counter(str(score2), 320, 5)

    if finish:
        if score1 >= 3:
            draw_result('Winner player 1', 200, 200, RED)
        elif score2 >= 3:
            draw_result('Winner player 2', 200, 200, BLUE)

    display.update()
    clock.tick(60)