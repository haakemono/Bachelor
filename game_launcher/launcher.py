import ui.log_inn as login_screen
import pygame

class GameLauncherApp:
    def __init__(self):
        pygame.init()
        self.running = True

    def run(self):
        # Start the application with the login screen
        login_screen.run_login_screen()

if __name__ == "__main__":
    app = GameLauncherApp()
    app.run()