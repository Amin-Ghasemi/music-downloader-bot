#          Imports          #
from pyrogram import Client, filters
from pyrogram.types import Message
from pytube import Search, YouTube
from os import listdir, rename
from random import randint
import requests
import subprocess

api_id = '1272537'
api_hash = '7cf7e855971ec61a606cc4ff5eaa3d1b'

app = Client('ytdl', api_id, api_hash)

def youtube_search(query):
    s = Search(query)
    return s.results

@app.on_message(filters.group & filters.text)
async def main(_:app, m:Message):
    text = m.text
    chat_id = m.chat.id
    user_id = m.from_user.id
    msg_id = m.message_id 

    if text == '.speed':
        try:
            cmd = [ 'speedtest-cli', '--share']
            output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
            output = output.decode().split("\n")

            addr = output[9].replace("Share results: ", "")

            r = requests.get(addr)

            with open("res.png", 'wb') as f:
                f.write(r.content)
                f.close()

            await app.send_photo(chat_id, "res.png", reply_to_message_id=msg_id)
        except Exception as e:
            await app.send_message(chat_id, e, reply_to_message_id=msg_id)

    if text.startswith(".s "):
        music_name = text.replace(".s ", '')
        try:
            msg = await app.send_message(chat_id, "**📥Uploading your music...**", reply_to_message_id=msg_id)
            msg_id2 = msg.message_id
            video = vars(youtube_search(music_name)[0])
            url = video.get("watch_url")
            title = video.get("_title")
            author = video.get('_author')
            
            folder_name = str(randint(5000000000000,999999999999999999999))
            yt = YouTube(url)
            yt.streams.get_audio_only().download(folder_name)

            if len(listdir(folder_name)) != 0:

                for i in listdir(folder_name):

                    with open(f"{folder_name}/{i}", 'rb') as video:
                        video_bytes = video.read()
                        with open(f"{folder_name}/{i}.mp3".replace(".mp4",""), 'wb') as audio:
                            audio.write(video_bytes)
                        video.close()
                        audio.close()

                    await app.send_audio(chat_id, f"{folder_name}/{i}.mp3".replace(".mp4",""), reply_to_message_id=msg_id)
            
            await app.delete_messages(chat_id, msg_id2)
                    
        except Exception as e:
            await app.send_message("dr_venom", e)


    elif text.startswith("آهنگ ") or text.startswith("اهنگ "):
        music_name = text
        try:
            msg = await app.send_message(chat_id, "**📥Uploading your music...**", reply_to_message_id=msg_id)
            msg_id2 = msg.message_id
            video = vars(youtube_search(music_name)[0])
            url = video.get("watch_url")
            title = video.get("_title")
            author = video.get('_author')
            
            folder_name = str(randint(5000000000000,999999999999999999999))
            yt = YouTube(url)
            yt.streams.get_audio_only().download(folder_name)

            if len(listdir(folder_name)) != 0:

                for i in listdir(folder_name):

                    with open(f"{folder_name}/{i}", 'rb') as video:
                        video_bytes = video.read()
                        with open(f"{folder_name}/{i}.mp3".replace(".mp4",""), 'wb') as audio:
                            audio.write(video_bytes)
                        video.close()
                        audio.close()

                    await app.send_audio(chat_id, f"{folder_name}/{i}.mp3".replace(".mp4",""), reply_to_message_id=msg_id)
            
            await app.delete_messages(chat_id, msg_id2)
                    
        except Exception as e:
            await app.send_message("dr_venom", e)

app.run()