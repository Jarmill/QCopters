import pygame

pygame.init()
screen = pygame.display.set_mode((400,300))
done = False
is_blue = True
clock = pygame.time.Clock()

x = 30
y = 30

while not done:
    for event in pygame.event.get():
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        
        if event.type == pygame.QUIT:
            done = True
            print "CLOSING!"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
            print "ESCAPING!"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
            print "CHANGING!"

        screen.fill((0,0,0))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3

        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
        

    clock.tick(60)

    pygame.display.flip()

#be IDLE friendly
pygame.quit()
