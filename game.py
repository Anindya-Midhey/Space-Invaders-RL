import pygame
import random
from spaceship import Spaceship
from obstarcle import Obstarcle, grid
from alien import Alien, UFO
from laser import Laser


class Game:
    def __init__(self, screen_width, screen_height, offset, render=True):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.render_enabled = render

        # ───────── DISPLAY ─────────
        if self.render_enabled:
            self.screen = pygame.display.set_mode(
                (self.screen_width + self.offset, self.screen_height)
            )
            pygame.display.set_caption("Space Invaders RL")
            self.font = pygame.font.Font("Font/monogram.ttf", 40)
        else:
            self.screen = None
            self.font = None

        self.reset()

    # ───────── RESET ─────────
    def reset(self):
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(
            Spaceship(self.screen_width, self.screen_height, self.offset)
        )

        self.obstarcles = self.create_obstarcles()

        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1

        self.alien_lasers_group = pygame.sprite.Group()
        self.UFO_group = pygame.sprite.GroupSingle()

        self.lives = 3
        self.run = True
        self.game_won = False

        self.score = 0
        self.load_highscore()

    # ───────── SETUP ─────────
    def create_obstarcles(self):
        obstarcle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstarcle_width)) / 5
        obstarcles = []

        for i in range(4):
            offset_x = (i + 1) * gap + i * obstarcle_width
            obstarcle = Obstarcle(offset_x, self.screen_height - 100)
            obstarcles.append(obstarcle)

        return obstarcles

    def create_aliens(self):
        for row in range(4):
            for col in range(6):
                x = 75 + col * 55
                y = 110 + row * 55
                alien_type = 3 if row == 0 else 2 if row < 3 else 1
                self.aliens_group.add(
                    Alien(alien_type, x + self.offset / 2, y)
                )

    # ───────── RENDER ─────────
    def render(self):
        if not self.render_enabled:
            return

        self.screen.fill((30, 30, 30))

        self.spaceship_group.draw(self.screen)
        self.spaceship_group.sprite.lasers_group.draw(self.screen)
        self.aliens_group.draw(self.screen)
        self.alien_lasers_group.draw(self.screen)
        self.UFO_group.draw(self.screen)

        for ob in self.obstarcles:
            ob.blocks_group.draw(self.screen)

        score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"LIVES: {self.lives}", True, (255, 0, 0))

        self.screen.blit(score_text, (20, 10))
        self.screen.blit(lives_text, (20, 50))

        pygame.display.update()

    # ───────── MOVEMENT ─────────
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        for alien in self.aliens_group:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(20)
                break
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(20)
                break

    def alien_move_down(self, distance):
        for alien in self.aliens_group:
            alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group:
            alien = random.choice(self.aliens_group.sprites())
            self.alien_lasers_group.add(
                Laser(alien.rect.center, -3, self.screen_height)
            )

    # ───────── STATE ─────────
    def get_discrete_state(self):
        ship = self.spaceship_group.sprite
        ship_x = int((ship.rect.x / self.screen_width) * 10)

        if self.aliens_group:
            alien = min(
                self.aliens_group,
                key=lambda a: abs(a.rect.x - ship.rect.x)
            )
            alien_x = int((alien.rect.x / self.screen_width) * 10)
            alien_y = int((alien.rect.y / self.screen_height) * 10)
        else:
            alien_x = alien_y = 0

        return (ship_x, alien_x, alien_y, self.lives)

    # ───────── STEP ─────────
    def step(self, action):
        reward = -0.01  # living penalty

        self.spaceship_group.sprite.apply_action(action)
        self.spaceship_group.update(use_keyboard=False)

        self.move_aliens()
        self.alien_lasers_group.update()
        self.UFO_group.update()

        if random.random() < 0.03:
            self.alien_shoot_laser()

        reward += self.check_for_collisions()

        if self.render_enabled:
            self.render()

        done = not self.run
        return self.get_discrete_state(), reward, done

    # ───────── COLLISION & REWARD ─────────
    def check_for_collisions(self):
        reward = 0

        # Player laser → alien
        for laser in self.spaceship_group.sprite.lasers_group:
            aliens_hit = pygame.sprite.spritecollide(laser, self.aliens_group, True)
            if aliens_hit:
                laser.kill()
                reward += 10 * len(aliens_hit)
                self.score += 100 * len(aliens_hit)
                self.check_for_highscore()

            for ob in self.obstarcles:
                if pygame.sprite.spritecollide(laser, ob.blocks_group, True):
                    laser.kill()

        # Alien laser → ship
        for laser in self.alien_lasers_group:
            if pygame.sprite.spritecollide(laser, self.spaceship_group, False):
                laser.kill()
                self.lives -= 1
                reward -= 20
                if self.lives <= 0:
                    self.run = False

            for ob in self.obstarcles:
                if pygame.sprite.spritecollide(laser, ob.blocks_group, True):
                    laser.kill()

        # Alien collision
        for alien in self.aliens_group:
            for ob in self.obstarcles:
                pygame.sprite.spritecollide(alien, ob.blocks_group, True)

            if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                self.run = False
                self.lives = 0
                reward -= 50

        # Win condition
        if len(self.aliens_group) == 0:
            self.game_won = True
            self.run = False
            reward += 100

        return reward

    # ───────── SCORE ─────────
    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                self.highscore = int(f.read())
        except FileNotFoundError:
            self.highscore = 0
