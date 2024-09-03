import pygame
import sys
 
# Initialize Pygame
pygame.init()
 
# Screen settings
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Multiple Scenes Example")
 
# Mini window settings
mini_window_width = 750
mini_window_height = 500
mini_window_x = (screen_width - mini_window_width) // 2
mini_window_y = (screen_height - mini_window_height) // 2
 
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
 
# Layer of image
# Storage and cashier background images
img_bg_storage = []
img_bg_cashier = []
item_prices = [5, 10, 15, 20, 25, 30, 35, 40]
# Load item images
item_pics = []
item_pic=['bowl.PNG', 'catnip.PNG', 'petdrigree.PNG', 'roza.PNG', 'ขนมแมวเลีย.PNG', 'ของเล่นหมา.PNG', 'ครีมอาบน้ำหมาแมว.PNG', 'ตุ๊กตาplush.PNG']
item=['bowl', 'catnip', 'petdrigree', 'roza', 'ขนมแมวเลีย', 'ของเล่นหมา', 'ครีมอาบน้ำหมาแมว', 'ตุ๊กตาplush']
resized_images = []
for image_name in item_pic:
    image = pygame.image.load(image_name)
    resized_image = pygame.transform.scale(image, (50, 50))
    resized_images.append(resized_image)
 
for k in item_pic:
    img = pygame.image.load(k).convert_alpha()
    item_pics.append(img)
for i in range(1, 4):
    bg_storage = pygame.image.load(f"storage{i}.PNG").convert_alpha()
    img_bg_storage.append(bg_storage)
for j in range(1, 3):
    bg_cashier = pygame.image.load(f"cashier{j}.PNG").convert_alpha()
    img_bg_cashier.append(bg_cashier)
start_bg=pygame.image.load('store.Png').convert_alpha()
 
# Button class
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = blue
        self.callback = callback
 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 18)
        text_surf = font.render(self.text, True, white)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
 
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
 
# Scene functions
def open_scene():
    screen.blit(start_bg,(0,0))  # Fill the screen with white before drawing buttons
    start_button.draw(screen)
 
def cashier_scene():
    for j in img_bg_cashier:
        screen.blit(j, (0, 0))
    to_stock_button.draw(screen)
    back_to_open_button.draw(screen)
   
    if shop_open:
        close_button.draw(screen)
        confirm_button.draw(screen)
    render_balance()
    render_stock_window()
       
def stock_scene():
    screen.blit(img_bg_storage[0], (0, 0))
    screen.blit(img_bg_storage[1], (0, 0))
    screen.blit(img_bg_storage[2], (0, 0))
    show_stock()
    #button add item to stock
    for button in buttons:
        button.draw(screen)
   
    if shop_open:
        close_button.draw(screen)
        confirm_button.draw(screen)
    back_to_open_button.draw(screen)
 
    shop_button.draw(screen)
    to_stock_button.draw(screen)
    render_balance()
    render_stock_window()
       
def draw_mini_window():
    mini_window_rect = pygame.Rect(mini_window_x, mini_window_y, mini_window_width, mini_window_height)
    pygame.draw.rect(screen, white, mini_window_rect)
    pygame.draw.rect(screen, black, mini_window_rect, 2)
 
    font = pygame.font.Font(None, 24)
    item_size = 50
    spacing_x = 140
    spacing_y = 130
    start_x = mini_window_x + 20
    start_y = mini_window_y + 20
 
    for i in range(8):
        row = i // 4
        col = i % 4
        item_x = start_x + (item_size + spacing_x) * col
        item_y = start_y + (item_size + spacing_y) * row
 
        item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
        screen.blit(item_pics[i], item_rect.topleft)
        price_text = f"${item_prices[i]}"
        text_surf = font.render(price_text, True, black)
        screen.blit(text_surf, (item_x + item_size + 10, item_y + 10))
 
    total_cost_text = f"Total Cost: ${total_cost}"
    total_cost_surf = font.render(total_cost_text, True, black)
    screen.blit(total_cost_surf, (mini_window_x + 20, mini_window_y + mini_window_height - 80))
    bowl_button.draw(screen)
    catnip_button.draw(screen)
    petdrigree_button.draw(screen)
    roza_button.draw(screen)
    cat_snack_button.draw(screen)
    dog_toy_button.draw(screen)
    shampoo_button.draw(screen)
    plush_toy_button.draw(screen)
 
    confirm_button.draw(screen)
    close_button.draw(screen)
 
def update_total_cost():
    global total_cost
    total_cost = sum(item_prices[i] * quantity for i, quantity in selected_items.items())
 
# Function to handle item purchase
def buy_item(item_index):
    global selected_items, total_cost
   
    if item_index not in selected_items:
        selected_items[item_index] = 1  # Add item to the cart with quantity 1
    else:
        selected_items[item_index] += 1  # Increment the quantity if it already exists
    update_total_cost()
 
# Function to handle purchase confirmation
def confirm():
    global user_balance, selected_items, item_stock
    if user_balance >= total_cost:
        user_balance -= total_cost
        for item_index in selected_items:
            if item_index in item_stock:
                item_stock[item_index] += selected_items[item_index]
            else:
                item_stock[item_index] = selected_items[item_index]
        print(f"Purchase confirmed! New balance: ${user_balance}")
        selected_items = {}  # Reset selected items
        update_total_cost()  # Reset total cost
        render_stock_window()
    else:
        print("Insufficient balance!")
    print(item_stock)
font = pygame.font.Font(None, 24)
# Function to render the balance at the top right with a black background
def render_balance():
    balance_text = f"Balance: ${user_balance}"
    balance_surface = font.render(balance_text, True, (255, 255, 255))
    # Create a rectangle for the black background behind the balance text
    balance_rect = balance_surface.get_rect()
    balance_rect.topright = (screen.get_width() - 10, 10)
    # Draw the black background rectangle (with some padding around the text)
    pygame.draw.rect(screen, (0, 0, 0), balance_rect.inflate(10, 10))
    # Draw the balance text on top of the black rectangle
    screen.blit(balance_surface, balance_rect)
 
# Function to render the stock window at the bottom right
def render_stock_window():
    #แถบเช็คของที่ซื้อแล้ว
    for i in range(len(resized_images)):
        # Calculate position
        x = 400 + (i % 8) * (60 )
        y =550 + (i // 8) * (50)
        # Draw rectangle
        pygame.draw.rect(screen, (100, 100, 100), (x, y, 80, 55))
        # Display image
        screen.blit(resized_images[i], (x + 15, y + 5))
        # Get stock information
        image_name = item_pic[i]
        stock = item_stock.get(image_name, 0)  
       
    t=-1
    for item, stock in item_stock.items():
        t+=1
        x = 400 + (t % 8) * (60 )
        y =550 + (t // 8) * (50)
        stock_text = f"{stock if stock > 0 else 0}"
        stock_surface = font.render(stock_text, True, (200, 255, 255))
        screen.blit(stock_surface,(x + 15, y + 5))
 
position = [[200,35-5,'None'],[240+15,40-5,'None'],[280+55,45-5,'None'],[340+55,50-5,'None'],[500,50,'None'],[540,55,'None'],
            [200,175,'None'],[240+15,180,'None'],[280+35,185,'None'],[320+35,190,'None'],[200+250,175+15,'None'],[240+15+250,180+20,'None'],[280+35+250,185+25,'None'],
            [200,175+150,'None'],[240+15,180+150,'None'],[280+35,185+150,'None'],[320+35,190+150,'None'],[200+250,175+15+150,'None'],[240+15+250,180+20+150,'None'],[280+35+250,185+25+150,'None'],
            ]
 
def add_stock(i):
    for j in range(len(position)):
        if position[j][2] == 'None':
            position[j][2] = i
            show_stock()
            break
        elif position[j] != 'None':
            continue
 
def show_stock():
    for j in range(len(position)):
        item_size = 15
        x = position[j][0]
        y = position[j][1]
        if position[j][2] == 'None':
            continue
        else:
            item_rect = pygame.Rect( x, y, item_size, item_size)
            screen.blit(item_pics[int(position[j][2])], item_rect.topleft)
 
def close_shop():
    """Callback to close the shop mini window."""
    global shop_open
    shop_open = False
    global selected_items
    selected_items = {}  # Reset selected items when closing
 
# Scene callbacks
def go_to_cashier():
    global current_scene
    current_scene = "cashier"
 
def go_to_stock():
    global current_scene
    current_scene = "stock"
 
def go_to_open():
    global current_scene
    current_scene = "open"
 
def go_to_shop():
    global shop_open
    shop_open = True
   
# Create buttons
start_button = Button("Start", screen_width // 2 - 100, screen_height // 2, 82, 36, go_to_cashier)
to_stock_button = Button("Stock", 24, screen_height // 5 + 50, 82, 36, go_to_stock)
back_to_open_button = Button("Home", 24, screen_height // 5 + 120, 82, 36, go_to_open)
back_to_cashier_button = Button("Cashier", 24, screen_height // 2 + 50, 82, 36, go_to_cashier)
shop_button = Button("Shop", 24, screen_height // 5 + 50, 82, 36, go_to_shop)
close_button = Button("Close", mini_window_x + mini_window_width - 100, mini_window_y + mini_window_height - 50, 80, 36, close_shop)
confirm_button = Button("Confirm", mini_window_x + mini_window_width - 180, mini_window_y + mini_window_height - 50, 80, 36, confirm)
ad1_button = Button('add',screen_width //2 - 40, screen_height *7/8,40,20,lambda: add_stock(0))
ad2_button = Button('add',screen_width //2 +30, screen_height *7/8,40,20,lambda: add_stock(1))
ad3_button = Button('add',screen_width //2 +70*1, screen_height *7/8,40,20,lambda: add_stock(2))
ad4_button = Button('add',screen_width //2+70*2,screen_height *7/8,40,20,lambda: add_stock(3))
ad5_button = Button('add',screen_width //2+70*3,screen_height *7/8,40,20,lambda: add_stock(4))
ad6_button = Button('add',screen_width //2+70*4,screen_height *7/8,40,20,lambda: add_stock(5))
ad7_button = Button('add',screen_width //2+70*5,screen_height *7/8,40,20,lambda: add_stock(6))
ad8_button = Button('add',screen_width //2+70*6,screen_height *7/8,40,20,lambda: add_stock(7))
buttons = [ad1_button, ad2_button, ad3_button, ad4_button, ad5_button, ad6_button, ad7_button, ad8_button]    
 
 
#mini shop button
bowl_button = Button("Buy", mini_window_x + (40 * 1), mini_window_y + 170, 100, 36, lambda: buy_item(0))
catnip_button = Button("Buy", mini_window_x + (90 * 2.5), mini_window_y + 170, 100, 36, lambda: buy_item(1))
petdrigree_button = Button("Buy", mini_window_x + (120 * 3.5), mini_window_y + 170, 100, 36, lambda: buy_item(2))
roza_button = Button("Buy", mini_window_x + (175 * 3.5), mini_window_y + 170, 100, 36, lambda: buy_item(3))
cat_snack_button = Button("Buy", mini_window_x + (40 * 1), mini_window_y + 360, 100, 36, lambda: buy_item(4))
dog_toy_button = Button("Buy", mini_window_x + (90 * 2.5), mini_window_y + 360, 100, 36, lambda: buy_item(5))
shampoo_button = Button("Buy", mini_window_x + (120 * 3.5), mini_window_y + 360, 100, 36, lambda: buy_item(6))
plush_toy_button = Button("Buy", mini_window_x + (175 * 3.5), mini_window_y + 360, 100, 36, lambda: buy_item(7))
 
# Initial scene and shop window state
current_scene = "open"
shop_open = False
market_price=1
item_prices = {i:((i + 1)*market_price) for i in range(len(item))}  # Example prices
selected_items = {}
total_cost = 0
 
 
# Initialize item stock (all items start at 0)
item_stock = {i: 0 for i in range(len(item))}
user_balance = 200  # Example initial balance
 
# Main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if current_scene == "open" and start_button.is_clicked(pos):
                start_button.callback()
            elif current_scene == "cashier":
               
                if to_stock_button.is_clicked(pos):
                    to_stock_button.callback()
                elif back_to_open_button.is_clicked(pos):
                    back_to_open_button.callback()
                elif shop_open:
                    if close_button.is_clicked(pos):
                        close_button.callback()
                    elif confirm_button.is_clicked(pos):
                        confirm_button.callback()
            elif current_scene == "stock":
                for button in buttons:
                    if button.is_clicked(pos):
                        button.callback()
                if back_to_cashier_button.is_clicked(pos):
                    back_to_cashier_button.callback()
                elif shop_button.is_clicked(pos):
                    shop_button.callback()
                elif shop_open:
                    if close_button.is_clicked(pos):
                        close_button.callback()
                    elif bowl_button.is_clicked(pos):
                        bowl_button.callback()
                    elif catnip_button.is_clicked(pos):
                        catnip_button.callback()
                    elif petdrigree_button.is_clicked(pos):
                        petdrigree_button.callback()
                    elif roza_button.is_clicked(pos):
                        roza_button.callback()
                    elif cat_snack_button.is_clicked(pos):
                        cat_snack_button.callback()
                    elif dog_toy_button.is_clicked(pos):
                        dog_toy_button.callback()
                    elif shampoo_button.is_clicked(pos):
                        shampoo_button.callback()
                    elif plush_toy_button.is_clicked(pos):
                        plush_toy_button.callback()
                    elif confirm_button.is_clicked(pos):
                        confirm_button.callback()
               
    if current_scene == "open":
        open_scene()
    elif current_scene == "cashier":
        cashier_scene()
    elif current_scene == "stock":
        stock_scene()
 
    if shop_open:
        draw_mini_window()
 
    pygame.display.flip()
    clock.tick(60)
