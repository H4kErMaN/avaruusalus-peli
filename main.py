import pygame
import random
from alus import Spaceship, Bullet
from vihut import Enemy, Background

pygame.init()
screen_width, screen_height = 1280, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

WHITE, YELLOW, GREEN, RED, BLACK = (255, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 0, 0)

font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)
hp_font = pygame.font.Font(None, 30)

volume = 0.5
pygame.mixer.init()
pygame.mixer.music.load("Brave Pilots (Menu Screen).ogg")
pygame.mixer.music.set_volume(volume)
shoot_sound = pygame.mixer.Sound("shoot.wav")
shoot_sound.set_volume(volume)

mainmenu_bg = pygame.image.load("mainmenu.jpg")

score = 0
player_lives = 3

enemy_images = ["örkki.png", "örkki2.png", "örkki3.png"]
enemy_sizes = [20, 5, 10]
enemy_speeds = [5, 6, 7]
enemy_scores = [10, 15, 20]

def show_start_screen(): #main menu systeemi
    global volume
    while True:
        screen.blit(mainmenu_bg, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        start_text = font.render("Start Game", True, YELLOW if 250 < mouse_y < 300 else WHITE)
        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, YELLOW if 350 < mouse_y < 400 else WHITE)
        quit_text = font.render("Quit", True, YELLOW if 450 < mouse_y < 500 else WHITE)

        screen.blit(start_text, (screen_width // 2 - 150, 250))
        screen.blit(volume_text, (screen_width // 2 - 150, 350))
        screen.blit(quit_text, (screen_width // 2 - 150, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 < mouse_y < 300:
                    pygame.mixer.music.play(-1)
                    return "start"
                if 350 < mouse_y < 400:
                    volume = (volume + 0.1) % 1.1
                    pygame.mixer.music.set_volume(volume)
                    shoot_sound.set_volume(volume)
                if 450 < mouse_y < 500:
                    pygame.quit()
                    return "quit"

def show_pause_menu():
    while True:
        screen.fill(BLACK)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(font.render("PAUSED", True, WHITE), (screen_width // 2 - 100, 150))
        screen.blit(font.render("Resume", True, YELLOW if 250 < mouse_y < 300 else WHITE), (screen_width // 2 - 100, 250))
        screen.blit(font.render("Main Menu", True, YELLOW if 350 < mouse_y < 400 else WHITE), (screen_width // 2 - 100, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 < mouse_y < 300:
                    return "resume"
                if 350 < mouse_y < 400:
                    return "start_screen"

def show_game_over_screen(): #pelipäättyi ruutu
    global score
    while True:
        screen.fill(BLACK)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(font.render("GAME OVER", True, RED), (screen_width // 2 - 200, 150))
        screen.blit(score_font.render(f"Score: {score}", True, WHITE), (screen_width // 2 - 100, 250))
        screen.blit(font.render("Restart", True, YELLOW if 250 < mouse_y < 300 else WHITE), (screen_width // 2 - 100, 350))
        screen.blit(font.render("Main Menu", True, YELLOW if 350 < mouse_y < 400 else WHITE), (screen_width // 2 - 100, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 < mouse_y < 300:
                    return "restart"
                if 350 < mouse_y < 400:
                    return "start_screen"

def game_loop():
    global score, player_lives
    spaceship = Spaceship(screen_height)
    background = Background()
    all_sprites = pygame.sprite.Group(spaceship)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    clock = pygame.time.Clock()
    paused = False
    running = True

    def draw_hp():
        screen.blit(hp_font.render(f"Lives: {player_lives}", True, WHITE), (10, 40))
        pygame.draw.rect(screen, RED, (10, 70, 200, 10))
        pygame.draw.rect(screen, GREEN, (10, 70, 200 * (player_lives / 3), 10))

    def spawn_enemy():
      if random.random() < 0.02:  # vihujen spawnaus jutska
        enemy_idx = random.randint(0, 2)
        image_path = enemy_images[enemy_idx]
        image = pygame.image.load(image_path).convert_alpha()
        image_rect = image.get_rect()

        spawn_margin = 10  #estää vihujen spawnaamisen alareunaan.
        max_spawn_y = screen_height - image_rect.height - spawn_margin
        spawn_y = random.randint(spawn_margin, max_spawn_y)

        enemy = Enemy(image_path, image_rect.height, enemy_speeds[enemy_idx], enemy_scores[enemy_idx])
        enemy.rect.y = spawn_y
        all_sprites.add(enemy)
        enemies.add(enemy)

    while running:
        screen.fill(BLACK)
        background.update()
        background.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    spaceship.speed_y = -5
                elif event.key == pygame.K_s:
                    spaceship.speed_y = 5
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(spaceship.rect.centerx, spaceship.rect.centery)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                elif event.key == pygame.K_ESCAPE:
                    paused = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    spaceship.speed_y = 0

        for bullet in bullets:
            hit = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy in hit:
                bullet.kill()
                score += enemy.score_value

        for enemy in enemies:
            if enemy.rect.right < spaceship.rect.left:
                player_lives -= 1
                enemy.kill()
                if player_lives <= 0:
                    running = False

        if paused:
            result = show_pause_menu()
            if result == "resume":
                paused = False
            elif result == "start_screen":
                return "menu"
            elif result == "quit":
                running = False
                break

        spawn_enemy()
        all_sprites.update()

        screen.blit(score_font.render(f"Score: {score}", True, WHITE), (10, 10))
        draw_hp()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return "game_over"

# pelin looppi 
while True:
    result = show_start_screen()
    if result == "start":
        game_result = game_loop()
        if game_result == "game_over":
            result = show_game_over_screen()
            if result == "restart":
                score = 0
                player_lives = 3
                continue
            elif result == "start_screen":
                continue
    elif result == "quit":
        break

pygame.quit()
