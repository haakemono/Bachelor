import pygame
import ui.main_menu as main_menu

WIDTH, HEIGHT = 640, 480

USERNAME = "asd"
PASSWORD = "123"

def run_login_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Launcher - Login")

    font = pygame.font.SysFont(None, 36)

    input_box_user = pygame.Rect(200, 150, 240, 40)
    input_box_pass = pygame.Rect(200, 220, 240, 40)
    login_button = pygame.Rect(250, 300, 140, 40)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_button = pygame.Color('green')

    user_text = ''
    pass_text = ''
    active_input = None

    clock = pygame.time.Clock()
    while True:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse clicked at {event.pos}")
                if input_box_user.collidepoint(event.pos):
                    print("Username box selected")
                    active_input = 'user'
                elif input_box_pass.collidepoint(event.pos):
                    print("Password box selected")
                    active_input = 'pass'
                elif login_button.collidepoint(event.pos):
                    print("Login button clicked")
                    if user_text == USERNAME and pass_text == PASSWORD:
                        print("Login successful")
                        main_menu.run_main_menu()
                        return
                    else:
                        print("Incorrect username or password")

            elif event.type == pygame.KEYDOWN:
                if active_input == 'user':
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                elif active_input == 'pass':
                    if event.key == pygame.K_BACKSPACE:
                        pass_text = pass_text[:-1]
                    else:
                        pass_text += event.unicode

        # Draw input boxes and text
        pygame.draw.rect(screen, color_active if active_input == 'user' else color_inactive, input_box_user)
        pygame.draw.rect(screen, color_active if active_input == 'pass' else color_inactive, input_box_pass)
        pygame.draw.rect(screen, color_button, login_button)

        screen.blit(font.render("Username:", True, (255, 255, 255)), (100, 155))
        screen.blit(font.render(user_text, True, (0, 0, 0)), (input_box_user.x + 5, input_box_user.y + 5))

        screen.blit(font.render("Password:", True, (255, 255, 255)), (100, 225))
        screen.blit(font.render("*" * len(pass_text), True, (0, 0, 0)), (input_box_pass.x + 5, input_box_pass.y + 5))

        screen.blit(font.render("Login", True, (255, 255, 255)), (login_button.x + 35, login_button.y + 5))

        pygame.display.flip()
        clock.tick(30)