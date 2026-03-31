import os, time
import pygame
import numpy as np

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_NOMOUSE']     = '1'

pygame.init()
screen = pygame.display.set_mode((480, 320))
font = pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)

screen.fill((0, 0, 0))
text = font.render('Hello World', False, (255, 255, 255), (0, 0, 0))
rect = text.get_rect(center=(240, 160))
screen.blit(text, rect)

arr    = pygame.surfarray.array3d(screen).transpose(1, 0, 2)
arr    = np.rot90(arr, 2)  # software 180° flip (tft35a:rotate=90 is upside-down)
r      = arr[:, :, 0].astype(np.uint16)
g      = arr[:, :, 1].astype(np.uint16)
b      = arr[:, :, 2].astype(np.uint16)
rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

with open('/dev/fb0', 'wb') as fb:
    fb.write(rgb565.astype('<u2').tobytes())

time.sleep(30)
