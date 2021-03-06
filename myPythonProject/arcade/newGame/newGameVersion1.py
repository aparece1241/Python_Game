import arcade
import threading
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NEW GAME"


class Button():
    def __init__(self, center_x, center_y, width, height,
                 color, text, function, text_color, tilt_angle=0):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.defualt = color
        self.shadow_color1 = arcade.color.DARK_GRAY
        self.shadow_color2 = arcade.color.WHITE
        self.text = text
        self.text_color = text_color
        self.function = function

    def draw_button(self):
        textLenght = len(self.text)
        deducX = 25
        if textLenght == 5:
            deducX = 25
        elif textLenght > 5:
            times = textLenght - 5
            while times > 0:
                deducX += 5
                times -= 1
        else:
            times = 5 - textLenght
            while times > 0:
                deducX -= 5
                times -= 1

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)
        arcade.draw_text_2(self.text, (self.center_x - deducX), (self.center_y - self.height * 0.15), self.text_color,
                           font_size=15)
        # Top
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         self.shadow_color1, 2)
        # Left
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.shadow_color1, 2)
        # Right
        arcade.draw_line(self.center_x + self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.shadow_color1, 2)
        # buttom
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.shadow_color1, 2)

    def on_press(self):
        self.shadow_color2 = arcade.color.DARK_GRAY
        self.shadow_color1 = arcade.color.WHITE
        self.color = (188, 190, 194)

    def on_release(self):
        self.shadow_color1 = arcade.color.DARK_GRAY
        self.shadow_color2 = arcade.color.WHITE
        self.color = self.defualt

    def check_mouse_press(self, x, y):
        if x > self.center_x - self.width / 2 and x < self.center_x + self.width / 2:
            if y > self.center_y - self.height / 2 and y < self.center_y + self.height / 2:
                self.on_press()

    def check_mouse_release(self, x, y):
        if x > self.center_x - self.width / 2 and x < self.center_x + self.width / 2:
            if y > self.center_y - self.height / 2 and y < self.center_y + self.height / 2:
                self.function()
                self.on_release()


def Start():
    Window.show_view(StartGame())


class MainMenu(arcade.View):
    Play = Button(305, 260, 150, 50,
                  arcade.color.AVOCADO, "Play",
                  Start, arcade.color.GREEN)
    Help = Button(390, 200, 150, 50,
                  arcade.color.AVOCADO, "Help"
                  , None, arcade.color.GREEN)
    Heroes = Button(485, 260, 150, 50,
                    arcade.color.AVOCADO, "Heroes",
                    None, arcade.color.GREEN)
    backdrop1 = arcade.Sprite("../../SpriteLists/zombie.png"
                              , center_x=400, center_y=400, scale=0.8)
    hero = arcade.Sprite("../../SpriteLists/hero.page.png"
                         , center_x=680, center_y=200)
    zombie = arcade.Sprite("../../SpriteLists/zombie.page.png"
                           , center_x=150, center_y=150)
    background = arcade.SpriteList()
    button_list = []
    back = arcade.load_texture("../image/head.png")

    def on_show(self):
        arcade.set_background_color(arcade.color.BISTRE_BROWN)
        self.button_list.append(self.Play)
        self.button_list.append(self.Help)
        self.button_list.append(self.Heroes)
        self.background.append(self.hero)
        self.background.append(self.backdrop1)
        self.background.append(self.zombie)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.back)
        self.Play.draw_button()
        self.Help.draw_button()
        self.Heroes.draw_button()
        self.background.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for i in self.button_list:
            i.check_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        for i in self.button_list:
            i.check_mouse_release(x, y)




class Barrier():
    def __init__(self, x, y):
        self.barrier_list_up = arcade.SpriteList()
        self.barrier_list_down = arcade.SpriteList()
        self.barrier_list_up.append(arcade.Sprite("../../SpriteLists/barrier.png", center_x=25, center_y=y))
        for i in range(0, int(SCREEN_WIDTH / 50) + 4):
            barrier = arcade.Sprite("../../SpriteLists/barrier.png", center_x=25 + (i * 41.6), center_y=y)
            self.barrier_list_up.append(barrier)
            barrier1 = arcade.Sprite("../../SpriteLists/barrier.png", center_x=25 + (i * 41.6), center_y=20)
            self.barrier_list_down.append(barrier1)

    def draw_wall_up(self):
        self.barrier_list_up.draw()

    def draw_wall_down(self):
        self.barrier_list_down.draw()

    def getWalllistUp(self):
        return self.barrier_list_up[0].center_y

    def getWalllistDown(self):
        return self.barrier_list_down[0].center_y


class hero():

    def __init__(self, life, name):
        self.lifePoints = life
        self.name = name
        self.direction = None
        self.movementSpeed = 5

        self.hero = arcade.AnimatedWalkingSprite()
        self.hero_list = arcade.SpriteList()

        self.hero.stand_right_textures = []
        self.hero.stand_left_textures = []
        self.hero.walk_right_textures = []
        self.hero.walk_left_textures = []
        self.hero.stand_right_textures.append(arcade.load_texture("../../SpriteLists/hero.walk.0.png"))
        self.hero.stand_left_textures.append(arcade.load_texture("../../SpriteLists/hero.walk.0.png", mirrored=True))

        self.bullet_direction = "RIGHT"
        for i in range(0, 5):
            self.hero.walk_right_textures.append(arcade.load_texture(f"../../SpriteLists/hero.walk.{i}.png"))
            self.hero.walk_left_textures.append(
                arcade.load_texture(f"../../SpriteLists/hero.walk.{i}.png", mirrored=True))
        self.hero.scale = 0.3
        self.hero.center_x = SCREEN_WIDTH // 2
        self.hero.center_y = SCREEN_HEIGHT * 0.15
        self.hero.texture_change_frames = 70

        self.hero_list.append(self.hero)
        self.hero_bullet = arcade.SpriteList()

    def move(self):
        if self.direction == "LEFT":
            self.hero.change_x = -self.movementSpeed
            self.hero.change_y = 0
            self.bullet_direction = self.direction
        if self.direction == "RIGHT":
            self.hero.change_x = self.movementSpeed
            self.hero.change_y = 0
            self.bullet_direction = self.direction
        if self.direction == "DOWN":
            self.hero.change_y = -self.movementSpeed
            self.hero.change_x = 0
        if self.direction == "UP":
            self.hero.change_y = self.movementSpeed
            self.hero.change_x = 0

    def update_hero(self):
        self.hero_list.update()
        self.hero_list.update_animation()

    def draw_hero(self):
        self.update_hero()
        self.hero_list.draw()

    def setDirection(self, newDirection):
        self.direction = newDirection

    def setSpeed(self, newSpeed):
        self.movementSpeed = newSpeed

    def getHeroY(self):
        return self.hero.center_y

    def getHeroX(self):
        return self.hero.center_x

    def hero_attact(self):
        bullet = arcade.Sprite("../../SpriteLists/bullet.png")
        bullet.scale = 0.3

        bullet.change_x = -5
        bullet.center_x = self.hero.left
        bullet.center_y = self.hero.center_y
        if self.bullet_direction == "RIGHT":
            bullet.angle = 180
            bullet.center_x = self.hero.right
            bullet.change_x = 5

        self.hero_bullet.append(bullet)

    def bulletUpadate(self):
        self.hero_bullet.update()

    def bulletDraw(self):
        self.hero_bullet.draw()

    def bulletCheck(self):
        for bullet in self.hero_bullet:
            if bullet.center_x < 0 or bullet.center_x > SCREEN_WIDTH:
                bullet.kill()

    def getBullets(self):
        return self.hero_bullet


class Enemy():
    def __init__(self, lifePoints, name, lowerBarrier, upperBarrier):
        self.name = name
        self.lifePoints = lifePoints
        self.lower = lowerBarrier
        self.upper = upperBarrier
        self.enemy = arcade.AnimatedTimeSprite()

        enemy = arcade.AnimatedTimeSprite()
        for i in range(0, 8):
            enemy.textures.append(arcade.load_texture(f"../../SpriteLists/z{i}.png"))
        enemy.center_x = 10
        enemy.center_y = random.randrange(self.lower + 20, self.upper - 20)
        enemy.scale = 0.3
        enemy.change_x = 0.5
        self.enemy1 = enemy

    def enemyUpdate(self):
        self.enemy1.update()
        self.enemy1.update_animation()

    def setXlocation(self,newX):
        self.enemy1.center_x = newX

    def drawEnemy(self):
        self.enemy1.draw()







class StartGame(arcade.View):
    Hero = hero(100, "Zkiller")
    Barriers = Barrier(25, 341)
    backdrop = arcade.load_texture("../../SpriteLists/backdrop.png")
    direction = ""
    valueFor = 5
    valueForX = 5
    wave = 1
    score = 0
    enemyList = []

    def setupHeroBoundary(self, lowerYbarrier, upperYbarrier, heroY, leftXbarrier, rightXbarrier, heroX):
        """ partial """
        if heroY > upperYbarrier:
            self.valueFor = 0
            if self.direction == "DOWN":
                self.Hero.setSpeed(self.valueForX)
                self.valueFor = 5
            if self.direction == "UP":
                self.Hero.setSpeed(self.valueFor)

        if heroY < lowerYbarrier + 50:
            self.valueFor = 0
            if self.direction == "UP":
                self.valueFor = 5
                self.Hero.setSpeed(self.valueForX)
            if self.direction == "DOWN":
                self.Hero.setSpeed(self.valueFor)

        if heroX > rightXbarrier:
            self.valueForX = 0
            if self.direction == "LEFT":
                self.Hero.setSpeed(self.valueFor)
                self.valueForX = 5
            if self.direction == "RIGHT":
                self.Hero.setSpeed(self.valueForX)

        if heroX < leftXbarrier:
            self.valueForX = 0
            if self.direction == "RIGHT":
                self.valueForX = 5
                self.Hero.setSpeed(self.valueFor)
            if self.direction == "LEFT":
                self.Hero.setSpeed(self.valueForX)


    def on_show(self):
        arcade.set_background_color((123, 156, 24, 255))


    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.backdrop)
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 100, (127, 212, 23, 127))
        arcade.draw_text_2(f"score:{self.score}", 100, SCREEN_HEIGHT - 100, arcade.color.WHITE, 15, align="center")
        self.Barriers.draw_wall_up()
        self.Hero.draw_hero()
        self.Barriers.draw_wall_down()
        self.Hero.bulletDraw()

    def on_key_press(self, key, modifier):
        if key == arcade.key.LEFT:
            self.Hero.setDirection("LEFT")
            self.Hero.setSpeed(self.valueForX)
            self.direction = "LEFT"
        if key == arcade.key.RIGHT:
            self.Hero.setDirection("RIGHT")
            self.Hero.setSpeed(self.valueForX)
            self.direction = "RIGHT"
        if key == arcade.key.DOWN:
            self.Hero.setDirection("DOWN")
            self.Hero.setSpeed(self.valueFor)
            self.direction = "DOWN"
        if key == arcade.key.UP:
            self.Hero.setDirection("UP")
            self.Hero.setSpeed(self.valueFor)
            self.direction = "UP"
        if key == arcade.key.A:
            self.Hero.hero_attact()

    def on_key_release(self, key, modifier):
        self.Hero.setSpeed(0)

    def on_update(self, delta_time):
        self.Hero.update_hero()
        self.Hero.move()
        self.setupHeroBoundary(self.Barriers.getWalllistDown(),
                               self.Barriers.getWalllistUp(),
                               self.Hero.getHeroY(), 50, SCREEN_WIDTH - 50,
                               self.Hero.getHeroX())

        self.Hero.bulletUpadate()

        self.Hero.bulletCheck()

        '''change = False 

        left = self.LEFT_Boundary + self.x_View
        right = self.RIGHT_Boundary + self.x_View

        if self.sprite1.center_x < left:
            self.x_View = self.x_View - self.movement_speed
            left = self.LEFT_Boundary - self.x_View
            right = self.RIGHT_Boundary - self.x_View
            change = True

        if self.sprite1.center_x > (right-25):
            self.x_View = self.x_View + self.movement_speed
            left = self.LEFT_Boundary - self.x_View
            change = True

        if change:
            arcade.set_viewport(self.x_View,SCREEN_WIDTH + self.x_View,0,SCREEN_HEIGHT)'''


Window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
Window.show_view(MainMenu())
arcade.run()


