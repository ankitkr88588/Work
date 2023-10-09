from telethon.sync import TelegramClient, events, Button
import os

api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6480106506:AAG3_E1hap62tZW_RVBREI4_FlJWKSK8gxo'
firmware_directory = '/home/u201853/firmware'

# Create a Telethon client
client = TelegramClient(None, api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user = await event.get_chat()
#    await event.reply(f"Hello, {user.first_name}! I'm your bot. Here are some .txt files in the current directory:")
    
    # Get a list of .txt files in the current directory
    txt_files = [os.path.splitext(file)[0] for file in os.listdir() if file.endswith('.txt')]
    
    if txt_files:
        # Create inline buttons for each .txt file, arranging them in pairs
        buttons = []
        for i in range(0, len(txt_files), 2):
            row_buttons = []
            for j in range(2):
                index = i + j
                if index < len(txt_files):
                    row_buttons.append(Button.inline(txt_files[index], data=txt_files[index]))
            buttons.append(row_buttons)
        
        await event.respond(f"👋 Hello! I'm your Firmware Provider bot. Here are some things you can do:\n\n\n\n"
                        "📱 Select your device to get firmware and custom ROMs.\n\nTo request firmware:@nub_coder_s"
                        "❓ Use /help to learn more about how to use this bot.", buttons=buttons)
    else:
        await event.reply("No .txt files found in the current directory.")

@client.on(events.CallbackQuery)
async def callback(event):
    selected_file = event.data.decode('utf-8')
    
    if selected_file == 'back':
        await event.delete()
        # User clicked the back button, go back to start event
        await start(event)
        return
    
    # Read the selected file and extract URLs with the format "V971: www.example.com"
    try:
        with open(selected_file + '.txt', 'r') as file:
            url_buttons = []
            urls = []
            for line in file:
                parts = line.strip().split(': ')
                if len(parts) == 2 and parts[1].startswith('http'):
                    urls.append((parts[0], parts[1]))
            
            # Create inline URL buttons, arranging them in pairs
            for i in range(0, len(urls), 2):
                row_buttons = []
                for j in range(2):
                    index = i + j
                    if index < len(urls):
                        row_buttons.append(Button.url(urls[index][0], urls[index][1]))
                url_buttons.append(row_buttons)
        
        # Add a back button to return to the start event
        url_buttons.append([Button.inline("Back", data="back")],)
        
        if url_buttons:
            #await event.edit(f"#CUSTOM-ROM1:\n\n***XOS 10 ReWorked***\n\n\n\nBy SOUROV KHAN N∆HID\n\nFlashing Guide :[Click Here](https://t.ly/23YsM)  \n\nReview : [Click Here](https://t.ly/rR7HS) \n\n\n\nChangelog :\n\n⚙️ Based on The latest Designed XOS\n\n⚙️ Boot Animation from Kali\n\n⚙️ Spoofing\n\n⚙️ Added Patches and Updates from Android 11,12 and 12L\n\n⚙️ All Bloatwares Removed\n\n⚙️ Added Voice Changer\n\n⚙️ Only Play Store and Pay Service PreLoaded\n\n⚙️ Stock Infinix Camera as default\n\n\n\nJoin :\n\nFollow @SourovKhanNahidYT (for Updates)\n\nReport Bugs on @SourovKhanNahid2\n\n\n\n\n\n#CUSTOM-ROM-2:\n\ndotOS | v5.2.1  | PORT | Android11By: Eko Rudianto\n\n\n\n🔹Port By: you n me\n\n🔹 How to Install: [click here](https://t.me/Infinix_Note11s/31552)\n\nNotes:\n\n• Boot will take upto 5-6 minutes\n\nBugs :\n\nScreenLock\n\nOTG (fix by magisk module)\n\nCheck other n fix together\n\n\n\nCredit:\n\n@InfinixHot10S@InfinixHot10\#dotOS\n\n#NOTE11s\n\n",buttons=url_buttons,link_preview=False)
        #else:
            await event.edit(f"Here are the some available firmware for your {selected_file}:\n\n⚠️Don't flash or use firmware from other devices, otherwise your phone might get bricked.\n\nPlease join:@nub_coder_s", buttons=url_buttons)

    except FileNotFoundError:
        await event.respond("Selected file not found.")
@client.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    help_message = """
    **Welcome to the Infinix Firmware Bot!**

This bot is designed to provide firmware and custom ROMs for various Infinix devices.

**How to Use:**
1. Start by using the /start command.
2. You will see a list of available device or model.
3. Select a device by clicking on its name WARNING: use your ow device firmware or custom rom.
4. The bot will then provide you with download links or information related to that device.

**Contact the Developer:**
If you have any questions, suggestions, or to request firmware, feel free to contact the developer:
- Bot managed by: @nub_coder_s

Thank you for using the Infinix Firmware Bot!
    """
    await event.reply(help_message, parse_mode='markdown')


client.run_until_disconnected()

