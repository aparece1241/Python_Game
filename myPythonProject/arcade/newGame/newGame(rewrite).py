from tkinter import *
import arcade
import random
import json
import os


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NEW GAME"
FIRTTIME_RUN = True


gamedata = [{"name" : "", "score" : 0 ,"waves" : 0 },
            {"name" : "", "score" : 0 ,"waves" : 0 },
            {"name" : "", "score" : 0 ,"waves" : 0 },
            {"name" : "", "score" : 0 ,"waves" : 0 },
            {"name" : "", "score" : 0 ,"waves" : 0 }
            ]
NAME = ""
DATAS = ""


def readFile():
    with open("gameData.txt", "r") as read:
        data = json.load(read)
        return data


def writeFile(data= gamedata):
    with open("gameData.txt", "w") as create:
        json.dump(data, create)


def CheckFileExist():
    if os.path.exists("gameData.txt"):
        global DATAS
        DATAS = readFile()
    else:
        writeFile()


CheckFileExist()


def getValue(Pop_up,UserInput):
    global NAME
    NAME = UserInput.get()
    Pop_up.destroy()

def get_input():
    Pop_up = Tk()
    Pop_up.title("Input")
    Pop_up.resizable = False
    L1 = Label(Pop_up, text="Enter your name")
    L1.place(x=55, y=80)
    L2 = Label(Pop_up, text="To Start The Game please")
    L2.place(x=36, y=20)
    E1 = Entry(Pop_up, fg="green")
    E1.place(x=40, y=100)
    B1 = Button(Pop_up, text="submit", command=lambda: getValue(Pop_up,E1))
    B1.place(x=70, y=120)
    Pop_up.mainloop()

get_input()

class Record():



    def getHighScore(self,score,wave):
        for data in DATAS:
            print(data["score"])
            if data["score"] < score:
                data["name"] = NAME
                data["score"] = score
                data["waves"] = wave
                print("data :",DATAS)
                writeFile(DATAS)
                readFile()
                break






class Buttons():
    def __init__(self,center_x,center_y,width,height,
                 color,text,function,text_color,tilt_angle = 0):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = color
        self.defualt = color
        self.shadow_color1 = arcade.color.DARK_GRAY
        self.shadow_color2 =arcade.color.WHITE
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
        
        arcade.draw_rectangle_filled(self.center_x,self.center_y,self.width,self.height,self.color)
        arcade.draw_text_2(self.text,(self.center_x - deducX),(self.center_y - self.height * 0.15),self.text_color,font_size = 15)
        #Top
        arcade.draw_line(self.center_x - self.width/2,self.center_y + self.height/2,
                         self.center_x + self.width/2,self.center_y + self.height/2,
                         self.shadow_color1,2)
        #Left
        arcade.draw_line(self.center_x - self.width/2,self.center_y + self.height/2,
                         self.center_x - self.width/2,self.center_y - self.height/2,
                         self.shadow_color1,2)
        #Right
        arcade.draw_line(self.center_x + self.width/2,self.center_y + self.height/2,
                         self.center_x + self.width/2,self.center_y - self.height/2,
                         self.shadow_color1,2)
        #buttom
        arcade.draw_line(self.center_x - self.width/2,self.center_y - self.height/2,
                         self.center_x + self.width/2,self.center_y - self.height/2,
                         self.shadow_color1,2)

    def draw_circle_button(self):
        pass
        
        
    def on_press(self):
        self.shadow_color2 = arcade.color.DARK_GRAY
        self.shadow_color1 = arcade.color.WHITE
        self.color = (188, 190, 194)
    def on_release(self):
        self.shadow_color1 = arcade.color.DARK_GRAY
        self.shadow_color2 = arcade.color.WHITE
        self.color = self.defualt

    def check_mouse_press(self,x,y):
        if x > self.center_x - self.width/2 and x < self.center_x + self.width/2 :
            if y > self.center_y - self.height/2 and y < self.center_y + self.height/2 :
                self.on_press()
    def check_mouse_release(self,x,y):
        if x > self.center_x - self.width/2 and x < self.center_x + self.width/2 :
            if y > self.center_y - self.height/2 and y < self.center_y + self.height/2 :
                self.on_release()
                if self.function != None:
                    self.function()



def Start():
    Window.show_view(StartGame())

def Main():
    Window.show_view(MainMenu())

def Instruct():
    Window.show_view(Introduction())

def Exit():
    exit()


class GameOver(arcade.View):
    Back = Buttons(400, 150, 120, 50, arcade.color.GRAY, "Back", Main, arcade.color.BLACK)
    Replay = Buttons(SCREEN_WIDTH - 400, 150, 120, 50, arcade.color.GRAY, "Replay", Start, arcade.color.BLACK)
    Button_list = []
    def on_show(self):
        arcade.set_background_color(arcade.color.AVOCADO)
        self.Button_list.append(self.Back)
        self.Button_list.append(self.Replay)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text_2("Game Over!", 320, SCREEN_HEIGHT/2, arcade.color.BLACK, 40, bold=True)
        self.Back.draw_button()
        self.Replay.draw_button()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for button in self.Button_list:
            button.check_mouse_press(x,y)
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        for button in self.Button_list:
            button.check_mouse_release(x,y)

class Introduction(arcade.View):
    back = Buttons(100, 80, 100, 50, arcade.color.GRAY, "Back", Main, arcade.color.WHITE)
    play = Buttons(SCREEN_WIDTH - 100, 80, 100, 50, arcade.color.GRAY, "Play", Start, arcade.color.WHITE)
    arrowButtonList = []
    def messageDisplay(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT/2,500,420,(110,100,20,50))
        arcade.draw_text_2("Controls :", 300, 470, arcade.color.WHITE, 20)
        arcade.draw_text_2("To move your hero use the", 300, 420, arcade.color.WHITE, 20)
        arcade.draw_text_2("arrow keys. ", 300, 370, arcade.color.WHITE, 20)
        arcade.draw_text_2("To attack use the 'A' key to attack", 300, 320, arcade.color.WHITE, 20)
        arcade.draw_text_2("Goal :", 300, 270, arcade.color.WHITE, 20)
        arcade.draw_text_2( "Dont be killed !!!", 300, 220, arcade.color.WHITE, 20)

    def on_show (self):
        arcade.set_background_color(arcade.color.AVOCADO)
        self.arrowButtonList.append(self.play)
        self.arrowButtonList.append(self.back)

    def on_draw (self):
        arcade.start_render()
        self.play.draw_button()
        self.back.draw_button()
        arcade.draw_text_2("User Guide", 425, 550, arcade.color.BLACK, 20, bold=True)
        self.messageDisplay()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for button in self.arrowButtonList:
            button.check_mouse_press(x,y)
    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        for button in self.arrowButtonList:
            button.check_mouse_release(x,y)




class MainMenu(arcade.View):

        
    Play = Buttons(305,260,150,50,
    arcade.color.AVOCADO,"Play",
    Instruct,arcade.color.GREEN)
    Exits = Buttons(390,200,150,50,
    arcade.color.AVOCADO,"Exit"
    ,Exit,arcade.color.GREEN)
    Heroes = Buttons(485,260,150,50,
    arcade.color.AVOCADO,"Heroes",
    None,arcade.color.GREEN)
    backdrop1 = arcade.Sprite("../../SpriteLists/zombie.png"
    ,center_x = 400,center_y = 400,scale = 0.8)
    hero = arcade.Sprite("../../SpriteLists/hero.page.png"
    ,center_x = 680,center_y = 200)
    zombie = arcade.Sprite("../../SpriteLists/zombie.page.png"
    ,center_x = 150,center_y = 150)
    background = arcade.SpriteList()
    button_list = []
    back = arcade.load_texture("../image/head.png")
    
    def on_show(self):
        arcade.set_background_color(arcade.color.BISTRE_BROWN)
        self.button_list.append(self.Play)
        self.button_list.append(self.Exits)
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
        self.Exits.draw_button()
        self.Heroes.draw_button()
        self.background.draw()

    def on_mouse_press(self,x,y,button,modifiers):
        for i in self.button_list:
            i.check_mouse_press(x,y)
            
    def on_mouse_release(self,x,y,button,modifiers):
        for i in self.button_list: 
            i.check_mouse_release(x,y)

    

class hero():

    def __init__(self,life,name):
        self.lifePoints = life
        self.name = name
        self.direction = None
        self.movementSpeed = 5
        self.bullet_damage = 20
        
        self.hero = arcade.AnimatedWalkingSprite()
        self.hero_list = arcade.SpriteList()

        self.hero.stand_right_textures = []
        self.hero.stand_left_textures = []
        self.hero.walk_right_textures = []
        self.hero.walk_left_textures = []
        self.hero.stand_right_textures.append(arcade.load_texture("../../SpriteLists/hero.walk.0.png"))
        self.hero.stand_left_textures.append(arcade.load_texture("../../SpriteLists/hero.walk.0.png",mirrored = True))

        self.bullet_direction = "RIGHT"
        for i in range(0,5):
            self.hero.walk_right_textures.append(arcade.load_texture(f"../../SpriteLists/hero.walk.{i}.png"))
            self.hero.walk_left_textures.append(arcade.load_texture(f"../../SpriteLists/hero.walk.{i}.png",mirrored = True))
        self.hero.scale = 0.3
        self.hero.center_x = SCREEN_WIDTH//2
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
        
    def setDirection(self,newDirection):
        self.direction = newDirection
        
    def setSpeed(self,newSpeed):
        self.movementSpeed = newSpeed

    def getHeroY(self):
        return self.hero.center_y

    def getHeroX(self):
        return self.hero.center_x

    def getHero(self):
        return self.hero

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

    def getBulletDamage(self):
        return self.bullet_damage

    def getLifePoints(self):
        return self.lifePoints

    def setlLifePoints(self,newLife):
        self.lifePoints = newLife




class Enemy():
    def __init__(self,lifePoints,name,lowerBarrier,upperBarrier):
        self.name = name
        self.lifePoints = lifePoints
        self.enemy_list = arcade.SpriteList()
        self.lower = lowerBarrier
        self.upper = upperBarrier
        self.enemyLifeDict = {}
        self.enemyDamage = 5


        enemy = arcade.AnimatedTimeSprite()
        for i in range(0,8):
            enemy.textures.append(arcade.load_texture(f"../../SpriteLists/z{i}.png"))

        enemy.center_x = enemy.center_x = random.choice([-10,SCREEN_WIDTH + 20])
        enemy.center_y = random.randrange(self.lower+20,self.upper - 20)
        enemy.scale = 0.3
        enemy.change_x = 0.5

        self.enemy_list.append(enemy)
        self.enemyLifeDict = {}
    def drawEnemy(self):
        self.enemy_list.draw()

    def getEnemy(self):
        return self.enemy_list

    def enemyUpdate(self):
        self.enemy_list.update()
        self.enemy_list.update_animation()


    def setChange(self, enemy):
        if enemy.originalPosition == "RIGHT":
            enemy.change_x = -0.5
        elif enemy.originalPosition == "LEFT":
            enemy.change_x = 0.5

    def find(self,enemy,HeroY,HeroX):
        if enemy.center_y > HeroY:
            enemy.change_y = -0.5
            self.setChange(enemy)
        if enemy.center_y < HeroY:
            enemy.change_y = 0.5
            self.setChange(enemy)
        if enemy.center_y == HeroY and enemy.center_x == HeroX:
            enemy.change_y = 0
            enemy.change_x = 0



    def newUpdate(self,HeroY : int ,HeroX : int):

        for enemy in self.enemy_list:
            if enemy.originalPosition == "RIGHT":
                if enemy.center_x < 800:
                    self.find(enemy,HeroY,HeroX)
            if enemy.originalPosition == "LEFT":
                if enemy.center_x > 100:
                    self.find(enemy, HeroY,HeroX)


    def defineXLocation(self):
        for i in range(len(self.enemy_list)):
            if self.enemy_list[i].originalPosition == "LEFT":
                self.enemy_list[i].center_x = -50 * i
            if self.enemy_list[i].originalPosition == "RIGHT":
                self.enemy_list[i].center_x = SCREEN_WIDTH + (50*(i+1))

    def setTexture(self):
        enemy = arcade.AnimatedTimeSprite()
        for i in range(0,8):
            enemy.textures.append(arcade.load_texture(f"../../SpriteLists/z{i}.png",mirrored=True))
        enemy.scale = 0.3
        enemy.change_x = -0.5
        enemy.center_y = random.randrange(self.lower + 20, self.upper - 20)
        enemy.originalPosition = "RIGHT"
        return enemy

    def addLifePoints(self):
        for enemy in self.enemy_list:
            self.enemyLifeDict[enemy] = self.lifePoints

    def enemyIncrease(self,level):
        waves = level * 5

        for wave in range(waves):
            enemy = arcade.AnimatedTimeSprite()
            for i in range(0, 8):
                enemy.textures.append(arcade.load_texture(f"../../SpriteLists/z{i}.png"))
            enemy.center_x = random.choice([-10,SCREEN_WIDTH + 20])
            enemy.change_x = 0.5
            enemy.center_y = random.randrange(self.lower + 20, self.upper - 20)
            enemy.scale = 0.3

            if enemy.center_x > 0:
                self.enemy_list.append(self.setTexture())
            self.enemy_list.append(enemy)

            self.addLifePoints()
            self.defineXLocation()

    def getEnemyLife(self):
        return self.enemyLifeDict

    def setEnemyLife(self, newLife,enemy):
        self.enemyLifeDict[enemy] = newLife

    def setEnemy(self,newValue):
        self.enemy_list = newValue

class Barrier():
    def __init__(self,x,y):
        self.barrier_list_up = arcade.SpriteList()
        self.barrier_list_down = arcade.SpriteList()
        self.barrier_list_up.append(arcade.Sprite("../../SpriteLists/barrier.png",center_x = 25,center_y = y))
        for i in range(0,int(SCREEN_WIDTH/50)+4):
            barrier = arcade.Sprite("../../SpriteLists/barrier.png",center_x = 25 + (i * 41.6) ,center_y = y)
            self.barrier_list_up.append(barrier)
            barrier1 = arcade.Sprite("../../SpriteLists/barrier.png",center_x = 25 + (i * 41.6),center_y = 20)
            self.barrier_list_down.append(barrier1)
            
    def draw_wall_up(self):
        self.barrier_list_up.draw()
        
    def draw_wall_down(self):
        self.barrier_list_down.draw()

    def getWalllistUp(self):
        return self.barrier_list_up[0].center_y
    
    def getWalllistDown(self):
        return self.barrier_list_down[0].center_y


    

class StartGame(arcade.View):
    Hero = hero(100,"Zkiller")
    Barriers = Barrier(25,341)
    Enemys = Enemy(100,"Enemy",Barriers.getWalllistDown(),Barriers.getWalllistUp())
    Recorder = Record()
    backdrop = arcade.load_texture("../../SpriteLists/backdrop.png")
    direction = ""
    valueFor = 5
    valueForX = 5
    wave = 1
    score = 0
    
    def setupHeroBoundary(self, lowerYbarrier, upperYbarrier  , heroY, leftXbarrier ,rightXbarrier , heroX):
        """ partial """
        if heroY > upperYbarrier:
            self.valueFor = 0
            if self.direction == "DOWN":
                self.Hero.setSpeed(self.valueForX)
                self.valueFor = 5
            if self.direction == "UP":
                self.Hero.setSpeed(self.valueFor)
                
        if heroY < lowerYbarrier+50:
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
        arcade.set_background_color((123,156,24,255))
        self.Enemys.enemyIncrease(self.wave)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.backdrop)
        arcade.draw_rectangle_filled(SCREEN_WIDTH/2,SCREEN_HEIGHT-50,SCREEN_WIDTH,100,(127,212,23,127))
        arcade.draw_text_2(f"score:{self.score}",50,SCREEN_HEIGHT - 20,arcade.color.WHITE,15,align="center")
        arcade.draw_text_2(f"wave:{self.wave}", 50, SCREEN_HEIGHT - 70, arcade.color.WHITE, 15, align="center")
        arcade.draw_text_2(f"life:{self.Hero.getLifePoints()}", 400, SCREEN_HEIGHT - 20, arcade.color.WHITE, 15, align="center")
        self.Barriers.draw_wall_up()
        self.Hero.draw_hero()
        self.Enemys.drawEnemy()
        self.Barriers.draw_wall_down()
        self.Hero.bulletDraw()
        
    
    def on_key_press(self,key,modifier):
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

    def on_key_release(self,key,modifier):
        self.Hero.setSpeed(0)

    def checkCollision(self,enemys,bullets):
        print(len(enemys))
        for bullet in bullets:
            for enemy in enemys:
                if arcade.check_for_collision(enemy,bullet):
                    bullet.kill()
                    newlife = self.Enemys.getEnemyLife()[enemy] - self.Hero.getBulletDamage()
                    self.Enemys.setEnemyLife(newlife,enemy)
                    if self.Enemys.getEnemyLife()[enemy] == 0:
                        enemy.kill()
                        self.score += 1
        for enemy in enemys:
            if arcade.check_for_collision(enemy,self.Hero.getHero()):
                newlifes = self.Hero.getLifePoints() - self.Enemys.enemyDamage
                self.Hero.setlLifePoints(newlifes)
                self.score += 1
                enemy.kill()



    def checkHero(self):
        if self.Hero.getLifePoints() == 0:
            self.Recorder.getHighScore(self.score,self.wave)
            self.Enemys.setEnemy(arcade.SpriteList())
            self.wave = 1
            self.score = 0
            self.Hero.setlLifePoints(100)
            Window.show_view(GameOver())

    def checkEnemys(self):
        if len(self.Enemys.getEnemy())  == 0:
            self.wave += 1
            self.Enemys.enemyIncrease(self.wave)
            self.Enemys.enemyUpdate()


    def on_update(self,delta_time):
        self.Hero.update_hero()
        self.Hero.move()
        self.setupHeroBoundary(self.Barriers.getWalllistDown(),
                                  self.Barriers.getWalllistUp(),
                                  self.Hero.getHeroY(),50,SCREEN_WIDTH - 50,
                                  self.Hero.getHeroX())



        self.Enemys.newUpdate(self.Hero.getHeroY(),self.Hero.getHeroX())
        self.Enemys.enemyUpdate()
        self.Hero.bulletUpadate()

        self.checkCollision(self.Enemys.getEnemy(),self.Hero.getBullets())
        self.Hero.bulletCheck()
        self.checkHero()
        self.checkEnemys()


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


Window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
Window.show_view(GameOver())
arcade.run()


