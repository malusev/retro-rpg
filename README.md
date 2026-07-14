# Mystic Valley Chronicles 🌲✨

An immersive 16-bit retro top-down Action RPG built natively on Python and Pygame-CE. Choose your class, explore a massive sandbox overworld, interact with rich story NPCs, and battle hostile slimes and goblins across varied climates.

---

## 🎮 Gameplay & Controls

### ⚔️ Choose Your Hero Class
1. **Warrior**: Heavy health and speed. Carries a broadsword and uses the tactical **Ground Stomp** stun ability (`D` key).
2. **Mage**: Uses long-range fire staff projectiles and cast-focused elemental **Meteor Showers** (`D` key).
3. **Hunter**: Fast movement with a tactical hunter bow and a wide-arc **Arrow Spray** (`D` key).

### 🕹️ Keyboard Bindings
| Key Bindings | Action |
|---|---|
| `Arrow Keys` | Walk up, down, left, right |
| `A` | Standard Class Weapon Attack (Sword Swing, Staff Shoot, Bow Shot) |
| `D` | Class Special AoE Tactical Ability (Stomp, Meteor, Arrow Spray) |
| `Space` | Interact (Talk to story NPCs / Harvest red berry bushes for +35 HP) / Advance Dialogue |
| `Escape` | Access Pause Menu / Return |

---

## 🚀 How to Start the Game

### macOS Quick-Launch (Double-Click)
We have prepared a double-clickable launch file in the repository root:
1. Double-click the file named **`Play_Mystic_Valley_Chronicles.command`**.
2. It will open your terminal, activate your virtual environment automatically, and boot the game client!

> [!IMPORTANT]
> ### 🛑 macOS "Malware / Unidentified Developer" Warning Fix
> When you download files or repositories from GitHub, macOS automatically puts them in your **Downloads** directory and attaches a **quarantine flag** for safety. To clear this block:
> 
> 1. Open your native macOS **Terminal** application.
> 2. Run the following command (which targets the default macOS downloads directory):
>    ```bash
>    xattr -cr ~/Downloads/retro-rpg-main/Play_Mystic_Valley_Chronicles.command 2>/dev/null || xattr -cr ~/Downloads/Play_Mystic_Valley_Chronicles.command
>    ```
> 3. Press **Enter**. This instantly clears the Gatekeeper block, allowing you to double-click and launch the game flawlessly!

### Manual Console Launch
To start the game client manually via terminal:
1. **Activate Virtual Environment:**
   ```bash
   source ./venv/bin/activate
   ```
2. **Install Requirements (if needed):**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Game:**
   ```bash
   python main.py
   ```

---

## 🛠️ How to Build Standalone Executables

If you want to package the game into a standalone native binary or macOS application bundle (`.app`), you can easily compile it using PyInstaller:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
2. **Compile Project:**
   Run the PyInstaller command specifying asset bundling paths:
   ```bash
   pyinstaller --onefile --windowed --add-data "assets:assets" --name "Mystic Valley Chronicles" main.py
   ```
3. **Output Location:**
   Your compiled native files will be exported to the `dist/` directory:
   * **`dist/Mystic Valley Chronicles.app`** (macOS application bundle)
   * **`dist/Mystic Valley Chronicles`** (Standalone executable binary)

---

## 🗺️ Overworld Sandbox Geography
* **Map Size**: Huge **100 x 60** grid (6,000 retro tiles).
* **Grass Meadows (North-West)**: Home to training dummies, friendly villages, and Green Meadows Slimes.
* **Azure Lake Basin (South-West)**: An aquatic region populated by Blue Water Slimes that can swim across water tiles to chase you.
* **Ancient East Forest**: A dark woodland packed with high-damage, fast Purple Goblins.
* **Story NPCs**: 
  * *Dread Knight Roderick* (Ruins clearing, row 8)
  * *Archmage Elena* (Lake shoreline pier, row 38)
  * *Ranger Gerald* (Forest path intersection, row 24)