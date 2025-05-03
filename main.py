import sys
import random
import pygame
from pygame.locals import *

# ini gaeme

pygame.init()

''' IMAGES '''
player_ship = 'plyship.png'
enemy_ship = 'enemyship.png'
ufo_ship = 'ufo.png'
player_bullet = 'pbullet.png'
enemy_bullet = 'enemybullet.png'
ufo_bullet = 'enemybullet.png'

screen = pygame.display.set_mode((800, 900))  # Example size, adjust as needed
pygame.display.set_caption("My Game")
s_width, s_height = screen.get_size()

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
ufobullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()

pygame.mouse.set_visible(False)

class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([x, y])
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        self.rect.x += 1
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
        self.alive = True
        self.count_to_live = 0
        self.activ_bullet = True
        self.alpha_duration = 0

    def update(self):
        if self.alive:
            self.image.set_alpha(80)
            self.alpha_duration += 1
            if self.alpha_duration >= 170:
                self.image.set_alpha(255)
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0] - 20
            self.rect.y = mouse[1] + 40
        else:
            self.alpha_duration = 0 
            expl_x = self.rect.x + 20
            expl_y = self.rect.y + 40
            explosion = Explosion(expl_x, expl_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(25)
            self.rect.y = s_height + 200 
            self.count_to_live += 1
            if self.count_to_live > 100:
                self.count_to_live = 0
                self.alive = True
                self.activ_bullet = True

    def shoot(self):
        if self.activ_bullet:
            bullet = PlayerBullet(player_bullet)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.top = self.rect.top
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)

    def dead(self):
        self.alive = False
        self.activ_bullet = False

class Enemy(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(80, s_width-80)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(80, s_width-50)
            self.rect.y = random.randrange(-2000, 0)
        self.shoot()
        

    def shoot(self):
        if self.rect.y in (0, 30, 70, 300, 700):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x + 15
            enemybullet.rect.y = self.rect.y + 50
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)


class Ufo(Enemy):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -200
        self.rect.y = 200
        self.move = 1

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 200:
            self.move *= -1
        elif self.rect.x < -200:
            self.move *= -1
        self.shoot()

    def shoot(self):
        if self.rect.x % 50 == 0:
            ufobullet = EnemyBullet(ufo_bullet)
            ufobullet.rect.x = self.rect.x + 50
            ufobullet.rect.y = self.rect.y + 70
            ufobullet_group.add(ufobullet)
            sprite_group.add(ufobullet)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y -= 18
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)
        self.image.set_colorkey('white')


    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1, 6):
            img = pygame.image.load(f'exp{i}.png').convert()
            img.set_colorkey('black')
            img = pygame.transform.scale(img, (120, 120))
            self.img_list.append(img)
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0

    def update(self):
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill()

        

class Game:
    def __init__(self):
        self.count_hit = 0
        self.count_hit2 = 0
        self.hidup = 3
        self.score = 0

        self.run_game()

    def create_background(self):
        for i in range(20):
            x = random.randint(1, 5)
            background_image = Background(x, x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)

    def create_player(self):
        self.player = Player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy(self):
        for i in range(10):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)

    def create_ufo(self):
        for i in range(1):
            self.ufo = Ufo(ufo_ship)
            ufo_group.add(self.ufo)
            sprite_group.add(self.ufo)

    def playerbullet_hits_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group, playerbullet_group, False , True)
        for i in hits: 
            self.count_hit += 1
            if self.count_hit == 2:
                self.score += 10
                exp1_x = i.rect.x + 20
                exp1_y = i.rect.y + 40
                explosion = Explosion(exp1_x, exp1_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0
    
    def playerbullet_hts_ufo(self):
        hits = pygame.sprite.groupcollide(ufo_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit2 += 1
            if self.count_hit2 == 10:
                self.score += 50
                exp1_x = i.rect.x + 50
                exp1_y = i.rect.y + 60
                explosion = Explosion(exp1_x, exp1_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = -199
                self.count_hit2 = 0
        
        
    
    def enemybullet_hits_player(self):
        if self.player.image.get_alpha() == 255: 
            hits = pygame.sprite.spritecollide(self.player, enemybullet_group, True)
            if hits:
                self.hidup -= 1
                self.player.dead()
                if self.hidup < 0:
                    pygame.quit()
                    sys.exit()

    def ufobullet_hits_player(self):
        if self.player.image.get_alpha() == 255: 
            hits = pygame.sprite.spritecollide(self.player, ufobullet_group, True)
            if hits:
                self.hidup -= 2
                self.player.dead()
                if self.hidup < 0:
                    pygame.quit()
                    sys.exit()

    def player_enemy_crach(self):  
        if self.player.image.get_alpha() == 255: 
            hits = pygame.sprite.spritecollide(self.player, enemy_group, False)
            if hits:
                for i in  hits:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.hidup -= 1
                    self.player.dead()
                    if self.hidup < 0:
                        pygame.quit()
                        sys.exit()

    def player_ufo_crach(self):  
        if self.player.image.get_alpha() == 255: 
            hits = pygame.sprite.spritecollide(self.player, ufo_group, False)
            if hits:
                for i in  hits:
                    i.rect.x = -199
                    self.hidup -= 1
                    self.player.dead()
                    if self.hidup < 0:
                        pygame.quit()
                        sys.exit()

    def create_hidup(self):
        self.live_img = pygame.image.load(player_ship)
        self.live_img = pygame.transform.scale(self.live_img, (20, 22))
        n = 0
        for i in range(self.hidup):
            screen.blit(self.live_img, (0+n, s_height-890))
            n += 60


    def create_score(self):
        score = self.score
        font = pygame.font.SysFont('freesansbold.ttf', 32)
        text = font.render(str(score), True, 'white')
        text_rect = text.get_rect(center=(s_width-150, s_height-850))
        screen.blit(text, text_rect)

    

    def run_update(self):
        sprite_group.update()
        sprite_group.draw(screen)

    def run_game(self):
        self.create_background()
        self.create_player()
        self.create_enemy()
        self.create_ufo()
        while True:
            screen.fill('black')
            self.playerbullet_hits_enemy()
            self.playerbullet_hts_ufo()
            self.enemybullet_hits_player()
            self.ufobullet_hits_player()
            self.player_enemy_crach()
            self.player_ufo_crach()
            self.run_update()
            pygame.draw.rect(screen, 'black', (0,0,s_height,30))
            self.create_hidup()
            self.create_score()


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.player.shoot()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            clock.tick(FPS)

def main():
    game = Game()

if __name__ == '__main__':
    main()