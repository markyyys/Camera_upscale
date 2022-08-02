from start_data import *
class Button():
    def __init__(self, func, image, image2, x, y):
        self.func = func
        self.img = pygame.image.load(image).convert_alpha()
        self.img2 = pygame.image.load(image2).convert_alpha()
        self.IMAGE = self.img
        self.rect = self.IMAGE.get_rect()
        self.surf = pygame.Surface(self.rect.size)


        self.rect.x = x
        self.rect.y = y

    def call_back(self, *args):
        self.IMAGE = self.img2
        if self.func:
            return self.func(*args)
    def release(self):
        self.IMAGE = self.img
    def draw(self, screen):
        screen.blit(self.IMAGE, self.rect)

class CheckButton():
    def __init__(self, func, image, image2, x, y,):
        self.func = func
        self.img = pygame.image.load(image).convert_alpha()
        self.img2 = pygame.image.load(image2).convert_alpha()
        self.IMAGE = self.img
        self.rect = self.IMAGE.get_rect()
        self.surf = pygame.Surface(self.rect.size)
        self.rect.x = x
        self.rect.y = y
        self.checked = False

    def call_back(self, *args):
        if self.checked:
            self.IMAGE = self.img
            self.checked = False
        else:
            self.IMAGE = self.img2
            self.checked = True

        if self.func:
            return self.func(*args)

    def draw(self, screen):
        screen.blit(self.IMAGE, self.rect)

class TextBox:
    def __init__(self, image, image2, x, y):
        self.font = pygame.font.Font(None, 25)
        self.img = pygame.image.load(image).convert_alpha()
        self.img2 = pygame.image.load(image2).convert_alpha()
        self.IMAGE = self.img
        self.rect = self.IMAGE.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False
        self.text = ""
        self.surf = pygame.Surface(self.rect.size)

    def activate(self):
        self.active = True
        self.IMAGE = self.img2

    def de_activate(self):
        self.active = False
        if self.text == "":
            self.IMAGE = self.img

    def input(self, uni):
        self.text += uni
        if self.text != "":
            self.IMAGE = self.img2

    def backspace(self):
        self.text = self.text[:-1]
        if self.text == "":
            self.IMAGE = self.img

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, (245, 246, 250))
        screen.blit(txt_surface, (self.rect.x + self.rect.w//2 - txt_surface.get_width()//2, self.rect.y + self.rect.h//2 - txt_surface.get_height()//2))
        screen.blit(self.IMAGE, self.rect)
        return self.text