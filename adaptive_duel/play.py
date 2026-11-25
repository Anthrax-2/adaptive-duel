import pygame
from pygame.math import Vector2

WIDTH = 900
HEIGHT = 400
SPEED = 350
GRAVITY = 1500
JUMP_SPEED = 550
GROUND_HEIGHT = 10

BULLET_SPEED = 1000
BULLETS_COUNT = 10


class Character:
    def __init__(self, position, size, color):

        self.position = Vector2(position)
        self.rect = pygame.Rect(self.position, size)
        self.color = color
        self.velocity_y = 0
        self.on_ground = False
        self.facing = 1

        self.ammo = BULLETS_COUNT
        self.bullets = []
        
    def update(self, dt, direction, jump_request):

        movement = SPEED * dt
        self.position.x += direction * movement

        if direction:
            self.facing = direction

        if self.on_ground and jump_request:
            self.velocity_y = -JUMP_SPEED

        self.velocity_y += GRAVITY * dt
        self.position.y += self.velocity_y * dt

        self.position.x = max(0, min(self.position.x, WIDTH - self.rect.width))

        if self.position.y >= HEIGHT - (self.rect.height + GROUND_HEIGHT):
            self.position.y = HEIGHT - (self.rect.height + GROUND_HEIGHT)
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.rect.topleft = self.position

        self.bullets = [bullet for bullet in self.bullets if bullet.exist]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def shoot(self):

        if self.ammo > 0:
            bullet = Bullet(self.rect.center, self.facing, (10, 5), "orange")
            self.bullets.append(bullet)
            self.ammo -= 1


class Bullet:
    def __init__(self, position, facing, size, color):

        self.position = Vector2(position)
        self.rect = pygame.Rect(self.position, size)
        self.color = color
        self.velocity_x = facing * BULLET_SPEED
        self.exist = True

    def update(self, dt):

        bullet_movement = dt * self.velocity_x
        self.position.x += bullet_movement

        if (self.position.x >= WIDTH) or (self.position.x <= -self.rect.width):
            self.exist = False

        self.rect.topleft = self.position

    def draw(self, surface):

        if self.exist:
            pygame.draw.rect(surface, self.color, self.rect)



if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("duel")

    c_1 = Character((200, 0), (25, 40), "red")
    c_2 = Character((300, 0), (25, 40), "blue")

    ground = pygame.Rect((0, 0), (WIDTH, GROUND_HEIGHT))
    ground.bottom = HEIGHT

    clock = pygame.time.Clock()

    running = True

    while running:

        jump_request = False

        dt = clock.tick(60) / 1000  # limits frame rate

        for event in pygame.event.get():  # retrieves events
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_request = True

                if event.key == pygame.K_j:
                    c_1.shoot()

        screen.fill((30, 30, 40))

        pygame.draw.rect(screen, "#20781d", ground)

        direction_1 = 0
        # direction_2 = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            direction_1 -= 1
        if keys[pygame.K_d]:
            direction_1 += 1

        # if keys[pygame.K_LEFT]:
        #     direction_2 -= 1
        # if keys[pygame.K_RIGHT]:
        #     direction_2 += 1

        for bullet in c_1.bullets:
            bullet.update(dt)
            bullet.draw(screen)

        c_1.update(dt, direction_1, jump_request)
        # c_2.update(dt, direction_2, jump_request)

        c_1.draw(screen)
        # c_2.draw(screen)

        pygame.display.flip()  # updates display

    pygame.quit()
