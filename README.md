# 📸 Discord Image Logger
 A V1.1 version with bugfixes, selfhosting capabilities, a better hosting platform, and more features will be coming soon!

**DISCORD RAT** is a simple yet powerful tool that I have created

Please note that this is **NOT** an "HACKING TOOL", but just an tool for being educated about shell commands

**If you're going to fork this repository, star it too while you're at it!**


# 💎 Features
* Fast, Free, and Easy!
* NOTE: its easily to reverse-engineere it. SO DONT USE IT AS HACKING TOOL 
* Requires only running it / compling it into an .EXE
* Have as many features as possible to make it untracable in the PDU'S
* ~~Under active development, many new features will be added!~~ Not so much, but a new version will be worked on soon! Drop ideas!

---

# 🔧 Configuration

Before setting it up, let's modify the **config.** <br>
Open up `bot.py` and edit the values, refer to the key below.

**WEBHOOK:** `Your DISCORD BOT HOOK!` <br>




* **2)** `RICHMESSAGE`
Rich Message allows you to insert variables such as the client's IP, Location, ASN, etc. for the Crashbrowser message. <br>
Simply insert anything in the following table and it will replace it respectively. <br>

| Commands |
|--------|
| `!kill` TERMINATE bot. |
| `!remove` Remove from startup |
| `!help` This menu but in discord chat <3|
| `!ping` Checek bot status |
| `!passwords` Browser passwords (obfscated urls) |
| `!apppass`  Application passwords |
| `!wifi` WiFi passwords |
| `!screenshot` Desktop screenshot |
| `!webcamss` Webcam screenshot |
| `!get <file>` Download an file |
| `!sysinfo` System information |
| `!clipboard` Get clipboard |
| `!active` Active window |
| `!remote` Enable Remote Desktop |
| `!unremote` Disable Remote Desktop |
| `!volume <0-100>` Set volume |
| `!lock` Lock workstation |
| `ANY OTHER COMMAND` Powershell execution |


---

# ⚒️ Setup

# Packaging main.py into an .exe with PyInstaller

## 1. Install Python dependencies
Download  `requirements.txt ` and `bot.py` and.:
Then install everything:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## 2. Install PyInstaller

\`\`\`bash
pip install pyinstaller
\`\`\`

## 3. Build the executable
From the folder containing main.py:

\`\`\`bash
pyinstaller --onefile main.py
\`\`\`

- `--onefile` bundles everything into a single .exe
- Omit it if you want a folder with the .exe plus its dependencies instead (faster startup, easier to inspect)

Useful optional flags:
- `--icon=youricon.ico` — custom icon
- `--noconsole` — hide the console window (GUI apps only — don't use this if your script prints output the user needs to see)
- `--name=YourAppName` — set the output filename
- `--add-data "source;dest"` — bundle extra files (configs, assets)

## 4. Find your .exe
After building, it'll be in:

\`\`\`
dist/main.exe
\`\`\`

The `build/` folder and `.spec` file are just intermediate build artifacts and can be deleted.

## 5. Test it
Run `dist/main.exe` on a clean machine (or VM) without Python installed, to confirm all dependencies were bundled correctly.

---

# 🐛 Bug Reports & Suggestions

**Found a bug? Have an idea?** Let me know [here!](../../issues) Please provide a detailed explanation of the expected behavior, actual behavior, and steps to reproduce, or what you want to see and how it could be done. You can be a small part of this project!
**Active/known bugs:**.
None at the moment!
---

# 📜 Closing Statements

Liked the project? I know you did! Support me, **drop a star!** <br>
here my [Ko-fi link](https://ko-fi.com/rjewi) 
Thank you for choosing my tools! 🙏
