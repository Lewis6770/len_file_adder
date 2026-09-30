"""import pygame
import random
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Characters database
CHARACTERS = {
    "Knight": {"hp": 150, "dmg": 20, "range": 40, "speed": 2, "cost": 3, "color": (120, 120, 255)},
    "Archer": {"hp": 80, "dmg": 15, "range": 120, "speed": 2.5, "cost": 2, "color": (255, 100, 100)},
    "Giant": {"hp": 300, "dmg": 40, "range": 30, "speed": 1.5, "cost": 5, "color": (200, 200, 100)},
    "Wizard": {"hp": 100, "dmg": 30, "range": 100, "speed": 2, "cost": 4, "color": (200, 0, 200)},
    "Bomber": {"hp": 60, "dmg": 50, "range": 80, "speed": 2, "cost": 3, "color": (100, 200, 200)},
}

# Init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# Classes
class Unit:
    def __init__(self, name, x, y, team):
        self.name = name
        self.stats = CHARACTERS[name]
        self.hp = self.stats["hp"]
        self.dmg = self.stats["dmg"]
        self.range = self.stats["range"]
        self.speed = self.stats["speed"]
        self.color = self.stats["color"]
        self.x = x
        self.y = y
        self.team = team

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)

    def move(self):
        if self.team == "player":
            self.x += self.speed
        else:
            self.x -= self.speed

    def is_enemy_in_range(self, enemies):
        for e in enemies:
            dist = abs(self.x - e.x)
            if dist <= self.range:
                return e
        return None

    def attack(self, enemy):
        enemy.hp -= self.dmg

# Towers
class Tower:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.hp = 500
        self.team = team

    def draw(self):
        pygame.draw.rect(screen, GREEN if self.team == "player" else RED, (self.x, self.y, 30, 60))
        hp_text = font.render(str(int(self.hp)), True, WHITE)
        screen.blit(hp_text, (self.x, self.y - 20))

    def attack_nearest(self, enemies):
        for e in enemies:
            if abs(self.x - e.x) < 120:
                e.hp -= 10
                break

# Game logic
player_units = []
bot_units = []
player_tower = Tower(50, HEIGHT//2 - 30, "player")
bot_tower = Tower(WIDTH - 80, HEIGHT//2 - 30, "bot")

elixir = 5
elixir_timer = 0
selected_difficulty = None

def spawn_unit(team, name):
    y = random.randint(100, HEIGHT - 100)
    if team == "player":
        player_units.append(Unit(name, 100, y, team))
    else:
        bot_units.append(Unit(name, WIDTH - 100, y, team))

def draw_ui():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))
    elixir_text = font.render(f"Elixir: {elixir}", True, WHITE)
    screen.blit(elixir_text, (10, HEIGHT - 40))
    help_text = font.render("1-Knight 2-Archer 3-Giant 4-Wizard 5-Bomber", True, WHITE)
    screen.blit(help_text, (200, HEIGHT - 40))

def bot_ai():
    global elixir
    if selected_difficulty == "easy":
        if random.random() < 0.01:
            name = random.choice(list(CHARACTERS.keys()))
            if CHARACTERS[name]["cost"] <= elixir:
                elixir -= CHARACTERS[name]["cost"]
                spawn_unit("bot", name)
    elif selected_difficulty == "hard":
        if random.random() < 0.03:
            options = sorted(CHARACTERS.items(), key=lambda x: -x[1]["dmg"])
            for name, stats in options:
                if stats["cost"] <= elixir:
                    elixir -= stats["cost"]
                    spawn_unit("bot", name)
                    break
    elif selected_difficulty == "impossible":
        for name, stats in CHARACTERS.items():
            if stats["cost"] <= elixir:
                elixir -= stats["cost"]
                spawn_unit("bot", name)
                break

# Difficulty selection menu
def menu():
    global selected_difficulty
    while selected_difficulty is None:
        screen.fill(BLACK)
        text1 = font.render("Choose difficulty: 1-Easy 2-Hard 3-Impossible", True, WHITE)
        screen.blit(text1, (WIDTH//2 - 200, HEIGHT//2 - 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_difficulty = "easy"
                elif event.key == pygame.K_2:
                    selected_difficulty = "hard"
                elif event.key == pygame.K_3:
                    selected_difficulty = "impossible"

# Game loop
menu()
running = True
while running:
    screen.fill((50, 50, 50))
    clock.tick(FPS)
    elixir_timer += 1
    if elixir_timer >= 60:
        elixir_timer = 0
        if elixir < 10:
            elixir += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
            names = list(CHARACTERS.keys())
            for i, k in enumerate(keys):
                if event.key == k and CHARACTERS[names[i]]["cost"] <= elixir:
                    elixir -= CHARACTERS[names[i]]["cost"]
                    spawn_unit("player", names[i])

    # Update units
    for unit in player_units + bot_units:
        unit.move()

    # Combat
    for team_units, enemies in [(player_units, bot_units), (bot_units, player_units)]:
        for unit in team_units:
            target = unit.is_enemy_in_range(enemies)
            if target:
                unit.attack(target)

    player_units = [u for u in player_units if u.hp > 0 and u.x < WIDTH]
    bot_units = [u for u in bot_units if u.hp > 0 and u.x > 0]

    # Tower logic
    player_tower.attack_nearest(bot_units)
    bot_tower.attack_nearest(player_units)

    # Draw
    player_tower.draw()
    bot_tower.draw()
    for u in player_units + bot_units:
        u.draw()
    draw_ui()

    # Bot AI
    bot_ai()

    # Win condition
    if player_tower.hp <= 0:
        screen.fill(BLACK)
        msg = font.render("YOU LOSE", True, RED)
        screen.blit(msg, (WIDTH//2 - 50, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    elif bot_tower.hp <= 0:
        screen.fill(BLACK)
        msg = font.render("YOU WIN", True, GREEN)
        screen.blit(msg, (WIDTH//2 - 50, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
"""
import pygame
import sys
import urllib.request
import io
from PIL import Image
import random
import time

# --- INIT ---
pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Clash Royale")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 48)

# --- CONSTANTS ---
CARD_WIDTH, CARD_HEIGHT = 80, 100
CARD_BAR_HEIGHT = 130
MAX_ELIXIR = 10
ELIXIR_REGEN_RATE = 1000  # milliseconds
GAME_TIME = 180  # seconds
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (30, 30, 40)
BAR_COLOR = (20, 20, 30)

# --- Load Images from URL ---
def load_image_from_url(url, size):
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        image = image.resize(size)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    except Exception as e:
        print(f"Failed to load image {url}: {e}")
        surf = pygame.Surface(size)
        surf.fill((150, 150, 150))
        return surf

image_urls = {
    "Knight": "https://i.imgur.com/6rW0wOf.png",
    "Archer": "https://i.imgur.com/pMxi77p.png",
    "Giant": "https://i.imgur.com/2FwUdkk.png",
    "Wizard": "https://i.imgur.com/lR4t0ZS.png",
    "Bomber": "https://i.imgur.com/KNhxMxu.png",
    "KingTower": "https://i.imgur.com/hjcLq5m.png",
    "Tower": "https://i.imgur.com/EHgT9Ex.png",
}

cards_data = {
    "Knight": {"cost": 3, "hp": 100, "speed": 1.5, "damage": 15, "img": None},
    "Archer": {"cost": 2, "hp": 60, "speed": 2, "damage": 10, "img": None},
    "Giant": {"cost": 5, "hp": 250, "speed": 1, "damage": 20, "img": None},
    "Wizard": {"cost": 4, "hp": 70, "speed": 1.8, "damage": 18, "img": None},
    "Bomber": {"cost": 3, "hp": 80, "speed": 1.4, "damage": 22, "img": None},
}

# Load images for cards
for name in cards_data:
    cards_data[name]["img"] = load_image_from_url(image_urls[name], (CARD_WIDTH, CARD_HEIGHT))
# Load tower images
king_tower_img = load_image_from_url(image_urls["KingTower"], (80, 100))
tower_img = load_image_from_url(image_urls["Tower"], (60, 80))

# --- Classes ---
class Card:
    def __init__(self, name, x, y):
        self.name = name
        self.cost = cards_data[name]["cost"]
        self.image = cards_data[name]["img"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.offset = (0, 0)

    def draw(self):
        screen.blit(self.image, self.rect)
        cost_text = font.render(str(self.cost), True, WHITE)
        screen.blit(cost_text, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event, elixir):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if elixir >= self.cost:
                    self.dragging = True
                    mx, my = event.pos
                    self.offset = (self.rect.x - mx, self.rect.y - my)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                mx, my = event.pos
                if my < HEIGHT - CARD_BAR_HEIGHT:
                    return (self.name, mx, my)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.rect.topleft = (mx + self.offset[0], my + self.offset[1])
        return None

    def reset_position(self, x, y):
        self.rect.topleft = (x, y)

class Unit:
    WIDTH = 50
    HEIGHT = 60

    def __init__(self, name, x, y, side):
        self.name = name
        self.side = side  # 'player' or 'ai'
        self.hp = cards_data[name]["hp"]
        self.speed = cards_data[name]["speed"]
        self.damage = cards_data[name]["damage"]
        self.image = cards_data[name]["img"]
        self.rect = self.image.get_rect(center=(x, y))
        self.target = None
        self.alive = True

    def move(self):
        if self.target and self.target.hp > 0:
            if self.rect.centerx < self.target.rect.centerx:
                self.rect.centerx += self.speed
            elif self.rect.centerx > self.target.rect.centerx:
                self.rect.centerx -= self.speed
        else:
            # Move towards enemy tower if no target
            if self.side == "player":
                self.rect.centerx += self.speed
            else:
                self.rect.centerx -= self.speed

    def attack(self):
        if self.target and self.rect.colliderect(self.target.rect):
            self.target.hp -= self.damage
            if self.target.hp <= 0:
                self.target.alive = False
                self.target = None

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        # Draw hp bar
        hp_ratio = max(self.hp, 0) / cards_data[self.name]["hp"]
        hp_bar_width = int(self.rect.width * hp_ratio)
        pygame.draw.rect(screen, (255,0,0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y - 10, hp_bar_width, 5))

class Tower:
    def __init__(self, x, y, is_king=False, side="player"):
        self.is_king = is_king
        self.side = side
        self.max_hp = 500 if is_king else 300
        self.hp = self.max_hp
        self.image = king_tower_img if is_king else tower_img
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        # HP bar
        hp_ratio = max(self.hp,0) / self.max_hp
        hp_bar_width = int(self.rect.width * hp_ratio)
        pygame.draw.rect(screen, (255,0,0), (self.rect.x, self.rect.y - 10, self.rect.width, 8))
        pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y - 10, hp_bar_width, 8))

# --- Game states ---
MENU = 0
LOADING = 1
BATTLE = 2
RESULTS = 3

# --- Global vars ---
game_state = MENU
difficulty = None
last_elixir_update = 0

# --- Initialize game variables ---
def init_game():
    global player_elixir, ai_elixir, last_elixir_update, deployed_units, player_towers, ai_towers, start_time, winner
    player_elixir = MAX_ELIXIR
    ai_elixir = MAX_ELIXIR
    last_elixir_update = pygame.time.get_ticks()
    deployed_units = []
    player_towers = [
        Tower(100, HEIGHT//2, is_king=False, side="player"),
        Tower(40, HEIGHT//3, is_king=True, side="player"),
        Tower(100, 2*HEIGHT//3, is_king=False, side="player")
    ]
    ai_towers = [
        Tower(WIDTH-100, HEIGHT//2, is_king=False, side="ai"),
        Tower(WIDTH-40, HEIGHT//3, is_king=True, side="ai"),
        Tower(WIDTH-100, 2*HEIGHT//3, is_king=False, side="ai")
    ]
    start_time = pygame.time.get_ticks()
    winner = None

# --- Cards for player ---
card_names = list(cards_data.keys())
cards = []
for i, name in enumerate(card_names):
    cards.append(Card(name, 10 + i * (CARD_WIDTH + 10), HEIGHT - CARD_BAR_HEIGHT + 15))

# --- AI Logic ---
def ai_play():
    global ai_elixir
    # Simple AI: tries to play a random card if enough elixir
    possible_cards = [name for name in card_names if cards_data[name]["cost"] <= ai_elixir]
    if possible_cards:
        # AI difficulty affects chance to deploy and frequency
        now = pygame.time.get_ticks()
        if difficulty == "Beginner" and random.random() < 0.005:
            card = random.choice(possible_cards)
        elif difficulty == "Hard" and random.random() < 0.015:
            card = random.choice(possible_cards)
        elif difficulty == "Impossible" and random.random() < 0.03:
            card = random.choice(possible_cards)
        else:
            return

        # AI deploy position: random y on own half
        y = random.randint(100, HEIGHT - CARD_BAR_HEIGHT - 50)
        deployed_units.append({"name": card, "x": WIDTH-150, "y": y, "side": "ai"})
        ai_elixir -= cards_data[card]["cost"]

# --- Assign targets ---
def assign_targets(units, towers):
    for unit in units:
        if unit.target is None or not unit.target.alive:
            # Prioritize enemy units closer to towers or towers if no units nearby
            enemy_units = [u for u in units if u.side != unit.side and u.alive]
            if enemy_units:
                closest_enemy = min(enemy_units, key=lambda e: abs(e.rect.centerx - unit.rect.centerx))
                unit.target = closest_enemy
            else:
                # Target nearest enemy tower
                enemy_towers = [t for t in towers if t.side != unit.side and t.alive]
                if enemy_towers:
                    closest_tower = min(enemy_towers, key=lambda t: abs(t.rect.centerx - unit.rect.centerx))
                    unit.target = closest_tower
                else:
                    unit.target = None

# --- Render elixir bars ---
def draw_elixir_bar(x, y, elixir):
    pygame.draw.rect(screen, (50, 50, 50), (x, y, 120, 20), border_radius=8)
    fill_width = int((elixir / MAX_ELIXIR) * 120)
    pygame.draw.rect(screen, (0, 150, 255), (x, y, fill_width, 20), border_radius=8)
    text = font.render(f"Elixir: {int(elixir)}", True, WHITE)
    screen.blit(text, (x + 130, y - 3))

# --- Draw Timer ---
def draw_timer():
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = max(0, GAME_TIME - elapsed)
    min_sec = f"{remaining//60}:{remaining%60:02d}"
    timer_text = big_font.render(min_sec, True, WHITE)
    screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 10))
    return remaining

# --- Draw Menu ---
def draw_menu():
    screen.fill(BG_COLOR)
    title = big_font.render("Mini Clash Royale", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

    beginner_text = font.render("1 - Beginner (Easy AI)", True, WHITE)
    hard_text = font.render("2 - Hard (Medium AI)", True, WHITE)
    impossible_text = font.render("3 - Impossible (Hard AI)", True, WHITE)

    screen.blit(beginner_text, (WIDTH//2 - beginner_text.get_width()//2, 200))
    screen.blit(hard_text, (WIDTH//2 - hard_text.get_width()//2, 250))
    screen.blit(impossible_text, (WIDTH//2 - impossible_text.get_width()//2, 300))

    info = font.render("Press 1, 2, or 3 to select difficulty and start", True, WHITE)
    screen.blit(info, (WIDTH//2 - info.get_width()//2, 400))

# --- Draw Loading ---
def draw_loading():
    screen.fill(BG_COLOR)
    loading = big_font.render("Loading...", True, WHITE)
    screen.blit(loading, (WIDTH//2 - loading.get_width()//2, HEIGHT//2 - loading.get_height()//2))

# --- Draw Battle ---
def draw_battle():
    screen.fill(BG_COLOR)
    # Draw Towers
    for tower in player_towers + ai_towers:
        tower.draw()

    # Draw Units
    for unit in units:
        unit.draw()

    # Draw Cards
    for card in cards:
        card.draw()

    # Draw elixir bars
    draw_elixir_bar(10, HEIGHT - CARD_BAR_HEIGHT - 30, player_elixir)
    draw_elixir_bar(WIDTH - 240, HEIGHT - CARD_BAR_HEIGHT - 30, ai_elixir)

    # Draw timer
    draw_timer()

# --- Draw Results ---
def draw_results():
    screen.fill(BG_COLOR)
    if winner == "player":
        msg = big_font.render("You Win!", True, (0, 255, 0))
    elif winner == "ai":
        msg = big_font.render("You Lose!", True, (255, 0, 0))
    else:
        msg = big_font.render("Draw!", True, WHITE)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
    restart_msg = font.render("Press R to return to menu", True, WHITE)
    screen.blit(restart_msg, (WIDTH//2 - restart_msg.get_width()//2, HEIGHT//2 + 60))

# --- Main game loop ---
units = []

while True:
    dt = clock.tick(60)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "Beginner"
                    game_state = LOADING
                    pygame.time.set_timer(pygame.USEREVENT, 2000)  # 2 sec loading
                elif event.key == pygame.K_2:
                    difficulty = "Hard"
                    game_state = LOADING
                    pygame.time.set_timer(pygame.USEREVENT, 2000)
                elif event.key == pygame.K_3:
                    difficulty = "Impossible"
                    game_state = LOADING
                    pygame.time.set_timer(pygame.USEREVENT, 2000)

        elif game_state == BATTLE:
            for card in cards:
                deploy = card.handle_event(event, player_elixir)
                if deploy:
                    name, x, y = deploy
                    # Deploy unit on player side left half only
                    if x < WIDTH // 2:
                        units.append(Unit(name, x, y, "player"))
                        player_elixir -= cards_data[name]["cost"]
                    card.reset_position(10 + card_names.index(card.name) * (CARD_WIDTH + 10), HEIGHT - CARD_BAR_HEIGHT + 15)

        elif game_state == RESULTS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = MENU

        if game_state == LOADING and event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            init_game()
            units = []
            game_state = BATTLE

    if game_state == MENU:
        draw_menu()

    elif game_state == LOADING:
        draw_loading()

    elif game_state == BATTLE:
        # Update elixir (player and AI)
        now = pygame.time.get_ticks()
        if now - last_elixir_update > ELIXIR_REGEN_RATE:
            last_elixir_update = now
            player_elixir = min(MAX_ELIXIR, player_elixir + 1)
            ai_elixir = min(MAX_ELIXIR, ai_elixir + 1)

        # AI deploy logic
        ai_play()

        # Update units
        # Convert dicts in deployed_units to Unit objects
        while deployed_units:
            d = deployed_units.pop()
            units.append(Unit(d["name"], d["x"], d["y"], d["side"]))

        # Assign targets for all units
        assign_targets(units, player_towers + ai_towers)

        # Move and attack
        for unit in units:
            if unit.alive:
                unit.move()
                unit.attack()
            else:
                units.remove(unit)

        # Remove dead towers
        for tower in player_towers + ai_towers:
            if tower.hp <= 0:
                tower.alive = False

        # Check win condition: if king tower destroyed
        player_king = next(t for t in player_towers if t.is_king)
        ai_king = next(t for t in ai_towers if t.is_king)
        if not player_king.alive:
            winner = "ai"
            game_state = RESULTS
        elif not ai_king.alive:
            winner = "player"
            game_state = RESULTS

        # Check timer end
        if draw_timer() == 0 and game_state == BATTLE:
            # Decide winner by tower hp total
            player_hp = sum(t.hp for t in player_towers if t.alive)
            ai_hp = sum(t.hp for t in ai_towers if t.alive)
            if player_hp > ai_hp:
                winner = "player"
            elif ai_hp > player_hp:
                winner = "ai"
            else:
                winner = None
            game_state = RESULTS

        draw_battle()

    elif game_state == RESULTS:
        draw_results()

    pygame.display.flip()
