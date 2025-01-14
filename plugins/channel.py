from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import CHANNELS, MOVIE_UPDATE_CHANNEL, ADMINS
from database.ia_filterdb import save_file, unpack_new_file_id
from utils import get_poster, temp
from Naman.util.file_properties import formate_file_name
import re
from Script import script
from database.users_chats_db import db


processed_movies = set()

media_filter = filters.document | filters.video | filters.audio

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            break
    else:
        return
    media.file_type = file_type
    media.caption = message.caption
    success_sts = await save_file(media)
    post_mode =await db.update_post_mode_handle()
    file_id= unpack_new_file_id(media.file_id)
    if post_mode.get('all_files_post_mode', False) or success_sts == 'suc':
        await send_movie_updates(bot, file_name=media.file_name, file_id=file_id, post_mode=post_mode)

def name_format(file_name: str):
    file_name = file_name.lower()
    file_name = re.sub(r'http\S+', '', re.sub(r'@\w+|#\w+', '', file_name).replace('_', ' ').replace('[', '').replace(']', '')).strip()
    file_name = re.split(r's\d+|season\s*\d+|chapter\s*\d+', file_name, flags=re.IGNORECASE)[0]
    file_name = file_name.strip()
    words = file_name.split()[:4]
    imdb_file_name = ' '.join(words)
    return imdb_file_name

async def get_imdb(file_name, post_mode):
    imdb_file_name = name_format(file_name)
    imdb = await get_poster(imdb_file_name)
    file_name = f'File Name : <code>{formate_file_name(file_name)}</code>' if post_mode.get('singel_post_mode' , True) else ''
    if imdb:
        caption = script.MOVIES_UPDATE_TXT.format(
            title=imdb.get('title'),
            rating=imdb.get('rating'),
            genres=imdb.get('genres'),
            description=imdb.get('plot'),
            file_name=file_name
        )
        return imdb.get('title'), imdb.get('poster'), caption
    return None, None, None

async def send_movie_updates(bot, file_name, caption, file_id):
    if not post_mode.get('singel_post_mode' , True):
        try:
        year_match = re.search(r"\b(19|20)\d{2}\b", caption)
        year = year_match.group(0) if year_match else None      
        pattern = r"(?i)(?:s|season)0*(\d{1,2})"
        season = re.search(pattern, caption)
        if not season:
            season = re.search(pattern, file_name) 
        if year:
            file_name = file_name[:file_name.find(year) + 4]      
        if not year:
            if season:
                season = season.group(1) if season else None       
                file_name = file_name[:file_name.find(season) + 1]
        qualities = ["ORG", "org", "hdcam", "HDCAM", "HQ", "hq", "HDRip", "hdrip", 
                     "camrip", "WEB-DL" "CAMRip", "hdtc", "predvd", "DVDscr", "dvdscr", 
                     "dvdrip", "dvdscr", "HDTC", "dvdscreen", "HDTS", "hdts"]
        quality = await check_qualities(caption, qualities) or "HDRip"
        language = ""
        nb_languages = ["Hindi", "Bengali", "English", "Marathi", "Tamil", "Telugu", "Malayalam", "Kannada", "Punjabi", "Gujrati", "Korean", "Japanese", "Bhojpuri", "Dual", "Multi"]    
        for lang in nb_languages:
            if lang.lower() in caption.lower():
                language += f"{lang}, "
        language = language.strip(", ") or "Not Idea"
        movie_name = await movie_name_format(file_name)    
        if movie_name in processed_movies:
            return 
        processed_movies.add(movie_name)    
        poster_url = await get_imdb(movie_name)
        caption_message = f"#New_File_Added ✅\n\nFile_Name:- <code>{movie_name}</code>\n\nLanguage:- {language}\n\nQuality:- {quality}" 
        search_movie = movie_name.replace(" ", '-')
        movie_update_channel = await db.movies_update_channel_id()    
        btn = [[
            InlineKeyboardButton('📂 ɢᴇᴛ ғɪʟᴇ 📂', url=f'https://telegram.me/{temp.U_NAME}?start=getfile-{search_movie}')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        if poster_url:
            await bot.send_photo(movie_update_channel if movie_update_channel else MOVIE_UPDATE_CHANNEL, 
                                 photo=poster_url, caption=caption_message, reply_markup=reply_markup)
        else:
            no_poster = "https://telegra.ph/file/88d845b4f8a024a71465d.jpg"
            await bot.send_photo(movie_update_channel if movie_update_channel else MOVIE_UPDATE_CHANNEL, 
                                 photo=no_poster, caption=caption_message, reply_markup=reply_markup)  
    except Exception as e:
        print('Error in send_movie_updates', e)
        pass
