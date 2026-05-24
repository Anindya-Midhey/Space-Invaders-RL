import pygame
from laser import Laser


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()

        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height

        # ───────── SAFE IMAGE LOADING (HEADLESS COMPATIBLE) ─────────
        raw_image = pygame.image.load("Graphics/spaceship.png")

        if pygame.display.get_surface():
            self.image = raw_image.convert_alpha()
        else:
            self.image = raw_image

        self.rect = self.image.get_rect(
            midbottom=((self.screen_width + self.offset) / 2, self.screen_height)
        )

        self.speed = 5
        self.lasers_group = pygame.sprite.Group()

        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300  # ms

    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

    def update(self, use_keyboard=True):
        if use_keyboard:
            self.get_user_input()

        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def apply_action(self, action):
        if action == 1:
            self.rect.x -= self.speed
        elif action == 2:
            self.rect.x += self.speed
        elif action == 3:
            self.shoot()

        self.constrain_movement()

    def shoot(self):
        if self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()

    def recharge_laser(self):
        if not self.laser_ready:
            if pygame.time.get_ticks() - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def reset(self):
        self.rect = self.image.get_rect(
            midbottom=((self.screen_width + self.offset) / 2, self.screen_height)
        )
        self.lasers_group.empty()
        self.laser_ready = True
