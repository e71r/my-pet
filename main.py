import pygame as pg
from config import *
import random
import json

# Инициализация pg
pg.init()

ICON_SIZE = 80
padding = 5

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 120

TOY_SIZE = 100

pg.font.init()

font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)
font_maxi = pg.font.Font(None, 200)

def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width,height))
    return image

def text_render(text, f=font, color = (0,0,0)):
    return f.render(text, True, color)

class Item:
    def __init__(self, name, price, file):
        self.name = name
        self.price = price
        self.is_bought = False
        self.is_using = False
        self.file = file

        self.image = load_image(file, DOG_WIDTH // 1.7, DOG_HEIGHT // 1.7)
        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)


class ClothesMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = game.screen

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        # self.items = [
        #     Item("Синяя Футболка", 10, "images/items/blue t-shirt.png"),
        #      Item("Ботинки", 50, "images/items/boots.png"),
        #      Item("Шляпа", 25, "images/items/hat.png"),
        #      Item("Очки", 5, "images/items/sunglasses.png"),
        #      Item("Желтая футболка", 10, "images/items/yellow t-shirt.png"),
        #      Item("Золотая цепь", 90, "images/items/gold chain.png"),
        #      Item("Серебрянная цепь", 60, "images/items/silver chain.png")
        # ]

        self.items = []

        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for f in data["clothes"]:
            item = Item(
                f["name"],
                f["price"],
                f["image"])
            
            item.is_bought = f["is_bought"]
            item.is_using = f["is_using"]
            self.items.append(item)

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперед", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.to_next)
        
        self.is_using_t = text_render("Надето")
        self.is_bought_t = text_render("Куплено")


        self.back_button = Button("Назад", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - 500, SCREEN_HEIGHT - MENU_NAV_YPAD,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.to_previous)
        
        self.wear_button = Button("Надеть", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - 500, SCREEN_HEIGHT - MENU_NAV_YPAD-70,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.wear)
        
        self.buy_button = Button("Купить", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - 250, SCREEN_HEIGHT - MENU_NAV_YPAD-70,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.buy)        
       
    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
        else:
            self.current_item = 0

    def wear(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_using = not self.items[self.current_item].is_using

    
    
    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1
        else:
            self.current_item = len(self.items) - 1
    

    def buy(self):
        if self.items[self.current_item].is_bought != True:
            if self.game.money >= self.items[self.current_item].price:

                self.game.money -= self.items[self.current_item].price

                self.items[self.current_item].is_bought = True

    def use_item(self):
        self.items[self.current_item].is_using = not self.items[self.current_item].is_using

    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.buy_button.update()
        self.wear_button.update()
        

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.buy_button.is_clicked(event)
        self.wear_button.is_clicked(event)    

    def draw(self, screen):
        screen.blit(self.menu_page, (0,0))
        screen.blit(self.items[self.current_item].image, self.item_rect)
        screen.blit(self.is_using_t, (SCREEN_WIDTH/2+190, SCREEN_HEIGHT/2-160))
        screen.blit(self.is_bought_t, (SCREEN_WIDTH/2+190, SCREEN_HEIGHT/2-90))

        name_t = text_render(self.items[self.current_item].name)
        price_t = text_render(str(self.items[self.current_item].price))

        screen.blit(name_t, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-160))
        screen.blit(price_t, (SCREEN_WIDTH/2-20, SCREEN_HEIGHT/2-110))

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0,0))
        else:
            screen.blit(self.bottom_label_off, (0,0))

        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on, (0,0))
        else:
            screen.blit(self.top_label_off, (0,0))

        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.wear_button.draw(screen)
        self.buy_button.draw(screen)

class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height = BUTTON_HEIGHT, text_font = font, func = None):
        self.idle_image = load_image("images/button.png", width,height)
        self.pressed_image = load_image("images/button_clicked.png", width,height)
        self.image = self.idle_image
        self.text = text
        self.func = func
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.text_font = text_font

        self.is_pressed = False
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        text = text_render(str(self.text), self.text_font)
        text_rect = text.get_rect()



        text_rect.center = self.rect.center
        screen.blit(text, text_rect)
    def update(self):
        mouse_pos = pg.mouse.get_pos()


        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                if self.func != None:
                    self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False

class Food:
    def __init__(self, name, satiety, file, price, medicine_power = 0):
        self.name = name
        self.satiety = satiety
        self.price = price
        self.medicine_power = medicine_power
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)

class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = game.screen

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [
            Food("Яблоко", 10, "images/food/apple.png", 5),

              Food("Кость", 20, "images/food/bone.png", 5),

              Food("Собачья еда", 15, "images/food/dog food.png", 5),

              Food("Мясо", 30 ,"images/food/meat.png", 5),

              Food("Лекарство", 100, "images/food/medicine.png", 20, 10)
        ]

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперед", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.to_next)
        
        self.is_using_t = text_render("Надето")
        self.is_bought_t = text_render("Куплено")


        self.back_button = Button("Назад", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - 500, SCREEN_HEIGHT - MENU_NAV_YPAD,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.to_previous)
        
        
        self.buy_button = Button("Съесть", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH - 250, SCREEN_HEIGHT - MENU_NAV_YPAD-70,
                             width = int(BUTTON_WIDTH // 1.2), height = int(BUTTON_HEIGHT // 1.2),
                             func = self.buy)        
       
    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
        else:
            self.current_item = 0

    def wear(self):
        
        self.items[self.current_item].is_using = not self.items[self.current_item].is_using

    
    
    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1
        else:
            self.current_item = len(self.items) - 1
    

    def buy(self):

        if self.game.money >= self.items[self.current_item].price:

            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            self.game.health += self.items[self.current_item].medicine_power if self.items[self.current_item].medicine_power != 0 or None else 0

            if self.game.satiety > 100:
                self.game.satiety = 100
            if self.game.health > 100:
                self.game.health = 100
    

    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.buy_button.update()
    
        

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.buy_button.is_clicked(event)
        

    def draw(self, screen):
        screen.blit(self.menu_page, (0,0))
        screen.blit(self.items[self.current_item].image, self.item_rect)
        

        name_t = text_render(self.items[self.current_item].name)
        price_t = text_render(str(self.items[self.current_item].price))

        screen.blit(name_t, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-160))
        screen.blit(price_t, (SCREEN_WIDTH/2-20, SCREEN_HEIGHT/2-110))

        

        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.buy_button.draw(screen)

class Toy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.n = random.choice(["images/toys/ball.png", "images/toys/blue bone.png", "images/toys/red bone.png"])

        self.speed = 5

        self.image = load_image(self.n, TOY_SIZE , TOY_SIZE)
        self.rect = self.image.get_rect()

        self.rect.centerx = random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - TOY_SIZE)
        self.rect.centery = MENU_NAV_YPAD - 30
    
    def update(self):
        if self.rect.y > SCREEN_HEIGHT - MENU_NAV_YPAD:
            self.kill()
        else:
            self.rect.y += self.speed

class Dog(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("images/dog.png", DOG_WIDTH / 2, DOG_HEIGHT / 2)
        self.rect = self.image.get_rect()

        self.speed = 10

        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT - MENU_NAV_YPAD - 10

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_d]:
            self.rect.x += self.speed
        if key[pg.K_a]:
            self.rect.x -= self.speed



class MiniGame:
    def __init__(self, game):
        self.game = game

        self.background = load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = MINI_GAME_DURATION

    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = MINI_GAME_DURATION

    def update(self):
        self.toys.update()
        self.dog.update()
        if random.randint(1,20) == 20:
            self.toys.add(Toy())

        hits = pg.sprite.spritecollide(self.dog, self.toys, True, 
                                       pg.sprite.collide_circle_ratio(0.6))
        
        self.score += len(hits)

        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score // 2)
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0,0))

        screen.blit(self.dog.image, self.dog.rect)
        

        screen.blit(text_render(str(self.score)), (MENU_NAV_XPAD + 20, 80))

        self.toys.draw(screen)
        

class Game:
    def __init__(self):
        
        
        self.clock = pg.time.Clock()
    

        with open("save.json", encoding= "utf-8") as file:
            data = json.load(file)

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.happiness = data["happiness"]
        self.satiety = data["satiety"]
        self.health = data["health"]
        self.money = data["money"]
        self.coins_per_second = data["coins_per_second"]
        self.costs_of_upgrade = {}

        for key,value in data["cost_of_upgrade"].items():
            self.costs_of_upgrade[int(key)] = value

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.happiness_image = load_image("images/happiness.png", ICON_SIZE, ICON_SIZE)
        self.satiety_image = load_image("images/satiety.png", ICON_SIZE, ICON_SIZE)
        self.health_image = load_image("images/health.png", ICON_SIZE, ICON_SIZE)
        self.money_image = load_image("images/money.png", ICON_SIZE, ICON_SIZE)
        self.dog_image = load_image("images/dog.png", 310,500)

        self.mode = "Main"

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - padding
        
        self.eat_button = Button("Еда", button_x, padding + ICON_SIZE,
                                 func = self.food_menu_on)
        self.clothes_button = Button("Одежда", button_x, padding + ICON_SIZE * 2,
                                     func = self.clothes_menu_on)
        self.games_button = Button("Игры", button_x, padding + ICON_SIZE * 3, 
                                   func = self.game_on)

     

        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0, width = BUTTON_WIDTH // 3, 
                                     height = BUTTON_HEIGHT // 3, text_font = mini_font, func = self.increase_money)
        
        self.buttons = [self.eat_button, self.clothes_button, self.games_button, self.upgrade_button]

        self.clothes_menu = ClothesMenu(self)
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.DECREASE = pg.USEREVENT + 2
        pg.time.set_timer(self.DECREASE, 3600)

        self.run()

    def clothes_menu_on(self):
        
        self.mode = "Clothes menu"

    def food_menu_on(self):
        self.mode = "Food menu"

    def game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ## сохранение ##
                if self.mode != "Game over":
                    clothes = []

                    for i in self.clothes_menu.items:
                        
                        clothes.append({
                            "name": i.name,
                            "price": i.price,
                            "image": i.file,

                            "is_bought": i.is_bought,
                            "is_using": i.is_using
                        })

                    with open("save.json", "w", encoding="utf-8") as file:
                        json.dump({
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coins_per_second": self.coins_per_second,
                        "cost_of_upgrade": {
                            "100": self.costs_of_upgrade[100],
                            "1000": self.costs_of_upgrade[1000],
                            "5000": self.costs_of_upgrade[5000],
                            "10000": self.costs_of_upgrade[10000]
                        },
                        "clothes": clothes
                        }, fp=file)

                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.mode != "Game over":
                    if event.button == 1:
                        self.money += self.coins_per_second

            if event.type == self.DECREASE:
                if self.mode != "Game over":
                    chance = random.randint(1,10)
                    if chance <= 5:
                        self.satiety -= 1
                    elif chance > 5 and chance <= 9:
                        self.happiness -= 1
                    else:
                        self.health -= 1

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and self.mode != "Game over":
                    self.mode = "Main"
                    

            if event.type == self.INCREASE_COINS:
                if self.mode != "Game over":
                    self.money += self.coins_per_second

            #self.eat_button.is_clicked(event)
            for i in self.buttons:
                i.is_clicked(event)
            if self.mode != "Main":
                self.clothes_menu.is_clicked(event)
                self.food_menu.is_clicked(event)

    def increase_money(self):
        if self.mode != "Game over":
            for cost,check in self.costs_of_upgrade.items():
                if not check and self.money >= cost:
                    self.money -= cost
                    self.costs_of_upgrade[cost] = True
                    self.coins_per_second += 1
    

                


    def update(self):
        for button in self.buttons:
            button.update()
        if self.mode == "Clothes menu":
            self.clothes_menu.update()
        if self.mode == "Food menu":
            self.food_menu.update()
        if self.mode == "Mini game":
            self.mini_game.update()

        if self.health <= 0 or self.satiety <= 0 or self.happiness <= 0:
            self.mode = "Game over"
    def draw(self):
        self.screen.blit(self.background, (0,0))

        self.screen.blit(self.happiness_image, (padding, padding))
        self.screen.blit(self.satiety_image, (padding, padding*15))
        self.screen.blit(self.health_image, (padding, padding*30))

        dog_y = SCREEN_HEIGHT/2-200
        dog_x = SCREEN_WIDTH/2-150

        self.screen.blit(self.money_image, (SCREEN_WIDTH-padding*15, padding*2))
        self.screen.blit(self.dog_image, (dog_x, dog_y)) # к середине

        self.screen.blit(text_render(f"{self.happiness}"), (padding + ICON_SIZE, padding*6))
        self.screen.blit(text_render(f"{self.satiety}"), (padding + ICON_SIZE, padding*20))
        self.screen.blit(text_render(f"{self.health}"), (padding + ICON_SIZE, padding*35))
        self.screen.blit(text_render(f"{self.money}"), (SCREEN_WIDTH-padding*20, padding+30))
        

        for item in self.clothes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (SCREEN_WIDTH/2 - DOG_WIDTH / 2, dog_y))

        for button in self.buttons:
            button.draw(self.screen)

        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)

            self.screen.blit(text_render("Надето"), (SCREEN_WIDTH/2+190, SCREEN_HEIGHT/2-160))
            self.screen.blit(text_render("Куплено"), (SCREEN_WIDTH/2+190, SCREEN_HEIGHT/2-90))

        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)

        if self.mode == "Mini game":
            self.mini_game.draw(self.screen)

        if self.mode == "Game over":
            text = text_render("ПРОИГРЫШ", color=(255,0,0), f = font_maxi)
            self.screen.blit(text, (10, SCREEN_HEIGHT/2))

            clothes = []

            for i in self.clothes_menu.items:
                    
                clothes.append({
                    "name": i.name,
                    "price": i.price,
                    "image": i.file,

                    "is_bought": False,
                    "is_using": False
                })

            with open("save.json", "w", encoding="utf-8") as file:
                json.dump({
                "happiness": 100,
                "satiety": 100,
                "health": 100,
                "money": 0,
                "coins_per_second": 1,
                "cost_of_upgrade": {
                    "100": False,
                    "1000": False,
                    "5000": False,
                    "10000": False
                },
                "clothes": clothes
                }, fp=file)

        
        pg.display.flip()


if __name__ == "__main__":
    Game()