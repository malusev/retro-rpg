import sys
import os
import pygame

# Automatically pre-render retro assets on startup if they don't exist
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
TILE_DIR = os.path.join(IMAGE_DIR, "tiles")

if not os.path.exists(TILE_DIR) or len(os.listdir(TILE_DIR)) < 11:
    print("Assets missing or incomplete. Pre-rendering sprites now...")
    try:
        import generate_assets
    except Exception as e:
        print(f"Error pre-rendering assets: {e}")

# Initialize pygame
pygame.init()

# --- WINDOW CONFIGURATION ---
TILE_SIZE = 32
GRID_COLS = 20
GRID_ROWS = 15
WINDOW_WIDTH = GRID_COLS * TILE_SIZE  # 640 px
WINDOW_HEIGHT = GRID_ROWS * TILE_SIZE # 480 px

# Create game window (Native Desktop Window)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mystic Valley Chronicles")
clock = pygame.time.Clock()

# --- LOAD RETRO GRAPHICS ---
def load_img(name, subfolder=""):
    path = os.path.join(IMAGE_DIR, subfolder, f"{name}.png")
    try:
        img = pygame.image.load(path).convert_alpha()
        return img
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))
        return surf

# Load tiles
TILES = {
    'grass': load_img("grass", "tiles"),
    'wall_stone': load_img("wall_stone", "tiles"),
    'roof': load_img("roof", "tiles"),
    'door': load_img("door", "tiles"),
    'wood_floor': load_img("wood_floor", "tiles"),
    'carpet': load_img("carpet", "tiles"),
    'water': load_img("water", "tiles"),
    'tree': load_img("tree", "tiles"),
    'bridge': load_img("bridge", "tiles"),
    'dirt_path': load_img("dirt_path", "tiles"),
    'flower': load_img("flower", "tiles"),
    'fence': load_img("fence", "tiles"),
    'black': pygame.Surface((32, 32))
}
TILES['black'].fill((0, 0, 0))

# Load player walk states for Warrior, Mage, and Hunter
PLAYER_SPRITES = {}
for c in ('warrior', 'mage', 'hunter'):
    PLAYER_SPRITES[c] = {}
    for d in ('down', 'up', 'left', 'right'):
        PLAYER_SPRITES[c][d] = {
            'stand': load_img(f"player_{c}_{d}_stand"),
            'walk1': load_img(f"player_{c}_{d}_walk1"),
            'walk2': load_img(f"player_{c}_{d}_walk2")
        }

# Load NPC sprites
NPC_SPRITES = {
    'npc_oldman_stand': load_img("npc_oldman_stand"),
    'npc_oldman_face': load_img("npc_oldman_face")
}
DUMMY_SPRITE = load_img("dummy")
SLIME_SPRITE = load_img("enemy_slime")
WATER_SLIME_SPRITE = load_img("enemy_water_slime")
FOREST_GOBLIN_SPRITE = load_img("enemy_forest_goblin")
FRUIT_PLANT_SPRITE = load_img("fruit_plant")
EMPTY_BUSH_SPRITE = load_img("empty_bush")


# --- EXPANDED 40x30 OVERWORLD MAP LAYOUT ---
# . = Grass, W = Wall, R = Roof, D = Door, ~ = Water, T = Tree, = = Bridge, p = Path, f = Flower, F = Fence

OVERWORLD_MAP = [
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT", # 0
    "Tf.................................................................................................T", # 1
    "T.......RRRR...............RRRR............TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT........................T", # 2
    "T.......RRRR...............RRRR............TfffffffffffffTfffffffffffffTTTT........................T", # 3
    "T.......WWWW...............WWWW............T.............T.............TTTT........................T", # 4
    "T.......WDWW...............WDWW............T.............T.............TTTT........................T", # 5
    "T........pp.................pp.............T...TTTTTTT...T...TTTTTTT...TTTT........................T", # 6
    "T........pp.................pp.............T...TfffffT...T...TfffffT...TTTT........................T", # 7
    "T........ppppppppppppppppppppp.............T...T.....T...T...T.....T...TTTT........................T", # 8
    "T..................pp.........TTTTTTTTTTpppppppppppppppppppppppppppppppppppp.......................T", # 9
    "T...F..F..F........pp........FTTTTTTTTT...................p........................................T", # 10
    "T...................pp........FTTf...fTTT...TTTTTTTTTTT.....p.....TTTTTTTTT........................T", # 11
    "T..................pp........FT.......TT....TfffffffffT.....p.....Tfffffffff.......................T", # 12
    "T..................pp........FT...f...TT....T.........T.....p.....T................................T", # 13
    "T..................pp........FTTT...TTTTTTTTT........T.....p.....TTTTTTTTT........................T", # 14
    "T~~~~~~~~~~~~~~~~~~==~~~~~~~~TTTTTTTTTTTTTTT.........T.....p.....TTTTTTTTT........................T", # 15
    "T~~~~~~~~~~~~~~~~~~==~~~~~~~~TTTTTTTTTTTTTTT.........T.....p.....TTTTTTTTT........................T", # 16
    "T...~~~~~~~~.......pp........FTT......TTTTTT.........T.....p.....T.........f......................T", # 17
    "T...~~~~~~~~~~......pp........FT...f...TTTTTT.........T.....ppppppp................................T", # 18
    "T..~~~~~~~~~~....ppppppppppppFT.......TT....T.........T.....p......................................T", # 19
    "T...~~~~~~~~~~....pp........ppFT...f...TTTTTT...TTTTTTT.....p.....TTTTTTTTTTT......................T", # 20
    "T....~~~~~~~~.....pp........RRRR.......TTTTTT...TfffffT.....p.....TfffffffffT......................T", # 21
    "T.................pp........RRRR.......TTTTTT...T.....T.....p.....T.........T......................T", # 22
    "T.................pp........WWWW.......TTTTTT...T.....T.....p.....T.........T......................T", # 23
    "T.................pp........WDWW.......TTTTTT...TTTTTTT.....p.....TTTTTTTTTTT......................T", # 24
    "T............................pp........TTTTTT...............p......................................T", # 25
    "Tf..........................pp........fTTffT................p......................................T", # 26
    "T............................pp............T................p......................................T", # 27
    "T..........................................T................p......................................T", # 28
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT.pp.TTTTTTTTTT................p......................................T", # 29
    "T~~~~~~~~~~~~~~~~~~~==~~~~~~~~.pp.TTTTTTTTTT................p......................................T", # 30
    "T~~~~~~~~~~~~~~~~~~==~~~~~~~~.pp.TffffTTTT..................ppppppppppppp..........................T", # 31
    "T~~~~~~~~~~~~~~~~~~==~~~~~~~~.pp.T....TTTT..............................p..........................T", # 32
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~.pp.T...TTTT....TTTTTTTTTTTTTTTTTTTTTT.....p..........................T", # 33
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~.pp.TfffffTTT...TffffffffffffffffffffT.....p..........................T", # 34
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~.pp.T............T...................T.....p..........................T", # 35
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~.pp.TTTTTTTTTTTTTT...................T.....p..........................T", # 36
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~.pppppppppppppppppppppppppppppppppppppppp...p..........................T", # 37
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~..........................................p..........................T", # 38
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~...............TTTTTTTTTTTTTTTTTTTTTT......p..........................T", # 39
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~...............TffffffffffffffffffffT......p..........................T", # 40
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~...............T....................T......p..........................T", # 41
    "Tf...........................................T....................T......p.....f....................T", # 42
    "T........................................................................p..........................T", # 43
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT..........................T", # 44
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~........p..........................T", # 45
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~........p..........................T", # 46
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~........p..........................T", # 47
    "T~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~........p..........................T", # 48
    "T........................................................................pppppppppppppppppppp......T", # 49
    "T...........................................................................................p......T", # 50
    "T......TTTTTTTTTTTTTTTT..................TTTTTTTTTTTTTTTTTTTTT..............................p......T", # 51
    "T......TffffffffffffffT..................TfffffffffffffffffTTT..............................p......T", # 52
    "T......T..............T..................T.................TTT..............................p......T", # 53
    "T......T..............T..................T.................TTT..............................p......T", # 54
    "T......T..............T..................T.................TTT..............................p......T", # 55
    "T......TTTTTTTTTTTTTTTT..................TTTTTTTTTTTTTTTTTTTTT..............................p......T", # 56
    "T...........................................................................................p......T", # 57
    "Tf..........................................................................................p.....fT", # 58
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"  # 59
]

# Map physical dimensions
MAP_COLS = len(OVERWORLD_MAP[0]) # 100
MAP_ROWS = len(OVERWORLD_MAP)    # 60
MAP_WIDTH_PX = MAP_COLS * TILE_SIZE   # 3200 px
MAP_HEIGHT_PX = MAP_ROWS * TILE_SIZE # 1920 px

# House Door Map Coordinates (Col, Row)
HOUSE_A_DOOR = (9, 5)   # Sandstone Cottage (Overworld coordinates)
HOUSE_B_DOOR = (28, 5)  # Timber Library (Overworld coordinates)
HOUSE_C_DOOR = (28, 25) # Wizard's Temple (Overworld coordinates)

# --- COZY INTERIOR ROOMS ---
INTERIOR_SANDSTONE = [
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKWWWWWWWWKKKKKK",
    "KKKKKKW......WKKKKKK",
    "KKKKKKW..C...WKKKKKK",
    "KKKKKKW.C.C..WKKKKKK",
    "KKKKKKW..C...WKKKKKK",
    "KKKKKKW......WKKKKKK",
    "KKKKKKWWWDWWWWKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK"
]

INTERIOR_LIBRARY = [
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKWWWWWWWWWWKKKK",
    "KKKKKKW........WKKKK",
    "KKKKKKW........WKKKK",
    "KKKKKKW...CC...WKKKK",
    "KKKKKKW..CCCC..WKKKK",
    "KKKKKKW...CC...WKKKK",
    "KKKKKKW........WKKKK",
    "KKKKKKW........WKKKK",
    "KKKKKKWWWWDWWWWWKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK"
]

INTERIOR_TEMPLE = [
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKWWWWWWWWWWKKKK",
    "KKKKKKW........WKKKK",
    "KKKKKKW.C....C.WKKKK",
    "KKKKKKW..C..C..WKKKK",
    "KKKKKKW...CC...WKKKK",
    "KKKKKKW..C..C..WKKKK",
    "KKKKKKW.C....C.WKKKK",
    "KKKKKKW........WKKKK",
    "KKKKKKWWWWDWWWWWKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK",
    "KKKKKKKKKKKKKKKKKKKK"
]


# --- CAMERA SCROLLING CONTROLLER ---
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shake_timer = 0
        self.shake_intensity = 0

    def shake(self, duration, intensity):
        self.shake_timer = duration
        self.shake_intensity = intensity

    def update(self, player_center_x, player_center_y):
        # Center target
        self.x = player_center_x - WINDOW_WIDTH / 2
        self.y = player_center_y - WINDOW_HEIGHT / 2
        # Clamp camera to map boundaries
        self.x = max(0, min(self.x, MAP_WIDTH_PX - WINDOW_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT_PX - WINDOW_HEIGHT))
        
        # Apply screen shake offsets
        if self.shake_timer > 0:
            import random
            self.x += random.randint(-self.shake_intensity, self.shake_intensity)
            self.y += random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_timer -= 1

    def apply(self, rect_or_coords):
        if isinstance(rect_or_coords, pygame.Rect):
            return rect_or_coords.move(-self.x, -self.y)
        else: # Coords tuple (x, y)
            return rect_or_coords[0] - self.x, rect_or_coords[1] - self.y

# --- PLAYER CONTROLLER CLASS ---
class Player:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.width = 24
        self.height = 24
        self.char_class = 'warrior' # 'warrior', 'mage', 'hunter'
        self.speed = 3.0
        self.direction = 'down'
        self.walking = False
        self.anim_timer = 0
        self.anim_frame = 'stand'
        
        # Combat Parameters
        self.attack_timer = 0
        self.stomp_timer = 0
        self.stomp_cooldown = 0 # In frames (60 fps, so 90 frames = 1.5s)
        
        # HP Parameters
        self.max_health = 100
        self.health = 100
        self.is_alive = True
        self.respawn_timer = 0

    def update_animation(self):
        # Handle death and resurrection loop
        if not self.is_alive:
            if self.respawn_timer > 0:
                self.respawn_timer -= 1
                if self.respawn_timer <= 0:
                    self.respawn()
            return

        # Decrement combat timers
        if self.stomp_cooldown > 0:
            self.stomp_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.stomp_timer > 0:
            self.stomp_timer -= 1

        if not self.walking:
            self.anim_frame = 'stand'
            return
        
        self.anim_timer += 1
        if self.anim_timer >= 6:
            self.anim_timer = 0
            if self.anim_frame == 'stand':
                self.anim_frame = 'walk1'
            elif self.anim_frame == 'walk1':
                self.anim_frame = 'stand_alt'
            elif self.anim_frame == 'stand_alt':
                self.anim_frame = 'walk2'
            else:
                self.anim_frame = 'stand'

    def draw(self, surf, camera, scene):
        if not self.is_alive:
            return

        frame_key = self.anim_frame
        if frame_key == 'stand_alt':
            frame_key = 'stand'
        
        sprite = PLAYER_SPRITES[self.char_class][self.direction][frame_key]
        # Offset rendering position using camera coordinates
        rx, ry = self.x, self.y
        if scene == 'overworld':
            rx, ry = camera.apply((self.x, self.y))
        surf.blit(sprite, (rx, ry))

        # --- DRAW COMBAT VISUALS ---
        p_center_x = self.x + self.width / 2
        p_center_y = self.y + self.height / 2
        rx_center, ry_center = p_center_x, p_center_y
        if scene == 'overworld':
            rx_center, ry_center = camera.apply((p_center_x, p_center_y))

        # 1. Normal Attack indicator
        if self.attack_timer > 0:
            if self.char_class == 'warrior':
                # Normal Warrior sword slash crescent swipe
                color = (178, 235, 242)
                offset_dist = 18
                if self.direction == 'up':
                    pygame.draw.circle(surf, color, (int(rx_center), int(ry_center - offset_dist)), 10 + self.attack_timer)
                    pygame.draw.circle(surf, (255, 255, 255), (int(rx_center), int(ry_center - offset_dist)), 6)
                elif self.direction == 'down':
                    pygame.draw.circle(surf, color, (int(rx_center), int(ry_center + offset_dist)), 10 + self.attack_timer)
                    pygame.draw.circle(surf, (255, 255, 255), (int(rx_center), int(ry_center + offset_dist)), 6)
                elif self.direction == 'left':
                    pygame.draw.circle(surf, color, (int(rx_center - offset_dist), int(ry_center)), 10 + self.attack_timer)
                    pygame.draw.circle(surf, (255, 255, 255), (int(rx_center - offset_dist), int(ry_center)), 6)
                else: # right
                    pygame.draw.circle(surf, color, (int(rx_center + offset_dist), int(ry_center)), 10 + self.attack_timer)
                    pygame.draw.circle(surf, (255, 255, 255), (int(rx_center + offset_dist), int(ry_center)), 6)
            elif self.char_class == 'mage':
                # Small blue spark halo at tip of staff
                pygame.draw.circle(surf, (3, 169, 244), (int(rx_center), int(ry_center)), 4 + self.attack_timer)
                pygame.draw.circle(surf, (224, 242, 241), (int(rx_center), int(ry_center)), 2)
            elif self.char_class == 'hunter':
                # Draw small white arrow nock visual
                pygame.draw.circle(surf, (244, 208, 63), (int(rx_center), int(ry_center)), 2)

        # 2. Secondary Skill AoE visual
        if self.stomp_timer > 0:
            elapsed = 15 - self.stomp_timer
            radius1 = elapsed * 5
            radius2 = max(0, (elapsed - 4) * 5)
            radius3 = max(0, (elapsed - 8) * 5)

            if self.char_class == 'warrior':
                # Warrior blue shockwaves
                if radius1 < 75:
                    pygame.draw.circle(surf, (33, 150, 243), (int(rx_center), int(ry_center)), radius1, 3)
                if radius2 > 0 and radius2 < 75:
                    pygame.draw.circle(surf, (179, 229, 252), (int(rx_center), int(ry_center)), radius2, 2)
                if radius3 > 0 and radius3 < 75:
                    pygame.draw.circle(surf, (255, 255, 255), (int(rx_center), int(ry_center)), radius3, 1)
            elif self.char_class == 'mage':
                # Mage blizzard concentric magical ice rings
                if radius1 < 85:
                    pygame.draw.circle(surf, (3, 169, 244), (int(rx_center), int(ry_center)), radius1, 3)
                if radius2 > 0 and radius2 < 85:
                    pygame.draw.circle(surf, (179, 229, 252), (int(rx_center), int(ry_center)), radius2, 2)
                if radius3 > 0 and radius3 < 85:
                    pygame.draw.circle(surf, (224, 242, 241), (int(rx_center), int(ry_center)), radius3, 1)
            elif self.char_class == 'hunter':
                # Green wind sweeps
                if radius1 < 60:
                    pygame.draw.circle(surf, (76, 175, 80), (int(rx_center), int(ry_center)), radius1, 2)
                if radius2 > 0 and radius2 < 60:
                    pygame.draw.circle(surf, (139, 195, 74), (int(rx_center), int(ry_center)), radius2, 1)

    def take_damage(self, damage, game):
        if not self.is_alive:
            return
        
        self.health = max(0, self.health - damage)
        
        # Shake screen slightly on bite!
        game.camera.shake(10, 2)
        
        # Spawn floating damage number
        game.floating_texts.append(
            FloatingText(self.x + 6, self.y - 8, f"-{damage}", (244, 67, 54))
        )
        
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_alive = False
        self.walking = False
        self.respawn_timer = 300 # 5 seconds at 60 fps

    def respawn(self):
        self.x = 19 * TILE_SIZE + 4
        self.y = 13 * TILE_SIZE + 4
        self.health = self.max_health
        self.is_alive = True
        self.direction = 'down'
        self.walking = False

    def get_rect(self):
        return pygame.Rect(self.x + 3, self.y + 8, self.width - 6, self.height - 10)

# --- FRUIT PLANT INTERACTIVE OBJECT CLASS ---
class FruitPlant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.has_fruit = True
        self.cooldown = 0 # Respawn fruit cooldown in frames

    def update(self):
        if not self.has_fruit:
            if self.cooldown > 0:
                self.cooldown -= 1
                if self.cooldown <= 0:
                    self.has_fruit = True

    def interact(self, player, game):
        if not self.has_fruit:
            game.floating_texts.append(
                FloatingText(self.x + 4, self.y - 8, "Bushes are bare...", (180, 180, 180))
            )
            return
            
        if player.health >= player.max_health:
            game.floating_texts.append(
                FloatingText(self.x + 4, self.y - 8, "Max HP!", (139, 195, 74))
            )
            return
            
        # Perform heal
        heal_amt = 35
        player.health = min(player.max_health, player.health + heal_amt)
        self.has_fruit = False
        self.cooldown = 1800 # 30 seconds at 60 FPS
        
        # Floating indicator with a beautiful critical feel
        game.floating_texts.append(
            FloatingText(self.x + 4, self.y - 12, f"+{heal_amt} HP", (76, 175, 80), is_crit=True)
        )

    def draw(self, surf, camera):
        rx, ry = camera.apply((self.x, self.y))
        sprite = FRUIT_PLANT_SPRITE if self.has_fruit else EMPTY_BUSH_SPRITE
        surf.blit(sprite, (rx, ry))


# --- DUMMY TARGET CLASS ---
class Dummy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.wiggle_timer = 0
        self.sprite = DUMMY_SPRITE

    def update(self):
        if self.wiggle_timer > 0:
            self.wiggle_timer -= 1

    def draw(self, surf, camera):
        rx, ry = camera.apply((self.x, self.y))
        # Horizontal wiggling offset
        if self.wiggle_timer > 0:
            import math
            offset_x = int(math.sin(self.wiggle_timer * 1.5) * 4)
            rx += offset_x
        surf.blit(self.sprite, (rx, ry))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- FLOATING DAMAGE TEXT SYSTEM ---
class FloatingText:
    def __init__(self, x, y, text, color=(255, 255, 255), is_crit=False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.is_crit = is_crit
        self.lifetime = 45 # Frames (0.75 seconds)
        self.vel_y = -1.2
        self.vel_x = (pygame.time.get_ticks() % 100 - 50) / 75.0 # Slight drift

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1

    def draw(self, surf, camera):
        rx, ry = camera.apply((self.x, self.y))
        
        # Adjust size based on critical hit
        font_size = 18 if self.is_crit else 12
        font = pygame.font.SysFont('Arial', font_size, bold=self.is_crit)
        
        # Shadows
        shadow_txt = font.render(self.text, True, (0, 0, 0))
        main_txt = font.render(self.text, True, self.color)
        
        surf.blit(shadow_txt, (rx + 1, ry + 1))
        surf.blit(main_txt, (rx, ry))

# --- ENEMY CONTROLLER CLASS ---
class Enemy:
    def __init__(self, start_x, start_y, name="Slime", enemy_type="slime"):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.width = 24
        self.height = 24
        self.name = name
        self.enemy_type = enemy_type
        
        # Configure stats by type
        if enemy_type == "water_slime":
            self.max_health = 65
            self.health = 65
            self.speed = 1.3
            self.sprite = WATER_SLIME_SPRITE
            self.damage_min = 12
            self.damage_max = 18
            self.chase_range = 140
        elif enemy_type == "forest_goblin":
            self.max_health = 90
            self.health = 90
            self.speed = 1.6
            self.sprite = FOREST_GOBLIN_SPRITE
            self.damage_min = 16
            self.damage_max = 24
            self.chase_range = 160
        else: # Standard slime
            self.max_health = 45
            self.health = 45
            self.speed = 1.0
            self.sprite = SLIME_SPRITE
            self.damage_min = 8
            self.damage_max = 14
            self.chase_range = 120
            
        self.is_alive = True
        self.respawn_timer = 0
        
        # Combat parameters
        self.wiggle_timer = 0
        self.attack_cooldown = 0 # Frames between bites
        self.attack_range = 24 # px

    def update(self, game, active_grid):
        player = game.player
        if not self.is_alive:
            if self.respawn_timer > 0:
                self.respawn_timer -= 1
                if self.respawn_timer <= 0:
                    self.respawn()
            return

        # Decrement cooldowns
        if self.wiggle_timer > 0:
            self.wiggle_timer -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Calculate distance to player
        import math
        p_center = (player.x + player.width / 2, player.y + player.height / 2)
        e_center = (self.x + self.width / 2, self.y + self.height / 2)
        
        dx = p_center[0] - e_center[0]
        dy = p_center[1] - e_center[1]
        dist = math.hypot(dx, dy)

        if player.is_alive and dist <= self.chase_range:
            # Active Chase State
            if dist > 0:
                # Normalize direction
                dir_x = dx / dist
                dir_y = dy / dist
                
                # Check target attack range
                if dist <= self.attack_range:
                    self.attack(player, game)
                else:
                    # Move towards player, but perform boundary/obstacle collisions!
                    self.move(dir_x * self.speed, dir_y * self.speed, active_grid)

    def move(self, dx, dy, active_grid):
        if dx != 0:
            original_x = self.x
            self.x += dx
            if self.x < 0 or self.x > MAP_WIDTH_PX - self.width or self.check_tile_collisions(active_grid):
                self.x = original_x

        if dy != 0:
            original_y = self.y
            self.y += dy
            if self.y < 0 or self.y > MAP_HEIGHT_PX - self.height or self.check_tile_collisions(active_grid):
                self.y = original_y

    def check_tile_collisions(self, active_grid):
        rect = self.get_rect()
        corners = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom)
        ]
        
        colliding_tiles = ['W', 'R', '~', 'T', 'K', 'F']
        # Water slimes can swim over water!
        if self.enemy_type == 'water_slime' and '~' in colliding_tiles:
            colliding_tiles.remove('~')
            
        for cx, cy in corners:
            col = int(cx // TILE_SIZE)
            row = int(cy // TILE_SIZE)
            if 0 <= col < len(active_grid[0]) and 0 <= row < len(active_grid):
                if active_grid[row][col] in colliding_tiles:
                    return True
        return False

    def attack(self, player, game):
        if self.attack_cooldown == 0:
            import random
            damage = random.randint(self.damage_min, self.damage_max)
            player.take_damage(damage, game)
            self.attack_cooldown = 45 # 0.75s between attacks

    def take_damage(self, damage, game):
        if not self.is_alive:
            return
        
        self.health = max(0, self.health - damage)
        self.wiggle_timer = 15
        
        if self.health <= 0:
            self.die(game)

    def die(self, game):
        self.is_alive = False
        self.respawn_timer = 1800 # 30 seconds at 60 fps
        game.floating_texts.append(
            FloatingText(self.x + 4, self.y - 10, "+50 XP", (139, 195, 74), is_crit=True)
        )

    def respawn(self):
        self.x = self.start_x
        self.y = self.start_y
        self.health = self.max_health
        self.is_alive = True
        self.respawn_timer = 0

    def draw(self, surf, camera):
        if not self.is_alive:
            return

        rx, ry = camera.apply((self.x, self.y))
        
        if self.wiggle_timer > 0:
            import math
            offset_x = int(math.sin(self.wiggle_timer * 1.5) * 4)
            rx += offset_x

        surf.blit(self.sprite, (rx, ry))

        # --- FLOATING ABOVE-HEAD HEALTH BAR ---
        bar_w = 24
        bar_h = 4
        bar_x = rx
        bar_y = ry - 8
        
        pygame.draw.rect(surf, (100, 100, 100), (bar_x, bar_y, bar_w, bar_h))
        fill_w = int((self.health / self.max_health) * bar_w)
        if fill_w > 0:
            color = (76, 175, 80) if self.health > self.max_health * 0.4 else (244, 67, 54)
            pygame.draw.rect(surf, color, (bar_x, bar_y, fill_w, bar_h))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)



# --- NPC CONTROLLER CLASS ---
class NPC:
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.name = name
        self.dialogue = dialogue

    def draw(self, surf, camera=None):
        rx, ry = self.x, self.y
        if camera:
            rx, ry = camera.apply((self.x, self.y))
            
        # Draw appropriate high-fidelity sprite based on name
        if self.name == "Dread Knight Roderick":
            sprite = PLAYER_SPRITES['warrior']['down']['stand']
        elif self.name == "Archmage Elena":
            sprite = PLAYER_SPRITES['mage']['down']['stand']
        elif self.name == "Ranger Gerald":
            sprite = PLAYER_SPRITES['hunter']['down']['stand']
        else:
            sprite = NPC_SPRITES['npc_oldman_stand']
            
        surf.blit(sprite, (rx, ry))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- RETRO PORTRAIT DIALOGUE SYSTEM ---
class DialogueSystem:
    def __init__(self):
        self.active = False
        self.npc = None
        self.page_idx = 0
        self.char_idx = 0.0
        self.typewriter_speed = 0.65 # Reveal characters per frame
        
    def start(self, npc):
        self.active = True
        self.npc = npc
        self.page_idx = 0
        self.char_idx = 0.0

    def update(self):
        if not self.active or not self.npc:
            return
        
        current_text = self.npc.dialogue[self.page_idx]
        if self.char_idx < len(current_text):
            self.char_idx += self.typewriter_speed
            if self.char_idx > len(current_text):
                self.char_idx = len(current_text)

    def next_page(self):
        if not self.active or not self.npc:
            return
        
        current_text = self.npc.dialogue[self.page_idx]
        # If text hasn't finished typing out, complete it instantly on press
        if self.char_idx < len(current_text):
            self.char_idx = len(current_text)
            return

        self.page_idx += 1
        self.char_idx = 0.0
        # If exceeded dialogue length, exit the conversation
        if self.page_idx >= len(self.npc.dialogue):
            self.active = False
            self.npc = None

    def draw(self, surf):
        if not self.active or not self.npc:
            return

        # 1. Dialogue Panel Dimensions
        margin = 16
        box_h = 110
        box_w = WINDOW_WIDTH - (margin * 2)
        box_x = margin
        box_y = WINDOW_HEIGHT - box_h - margin

        # Draw semi-transparent black dialog plate
        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((10, 10, 15, 230)) # Very dark glassmorphic navy
        surf.blit(box_surf, (box_x, box_y))

        # Elegant double retro ornamental borders
        pygame.draw.rect(surf, (251, 192, 45), (box_x, box_y, box_w, box_h), 2) # Gold outer
        pygame.draw.rect(surf, (244, 244, 244), (box_x + 3, box_y + 3, box_w - 6, box_h - 9), 1) # Silver inner

        # 2. Render Character Face Portrait (48x48 px, scaled up to 72x72 px for retro visual impact!)
        port_margin = 12
        port_size = 72
        port_x = box_x + port_margin
        port_y = box_y + port_margin

        # Black background for portrait
        pygame.draw.rect(surf, (0, 0, 0), (port_x, port_y, port_size, port_size))
        # Scaled blit
        portrait_img = pygame.transform.scale(NPC_SPRITES['npc_oldman_face'], (port_size, port_size))
        surf.blit(portrait_img, (port_x, port_y))
        # Portrait gold frame border
        pygame.draw.rect(surf, (251, 192, 45), (port_x, port_y, port_size, port_size), 2)

        # 3. Render NPC Name Plate
        font_name = pygame.font.SysFont('Georgia', 13, bold=True)
        name_txt = font_name.render(self.npc.name.upper(), True, (255, 235, 59))
        surf.blit(name_txt, (port_x + port_size + 14, box_y + 10))

        # Divider line
        pygame.draw.line(surf, (251, 192, 45, 120), (port_x + port_size + 14, box_y + 26), (box_x + box_w - 14, box_y + 26), 1)

        # 4. Render typewriter wrapped dialogue text
        font_body = pygame.font.SysFont('Arial', 13)
        full_text = self.npc.dialogue[self.page_idx]
        visible_text = full_text[:int(self.char_idx)]

        # Wrap text algorithm (Max character width per line)
        words = visible_text.split(' ')
        lines = []
        current_line = ""
        max_line_width = box_w - port_size - port_margin - 36 # Remaining text box width

        for word in words:
            test_line = current_line + " " + word if current_line else word
            width = font_body.size(test_line)[0]
            if width < max_line_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Blit each text line
        line_height = 18
        for l_idx, line in enumerate(lines[:3]): # Max 3 lines fit inside box
            txt_surf = font_body.render(line, True, (240, 240, 240))
            surf.blit(txt_surf, (port_x + port_size + 14, box_y + 34 + (l_idx * line_height)))

        # Press space indicator blinking symbol (on text finish)
        if int(self.char_idx) >= len(full_text):
            if (pygame.time.get_ticks() // 350) % 2 == 0:
                indicator = font_name.render("▶", True, (255, 235, 59))
                surf.blit(indicator, (box_x + box_w - 24, box_y + box_h - 22))

# --- RANGE PROJECTILES ENGINE ---
class Projectile:
    def __init__(self, x, y, dx, dy, speed, max_range, proj_type):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.max_range = max_range
        self.proj_type = proj_type # 'magic' or 'arrow'
        self.distance_traveled = 0
        self.width = 8
        self.height = 8
        self.is_active = True

    def update(self):
        move_dist = self.speed
        self.x += self.dx * move_dist
        self.y += self.dy * move_dist
        self.distance_traveled += move_dist
        if self.distance_traveled >= self.max_range:
            self.is_active = False

    def draw(self, surf, camera):
        # Apply camera offsets
        rx, ry = camera.apply((self.x, self.y))
        if self.proj_type == 'magic':
            # Glowing blue magical sphere
            pygame.draw.circle(surf, (3, 169, 244), (int(rx), int(ry)), 4)
            pygame.draw.circle(surf, (224, 242, 241), (int(rx), int(ry)), 2) # white center core
        elif self.proj_type == 'arrow':
            # Golden brown line arrow pointing in direction of movement
            end_x = rx + self.dx * 8
            end_y = ry + self.dy * 8
            pygame.draw.line(surf, (244, 208, 63), (int(rx), int(ry)), (int(end_x), int(end_y)), 2)

# --- MAIN GAME STATE MANAGEMENT ENGINE ---
class Game:
    def __init__(self):
        self.scene = 'overworld'
        self.menu_bg = load_img("menu_background")
        if self.menu_bg:
            self.menu_bg = pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # Player starting position (centered on overworld map)
        self.player = Player(19 * TILE_SIZE + 4, 13 * TILE_SIZE + 4)
        self.camera = Camera()
        
        # Instantiate Training Dummy in the center-left meadow
        self.dummy = Dummy(15 * TILE_SIZE + 4, 11 * TILE_SIZE + 4)
        self.floating_texts = []

        # Instantiate 25 Enemies across 3 different ecological varieties
        self.enemies = [
            # Grass Meadows: Green Slimes (7)
            Enemy(8 * TILE_SIZE + 4, 12 * TILE_SIZE + 4, "Meadow Slime A", "slime"),
            Enemy(21 * TILE_SIZE + 4, 8 * TILE_SIZE + 4, "Meadow Slime B", "slime"),
            Enemy(15 * TILE_SIZE + 4, 27 * TILE_SIZE + 4, "Meadow Slime C", "slime"),
            Enemy(32 * TILE_SIZE + 4, 30 * TILE_SIZE + 4, "Meadow Slime D", "slime"),
            Enemy(18 * TILE_SIZE + 4, 18 * TILE_SIZE + 4, "Meadow Slime E", "slime"),
            Enemy(25 * TILE_SIZE + 4, 23 * TILE_SIZE + 4, "Meadow Slime F", "slime"),
            Enemy(34 * TILE_SIZE + 4, 3 * TILE_SIZE + 4, "Meadow Slime G", "slime"),
            
            # South-West Lake Basin: Blue Water Slimes (8) - can swim on lake water!
            Enemy(6 * TILE_SIZE + 4, 19 * TILE_SIZE + 4, "Lake Slime A", "water_slime"),
            Enemy(10 * TILE_SIZE + 4, 21 * TILE_SIZE + 4, "Lake Slime B", "water_slime"),
            Enemy(8 * TILE_SIZE + 4, 35 * TILE_SIZE + 4, "Lake Slime C", "water_slime"),
            Enemy(22 * TILE_SIZE + 4, 39 * TILE_SIZE + 4, "Lake Slime D", "water_slime"),
            Enemy(15 * TILE_SIZE + 4, 42 * TILE_SIZE + 4, "Lake Slime E", "water_slime"),
            Enemy(2 * TILE_SIZE + 4, 32 * TILE_SIZE + 4, "Lake Slime F", "water_slime"),
            Enemy(11 * TILE_SIZE + 4, 43 * TILE_SIZE + 4, "Lake Slime G", "water_slime"),
            Enemy(28 * TILE_SIZE + 4, 36 * TILE_SIZE + 4, "Lake Slime H", "water_slime"),
            
            # East Ancient Forest: Purple Forest Goblins (10) - high damage, very fast
            Enemy(48 * TILE_SIZE + 4, 10 * TILE_SIZE + 4, "Forest Goblin A", "forest_goblin"),
            Enemy(55 * TILE_SIZE + 4, 14 * TILE_SIZE + 4, "Forest Goblin B", "forest_goblin"),
            Enemy(62 * TILE_SIZE + 4, 8 * TILE_SIZE + 4, "Forest Goblin C", "forest_goblin"),
            Enemy(52 * TILE_SIZE + 4, 25 * TILE_SIZE + 4, "Forest Goblin D", "forest_goblin"),
            Enemy(68 * TILE_SIZE + 4, 28 * TILE_SIZE + 4, "Forest Goblin E", "forest_goblin"),
            Enemy(58 * TILE_SIZE + 4, 40 * TILE_SIZE + 4, "Forest Goblin F", "forest_goblin"),
            Enemy(44 * TILE_SIZE + 4, 15 * TILE_SIZE + 4, "Forest Goblin G", "forest_goblin"),
            Enemy(72 * TILE_SIZE + 4, 12 * TILE_SIZE + 4, "Forest Goblin H", "forest_goblin"),
            Enemy(60 * TILE_SIZE + 4, 32 * TILE_SIZE + 4, "Forest Goblin I", "forest_goblin"),
            Enemy(74 * TILE_SIZE + 4, 42 * TILE_SIZE + 4, "Forest Goblin J", "forest_goblin")
        ]

        # Instantiate 12 Scattered Fruit Plants (healing berry bushes)
        self.fruit_plants = [
            FruitPlant(4 * TILE_SIZE + 4, 3 * TILE_SIZE + 4),   # North-West meadow
            FruitPlant(22 * TILE_SIZE + 4, 3 * TILE_SIZE + 4),  # North-East meadow
            FruitPlant(18 * TILE_SIZE + 4, 14 * TILE_SIZE + 4), # Center-meadow near river
            FruitPlant(31 * TILE_SIZE + 4, 10 * TILE_SIZE + 4), # East Forest entrance
            FruitPlant(36 * TILE_SIZE + 4, 18 * TILE_SIZE + 4), # Deep East Forest
            FruitPlant(14 * TILE_SIZE + 4, 25 * TILE_SIZE + 4), # South-West Meadow near Lake border
            FruitPlant(45 * TILE_SIZE + 4, 12 * TILE_SIZE + 4), # new deep forest north
            FruitPlant(72 * TILE_SIZE + 4, 5 * TILE_SIZE + 4),  # new deep forest far-east
            FruitPlant(52 * TILE_SIZE + 4, 28 * TILE_SIZE + 4), # new forest trail
            FruitPlant(70 * TILE_SIZE + 4, 35 * TILE_SIZE + 4), # new forest trail south
            FruitPlant(5 * TILE_SIZE + 4, 40 * TILE_SIZE + 4),  # new lake shore west
            FruitPlant(32 * TILE_SIZE + 4, 42 * TILE_SIZE + 4)  # new lake shore east
        ]

        # Instantiate Old Sage NPC inside House B (Timber Library)
        self.old_sage = NPC(
            8 * TILE_SIZE + 4,
            5 * TILE_SIZE + 4,
            "Old Sage",
            [
                "Greetings, young traveler! I am the Sage of these green meadows.",
                "The river dividing our valley has grown dangerous... Take care when crossing it.",
                "To cross safely, follow the dirt paths straight to the wooden bridge.",
                "The red brick temple in the south-east contains mysterious powers... ",
                "Feel free to rest here as long as you wish! Press SPACE to close."
            ]
        )

        # Instantiate 3 Overworld Story NPCs in the new expanded regions
        self.overworld_npcs = [
            NPC(
                55 * TILE_SIZE + 4,
                8 * TILE_SIZE + 4,
                "Dread Knight Roderick",
                [
                    "Halt, stranger! I am Roderick, the cursed Knight of the East Woods.",
                    "An ancient spell keeps me bound to these woods. Only when the valley is at peace may I rest.",
                    "Beware the purple forest goblins that roam deep within this woodland canopy...",
                    "They are fast, hostile, and strike with high-powered woodland clubs!"
                ]
            ),
            NPC(
                12 * TILE_SIZE + 4,
                38 * TILE_SIZE + 4,
                "Archmage Elena",
                [
                    "Welcome to the Azure Lake shore, young traveler.",
                    "The waters here contain intense magical auras... and deep blue aquatic slimes.",
                    "These water slimes are capable of gliding across the water's surface to chase you!",
                    "If you choose the Mage class, your staff magic can blast them from a safe distance."
                ]
            ),
            NPC(
                64 * TILE_SIZE + 4,
                24 * TILE_SIZE + 4,
                "Ranger Gerald",
                [
                    "Ah! A traveler navigating our forest trails. I am Ranger Gerald.",
                    "The paths here are winding but safe. I maintain them to keep the forest walkable.",
                    "If you require healing, seek out the wild bushes bearing sweet red berries.",
                    "Stand close to them and press SPACE to consume the berries for instant recovery!"
                ]
            )
        ]

        self.dialogue_system = DialogueSystem()

        # Multi-State Game Manager parameters
        self.state = 'loading' # States: 'loading', 'main_menu', 'class_select', 'playing', 'pause_menu'
        self.loading_timer = 0
        self.menu_idx = 0 # 0: New Game, 1: Exit Game
        self.pause_idx = 0 # 0: Resume, 1: Main Menu, 2: Exit Game
        self.class_idx = 0 # 0: Warrior, 1: Mage, 2: Hunter
        self.projectiles = [] # Active range weapon projectles

    def get_tile_at(self, map_grid, x, y):
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if 0 <= col < len(map_grid[0]) and 0 <= row < len(map_grid):
            return map_grid[row][col]
        return 'K'

    def check_collisions(self, map_grid, rect):
        corners = [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.right, rect.bottom)
        ]
        
        colliding_tiles = ('W', 'R', '~', 'T', 'K', 'F')
        for cx, cy in corners:
            tile = self.get_tile_at(map_grid, cx, cy)
            if tile in colliding_tiles:
                return True
        return False

    def handle_input(self):
        # Freeze movement input during conversations or if player is dead!
        if self.dialogue_system.active or not self.player.is_alive:
            self.player.walking = False
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        self.player.walking = False

        if keys[pygame.K_LEFT]:
            dx = -self.player.speed
            self.player.direction = 'left'
            self.player.walking = True
        elif keys[pygame.K_RIGHT]:
            dx = self.player.speed
            self.player.direction = 'right'
            self.player.walking = True
        elif keys[pygame.K_UP]:
            dy = -self.player.speed
            self.player.direction = 'up'
            self.player.walking = True
        elif keys[pygame.K_DOWN]:
            dy = self.player.speed
            self.player.direction = 'down'
            self.player.walking = True

        # Determine current grid collision constraints
        if self.scene == 'overworld':
            active_grid = OVERWORLD_MAP
        elif self.scene == 'interior_sandstone':
            active_grid = INTERIOR_SANDSTONE
        elif self.scene == 'interior_library':
            active_grid = INTERIOR_LIBRARY
        else: # interior_temple
            active_grid = INTERIOR_TEMPLE

        # Horizontal movement
        if dx != 0:
            original_x = self.player.x
            self.player.x += dx
            
            # Boundary checks
            map_w = MAP_WIDTH_PX if self.scene == 'overworld' else WINDOW_WIDTH
            if self.player.x < 0:
                self.player.x = 0
            elif self.player.x > map_w - self.player.width:
                self.player.x = map_w - self.player.width

            # Collision constraints
            if self.check_collisions(active_grid, self.player.get_rect()):
                self.player.x = original_x
            
            # NPC collision constraint (inside Library)
            if self.scene == 'interior_library':
                if self.player.get_rect().colliderect(self.old_sage.get_rect()):
                    self.player.x = original_x

            # Dummy collision constraint (overworld)
            if self.scene == 'overworld':
                if self.player.get_rect().colliderect(self.dummy.get_rect()):
                    self.player.x = original_x

            # Alive Enemies collision constraint (overworld)
            if self.scene == 'overworld':
                for enemy in self.enemies:
                    if enemy.is_alive and self.player.get_rect().colliderect(enemy.get_rect()):
                        self.player.x = original_x

        # Vertical movement
        if dy != 0:
            original_y = self.player.y
            self.player.y += dy
            
            map_h = MAP_HEIGHT_PX if self.scene == 'overworld' else WINDOW_HEIGHT
            if self.player.y < 0:
                self.player.y = 0
            elif self.player.y > map_h - self.player.height:
                self.player.y = map_h - self.player.height

            # Collision constraints
            if self.check_collisions(active_grid, self.player.get_rect()):
                self.player.y = original_y
            
            # NPC collision constraint (inside Library)
            if self.scene == 'interior_library':
                if self.player.get_rect().colliderect(self.old_sage.get_rect()):
                    self.player.y = original_y

            # Dummy collision constraint (overworld)
            if self.scene == 'overworld':
                if self.player.get_rect().colliderect(self.dummy.get_rect()):
                    self.player.y = original_y

            # Alive Enemies collision constraint (overworld)
            if self.scene == 'overworld':
                for enemy in self.enemies:
                    if enemy.is_alive and self.player.get_rect().colliderect(enemy.get_rect()):
                        self.player.y = original_y

    def check_transitions(self):
        player_center_x = self.player.x + self.player.width / 2
        player_center_y = self.player.y + self.player.height / 2
        
        if self.scene == 'overworld':
            tile = self.get_tile_at(OVERWORLD_MAP, player_center_x, player_center_y)
            if tile == 'D':
                # Determine which house doorway we entered using grid coords
                col = int(player_center_x // TILE_SIZE)
                row = int(player_center_y // TILE_SIZE)
                
                # Check Sandstone cottage (House A)
                if abs(col - HOUSE_A_DOOR[0]) <= 1 and abs(row - HOUSE_A_DOOR[1]) <= 1:
                    print("Entering House A (Sandstone cottage)...")
                    self.scene = 'interior_sandstone'
                    self.player.x = 9 * TILE_SIZE + 4
                    self.player.y = 8 * TILE_SIZE + 4
                    
                # Check Timber Library (House B)
                elif abs(col - HOUSE_B_DOOR[0]) <= 1 and abs(row - HOUSE_B_DOOR[1]) <= 1:
                    print("Entering House B (Timber Library)...")
                    self.scene = 'interior_library'
                    self.player.x = 9 * TILE_SIZE + 4
                    self.player.y = 8 * TILE_SIZE + 4
                    
                # Check Wizard Temple (House C)
                elif abs(col - HOUSE_C_DOOR[0]) <= 1 and abs(row - HOUSE_C_DOOR[1]) <= 1:
                    print("Entering House C (Wizard's Temple)...")
                    self.scene = 'interior_temple'
                    self.player.x = 9 * TILE_SIZE + 4
                    self.player.y = 8 * TILE_SIZE + 4
                    
                self.player.direction = 'up'
                self.player.walking = False
                
        elif self.scene == 'interior_sandstone':
            tile = self.get_tile_at(INTERIOR_SANDSTONE, player_center_x, player_center_y)
            if tile == 'D':
                print("Leaving House A...")
                self.scene = 'overworld'
                self.player.x = HOUSE_A_DOOR[0] * TILE_SIZE + 4
                self.player.y = (HOUSE_A_DOOR[1] + 1) * TILE_SIZE + 12
                self.player.direction = 'down'
                self.player.walking = False
                
        elif self.scene == 'interior_library':
            tile = self.get_tile_at(INTERIOR_LIBRARY, player_center_x, player_center_y)
            if tile == 'D':
                print("Leaving House B...")
                self.scene = 'overworld'
                self.player.x = HOUSE_B_DOOR[0] * TILE_SIZE + 4
                self.player.y = (HOUSE_B_DOOR[1] + 1) * TILE_SIZE + 12
                self.player.direction = 'down'
                self.player.walking = False
                
        elif self.scene == 'interior_temple':
            tile = self.get_tile_at(INTERIOR_TEMPLE, player_center_x, player_center_y)
            if tile == 'D':
                print("Leaving House C...")
                self.scene = 'overworld'
                self.player.x = HOUSE_C_DOOR[0] * TILE_SIZE + 4
                self.player.y = (HOUSE_C_DOOR[1] + 1) * TILE_SIZE + 12
                self.player.direction = 'down'
                self.player.walking = False

    def trigger_interaction(self):
        # Trigger NPC dialogues when next to NPC and Space is pressed
        if self.scene == 'interior_library':
            # Check proximity to Old Sage (distance < 45 px)
            p_center = pygame.math.Vector2(self.player.x + 12, self.player.y + 12)
            npc_center = pygame.math.Vector2(self.old_sage.x + 12, self.old_sage.y + 12)
            distance = p_center.distance_to(npc_center)
            
            if distance < 45:
                if not self.dialogue_system.active:
                    print("Talking to Old Sage...")
                    # Force player to face NPC
                    dx = self.old_sage.x - self.player.x
                    dy = self.old_sage.y - self.player.y
                    if abs(dx) > abs(dy):
                        self.player.direction = 'right' if dx > 0 else 'left'
                    else:
                        self.player.direction = 'down' if dy > 0 else 'up'
                        
                    self.dialogue_system.start(self.old_sage)
                else:
                    self.dialogue_system.next_page()
        elif self.scene == 'overworld':
            if self.dialogue_system.active:
                self.dialogue_system.next_page()
                return

            p_center = pygame.math.Vector2(self.player.x + 12, self.player.y + 12)
            print(f"[Interaction Debug] Player at ({self.player.x:.1f}, {self.player.y:.1f}) pressed SPACE.")
            
            # 1. Check proximity to overworld story NPCs (distance < 64 px)
            interacted_npc = False
            closest_npc_dist = 9999.0
            closest_npc_name = ""
            for npc in self.overworld_npcs:
                npc_center = pygame.math.Vector2(npc.x + 12, npc.y + 12)
                dist = p_center.distance_to(npc_center)
                if dist < closest_npc_dist:
                    closest_npc_dist = dist
                    closest_npc_name = npc.name
                if dist < 64:
                    print(f"[Interaction Log] Talking to story NPC {npc.name}. Distance: {dist:.1f} px.")
                    # Force player to face NPC
                    dx = npc.x - self.player.x
                    dy = npc.y - self.player.y
                    if abs(dx) > abs(dy):
                        self.player.direction = 'right' if dx > 0 else 'left'
                    else:
                        self.player.direction = 'down' if dy > 0 else 'up'
                        
                    self.dialogue_system.start(npc)
                    interacted_npc = True
                    break
                    
            if interacted_npc:
                return

            # 2. Check proximity to any FruitPlant (distance increased to 64 px for extremely generous usability!)
            interacted_plant = False
            closest_plant_dist = 9999.0
            for plant in self.fruit_plants:
                plant_center = pygame.math.Vector2(plant.x + 12, plant.y + 12)
                dist = p_center.distance_to(plant_center)
                if dist < closest_plant_dist:
                    closest_plant_dist = dist
                if dist < 64:
                    print(f"[Interaction Log] Interacting with berry bush at ({plant.x}, {plant.y}). Distance: {dist:.1f} px. Player health: {self.player.health}/{self.player.max_health}")
                    plant.interact(self.player, self)
                    interacted_plant = True
                    break
                    
            if not interacted_plant:
                print(f"[Interaction Debug] No overworld interaction triggered. Nearest story NPC: '{closest_npc_name}' ({closest_npc_dist:.1f} px away). Nearest berry bush: {closest_plant_dist:.1f} px away. Required: < 64 px.")

    def trigger_attack(self):
        if self.dialogue_system.active or not self.player.is_alive:
            return
        
        if self.player.char_class == 'warrior':
            # Initiate attack visual timer
            self.player.attack_timer = 10
            
            # Determine sword attack collision box based on current player direction
            offset_dist = 22
            if self.player.direction == 'up':
                attack_rect = pygame.Rect(self.player.x, self.player.y - offset_dist, 24, offset_dist)
            elif self.player.direction == 'down':
                attack_rect = pygame.Rect(self.player.x, self.player.y + 24, 24, offset_dist)
            elif self.player.direction == 'left':
                attack_rect = pygame.Rect(self.player.x - offset_dist, self.player.y, offset_dist, 24)
            else: # right
                attack_rect = pygame.Rect(self.player.x + 24, self.player.y, offset_dist, 24)

            # Check collision with dummy target (only in Overworld meadow!)
            if self.scene == 'overworld':
                if attack_rect.colliderect(self.dummy.get_rect()):
                    import random
                    damage = random.randint(12, 18)
                    self.dummy.wiggle_timer = 15
                    
                    # Spawn floating damage number
                    self.floating_texts.append(
                        FloatingText(self.dummy.x + 6, self.dummy.y - 8, f"-{damage}", (244, 67, 54))
                    )

                # Check collision with active slime enemies!
                for enemy in self.enemies:
                    if enemy.is_alive and attack_rect.colliderect(enemy.get_rect()):
                        import random
                        damage = random.randint(12, 18)
                        enemy.take_damage(damage, self)
                        
        elif self.player.char_class == 'mage':
            # Staff ranged magic sphere shoot
            self.player.attack_timer = 10
            dx, dy = 0, 0
            if self.player.direction == 'up': dy = -1
            elif self.player.direction == 'down': dy = 1
            elif self.player.direction == 'left': dx = -1
            elif self.player.direction == 'right': dx = 1
            else: dy = 1
            
            p_center_x = self.player.x + 8
            p_center_y = self.player.y + 8
            self.projectiles.append(
                Projectile(p_center_x, p_center_y, dx, dy, speed=5.0, max_range=180, proj_type='magic')
            )
            
        elif self.player.char_class == 'hunter':
            # Bow ranged arrow shoot
            self.player.attack_timer = 10
            dx, dy = 0, 0
            if self.player.direction == 'up': dy = -1
            elif self.player.direction == 'down': dy = 1
            elif self.player.direction == 'left': dx = -1
            elif self.player.direction == 'right': dx = 1
            else: dy = 1
            
            p_center_x = self.player.x + 8
            p_center_y = self.player.y + 8
            self.projectiles.append(
                Projectile(p_center_x, p_center_y, dx, dy, speed=6.5, max_range=160, proj_type='arrow')
            )

    def trigger_stomp(self):
        if self.dialogue_system.active or not self.player.is_alive:
            return
        if self.player.stomp_cooldown > 0:
            return

        # Trigger stomp visuals & cooldown
        self.player.stomp_timer = 15
        self.player.stomp_cooldown = 90 # 1.5s cooldown
        
        # Viewport Screen Shake! High retro feel impact feedback
        self.camera.shake(15, 4)

        if self.player.char_class == 'warrior':
            # Hit detection: circle area range of 75 pixels (only in Overworld)
            if self.scene == 'overworld':
                p_center = pygame.math.Vector2(self.player.x + 12, self.player.y + 12)
                d_center = pygame.math.Vector2(self.dummy.x + 12, self.dummy.y + 12)
                dist = p_center.distance_to(d_center)

                if dist < 75:
                    import random
                    damage = random.randint(40, 60)
                    self.dummy.wiggle_timer = 28
                    
                    # Spawn massive critical text
                    self.floating_texts.append(
                        FloatingText(self.dummy.x - 12, self.dummy.y - 12, f"STOMP! -{damage}", (253, 216, 53), is_crit=True)
                    )

                # Check stomp hits on active slimes inside radius
                for enemy in self.enemies:
                    if enemy.is_alive:
                        e_center = pygame.math.Vector2(enemy.x + 12, enemy.y + 12)
                        dist_to_enemy = p_center.distance_to(e_center)
                        if dist_to_enemy < 75:
                            import random
                            damage = random.randint(40, 60)
                            enemy.take_damage(damage, self)
                            
        elif self.player.char_class == 'mage':
            # Blizzard: massive area damage around player
            if self.scene == 'overworld':
                p_center = pygame.math.Vector2(self.player.x + 12, self.player.y + 12)
                d_center = pygame.math.Vector2(self.dummy.x + 12, self.dummy.y + 12)
                dist = p_center.distance_to(d_center)

                if dist < 85:
                    import random
                    damage = random.randint(45, 65)
                    self.dummy.wiggle_timer = 28
                    
                    # Spawn massive critical text
                    self.floating_texts.append(
                        FloatingText(self.dummy.x - 12, self.dummy.y - 12, f"BLIZZARD! -{damage}", (3, 169, 244), is_crit=True)
                    )

                # Check hits on slimes
                for enemy in self.enemies:
                    if enemy.is_alive:
                        e_center = pygame.math.Vector2(enemy.x + 12, enemy.y + 12)
                        dist_to_enemy = p_center.distance_to(e_center)
                        if dist_to_enemy < 85:
                            import random
                            damage = random.randint(45, 65)
                            enemy.take_damage(damage, self)
                            
        elif self.player.char_class == 'hunter':
            # Arrow Spray: shoot 5 arrows in a fan/cone front facing angle
            if self.scene == 'overworld':
                base_angle = 0
                if self.player.direction == 'right': base_angle = 0
                elif self.player.direction == 'down': base_angle = 90
                elif self.player.direction == 'left': base_angle = 180
                elif self.player.direction == 'up': base_angle = 270
                
                import math
                angles = [-30, -15, 0, 15, 30]
                p_center_x = self.player.x + 8
                p_center_y = self.player.y + 8
                for offset in angles:
                    rad = math.radians(base_angle + offset)
                    dx = math.cos(rad)
                    dy = math.sin(rad)
                    self.projectiles.append(
                        Projectile(p_center_x, p_center_y, dx, dy, speed=6.0, max_range=110, proj_type='arrow')
                    )

    def update_projectiles(self):
        if self.scene != 'overworld':
            self.projectiles.clear()
            return
            
        for proj in list(self.projectiles):
            proj.update()
            
            # Hit detection
            dummy_rect = self.dummy.get_rect()
            proj_rect = pygame.Rect(proj.x - 4, proj.y - 4, 8, 8)
            
            if proj_rect.colliderect(dummy_rect):
                proj.is_active = False
                import random
                damage = random.randint(10, 16) if proj.proj_type == 'magic' else random.randint(8, 14)
                self.dummy.wiggle_timer = 20
                self.floating_texts.append(
                    FloatingText(self.dummy.x + 6, self.dummy.y - 12, f"-{damage}", (3, 169, 244) if proj.proj_type == 'magic' else (255, 152, 0))
                )
                
            for enemy in self.enemies:
                if enemy.is_alive:
                    enemy_rect = enemy.get_rect()
                    if proj_rect.colliderect(enemy_rect):
                        proj.is_active = False
                        import random
                        damage = random.randint(10, 16) if proj.proj_type == 'magic' else random.randint(8, 14)
                        enemy.take_damage(damage, self)
                        
            if not proj.is_active:
                if proj in self.projectiles:
                    self.projectiles.remove(proj)

    def draw(self, surf):
        if self.state == 'loading':
            self.draw_loading_screen(surf)
            return
        elif self.state == 'main_menu':
            self.draw_main_menu(surf)
            return
        elif self.state == 'class_select':
            self.draw_class_select(surf)
            return

        # Handle camera tracking (Overworld only)
        if self.scene == 'overworld':
            p_center_x = self.player.x + self.player.width / 2
            p_center_y = self.player.y + self.player.height / 2
            self.camera.update(p_center_x, p_center_y)

            # Update training dummy wiggle updates
            self.dummy.update()

            # Update floating texts
            for ft in list(self.floating_texts):
                ft.update()
                if ft.lifetime <= 0:
                    self.floating_texts.remove(ft)

        # Resolve active map grid
        if self.scene == 'overworld':
            active_grid = OVERWORLD_MAP
        elif self.scene == 'interior_sandstone':
            active_grid = INTERIOR_SANDSTONE
        elif self.scene == 'interior_library':
            active_grid = INTERIOR_LIBRARY
        else:
            active_grid = INTERIOR_TEMPLE

        # Update enemies (overworld only)
        if self.scene == 'overworld':
            for enemy in self.enemies:
                enemy.update(self, active_grid)
            for plant in self.fruit_plants:
                plant.update()

        # 1. RENDER TILES LAYER
        if self.scene == 'overworld':
            start_col = max(0, int(self.camera.x // TILE_SIZE))
            end_col = min(MAP_COLS, int((self.camera.x + WINDOW_WIDTH) // TILE_SIZE) + 1)
            start_row = max(0, int(self.camera.y // TILE_SIZE))
            end_row = min(MAP_ROWS, int((self.camera.y + WINDOW_HEIGHT) // TILE_SIZE) + 1)
        else:
            start_col, end_col = 0, GRID_COLS
            start_row, end_row = 0, GRID_ROWS

        for r_idx in range(start_row, end_row):
            row_str = active_grid[r_idx]
            for c_idx in range(start_col, end_col):
                char = row_str[c_idx]
                px = c_idx * TILE_SIZE
                py = r_idx * TILE_SIZE

                # Map character to tile image blits
                if char == '.':
                    tile_img = TILES['grass'] if self.scene == 'overworld' else TILES['wood_floor']
                elif char == 'W':
                    tile_img = TILES['wall_stone']
                elif char == 'R':
                    tile_img = TILES['roof']
                elif char == 'D':
                    tile_img = TILES['door']
                elif char == '~':
                    tile_img = TILES['water']
                elif char == 'T':
                    surf.blit(TILES['grass'], (px - self.camera.x, py - self.camera.y) if self.scene == 'overworld' else (px, py))
                    tile_img = TILES['tree']
                elif char == 'C':
                    surf.blit(TILES['wood_floor'], (px, py))
                    tile_img = TILES['carpet']
                elif char == '=':
                    tile_img = TILES['bridge']
                elif char == 'p':
                    tile_img = TILES['dirt_path']
                elif char == 'f':
                    surf.blit(TILES['grass'], (px - self.camera.x, py - self.camera.y))
                    tile_img = TILES['flower']
                elif char == 'F':
                    surf.blit(TILES['grass'], (px - self.camera.x, py - self.camera.y))
                    tile_img = TILES['fence']
                else:
                    tile_img = TILES['black']

                # Apply Camera offset
                rx, ry = px, py
                if self.scene == 'overworld':
                    rx, ry = self.camera.apply((px, py))

                surf.blit(tile_img, (rx, ry))

        # 2. RENDER NPC LAYER
        if self.scene == 'interior_library':
            self.old_sage.draw(surf)
        elif self.scene == 'overworld':
            for npc in self.overworld_npcs:
                npc.draw(surf, self.camera)

        # 3. RENDER DUMMY TARGET (Meadow only)
        if self.scene == 'overworld':
            self.dummy.draw(surf, self.camera)

        # 3a. RENDER SCAVENGEABLE FRUIT PLANTS (Meadow only)
        if self.scene == 'overworld':
            for plant in self.fruit_plants:
                plant.draw(surf, self.camera)

        # 3b. RENDER ACTIVE SLIME ENEMIES (Meadow only)
        if self.scene == 'overworld':
            for enemy in self.enemies:
                enemy.draw(surf, self.camera)

        # 4. RENDER PLAYER LAYER
        self.player.draw(surf, self.camera, self.scene)

        # 4b. RENDER ACTIVE PROJECTILES (Meadow only)
        if self.scene == 'overworld':
            for proj in self.projectiles:
                proj.draw(surf, self.camera)

        # 5. RENDER FLOATING TEXTS LAYER
        if self.scene == 'overworld':
            for ft in self.floating_texts:
                ft.draw(surf, self.camera)

        # 6. RENDER DIALOGUE OVERLAY WINDOW
        if self.dialogue_system.active:
            self.dialogue_system.draw(surf)

        # 7. RENDER TRANS-BANNER UI HUD
        font = pygame.font.SysFont('Arial', 14, bold=True)
        
        # Translate Scene identifier
        if self.scene == 'overworld':
            area_name = "MEADOW VALES (SCROLLING MAP)"
        elif self.scene == 'interior_sandstone':
            area_name = "HOUSE A: SANDSTONE COTTAGE"
        elif self.scene == 'interior_library':
            area_name = "HOUSE B: TIMBER SAGE CABIN"
        else:
            area_name = "HOUSE C: WIZARD'S BRICK TEMPLE"

        txt_area = font.render(f"AREA: {area_name}", True, (255, 255, 255))
        
        if self.scene == 'interior_library':
            txt_ctrl = font.render("Move: WASD/Arrows | Stand near Old Sage & press SPACE to Chat!", True, (255, 235, 59))
        else:
            txt_ctrl = font.render("Move: WASD/Arrows  |  Attack [J]  |  Stomp [K]  |  Doors to Enter/Exit", True, (200, 200, 200))
        
        banner = pygame.Surface((WINDOW_WIDTH, 22), pygame.SRCALPHA)
        banner.fill((0, 0, 0, 165))
        surf.blit(banner, (0, 0))
        
        surf.blit(txt_area, (10, 3))
        surf.blit(txt_ctrl, (WINDOW_WIDTH - txt_ctrl.get_width() - 10, 3))

        # 8. RENDER PREMIUM CORNER HUD STATS PANEL (Meadow only)
        if self.scene == 'overworld':
            hud_x = 6
            hud_y = 24
            hud_w = 140
            hud_h = 52
            
            # Gold plate container base
            hud_bg = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
            hud_bg.fill((10, 10, 15, 205)) # dark navy-black glass
            surf.blit(hud_bg, (hud_x, hud_y))
            pygame.draw.rect(surf, (251, 192, 45), (hud_x, hud_y, hud_w, hud_h), 1) # gold border
            pygame.draw.rect(surf, (244, 244, 244, 80), (hud_x + 2, hud_y + 2, hud_w - 4, hud_h - 4), 1) # silver trim

            # --- PLAYER HEALTH BAR ---
            bar_x = hud_x + 10
            bar_y = hud_y + 8
            bar_w = 120
            bar_h = 15
            
            pygame.draw.rect(surf, (30, 30, 30), (bar_x, bar_y, bar_w, bar_h)) # HP dark background
            fill_hp_w = int((self.player.health / self.player.max_health) * bar_w)
            if fill_hp_w > 0:
                # Smooth HP color gradient
                pct = self.player.health / self.player.max_health
                if pct > 0.5:
                    hp_color = (76, 175, 80) # Vibrant green
                elif pct > 0.25:
                    hp_color = (255, 152, 0) # Orange warning
                else:
                    hp_color = (244, 67, 54) # Red danger
                pygame.draw.rect(surf, hp_color, (bar_x, bar_y, fill_hp_w, bar_h))
            
            # HP Numbers overlay
            font_hud = pygame.font.SysFont('Arial', 10, bold=True)
            txt_hp = font_hud.render(f"HP: {self.player.health} / {self.player.max_health}", True, (255, 255, 255))
            surf.blit(txt_hp, (bar_x + (bar_w - txt_hp.get_width()) / 2, bar_y + 1))

            # --- STOMP COOLDOWN BAR ---
            cd_x = bar_x
            cd_y = hud_y + 29
            cd_w = 120
            cd_h = 15
            
            pygame.draw.rect(surf, (30, 30, 30), (cd_x, cd_y, cd_w, cd_h)) # Cooldown dark background
            font_small = pygame.font.SysFont('Arial', 9, bold=True)

            if self.player.stomp_cooldown > 0:
                filled_w = int(((90 - self.player.stomp_cooldown) / 90.0) * cd_w)
                pygame.draw.rect(surf, (156, 39, 176), (cd_x, cd_y, filled_w, cd_h)) # Purple cooldown filling
                
                secs_left = int(self.player.stomp_cooldown / 60.0 * 10) / 10.0
                lbl_text = font_small.render(f"STOMP CD: {secs_left}s", True, (255, 255, 255))
            else:
                pygame.draw.rect(surf, (33, 150, 243), (cd_x, cd_y, cd_w, cd_h)) # Vibrant blue Ready bar
                lbl_text = font_small.render("STOMP [D]: READY!", True, (255, 255, 255))
                
            surf.blit(lbl_text, (cd_x + (cd_w - lbl_text.get_width()) / 2, cd_y + 2))        # 9. RENDER RED GAME OVER COOLDOWN OVERLAY (If player died!)
        if not self.player.is_alive:
            death_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            death_surf.fill((40, 10, 10, 210)) # Deep crimson transparent tint
            surf.blit(death_surf, (0, 0))
            
            font_title = pygame.font.SysFont('Georgia', 34, bold=True)
            font_sub = pygame.font.SysFont('Arial', 14, bold=True)
            
            txt_died = font_title.render("YOU DIED", True, (244, 67, 54))
            
            # Show remaining ticking seconds
            secs_left = int(self.player.respawn_timer / 60.0 * 10) / 10.0
            txt_count = font_sub.render(f"Resurrecting in {secs_left} seconds...", True, (255, 235, 59))
            
            surf.blit(txt_died, ((WINDOW_WIDTH - txt_died.get_width()) / 2, WINDOW_HEIGHT / 2 - 32))
            surf.blit(txt_count, ((WINDOW_WIDTH - txt_count.get_width()) / 2, WINDOW_HEIGHT / 2 + 12))

        # 10. RENDER IN-GAME PAUSE MENU (If state is pause_menu)
        if self.state == 'pause_menu':
            self.draw_pause_menu(surf)

    def draw_loading_screen(self, surf):
        # 1. Base Dark Slate Background
        surf.fill((10, 10, 15))
        
        # Increment timer
        self.loading_timer += 1
        if self.loading_timer >= 300: # 5 seconds at 60 fps total
            self.state = 'main_menu'
            return
            
        # Determine active splash text and calculate alpha opacity
        if self.loading_timer < 150:
            # "Code Studio M" Splash
            text_to_draw = "Code Studio M"
            sub_timer = self.loading_timer
            if sub_timer < 45:
                alpha = int((sub_timer / 45.0) * 255)
            elif sub_timer < 105:
                alpha = 255
            else:
                alpha = int((1.0 - (sub_timer - 105) / 45.0) * 255)
        else:
            # "miša prodakšn" Splash
            text_to_draw = "miša prodakšn"
            sub_timer = self.loading_timer - 150
            if sub_timer < 45:
                alpha = int((sub_timer / 45.0) * 255)
            elif sub_timer < 105:
                alpha = 255
            else:
                alpha = int((1.0 - (sub_timer - 105) / 45.0) * 255)
                
        alpha = max(0, min(255, alpha))

        # 2. Render Fading Splash Text
        font_splash = pygame.font.SysFont('Georgia', 36, bold=True, italic=True)
        txt_surf = font_splash.render(text_to_draw, True, (235, 240, 250)) # Silver/White-ish
        
        # Create a surface with identical dimensions with support for per-pixel alphas
        splash_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
        splash_surf.blit(txt_surf, (0, 0))
        
        # Blit a transparent tint
        tint_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
        tint_surf.fill((255, 255, 255, alpha))
        splash_surf.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        tx = (WINDOW_WIDTH - txt_surf.get_width()) / 2
        ty = (WINDOW_HEIGHT - txt_surf.get_height()) / 2
        surf.blit(splash_surf, (tx, ty))

    def draw_class_select(self, surf):
        # 1. Background forest gradient
        for y in range(WINDOW_HEIGHT):
            r = int(10 + (y / WINDOW_HEIGHT) * 15)
            g = int(10 + (y / WINDOW_HEIGHT) * 20)
            b = int(20 + (y / WINDOW_HEIGHT) * 25)
            pygame.draw.line(surf, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        # Borders
        pygame.draw.rect(surf, (251, 192, 45), (10, 10, WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20), 2)
        pygame.draw.rect(surf, (244, 244, 244, 40), (14, 14, WINDOW_WIDTH - 28, WINDOW_HEIGHT - 28), 1)

        # Header Title
        font_title = pygame.font.SysFont('Georgia', 28, bold=True)
        txt_title = font_title.render("SELECT YOUR HERO", True, (255, 235, 59))
        surf.blit(txt_title, ((WINDOW_WIDTH - txt_title.get_width()) / 2, 35))

        font_sub = pygame.font.SysFont('Georgia', 12, italic=True)
        txt_sub = font_sub.render("Choose a destiny to enter the overworld vales", True, (180, 180, 180))
        surf.blit(txt_sub, ((WINDOW_WIDTH - txt_sub.get_width()) / 2, 68))

        # 3 side-by-side cards
        card_w = 110
        card_h = 175
        card_gap = 14
        start_x = (WINDOW_WIDTH - (3 * card_w + 2 * card_gap)) / 2
        card_y = 95

        classes = [
            {
                'name': "WARRIOR",
                'type': 'warrior',
                'desc_weapon': "Sword Slash",
                'desc_skill': "Ground Stomp",
                'color': (30, 136, 229)
            },
            {
                'name': "MAGE",
                'type': 'mage',
                'desc_weapon': "Staff Orbs",
                'desc_skill': "Blizzard Blast",
                'color': (106, 27, 154)
            },
            {
                'name': "HUNTER",
                'type': 'hunter',
                'desc_weapon': "Bow & Arrow",
                'desc_skill': "Arrow Spray",
                'color': (56, 142, 60)
            }
        ]

        font_card_title = pygame.font.SysFont('Georgia', 14, bold=True)
        font_card_desc = pygame.font.SysFont('Arial', 10, bold=True)
        font_card_label = pygame.font.SysFont('Arial', 9)

        for idx, cls in enumerate(classes):
            cx = start_x + idx * (card_w + card_gap)
            cy = card_y
            is_selected = (idx == self.class_idx)

            # Draw card background
            card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            card_surf.fill((10, 10, 15, 220)) # Translucent obsidian
            surf.blit(card_surf, (cx, cy))

            # Draw card outline
            if is_selected:
                # Golden glowing border
                pygame.draw.rect(surf, (255, 235, 59), (cx, cy, card_w, card_h), 2)
                # Draw tiny glowing stars in corners
                pygame.draw.rect(surf, (255, 235, 59), (cx - 2, cy - 2, 5, 5))
                pygame.draw.rect(surf, (255, 235, 59), (cx + card_w - 3, cy - 2, 5, 5))
                pygame.draw.rect(surf, (255, 235, 59), (cx - 2, cy + card_h - 3, 5, 5))
                pygame.draw.rect(surf, (255, 235, 59), (cx + card_w - 3, cy + card_h - 3, 5, 5))
            else:
                pygame.draw.rect(surf, (100, 100, 110, 150), (cx, cy, card_w, card_h), 1)

            # Card Content
            # Class Name
            txt_name = font_card_title.render(cls['name'], True, (255, 235, 59) if is_selected else (200, 200, 200))
            surf.blit(txt_name, (cx + (card_w - txt_name.get_width()) / 2, cy + 12))

            # Render standing sprite centered on card
            sprite = PLAYER_SPRITES[cls['type']]['down']['stand']
            scaled_sprite = pygame.transform.scale(sprite, (36, 36))
            surf.blit(scaled_sprite, (cx + (card_w - 36) / 2, cy + 34))

            # Horizontal line
            pygame.draw.line(surf, (251, 192, 45, 60), (cx + 12, cy + 78), (cx + card_w - 12, cy + 78), 1)

            # Weapon label & name
            txt_w_lbl = font_card_label.render("PRIMARY WEAPON", True, (130, 130, 140))
            txt_w_val = font_card_desc.render(cls['desc_weapon'], True, (255, 255, 255))
            surf.blit(txt_w_lbl, (cx + (card_w - txt_w_lbl.get_width()) / 2, cy + 86))
            surf.blit(txt_w_val, (cx + (card_w - txt_w_val.get_width()) / 2, cy + 98))

            # Skill label & name
            txt_s_lbl = font_card_label.render("SPECIAL ABILITY", True, (130, 130, 140))
            txt_s_val = font_card_desc.render(cls['desc_skill'], True, cls['color'])
            surf.blit(txt_s_lbl, (cx + (card_w - txt_s_lbl.get_width()) / 2, cy + 120))
            surf.blit(txt_s_val, (cx + (card_w - txt_s_val.get_width()) / 2, cy + 132))

        # Bottom controls instructions
        font_inst = pygame.font.SysFont('Georgia', 12)
        txt_inst = font_inst.render("Press LEFT / RIGHT to choose  •  SPACE to confirm", True, (244, 244, 244, 180))
        surf.blit(txt_inst, ((WINDOW_WIDTH - txt_inst.get_width()) / 2, WINDOW_HEIGHT - 38))

    def draw_main_menu(self, surf):
        # 1. Blit the beautiful pixel art background
        if self.menu_bg:
            surf.blit(self.menu_bg, (0, 0))
        else:
            # Fallback forest gradient
            for y in range(WINDOW_HEIGHT):
                r = int(10 + (y / WINDOW_HEIGHT) * 15)
                g = int(10 + (y / WINDOW_HEIGHT) * 25)
                b = int(15 + (y / WINDOW_HEIGHT) * 20)
                pygame.draw.line(surf, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        # Translucent glass panel in center for beautiful contrast and readability
        pane_w = 240
        pane_h = 120
        pane_x = (WINDOW_WIDTH - pane_w) / 2
        pane_y = (WINDOW_HEIGHT - pane_h) / 2
        pane = pygame.Surface((pane_w, pane_h), pygame.SRCALPHA)
        pane.fill((5, 7, 12, 190)) # Elegant translucent charcoal
        surf.blit(pane, (pane_x, pane_y))
        
        # Sleek silver/white dual frames for card
        pygame.draw.rect(surf, (230, 235, 245, 140), (pane_x, pane_y, pane_w, pane_h), 2) # Outer
        pygame.draw.rect(surf, (244, 244, 244, 50), (pane_x + 4, pane_y + 4, pane_w - 8, pane_h - 8), 1) # Inner

        # 3. Selections (Centred inside glass panel)
        options = ["NEW GAME", "EXIT GAME"]
        font_opt = pygame.font.SysFont('Arial', 15, bold=True)
        
        start_y = pane_y + 26
        option_gap = 40
        
        for idx, opt in enumerate(options):
            is_selected = (idx == self.menu_idx)
            
            if is_selected:
                color = (255, 255, 255) # Clean White
                txt_opt = font_opt.render(f"▶  {opt}  ◀", True, color)
            else:
                color = (150, 155, 165) # Cool Grey
                txt_opt = font_opt.render(opt, True, color)
                
            ox = (WINDOW_WIDTH - txt_opt.get_width()) / 2
            oy = start_y + (idx * option_gap)
            
            if is_selected:
                plate = pygame.Surface((180, 26), pygame.SRCALPHA)
                plate.fill((240, 244, 255, 40)) # faint silvery plate
                surf.blit(plate, ((WINDOW_WIDTH - 180) / 2, oy - 3))
                pygame.draw.rect(surf, (240, 244, 255, 120), ((WINDOW_WIDTH - 180) / 2, oy - 3, 180, 26), 1)
                
            surf.blit(txt_opt, (ox, oy))

        # Bottom copyright
        font_copy = pygame.font.SysFont('Arial', 10)
        txt_copy = font_copy.render("© 2026 MIŠA PRODAKŠN. ALL RIGHTS RESERVED.", True, (140, 145, 155))
        surf.blit(txt_copy, ((WINDOW_WIDTH - txt_copy.get_width()) / 2, WINDOW_HEIGHT - 38))

    def draw_pause_menu(self, surf):
        # 1. Dim backplane
        dim_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((5, 5, 10, 175))
        surf.blit(dim_surf, (0, 0))

        # 2. Centered glassmorphic modal box
        box_w = 200
        box_h = 160
        box_x = (WINDOW_WIDTH - box_w) / 2
        box_y = (WINDOW_HEIGHT - box_h) / 2
        
        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((10, 10, 15, 240))
        surf.blit(box_surf, (box_x, box_y))
        
        pygame.draw.rect(surf, (251, 192, 45), (box_x, box_y, box_w, box_h), 2) # Gold
        pygame.draw.rect(surf, (244, 244, 244, 100), (box_x + 3, box_y + 3, box_w - 6, box_h - 6), 1) # Silver

        # 3. Pause title
        font_p = pygame.font.SysFont('Georgia', 18, bold=True)
        txt_p = font_p.render("GAME PAUSED", True, (255, 235, 59))
        surf.blit(txt_p, (box_x + (box_w - txt_p.get_width()) / 2, box_y + 16))

        pygame.draw.line(surf, (251, 192, 45, 80), (box_x + 30, box_y + 40), (box_x + box_w - 30, box_y + 40), 1)

        # 4. Options
        options = ["RESUME", "MAIN MENU", "EXIT GAME"]
        font_opt = pygame.font.SysFont('Arial', 13, bold=True)
        
        start_y = box_y + 54
        gap = 32
        
        for idx, opt in enumerate(options):
            is_selected = (idx == self.pause_idx)
            if is_selected:
                color = (255, 235, 59)
                txt_opt = font_opt.render(f"▶  {opt}  ◀", True, color)
            else:
                color = (180, 180, 180)
                txt_opt = font_opt.render(opt, True, color)
                
            ox = box_x + (box_w - txt_opt.get_width()) / 2
            oy = start_y + (idx * gap)
            
            if is_selected:
                pygame.draw.rect(surf, (255, 235, 59, 40), (box_x + 10, oy - 3, box_w - 20, 20))
                pygame.draw.rect(surf, (255, 235, 59, 100), (box_x + 10, oy - 3, box_w - 20, 20), 1)
                
            surf.blit(txt_opt, (ox, oy))



# --- MAIN ENTRY AND LOOPS ---
def main():
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.state == 'loading':
                    # Splash screen is non-interactive
                    pass
                elif game.state == 'main_menu':
                    if event.key == pygame.K_UP:
                        game.menu_idx = (game.menu_idx - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        game.menu_idx = (game.menu_idx + 1) % 2
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if game.menu_idx == 0:
                            # Go to class selection screen
                            game.state = 'class_select'
                            game.class_idx = 0
                        elif game.menu_idx == 1:
                            running = False
                elif game.state == 'class_select':
                    if event.key == pygame.K_LEFT:
                        game.class_idx = (game.class_idx - 1) % 3
                    elif event.key == pygame.K_RIGHT:
                        game.class_idx = (game.class_idx + 1) % 3
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        classes = ['warrior', 'mage', 'hunter']
                        game.player.char_class = classes[game.class_idx]
                        
                        # Reset stats based on class
                        if game.player.char_class == 'warrior':
                            game.player.max_health = 120
                            game.player.health = 120
                            game.player.speed = 3.0
                        elif game.player.char_class == 'mage':
                            game.player.max_health = 80
                            game.player.health = 80
                            game.player.speed = 2.8
                        else: # hunter
                            game.player.max_health = 100
                            game.player.health = 100
                            game.player.speed = 3.4
                        
                        game.state = 'playing'
                        game.player.respawn()
                        game.projectiles.clear()
                        for enemy in game.enemies:
                            enemy.respawn()
                elif game.state == 'playing':
                    if event.key == pygame.K_ESCAPE:
                        game.state = 'pause_menu'
                        game.pause_idx = 0
                    elif event.key == pygame.K_SPACE:
                        if game.dialogue_system.active:
                            game.dialogue_system.next_page()
                        else:
                            game.trigger_interaction()
                    elif event.key == pygame.K_a: # Remapped Attack key A
                        game.trigger_attack()
                    elif event.key == pygame.K_d: # Remapped Stomp key D
                        game.trigger_stomp()
                elif game.state == 'pause_menu':
                    if event.key == pygame.K_ESCAPE:
                        game.state = 'playing'
                    elif event.key == pygame.K_UP:
                        game.pause_idx = (game.pause_idx - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        game.pause_idx = (game.pause_idx + 1) % 3
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        if game.pause_idx == 0: # Resume
                            game.state = 'playing'
                        elif game.pause_idx == 1: # Return to Main Menu
                            game.state = 'main_menu'
                            game.menu_idx = 0
                        elif game.pause_idx == 2: # Exit Game
                            running = False

        # Update frame iterations
        if game.state == 'playing':
            game.handle_input()
            game.player.update_animation()
            game.dialogue_system.update()
            game.update_projectiles()
            game.check_transitions()
        elif game.state == 'loading':
            # We must call game.draw to tick loading_timer inside draw_loading_screen
            pass

        # Render everything
        game.draw(screen)
        pygame.display.flip()

        # Frame capping
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
