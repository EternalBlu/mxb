import pygame
import random
from sys import exit

pygame.init()
disp_size = (500, 500)
disp = pygame.display.set_mode(disp_size)
pygame.display.set_caption("mx + b")
points = 0

black = (0, 0, 0)
white = (255, 255, 255)

slope = (500, 200)

font = pygame.font.SysFont("microsoftsansserif", 60)
text = font.render("Retry", True, black)
text_rect = text.get_rect()
text_rect.center = (disp_size[0] // 2, disp_size[1] // 2)

score = font.render(str(points), True, white)
score_rect = score.get_rect()
score_rect[0] = 10
score_rect[1] = 10



class Slope:
  def __init__(self):
    self.shape = ((0, 300), (500, 500), (0, 500))
    pygame.draw.polygon(disp, white, self.shape)
    pygame.display.flip

  def update(self):
    pygame.draw.polygon(disp, white, self.shape)



class Player:
  def __init__(self, size):
    self.y_vel = 0
    self.x = 150
    self.y = 360 - size
    self.size = size
    self.hitbox = pygame.Rect(self.x, self.y, size, size)
    pygame.draw.circle(disp, white, (self.x, self.y), size)
    

  def update(self):
    if self.y >= 360 - self.size:
      self.y_vel = 0
      self.y = 360 - self.size
   
    else:
      self.y_vel += 0.05
    self.y += self.y_vel
    self.hitbox.center = (self.x, self.y)
    pygame.draw.circle(disp, white, (self.x, self.y), self.size)



class Spike:
  def __init__(self, multiplier):
    self.p1 = [510, 510]
    self.p2 = [500, 450]
    self.p3 = [450, 490]
    self.hitbox = pygame.Rect(475, 475, 25, 25)
    self.multiplier = multiplier
    pygame.draw.polygon(disp, white, (self.p1, self.p2, self.p3))


  def update(self):
    self.p1[0] -= 1 * self.multiplier
    self.p1[1] -= (200 / 500) * self.multiplier
    self.p2[0] -= 1 * self.multiplier
    self.p2[1] -= (200 / 500) * self.multiplier
    self.p3[0] -= 1 * self.multiplier
    self.p3[1] -= (200 / 500) * self.multiplier
    self.hitbox[0] = self.p3[0] + 25
    self.hitbox[1] = self.p3[1] - 20
    pygame.draw.polygon(disp, white, (self.p1, self.p2, self.p3))



class RetryButton:
  def __init__(self):
    self.button = pygame.Rect(0, 0, 200, 100)
    self.button.center = (disp_size[0] // 2, disp_size[1] // 2)
    pygame.draw.rect(disp, white, self.button, width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1)


  def update(self):
    pygame.draw.rect(disp, white, self.button, width=0, border_radius=20, border_top_left_radius=-10, border_top_right_radius=-10, border_bottom_left_radius=-10, border_bottom_right_radius=-10)
    disp.blit(text, text_rect)


slope = Slope()
retry_button = RetryButton()
player = Player(30)
spikes = []
multiplier = 1
alive = True


def game_actions(alive):
  events = pygame.event.get()
  disp.blit(score, score_rect)
  
  for event in events:
    keys = pygame.key.get_pressed()

    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    
    if alive:
      if keys[pygame.K_w] and player.y == 360 - player.size:
        player.y -= 1
        player.y_vel = -4
      
      if keys[pygame.K_s]:
          player.y_vel = 10
  
running = True

while running:
  
  disp.fill(black)

  for spike in spikes:
    if pygame.Rect.colliderect(player.hitbox, spike.hitbox):
      alive = False
      for spike in spikes:
        spike.multiplier = 0

  game_actions(alive)

  if alive:
    if random.randrange(1, 400) == 45:
      spikes.append(Spike(multiplier))

  else:
    retry_button.update()
    if pygame.Rect.collidepoint(retry_button.button, pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
      spikes = []
      multiplier = 1
      points = 0
      score = font.render(str(points), True, white)
      alive = True
  


  for spike in spikes:
    try:
      spike.update()
      
      if spike.p1[0] < 0:
        spikes.remove(spike)
        multiplier += 0.05
        points += 1
        score = font.render(str(points), True, white)
    
    except:
      pass

  slope.update()
  player.update()
    
  pygame.time.wait(4)
  pygame.display.flip()