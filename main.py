import pygame
import sys
import random
from os import path

import time

# Window Size And FPS
TITLE = "PONG"
WIDTH = 1000
HEIGHT = 600
MID_W = WIDTH // 2
MID_H = HEIGHT // 2
FPS = 60

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Folders Assets
game_folder = path.dirname(__file__)
image_folder = path.join(game_folder, 'images')
sound_folder = path.join(game_folder, 'sound')


# Player
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.name = name
        self.speed = 7
        self.score = 0
        self.is_winner = False
        # pygame.draw.rect(self.image, color, self.rect)

    def update(self):
        key_state = pygame.key.get_pressed()
        # if key_state[pygame.K_UP] and self.rect.top > 0:
        #     self.rect.y -= self.speed
        # if key_state[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
        #     self.rect.y += self.speed

    def move_up(self):
        self.rect.y -= self.speed
        # Check if Paddle Not Going Off The Screen
        if self.rect.top < 0:
            self.rect.y = 0

    def move_down(self):
        self.rect.y += self.speed
        # Check if Paddle Not Going Off The Screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def restart(self):
        self.rect.centery = MID_H

    def is_winner(self):
        if self.score >= 3:
            self.is_winner = True
        else:
            self.is_winner = False


# Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_img_mini
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speed = [random.randint(4, 8), random.randint(-8, 8)]
        self.no_moving = False
        self.time = pygame.time.get_ticks()
        pygame.draw.ellipse(self.image, color, self.rect)

    def update(self):
        if not self.no_moving:
            self.rect.y += self.speed[1]
            self.rect.x += self.speed[0]

    # Return The Ball To The Start Position
    def back_to_start(self):
        self.rect.centerx = MID_W
        self.rect.centery = MID_H

    def restart(self):
        # Get The Current Time
        current_time = pygame.time.get_ticks()
        # And Than if Current Time Minus The Time That The Ball Run Off The Screen is Less Than 3 Second
        if current_time - self.time < 3000:
            # Set The Ball To Start Position
            self.back_to_start()

            # Give The Ball New Speed And Direction
            self.speed = [random.randint(4, 8), random.randint(-8, 8)]

            counter = counter_font.render("3", True, WHITE, BLACK)

            # Count 3...2...1 and Start The Game After 3 Seconds
            if 1000 < current_time - self.time < 2000:
                counter = counter_font.render("2", True, WHITE, BLACK)
            elif 2000 < current_time - self.time < 3000:
                counter = counter_font.render("Play!", True, WHITE, BLACK)

            # Draw The Counter On The Screen One By One Every Second
            screen.blit(counter, (MID_W - counter.get_rect().width // 2, 150))
        else:
            # After Counts, Ball Can Move on The Screen Start From The Middle
            self.no_moving = False


def game_over_screen():
    game_over = True

    winner = who_is_winner()
    while game_over:
        for event in pygame.event.get():
            # Check For Closing Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False

        text_winner = game_font.render("{} is The WINNER!".format(winner), True, GREEN)
        text_click_space = game_font.render("Click 'SPACE' if You Want To Continue".format(winner), True, WHITE)

        # Fill The Background With Color
        screen.fill(BLACK)

        # Show The GAME OVER Text On Screen
        screen.blit(text_winner, (MID_W - text_winner.get_width() // 2, MID_H - 100))
        screen.blit(text_click_space, (MID_W - text_click_space.get_width() // 2, MID_H - 200))
        pygame.display.flip()


def start_game_screen():
    # True = Game On
    start = True

    # Set The Ball Steel Until Counter Finish
    ball.no_moving = True

    #Main Loop
    while start:
        for event in pygame.event.get():
            # Check For Closing Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        text_winner = game_font.render("Welcome To Pong Game!", True, GREEN)
        text_click_space = game_font.render("Click 'SPACE' if You Want To Start", True, WHITE)
        text_buttons = game_font.render("Move With Arrows And 'W'+'S'", True, WHITE)

        # Fill The Background With Color
        screen.fill(BLACK)

        # Show The GAME OVER Text On Screen
        screen.blit(text_winner, (MID_W - text_winner.get_width() // 2, MID_H - 100))
        screen.blit(text_click_space, (MID_W - text_click_space.get_width() // 2, MID_H - 200))
        screen.blit(text_buttons, (MID_W - text_buttons.get_width() // 2, MID_H))
        pygame.display.flip()


# Return The Name of The Winner
def who_is_winner():
    if player1.score > player2.score:
        return player1.name
    else:
        return player2.name


# Initialize PyGame And Create Window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Fonts
game_font = pygame.font.Font('freesansbold.ttf', 32)
counter_font = pygame.font.Font('freesansbold.ttf', 48)

# Images
player_img = pygame.image.load(path.join(image_folder, 'player_bar.png')).convert_alpha()
ball_img = pygame.image.load(path.join(image_folder, 'ball.png')).convert_alpha()
ball_img_mini = pygame.transform.scale(ball_img, (20, 20))

# Loads Sounds
hit_sound = pygame.mixer.Sound(path.join(sound_folder, 'ball_hit.wav'))
counter_sound = pygame.mixer.Sound(path.join(sound_folder, 'counter.wav'))
counter_last_sound = pygame.mixer.Sound(path.join(sound_folder, 'counter_last.wav'))
game_over_sound = pygame.mixer.Sound(path.join(sound_folder, 'game_over.wav'))

# This Will Be a List That Will Contain All The Sprites We Intend To Use In Our Game.
all_sprites = pygame.sprite.Group()

# Create The First Player and Center it In Place
player1 = Paddle(GREY, 20, 140, "Player1")
player1.rect.left = 10
player1.rect.centery = MID_H

# Create The Second Player and Center it In Place
player2 = Paddle(GREY, 20, 140, "Player2")
player2.rect.right = WIDTH - 10
player2.rect.centery = MID_H

# Create The Ball and Draw it On The Middle
ball = Ball(20, 20, WHITE)
ball.rect.centery = MID_H
ball.rect.centerx = MID_W

# Add The Paddles To The List of Sprites
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)


def main():
    # The loop will running until the user exit the game (e.g. clicks the close button).
    running = True

    # Show Start Screen Until Hit SPACE Key
    start_game_screen()

    while running:
        # Keep Loop Running At The Right Speed
        # Limit To 60 Frames Per Second
        clock.tick(FPS)

        # Process Input (Events)
        for event in pygame.event.get():
            # Check For Closing Window
            if event.type == pygame.QUIT:
                # Stop Looping When Getting To The End Of The While Loop
                running = False

        # Moving The Paddles When The Use Uses The Arrow Keys (Player 1) or "W/S" Keys (Player 2)
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_UP]:
            player2.move_up()
        if key_state[pygame.K_DOWN]:
            player2.move_down()
        if key_state[pygame.K_w]:
            player1.move_up()
        if key_state[pygame.K_s]:
            player1.move_down()

        # Update
        all_sprites.update()

        # Check if the ball is bouncing against any of the 2 walls:
        if ball.rect.top <= 0:
            ball.speed[1] = -ball.speed[1]
            hit_sound.play()
        if ball.rect.bottom >= HEIGHT:
            ball.speed[1] = -ball.speed[1]
            hit_sound.play()

        # Check if The Ball Pass The Left Wall
        if ball.rect.left <= 0:
            # Play Game Over Sound
            game_over_sound.play()
            # Add 1 to Score for Player 2
            player2.score += 1
            # Stop The ball From Moving
            ball.no_moving = True
            # Set The Ball Time To Current Time
            ball.time = pygame.time.get_ticks()
            # Set The Players Paddles Back To Start Position
            player1.restart()
            player2.restart()

        # Check if The Ball Pass The Right Wall
        elif ball.rect.right >= WIDTH:
            # Play Game Over Sound
            game_over_sound.play()
            # Add 1 to Score for Player 1
            player1.score += 1
            # Stop The ball From Moving
            ball.no_moving = True
            # Set The Ball Time To Current Time
            ball.time = pygame.time.get_ticks()
            # Set The Players Paddles Back To Start Position
            player1.restart()
            player2.restart()

        # Detect Collisions Between The Ball And The Paddles
        if pygame.sprite.collide_mask(ball, player2) or pygame.sprite.collide_mask(ball, player1):
            # Change The Speed To Other Direction  -->  8 * -1 = -8
            ball.speed[0] = -ball.speed[0]
            # Play Hit Sound When Paddle Hit The Ball
            hit_sound.play()

        # Fill The Background in Black
        screen.fill(BLACK)
        # Draw The Net
        pygame.draw.aaline(screen, GREY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Display scores:
        score_player1 = game_font.render("Player1: {}".format(str(player1.score)), True, GREEN)  # PLAYER 1
        screen.blit(score_player1, (MID_W // 2 - 50, MID_H - 200))
        score_player2 = game_font.render("Player2: {}".format(str(player2.score)), True, GREEN)  # PLAYER 2
        screen.blit(score_player2, (MID_W + (MID_W // 2 - 50), MID_H - 200))

        # if The Ball is Out of The Screen So The Ball Will Go Back To The Middle of The screen
        # and Start in 3 Second
        if ball.no_moving:
            # Stop The Game And Show Game Over Screen If One of The Players Reach 3 Points
            if player1.score >= 3 or player2.score >= 3:
                game_over_screen()
                player1.score = 0
                player2.score = 0
                ball.time = pygame.time.get_ticks()
            ball.restart()

        # Draw All Spirits To The Screen
        all_sprites.draw(screen)

        # After Drawing Everything Flip The Display
        pygame.display.flip()

    # Quit The Game
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
