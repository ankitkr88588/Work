
from telethon.sync import TelegramClient, events, types
from telethon.sessions import StringSession
import re

api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6059901507:AAGnG6i4njSJ2GM0398xfX5vKHG80JzNU_s'

# Create a Telethon client
client = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)


# Open the file for reading
#file = open("admin.txt", "r")

# Read the entire content of the file
#file_content = file.read()

# Check if the number is in the file content
#if "6476862483" in file_content:
# Create the inline button
button = types.KeyboardButtonSwitchInline(
    text="Click me",
    query='',same_peer=True)

@client.on(events.NewMessage(pattern='/start|/notes|notes|Notes'))
async def start(event):
    # Send a response when someone starts the bot
    await event.reply(f'Click here to view all notes in\ninline.', buttons=[[button]])    



# Dictionary to store saved notes
saved_notes = {}

@client.on(events.NewMessage(pattern='/note (.+)'))
async def save_note_with_file(event):
    file = open("admin.txt", "r")
    file_content = file.read()
    print(event.sender_id, file_content)
    if event.reply_to_msg_id and str(event.sender_id) in str(file_content):
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id
        note_text = reply_message.text
        title = event.pattern_match.group(1).strip()
        
        note_file = None
        if reply_message.media:
            note_file = reply_message.media
            
        saved_notes[title] = {'text': note_text, 'file': note_file}
        await event.reply(f"Note with title '{title}' saved!")
        file.close()
@client.on(events.NewMessage(pattern='/cnote (.+)'))
async def clear_note(event):
    file = open("admin.txt", "r")
    file_content = file.read()
    note_title = event.pattern_match.group(1).strip()
    
    if note_title in saved_notes and str(event.sender_id) in str(file_content):
        del saved_notes[note_title]
        await event.reply(f"Note with title '{note_title}' cleared!")
        file.close()
    else:
        await event.reply(f"No note with title '{note_title}' found.")
        file.close()
@client.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text.lower()

    # Generate results based on saved notes' titles
    results = []
    for title, note_data in saved_notes.items():
        if query in title.lower():
            text = note_data['text']
            file = note_data['file']
            
            if file:
                results.append(
                    builder.document(
                        title=title,
                        text=text,
                        file=file,
                    )
                )
            else:
                results.append(
                    builder.article(
                        title=title,
                        description=text,
                        text=text,
                    )
                )
    
    await event.answer(results)

# Start the client
client.run_until_disconnected()

