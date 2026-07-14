import os
import pygame

# Initialize pygame for surface handling (headless mode)
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

# Define directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
TILE_DIR = os.path.join(IMAGE_DIR, "tiles")

os.makedirs(TILE_DIR, exist_ok=True)

# Helper function to create a surface and draw pixels
def save_sprite(name, draw_func, size=(32, 32), is_tile=True):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    draw_func(surf)
    subfolder = TILE_DIR if is_tile else IMAGE_DIR
    path = os.path.join(subfolder, f"{name}.png")
    pygame.image.save(surf, path)
    print(f"Saved: {path}")

# --- DRAW TILE FUNCTIONS (32x32 px) ---

def draw_grass(surf):
    surf.fill((76, 175, 80)) # Green base
    # Add grass blade details
    pixels = pygame.PixelArray(surf)
    for x in range(32):
        for y in range(32):
            # Deterministic noise for beautiful textures
            noise = (x * 37 + y * 57) % 100
            if noise < 12:
                pixels[x, y] = (56, 142, 60) # Darker grass
            elif noise < 18:
                pixels[x, y] = (139, 195, 74) # Lighter grass
    del pixels

def draw_sandstone_wall(surf):
    surf.fill((210, 180, 140)) # Tan/sandstone base
    pixels = pygame.PixelArray(surf)
    # Draw horizontal mortar lines
    for y in (0, 15, 31):
        for x in range(32):
            pixels[x, y] = (101, 84, 70) # Dark mortar
    # Draw vertical mortar lines (offset bricks)
    for x in (0, 16):
        for y in range(16):
            pixels[x, y] = (101, 84, 70)
    for x in (8, 24):
        for y in range(16, 32):
            pixels[x, y] = (101, 84, 70)
    # Add minor brick highlights
    for x in range(32):
        for y in range(32):
            if (x + y) % 11 == 0 and pixels[x, y] == (210, 180, 140):
                pixels[x, y] = (230, 205, 170)
    del pixels

def draw_roof(surf):
    surf.fill((194, 24, 91)) # Crimson terracotta base
    pixels = pygame.PixelArray(surf)
    # Diagonal tile shading
    for x in range(32):
        for y in range(32):
            val = (x - y) % 8
            if val == 0:
                pixels[x, y] = (136, 14, 79) # Deep dark shadow
            elif val == 7:
                pixels[x, y] = (233, 30, 99) # Bright tile edge highlight
    del pixels

def draw_door(surf):
    surf.fill((93, 64, 55)) # Wood base brown
    pixels = pygame.PixelArray(surf)
    # Frame borders
    for x in range(32):
        for y in range(32):
            if x < 2 or x > 29 or y < 2:
                pixels[x, y] = (46, 34, 28) # Dark frame
    # Vertical plank grooves
    for x in (9, 16, 22):
        for y in range(2, 32):
            pixels[x, y] = (46, 34, 28)
    del pixels
    # Brass door knob (Yellow-gold)
    pygame.draw.circle(surf, (251, 192, 45), (26, 18), 2)
    pygame.draw.circle(surf, (245, 127, 23), (27, 18), 1)

def draw_wood_floor(surf):
    surf.fill((141, 110, 99)) # Light wood planks
    pixels = pygame.PixelArray(surf)
    # Draw floorboards vertical dividers
    for x in (0, 10, 21, 31):
        for y in range(32):
            pixels[x, y] = (78, 52, 46) # Dark brown divider
    # Draw minor wood grain highlights
    for x in range(32):
        for y in range(32):
            if (x * 7 + y) % 17 == 0 and pixels[x, y] == (141, 110, 99):
                pixels[x, y] = (161, 136, 127)
    del pixels

def draw_carpet(surf):
    surf.fill((183, 28, 28)) # Ruby red base
    # Draw gold border
    pygame.draw.rect(surf, (251, 192, 45), (2, 2, 28, 28), 2)
    # Inner blue royal sigil details
    pygame.draw.rect(surf, (21, 101, 192), (8, 8, 16, 16), 1)
    pygame.draw.circle(surf, (251, 192, 45), (16, 16), 2)

def draw_water(surf):
    surf.fill((2, 136, 209)) # Deep blue base
    pixels = pygame.PixelArray(surf)
    # Wavy dynamic patterns
    for x in range(32):
        for y in range(32):
            wave = (x + int(pygame.math.Vector2(0, y).length() * 0.5)) % 16
            if wave == 0:
                pixels[x, y] = (179, 229, 252) # Cyan highlight
            elif wave == 15:
                pixels[x, y] = (1, 87, 155) # Dark blue wave crease
    del pixels

def draw_tree_tile(surf):
    # Base transparent, we draw trunk and leafy head
    pygame.draw.rect(surf, (93, 64, 55), (12, 18, 8, 14)) # Trunk
    pygame.draw.circle(surf, (46, 125, 50), (16, 12), 10) # Center foliage
    pygame.draw.circle(surf, (56, 142, 60), (12, 10), 7)  # Top-left puff
    pygame.draw.circle(surf, (56, 142, 60), (20, 10), 7)  # Top-right puff
    pygame.draw.circle(surf, (104, 159, 56), (14, 8), 5)  # Sunlight puff top

def get_class_colors(char_class):
    if char_class == 'warrior':
        return {
            'cap': (229, 57, 53),      # Red cap
            'cap_bill': (229, 57, 53),
            'tunic': (30, 136, 229),    # Blue tunic
            'belt': (33, 33, 33),      # Black belt
            'pants': (62, 39, 35)       # Brown boots
        }
    elif char_class == 'mage':
        return {
            'cap': (123, 31, 162),     # Purple hood
            'cap_bill': (106, 27, 154),
            'tunic': (106, 27, 154),    # Purple robe
            'belt': (251, 192, 45),     # Golden belt
            'pants': (141, 110, 99)     # Light brown boots
        }
    else: # hunter
        return {
            'cap': (46, 125, 50),      # Forest green archer hood
            'cap_bill': (46, 125, 50),
            'tunic': (56, 142, 60),     # Green tunic
            'belt': (141, 110, 99),     # Brown leather belt
            'pants': (33, 33, 33)       # Charcoal boots
        }

def draw_player_down(surf, frame, char_class):
    colors = get_class_colors(char_class)
    # Cap / Hood
    pygame.draw.ellipse(surf, colors['cap'], (4, 2, 16, 8))
    # Cap bill / Hood rim
    pygame.draw.rect(surf, colors['cap_bill'], (12, 6, 8, 2))
    # Hair
    pygame.draw.rect(surf, (93, 64, 55), (5, 8, 14, 4))
    # Face (Peach)
    pygame.draw.rect(surf, (255, 204, 128), (6, 10, 12, 6))
    # Eyes (Black specs)
    surf.set_at((9, 12), (0, 0, 0))
    surf.set_at((14, 12), (0, 0, 0))
    # Tunic
    pygame.draw.rect(surf, colors['tunic'], (5, 15, 14, 6))
    # Belt
    pygame.draw.rect(surf, colors['belt'], (5, 18, 14, 2))
    # Legs / Feet
    if frame == 'stand':
        pygame.draw.rect(surf, colors['pants'], (6, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (14, 21, 4, 3))
    elif frame == 'walk1':
        pygame.draw.rect(surf, colors['pants'], (6, 19, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (14, 21, 4, 3))
    elif frame == 'walk2':
        pygame.draw.rect(surf, colors['pants'], (6, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (14, 19, 4, 3))

    # Weapon overlays (Down view)
    if char_class == 'warrior':
        # Steel Sword in right hand pointing down-right
        pygame.draw.line(surf, (189, 189, 189), (18, 14), (22, 18), 2)
        surf.set_at((18, 14), (121, 85, 72)) # Hilt
    elif char_class == 'mage':
        # Wooden Staff on right side with shining blue orb
        pygame.draw.line(surf, (121, 85, 72), (18, 22), (18, 8), 2)
        pygame.draw.circle(surf, (3, 169, 244), (18, 7), 2) # Sky blue magic tip
    elif char_class == 'hunter':
        # Curved wooden bow on the right
        pygame.draw.line(surf, (141, 110, 99), (18, 10), (21, 13), 2)
        pygame.draw.line(surf, (141, 110, 99), (21, 13), (18, 16), 2)
        pygame.draw.line(surf, (255, 255, 255), (18, 10), (18, 16), 1) # bowstring

def draw_player_up(surf, frame, char_class):
    colors = get_class_colors(char_class)
    # Cap / Hood
    pygame.draw.ellipse(surf, colors['cap'], (4, 2, 16, 8))
    # Hair (Back of head)
    pygame.draw.rect(surf, (93, 64, 55), (4, 8, 16, 8))
    # Tunic
    pygame.draw.rect(surf, colors['tunic'], (5, 15, 14, 6))
    # Belt
    pygame.draw.rect(surf, colors['belt'], (5, 18, 14, 2))
    # Legs / Feet
    if frame == 'stand':
        pygame.draw.rect(surf, colors['pants'], (6, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (14, 21, 4, 3))
    elif frame == 'walk1':
        pygame.draw.rect(surf, colors['pants'], (6, 19, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (14, 21, 4, 3))
    elif frame == 'walk2':
        pygame.draw.rect(surf, colors['pants'], (6, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (14, 19, 4, 3))

    # Weapon on back (Up view)
    if char_class == 'warrior':
        # Sword strapped diagonally across back
        pygame.draw.line(surf, (189, 189, 189), (8, 18), (17, 8), 2)
        surf.set_at((8, 18), (121, 85, 72))
    elif char_class == 'mage':
        # Staff on back
        pygame.draw.line(surf, (121, 85, 72), (16, 22), (16, 8), 2)
        pygame.draw.circle(surf, (3, 169, 244), (16, 7), 2)
    elif char_class == 'hunter':
        # Bow slung on back
        pygame.draw.line(surf, (141, 110, 99), (14, 10), (17, 13), 2)
        pygame.draw.line(surf, (141, 110, 99), (17, 13), (14, 16), 2)

def draw_player_left(surf, frame, char_class):
    colors = get_class_colors(char_class)
    # Cap / Hood
    pygame.draw.ellipse(surf, colors['cap'], (6, 2, 12, 8))
    pygame.draw.rect(surf, colors['cap_bill'], (4, 6, 4, 2)) # Bill profile
    # Hair
    pygame.draw.rect(surf, (93, 64, 55), (8, 8, 10, 4))
    # Face Profile
    pygame.draw.rect(surf, (255, 204, 128), (6, 10, 10, 6))
    # Eye (profile)
    surf.set_at((8, 12), (0, 0, 0))
    # Tunic
    pygame.draw.rect(surf, colors['tunic'], (6, 15, 12, 6))
    # Belt
    pygame.draw.rect(surf, colors['belt'], (6, 18, 12, 2))
    # Legs / Feet
    if frame == 'stand':
        pygame.draw.rect(surf, colors['pants'], (7, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (12, 21, 4, 3))
    elif frame == 'walk1':
        pygame.draw.rect(surf, colors['pants'], (7, 19, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (12, 21, 4, 3))
    elif frame == 'walk2':
        pygame.draw.rect(surf, colors['pants'], (7, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (12, 19, 4, 3))

    # Weapon pointing left in front (Left view)
    if char_class == 'warrior':
        pygame.draw.line(surf, (189, 189, 189), (6, 14), (1, 10), 2)
        surf.set_at((6, 14), (121, 85, 72))
    elif char_class == 'mage':
        pygame.draw.line(surf, (121, 85, 72), (5, 22), (5, 8), 2)
        pygame.draw.circle(surf, (3, 169, 244), (5, 7), 2)
    elif char_class == 'hunter':
        pygame.draw.line(surf, (141, 110, 99), (4, 10), (1, 13), 2)
        pygame.draw.line(surf, (141, 110, 99), (1, 13), (4, 16), 2)
        pygame.draw.line(surf, (255, 255, 255), (4, 10), (4, 16), 1)

def draw_player_right(surf, frame, char_class):
    colors = get_class_colors(char_class)
    # Cap / Hood
    pygame.draw.ellipse(surf, colors['cap'], (6, 2, 12, 8))
    pygame.draw.rect(surf, colors['cap_bill'], (16, 6, 4, 2)) # Bill right
    # Hair
    pygame.draw.rect(surf, (93, 64, 55), (6, 8, 10, 4))
    # Face profile
    pygame.draw.rect(surf, (255, 204, 128), (8, 10, 10, 6))
    # Eye (profile)
    surf.set_at((15, 12), (0, 0, 0))
    # Tunic
    pygame.draw.rect(surf, colors['tunic'], (6, 15, 12, 6))
    # Belt
    pygame.draw.rect(surf, colors['belt'], (6, 18, 12, 2))
    # Legs / Feet
    if frame == 'stand':
        pygame.draw.rect(surf, colors['pants'], (8, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (13, 21, 4, 3))
    elif frame == 'walk1':
        pygame.draw.rect(surf, colors['pants'], (8, 19, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (13, 21, 4, 3))
    elif frame == 'walk2':
        pygame.draw.rect(surf, colors['pants'], (8, 21, 4, 3))
        pygame.draw.rect(surf, colors['pants'], (13, 19, 4, 3))

    # Weapon pointing right (Right view)
    if char_class == 'warrior':
        pygame.draw.line(surf, (189, 189, 189), (18, 14), (23, 10), 2)
        surf.set_at((18, 14), (121, 85, 72))
    elif char_class == 'mage':
        pygame.draw.line(surf, (121, 85, 72), (19, 22), (19, 8), 2)
        pygame.draw.circle(surf, (3, 169, 244), (19, 7), 2)
    elif char_class == 'hunter':
        pygame.draw.line(surf, (141, 110, 99), (20, 10), (23, 13), 2)
        pygame.draw.line(surf, (141, 110, 99), (23, 13), (20, 16), 2)
        pygame.draw.line(surf, (255, 255, 255), (20, 10), (20, 16), 1)

def draw_bridge(surf):
    surf.fill((161, 136, 127)) # Light grey-brown wood
    # Planks lines
    pixels = pygame.PixelArray(surf)
    for y in range(0, 32, 6):
        for x in range(32):
            if 0 <= y < 32:
                pixels[x, y] = (93, 64, 55) # Dark mortar plank separators
    # Draw side rails
    for x in (0, 1, 30, 31):
        for y in range(32):
            pixels[x, y] = (78, 52, 46) # Thick handrails
    del pixels

def draw_dirt_path(surf):
    surf.fill((224, 195, 155)) # Warm sandy beige path
    pixels = pygame.PixelArray(surf)
    for x in range(32):
        for y in range(32):
            noise = (x * 13 + y * 97) % 100
            if noise < 8:
                pixels[x, y] = (194, 161, 121) # Dark dirt spot
            elif noise < 12:
                pixels[x, y] = (235, 212, 180) # Light dirt spot
    del pixels

def draw_flower(surf):
    # Base transparent, draw a little red and yellow flower
    pygame.draw.rect(surf, (56, 142, 60), (15, 16, 2, 16)) # Stem
    pygame.draw.circle(surf, (224, 242, 241), (16, 12), 6) # Petals
    pygame.draw.circle(surf, (229, 57, 53), (12, 12), 3) # Left petal
    pygame.draw.circle(surf, (229, 57, 53), (20, 12), 3) # Right petal
    pygame.draw.circle(surf, (229, 57, 53), (16, 8), 3) # Top petal
    pygame.draw.circle(surf, (229, 57, 53), (16, 16), 3) # Bottom petal
    pygame.draw.circle(surf, (253, 216, 53), (16, 12), 3) # Golden flower eye center

def draw_fence(surf):
    # Base transparent, draw a wooden fence tile
    # Post left & right
    pygame.draw.rect(surf, (109, 76, 65), (4, 4, 4, 28))
    pygame.draw.rect(surf, (109, 76, 65), (24, 4, 4, 28))
    # Top post cap
    pygame.draw.polygon(surf, (78, 52, 46), [(4, 4), (6, 0), (8, 4)])
    pygame.draw.polygon(surf, (78, 52, 46), [(24, 4), (26, 0), (28, 4)])
    # Two horizontal cross-beams
    pygame.draw.rect(surf, (141, 110, 99), (0, 8, 32, 4))
    pygame.draw.rect(surf, (141, 110, 99), (0, 20, 32, 4))

def draw_npc_oldman(surf):
    # Old wise sage standing (24x24 px)
    # Head / Hair (Grey)
    pygame.draw.circle(surf, (224, 224, 224), (12, 6), 6)
    # Face (Peach)
    pygame.draw.rect(surf, (255, 204, 128), (8, 6, 8, 5))
    # Beard (White)
    pygame.draw.polygon(surf, (255, 255, 255), [(7, 10), (12, 16), (17, 10)])
    # Eyes (Small specs)
    surf.set_at((10, 8), (0, 0, 0))
    surf.set_at((13, 8), (0, 0, 0))
    # Robe (Purple)
    pygame.draw.rect(surf, (106, 27, 154), (6, 12, 12, 10))
    # Sleeves & Hands
    pygame.draw.rect(surf, (123, 31, 162), (3, 12, 3, 7)) # Left sleeve
    pygame.draw.rect(surf, (123, 31, 162), (18, 12, 3, 7)) # Right sleeve
    surf.set_at((4, 19), (255, 204, 128)) # Left hand
    surf.set_at((19, 19), (255, 204, 128)) # Right hand
    # Walking stick (Brown)
    pygame.draw.rect(surf, (141, 110, 99), (2, 8, 2, 16))

def draw_npc_oldman_face(surf):
    # High-quality pixel portrait face of the old sage (48x48 px!)
    surf.fill((0, 0, 0, 0)) # Transparent base
    # Outer frame container circle (Grey hair bubble background)
    pygame.draw.circle(surf, (200, 200, 200), (24, 24), 22)
    # Inner Face (Peach skin)
    pygame.draw.rect(surf, (255, 213, 156), (12, 10, 24, 22))
    # Big bushy eyebrows (White-grey)
    pygame.draw.rect(surf, (245, 245, 245), (13, 12, 9, 4))
    pygame.draw.rect(surf, (245, 245, 245), (26, 12, 9, 4))
    # Wise kind eyes (Black)
    pygame.draw.rect(surf, (0, 0, 0), (15, 18, 4, 3))
    pygame.draw.rect(surf, (0, 0, 0), (29, 18, 4, 3))
    # Rose-pink cheeks
    pygame.draw.rect(surf, (255, 138, 128), (12, 23, 5, 3))
    pygame.draw.rect(surf, (255, 138, 128), (31, 23, 5, 3))
    # Long epic flowing beard (Bright White)
    pygame.draw.polygon(surf, (255, 255, 255), [(10, 26), (24, 46), (38, 26)])
    pygame.draw.rect(surf, (245, 245, 245), (14, 26, 20, 10))
    # Mustache (White overlay)
    pygame.draw.rect(surf, (255, 255, 255), (17, 26, 14, 4))
    # Eyes highlights (tiny white sparkle specs)
    surf.set_at((16, 18), (255, 255, 255))
    surf.set_at((30, 18), (255, 255, 255))
def draw_dummy(surf):
    # Straw training dummy (24x24 px)
    # Wood base post
    pygame.draw.rect(surf, (93, 64, 55), (10, 16, 4, 8)) # vertical pole
    pygame.draw.rect(surf, (78, 52, 46), (6, 22, 12, 2))  # base stand
    # Straw body (Beige/yellow cylinder)
    pygame.draw.ellipse(surf, (244, 208, 63), (6, 4, 12, 14))
    # Wood cross-arm posts
    pygame.draw.rect(surf, (93, 64, 55), (2, 8, 20, 3)) # horizontal arm bar
    # Red leather targets/straps on chest
    pygame.draw.rect(surf, (229, 57, 53), (9, 9, 6, 4)) # red chest block
    pygame.draw.circle(surf, (255, 255, 255), (12, 11), 1) # target center bullseye

def draw_slime(surf):
    # High-quality green bouncing slime sprite (24x24 px)
    surf.fill((0, 0, 0, 0)) # Transparent base
    # Outer dark shadow/border base
    pygame.draw.ellipse(surf, (27, 94, 32), (2, 6, 20, 16)) # Dark green outline
    # Inner body (Vibrant toxic green)
    pygame.draw.ellipse(surf, (76, 175, 80), (3, 7, 18, 14)) # Main lime green body
    # Highlights (Lighter green spec for wet gloss)
    pygame.draw.ellipse(surf, (139, 195, 74), (6, 9, 12, 5)) # Top wet light
    pygame.draw.circle(surf, (255, 255, 255), (8, 10), 1) # Wet specular dot
    # Angry red glowing eyes (classic retro mob!)
    pygame.draw.rect(surf, (229, 57, 53), (7, 13, 3, 2))  # Left eye red
    pygame.draw.rect(surf, (229, 57, 53), (14, 13, 3, 2)) # Right eye red
    # Tiny white sparkle in eyes
    surf.set_at((8, 13), (255, 255, 255))
    surf.set_at((15, 13), (255, 255, 255))
    # Small cute smile (dark green line)
    # Small cute smile (dark green line)
    pygame.draw.line(surf, (27, 94, 32), (11, 16), (13, 16))

def draw_water_slime(surf):
    surf.fill((0, 0, 0, 0)) # Transparent
    # Outer deep blue
    pygame.draw.ellipse(surf, (13, 71, 161), (2, 6, 20, 16))
    # Inner sky blue
    pygame.draw.ellipse(surf, (33, 150, 243), (3, 7, 18, 14))
    # Top wet light
    pygame.draw.ellipse(surf, (129, 212, 250), (6, 9, 12, 5))
    pygame.draw.circle(surf, (255, 255, 255), (8, 10), 1)
    # Angry eyes (Yellow-gold)
    pygame.draw.rect(surf, (255, 235, 59), (7, 13, 3, 2))
    pygame.draw.rect(surf, (255, 235, 59), (14, 13, 3, 2))
    # Sparkle
    surf.set_at((8, 13), (255, 255, 255))
    surf.set_at((15, 13), (255, 255, 255))
    # Smile
    pygame.draw.line(surf, (13, 71, 161), (11, 16), (13, 16))

def draw_forest_goblin(surf):
    surf.fill((0, 0, 0, 0))
    # Dark purple tunic
    pygame.draw.rect(surf, (74, 20, 140), (4, 10, 16, 12))
    # Large head
    pygame.draw.circle(surf, (142, 36, 170), (12, 8), 6) # Purple goblin head
    # Pointy ears
    pygame.draw.polygon(surf, (142, 36, 170), [(6, 8), (2, 4), (6, 6)]) # Left ear
    pygame.draw.polygon(surf, (142, 36, 170), [(18, 8), (22, 4), (18, 6)]) # Right ear
    # Angry red glowing eyes
    pygame.draw.circle(surf, (244, 67, 54), (10, 8), 1)
    pygame.draw.circle(surf, (244, 67, 54), (14, 8), 1)
    # Yellow boots
    pygame.draw.rect(surf, (191, 144, 0), (6, 21, 4, 3))
    pygame.draw.rect(surf, (191, 144, 0), (14, 21, 4, 3))

def draw_fruit_plant(surf):
    surf.fill((0, 0, 0, 0))
    # Shrub/Bush base
    pygame.draw.circle(surf, (27, 94, 32), (12, 14), 8) # Main body
    pygame.draw.circle(surf, (46, 125, 50), (8, 12), 6)  # Left puff
    pygame.draw.circle(surf, (46, 125, 50), (16, 12), 6) # Right puff
    pygame.draw.circle(surf, (139, 195, 74), (12, 8), 5) # Top highlights
    # Brown woody stem
    pygame.draw.rect(surf, (141, 110, 99), (11, 20, 3, 4))
    # Glowing red berries
    pygame.draw.circle(surf, (229, 57, 53), (7, 13), 2)  # Berry 1
    pygame.draw.circle(surf, (229, 57, 53), (17, 14), 2) # Berry 2
    pygame.draw.circle(surf, (229, 57, 53), (12, 10), 2) # Berry 3
    # Specular reflections on berries
    surf.set_at((7, 12), (255, 255, 255))
    surf.set_at((17, 13), (255, 255, 255))
    surf.set_at((12, 9), (255, 255, 255))

def draw_empty_bush(surf):
    surf.fill((0, 0, 0, 0))
    # Shrub/Bush base
    pygame.draw.circle(surf, (27, 94, 32), (12, 14), 8)
    pygame.draw.circle(surf, (46, 125, 50), (8, 12), 6)
    pygame.draw.circle(surf, (46, 125, 50), (16, 12), 6)
    pygame.draw.circle(surf, (139, 195, 74), (12, 8), 5)
    # Brown woody stem
    pygame.draw.rect(surf, (141, 110, 99), (11, 20, 3, 4))



# --- RUN GENERATION ---

print("Generating retro RPG pixel assets...")

# Tiles
save_sprite("grass", draw_grass)
save_sprite("wall_stone", draw_sandstone_wall)
save_sprite("roof", draw_roof)
save_sprite("door", draw_door)
save_sprite("wood_floor", draw_wood_floor)
save_sprite("carpet", draw_carpet)
save_sprite("water", draw_water)
save_sprite("tree", draw_tree_tile)
save_sprite("bridge", draw_bridge)
save_sprite("dirt_path", draw_dirt_path)
save_sprite("flower", draw_flower)
save_sprite("fence", draw_fence)

# Player Animations (Warrior, Mage, Hunter)
for c in ('warrior', 'mage', 'hunter'):
    for d in ('down', 'up', 'left', 'right'):
        for f in ('stand', 'walk1', 'walk2'):
            name = f"player_{c}_{d}_{f}"
            if d == 'down':
                save_sprite(name, lambda s, f=f, c=c: draw_player_down(s, f, c), size=(24, 24), is_tile=False)
            elif d == 'up':
                save_sprite(name, lambda s, f=f, c=c: draw_player_up(s, f, c), size=(24, 24), is_tile=False)
            elif d == 'left':
                save_sprite(name, lambda s, f=f, c=c: draw_player_left(s, f, c), size=(24, 24), is_tile=False)
            elif d == 'right':
                save_sprite(name, lambda s, f=f, c=c: draw_player_right(s, f, c), size=(24, 24), is_tile=False)

# NPC Sprites
save_sprite("npc_oldman_stand", draw_npc_oldman, size=(24, 24), is_tile=False)
save_sprite("npc_oldman_face", draw_npc_oldman_face, size=(48, 48), is_tile=False)

# Dummy target sprite
save_sprite("dummy", draw_dummy, size=(24, 24), is_tile=False)

# Enemy Slime sprites
save_sprite("enemy_slime", draw_slime, size=(24, 24), is_tile=False)
save_sprite("enemy_water_slime", draw_water_slime, size=(24, 24), is_tile=False)
save_sprite("enemy_forest_goblin", draw_forest_goblin, size=(24, 24), is_tile=False)

# Fruit plants & empty bush
save_sprite("fruit_plant", draw_fruit_plant, size=(24, 24), is_tile=False)
save_sprite("empty_bush", draw_empty_bush, size=(24, 24), is_tile=False)

print("Asset generation complete successfully!")


