from start_data import *
from frame_processing import FrameProccessing
from ui_parts import Button, CheckButton, TextBox
from PIL import Image
from firebase_auth import *
import random
import numpy as np
import pygame
from main import *
from numba import jit
import cv2
import multiprocessing
from PIL import Image


class Window:
    def __init__(self):
        self.pygame = pygame.init()
        self.bg_img = pygame.image.load("ui_parts/Bg.png")
        self.bg_rect = self.bg_img.get_rect()
        self.name_img = pygame.image.load("ui_parts/Name.png")
        self.name_rect = self.bg_img.get_rect()
        self.substr_img = pygame.image.load("ui_parts/WhiteSubstr.png")
        self.substr_rect = self.bg_img.get_rect()
        self.running = True
        self.auth_running = True
        self.font = pygame.font.Font(None, 34)
        pygame.init()

        self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("AIWatcher")
        self.clock = pygame.time.Clock()
        self.iters = 4
        self.face_rect = False
        self.state = "in"
        self.mode = False
        self.sign_in_data = ["", ""]
        self.sign_up_data = ["", "", ""]

    def sign_in(self):
        self.state = "in"
        self.s_up.IMAGE = self.s_up.img
        self.s_in.IMAGE = self.s_in.img

    def sign_up(self):
        self.state = "up"
        self.s_in.IMAGE = self.s_in.img2
        self.s_up.IMAGE = self.s_up.img2

    def auth_state(self):
        self.bg_rect.x = -80
        self.bg_rect.y = -17
        self.name_rect.x = 50
        self.name_rect.y = 50

        text_boxes_in = []
        text_boxes_in.append(TextBox("ui_parts/TextBoxLogin.png", "ui_parts/TextBox.png", 50, 220))
        text_boxes_in.append(TextBox("ui_parts/TextBoxPassword.png", "ui_parts/TextBox.png", 50, 284))
        text_boxes_up = []
        text_boxes_up.append(TextBox("ui_parts/TextBoxLogin.png", "ui_parts/TextBox.png", 50, 220))
        text_boxes_up.append(TextBox("ui_parts/TextBoxPassword.png", "ui_parts/TextBox.png", 50, 284))
        text_boxes_up.append(TextBox("ui_parts/TextBoxPassword.png", "ui_parts/TextBox.png", 50, 348))

        self.s_in = Button(self.sign_in, "ui_parts/SignInPressed.png", "ui_parts/SignInUnpressed.png", 50, 150)
        self.s_up = Button(self.sign_up, "ui_parts/SignUpUnpressed.png", "ui_parts/SignUpPressed.png", 200, 150)

        self.enter = Button(self.auth, "ui_parts/EnterUnpressed.png", "ui_parts/EnterPressed.png", 87,
                            284 + 59 * 2 + 5 * 2)

        while self.running and self.auth_running:
            pygame.display.flip()

            self.screen.fill((47, 54, 64))
            self.screen.blit(self.bg_img, self.bg_rect)
            self.screen.blit(self.name_img, self.name_rect)

            self.s_in.draw(self.screen)
            self.s_up.draw(self.screen)
            self.enter.draw(self.screen)

            if self.state == "in":
                self.sign_in_data[0] = text_boxes_in[0].draw(self.screen)
                self.sign_in_data[1] = text_boxes_in[1].draw(self.screen)
            if self.state == "up":
                self.sign_up_data[0] = text_boxes_up[0].draw(self.screen)
                self.sign_up_data[1] = text_boxes_up[1].draw(self.screen)
                self.sign_up_data[2] = text_boxes_up[2].draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.s_in.rect.collidepoint(pos):
                            self.s_in.call_back()
                        if self.s_up.rect.collidepoint(pos):
                            self.s_up.call_back()
                        if self.enter.rect.collidepoint(pos):
                            self.enter.call_back()
                        if self.state == "in":
                            for t in text_boxes_in:
                                if t.rect.collidepoint(pos):
                                    t.activate()
                                else:
                                    t.de_activate()
                        elif self.state == "up":
                            for t in text_boxes_up:
                                if t.rect.collidepoint(pos):
                                    t.activate()
                                else:
                                    t.de_activate()

                if event.type == pygame.KEYDOWN:
                    for t in text_boxes_in:
                        if t.active:
                            if event.key == pygame.K_BACKSPACE:
                                t.backspace()
                            else:
                                t.input(event.unicode)
                    for t in text_boxes_up:
                        if t.active:
                            if event.key == pygame.K_BACKSPACE:
                                t.backspace()
                            else:
                                t.input(event.unicode)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        try:
                            self.enter.release()
                        except AttributeError:
                            continue

    def auth(self):
        if self.state == "in":
            if login(self.sign_in_data[0], self.sign_in_data[1]):
                self.auth_running = False
            else:
                return
        elif self.state == "up":
            if self.sign_up_data[1] == self.sign_up_data[2]:
                if signup(self.sign_up_data[0], self.sign_up_data[1]):
                    self.auth_running = False
                else:
                    return
            else:
                return

    def main_state(self):
        button_list = []
        self.substr_rect.x = 1600 - 60 - 277
        self.substr_rect.y = 100
        self.bg_rect.x = 1200 - 34
        self.bg_rect.y = -17
        fp = FrameProccessing()
        button_list.append(
            Button(self.iters_minus, "ui_parts/LeftUnpressed.png", "ui_parts/LeftPressed.png", 1600 - 60 - 277, 100))
        button_list.append(
            Button(self.iters_plus, "ui_parts/RightUnpressed.png", "ui_parts/RightPressed.png", 1600 - 60 - 64, 100))
        button_list.append(
            CheckButton(self.face_rect_set, "ui_parts/Check.png", "ui_parts/CheckChecked.png", 1600 - 60 - 277, 200))
        btn_switch = Button(self.mode_switch, "ui_parts/OnlyCamUnpressed.png", "ui_parts/OnlyCamPressed.png",
                            1200 - 147, 900 - 61)
        btn_switch2 = Button(self.mode_switch, "ui_parts/OnlyCamUnpressed.png", "ui_parts/OnlyCamPressed.png",
                             1200 - 147 + 200, 900 - 61)
        while self.running:
            pygame.display.flip()
            self.screen.fill((47, 54, 64))

            self.screen.blit(self.bg_img, self.bg_rect)
            self.screen.blit(self.substr_img, self.substr_rect)
            txt_iters = self.font.render(str(self.iters), True, (245, 246, 250))
            self.screen.blit(txt_iters, (1600 - 60 - 277 + 130, 100 + 16))
            txt_iters_desc = self.font.render("Level of neural layers", True, (245, 246, 250))
            self.screen.blit(txt_iters_desc, (1600 - 60 - 277, 100 - 20))
            txt_rect_desc = self.font.render("Show face borders", True, (245, 246, 250))
            self.screen.blit(txt_rect_desc, (1600 - 60 - 277 + 35 + 10, 200 + 8))

            if self.mode:
                self.screen.fill((47, 54, 64))
                self.camera(fp, 200)
                btn_switch2.draw(self.screen)

            else:
                for b in button_list:
                    b.draw(self.screen)

                self.camera(fp, 0)
                btn_switch.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for b in button_list:
                            if b.rect.collidepoint(pos):
                                b.call_back()
                        if btn_switch.rect.collidepoint(pos):
                            btn_switch.call_back()
                        if btn_switch2.rect.collidepoint(pos):
                            btn_switch2.call_back()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for b in button_list:
                            try:
                                b.release()
                                btn_switch.release()
                                btn_switch2.release()
                            except AttributeError:
                                continue

    def iters_plus(self):
        self.iters += 1

    def iters_minus(self):
        if self.iters > 1:
            self.iters -= 1

    def face_rect_set(self):
        self.face_rect = not self.face_rect

    def mode_switch(self):
        self.mode = not self.mode

    def camera(self, fp, _x):
        img = fp.get_camera_frame()
        img = fp.image_filtering(img)
        faces = fp.face_detection(img)
        segs = fp.face_segmentation(faces, 50)
        img = fp.face_upscale(img, segs, self.iters)
        img = fp.image_sizing(img)
        faces = fp.face_detection(img)
        img_done = Image.fromarray(img)
        self.screen.blit(pygame.image.fromstring(img_done.tobytes(), img_done.size, img_done.mode).convert(), (_x, 0))
        if self.face_rect:
            for (y, x, w, h) in faces:
                pygame.draw.rect(self.screen, (255, 255, 255), (_x + y, x, w, h), 1)
