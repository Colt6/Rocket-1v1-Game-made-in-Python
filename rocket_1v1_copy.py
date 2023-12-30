import pygame
import os

pygame.init()
pygame.font.init()

width, height = (1000, 600)

WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Isreal vs Palestine")

FPS = 90
speed = 4
bullet_speed = 11
max_bullets = 3

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

player1_hit = pygame.USEREVENT + 1
player2_hit = pygame.USEREVENT + 2

boarder = pygame.Rect((width // 2) - 5, 0, 10, height)
health_font = pygame.font.SysFont("consolas", 36)
winner_font = pygame.font.SysFont("consolas", 100)

spaceimg = pygame.transform.scale((pygame.image.load(os.path.join("Space.png"))), (width, height))

spaceship_image1 = pygame.image.load(os.path.join("red_spaceeship.png"))
spaceship1 = pygame.transform.scale(pygame.transform.rotate(spaceship_image1, 180), (150, 90))

spaceship_image2 = pygame.image.load(os.path.join("blue_spaceship.png"))
spaceship2 = pygame.transform.scale(spaceship_image2, (150, 90))

font = pygame.font.SysFont(None, 36)

def show_winner(text):
    if text == "Blue  Won!":
        draw_winner_text = winner_font.render(text, 1, blue)
    else:
        draw_winner_text = winner_font.render(text, 1, red)
    WIN.blit(draw_winner_text, (250, 300))
    pygame.display.update()
    pygame.time.delay(3000)

def draw_window(player_one, player_two, player1_bullet, player2_bullet, fps, player1_health, player2_health):
    WIN.fill((white))
    WIN.blit(spaceimg, (0, 0))
    
    WIN.blit(spaceship1, (player_one.x, player_one.y))
    WIN.blit(spaceship2, (player_two.x, player_two.y))
    pygame.draw.rect(WIN, black, boarder)

    fps_text = font.render(f"FPS: {fps}", True, (255, 0, 0))
    player2_health_text = health_font.render("Health: " + str(player2_health), 1, blue)
    player1_health_text = health_font.render("Health: " + str(player1_health), 1, red)

    WIN.blit(fps_text, (890, height - 50))
    WIN.blit(player1_health_text, (20, 20))
    WIN.blit(player2_health_text, (780, 20))

    for bullet in player1_bullet:
        pygame.draw.rect(WIN, red, bullet)

    for bullet in player2_bullet:
        pygame.draw.rect(WIN, blue, bullet)

    pygame.display.update()

def player1_movement(pressed_key, player_one):
    if pressed_key[pygame.K_a] and player_one.x - speed > 0:
        player_one.x -= speed
        
    if pressed_key[pygame.K_d] and player_one.x + speed + player_one.width < boarder.x + boarder.width:
        player_one.x += speed

    if pressed_key[pygame.K_w] and player_one.y - speed > 0:
        player_one.y -= speed
        
    if pressed_key[pygame.K_s] and player_one.y + speed + player_one.height < height:
        player_one.y += speed

def player2_movement(pressed_key, player_two):
    if pressed_key[pygame.K_UP] and player_two.y - speed > 0:
        player_two.y -= speed

    if pressed_key[pygame.K_DOWN] and player_two.y + speed + player_two.height < height:
        player_two.y += speed

    if pressed_key[pygame.K_LEFT] and player_two.x - speed - player_two.width > boarder.x - 80:
        player_two.x -= speed
        
    if pressed_key[pygame.K_RIGHT] and (player_two.x + speed + player_two.width) < width:
        player_two.x += speed

def handle_bullets(player1_bullet, player2_bullet, player_one, player_two):
    for bullet in player1_bullet:
        bullet.x += bullet_speed
        if player_two.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player2_hit))
            player1_bullet.remove(bullet)

        elif bullet.x > width:
            player1_bullet.remove(bullet)

    for bullet in player2_bullet:
        bullet.x -= bullet_speed
        if player_one.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player1_hit))
            player2_bullet.remove(bullet)

        elif bullet.x < 0:
            player2_bullet.remove(bullet)


def main():
    player_one = pygame.Rect(200, 200, 150, 90)
    player_two = pygame.Rect(800, 200, 150, 90)

    player1_bullet = []
    player2_bullet = []
    
    clock = pygame.time.Clock()

    player1_health = 10
    player2_health = 10

    run = True
    while run == True:
        clock.tick(FPS)
        fps = int(clock.get_fps())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(player1_bullet) < max_bullets:
                    bullet = pygame.Rect(
                        player_one.x + player_one.width - 30, player_one.y - player_one.height//2 + 92, 10, 5
                    )
                    player1_bullet.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(player2_bullet) < max_bullets:
                    bullet = pygame.Rect(
                        player_two.x, player_two.y + player_two.height//2 - 2, 10, 5 
                    )
                    player2_bullet.append(bullet)

            if event.type == player1_hit:
                player1_health -= 1

            if event.type == player2_hit:
                player2_health -= 1
        
        winner_text = ""
        if player1_health <= 0:
            winner_text = "Blue  Won!"
            

        if player2_health <= 0:
            winner_text = "Red  Won!"

        if winner_text != "":
            show_winner(winner_text)
            break
            
        
        pressed_key = pygame.key.get_pressed()

        player1_movement(pressed_key, player_one)
        player2_movement(pressed_key, player_two)

        handle_bullets(player1_bullet, player2_bullet, player_one, player_two)
        
        draw_window(player_one, player_two,  player1_bullet, player2_bullet, fps, player1_health, player2_health)

    pygame.quit()

if __name__ == "__main__":
    main()
