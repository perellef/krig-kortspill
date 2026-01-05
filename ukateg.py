import pygame


# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 430
SCREEN_HEIGHT = 410

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 30


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("Tracking System")

# - objects -

bredde = 46
hoyde = 70
x = 0
y = 0

image = pygame.transform.scale(pygame.image.load(f"assets/bakside.png"),(bredde,hoyde))

positions = [(100,100),(100,200),(200,100),(200,200)]

def draw_pic(image,pos,dim):
    screen.blit(image, pos)
    if holding and pos == dim:
        pygame.draw.rect(screen, RED, pygame.Rect(pos[0],pos[1],bredde,hoyde),2)

def draw_screen(dim):
    screen.fill(WHITE)
    
    draw_pic(image,(100,100),dim)
    draw_pic(image,(100,200),dim)
    draw_pic(image,(200,100),dim)
    draw_pic(image,(200,200),dim)
    screen.blit(image, (x,y))

clock = pygame.time.Clock()

running = True
holding = False

while running:

    dim = (0,0)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  
            
            pekerOverBilde = all((
                mouse_x >= x,
                mouse_x <= x+bredde,
                mouse_y >= y,
                mouse_y <= y+hoyde,
            ))

            if pekerOverBilde:
            
                x = mouse_x - bredde//2
                y = mouse_y - hoyde//2

                holding = True
           

        if event.type == pygame.MOUSEBUTTONUP:
            holding = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if holding:
                x = mouse_x - bredde//2
                y = mouse_y - hoyde//2

            for dimx,dimy in [(100,100),(100,200),(200,100),(200,200)]:
                
                pekerOverAnnen = all((
                    mouse_x >= dimx,
                    mouse_x <= dimx+bredde,
                    mouse_y >= dimy,
                    mouse_y <= dimy+hoyde,
                ))
                if pekerOverAnnen:
                    dim = (dimx,dimy)

        draw_screen(dim)


    pygame.display.update()

    clock.tick(FPS)

pygame.quit()