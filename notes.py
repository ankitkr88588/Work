from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import re

api_id = 21856699
api_hash = '73f10cf0979637857170f03d4c86f251'
bot_token = '6400640505:AAEkS-gVOM_-W1eL_qRtjS3X9ARjBu14S18'

# Create a Telethon client
client = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)

# Dictionary to store saved notes
saved_notes = {}

@client.on(events.NewMessage(pattern='/save (.+)'))
async def save_note_with_file(event):
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id
        note_text = reply_message.text
        title = event.pattern_match.group(1).strip()
        
        note_file = None
        if reply_message.media:
            note_file = reply_message.media
            
        saved_notes[title] = {'text': note_text, 'file': note_file}
        await event.reply(f"Note with title '{title}' saved!")

@client.on(events.NewMessage(pattern='/clear (.+)'))
async def clear_note(event):
    note_title = event.pattern_match.group(1).strip()
    
    if note_title in saved_notes:
        del saved_notes[note_title]
        await event.reply(f"Note with title '{note_title}' cleared!")
    else:
        await event.reply(f"No note with title '{note_title}' found.")

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

