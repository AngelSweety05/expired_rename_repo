from asyncio import sleep
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery, Message
from pyrogram.errors import FloodWait
import humanize
import random
from helpo.txt import mr
from helpo.database import db
from config import START_PIC, FLOOD, ADMIN 
from plugins.cb_data import lazydevelopertaskmanager
import time
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ===========================================================================
# ===========================================================================
                    ### AUTO RENAME = STEP 1
# ===========================================================================

import re


# Mappings
resolutions = {
    "144p": "144p",
    "240p": "240p",
    "360p": "360p",
    "480p": "480p",
    "520p": "520p",
    "540p": "540p",
    "640p": "640p",
    "720p": "720p",
    "1080p": "1080p",
    "1440p": "1440p",
    "2160p": "2160p",
    "4320p": "4320p",
    "4k": "4K UHD",
    "8k": "8K UHD",
    "2K": "2K",
    "720i": "720i",
    "1080i": "1080i",
    "2.7K": "2.7K",
    "3K": "3K"
}
audios = {
    "dual audio": "Dual-Audio",
    "multi audio": "Multi-Audio",
}

languages = {
    "HIN": "Hindi",
    "ENG": "English",
    "TAM": "Tamil",
    "TEL": "Telugu",
    "MAY": "Malayalam",
    "PAN": "Punjabi",
    "SPA": "Spanish",
    "FRE": "French",
    "GER": "German",
    "CHN": "Chinese",
    "JPN": "Japanese",
    "KOR": "Korean",
    "RUS": "Russian",
    "ARA": "Arabic",
    "POR": "Portuguese",
    "ITA": "Italian",
    "BEN": "Bengali",
    "URD": "Urdu",
    "TUR": "Turkish",
    "POL": "Polish",
    "SWE": "Swedish",
    "DAN": "Danish",
    "FIN": "Finnish",
    "UKR": "Ukrainian",
    "ROM": "Romanian",
}

qualities = {
    
    "NF WEB-DL": "NF-WEB-DL",
    "NF WEBRip": "NF-WEBRip",
    "AMZN WEB-DL": "AMZN-WEB-DL",
    "4K WEB-DL": "4K WEB-DL",
    "WEB-DL": "WEB-DL",
    "NF WEBRIP": "NF-WEBRip",
    "AMZN WEBRIP": "AMZN-WEBRip",
    "WEBRIP": "WEBRip",
    #"HQ HDRIP": "HQ HDRip",
    "HDRIP": "HDRip",
    "DVDRIP": "DVDRip",
    "HDTV": "HDTV",
    "HDTS": "HDTS",
    "CamRip": "CamRip",
    "PreDvd": "PreDvd",
    "BDRip": "BDRip",
    "BRRip": "BRRip",
    "HDCAM": "HDCAM",
    "4K HDR": "4K HDR",
    "4K BluRay": "4K BluRay",
    "BLURAY": "BluRay",
    "10Bit HDR": "10Bit HDR",
    "8K WEB-DL": "8K WEB-DL",
    "8K HDR": "8K HDR",

}

subtitles = {
    "esubs": "ESub",
    "esub": "ESub",
    "hsubs": "HSub",
    "hsub": "HSub",
    "forcedsub": "Forced Subtitles",
    "multisub": "Multi-Language Subtitles",
    "cc": "Closed Captions",
    "subs": "Subtitles",
    "dualsub": "Dual Subtitles",
}

codecs = {
    "H.264": "AVC",
    "AVC": "AVC",
    "H.265": "HEVC",
    "HEVC": "HEVC",
    "DDP": "DDP",
    "10bit HEVC": "10Bit HEVC",
    "XviD": "XviD",
    "x264": "x264",
    "x265": "x265",
    "AAC": "AAC",
    "DTS": "DTS",
    "DTS-HD": "DTS-HD",
    "Dolby Atmos": "Dolby Atmos",
    "TrueHD": "TrueHD",
    "FLAC": "FLAC",
    "EAC3": "EAC3",
    "AC3": "AC3",
    "PCM": "PCM",
    "FHD": "Full HD",
    "QHD": "Quad HD",
    "HQ": "HQ",
    #"HD": "HD",
    #"SD": "SD",
    "HDR10": "HDR10",
    "HDR10+": "HDR10+",
    "Dolby Vision": "Dolby Vision",
}

# Updated regex patterns
season_regex = r"S(\d{1,3})"
episode_regex1 = r"E(\d{1,3})"
episode_regex2 = r"EP(\d{1,3})"
# multi_episode_regex = r"E(\d{1,3})[-](\d{1,3})"
# multi_episode_regex = r"E(\d{1,3})[-_](\d{1,3})"
# multi_episode_regex = r"(?:\bEP|E)(\d{1,3})\s*[-_]\s*(?!\d{3,4}p)(\d{1,3})"
multi_episode_regex1 = r"E(\d{1,3})\s*[-_]\s*(?!\d{3,4}p)(\d{1,3})"  # Matches E01-E10 (but not E01-1080p)
multi_episode_regex2 = r"EP(\d{1,3})\s*[-_]\s*(?!\d{3,4}p)(\d{1,3})"  # Matches E01-E10 (but not E01-1080p)

special_episode_regex = r"S(\d{1,3})E00"
complete_regex = r"Complete"  # Detects the word "Complete"


# 
unwanted_list = [
            '.','@','movies4u', 'pop', 'bid', 'clipmatemovies','clipmatemovie', 'bm_links', 
            'clipmatemovies', 'bm_links', 'piro', 'team_tamilanda', 'real_moviesadda', 
            'moviezaddiction', 'hdmovies', 'movieshub', 'telegrammovies', 'moviesboss', 
            'tamilrockers', 'katmoviehd', 'mkvcinemas', 'bolly4u', 'extramovies', '9xmovies', 
            'movierulz', 'hdhub4u', 'filmyzilla', 'worldfree4u', 'khatrimaza', 'desiremovies', 
            'mp4mania', 'skymovies', 'gofilms4u', 
            'pahe',    'watch online', 'free download', 'full hd', 'ad-free', 'no ads', 'official', 
            'exclusive', 'fast download', 'best quality', 'original print',
            'mkv', 'mp4', 'avi', 'flv', 'mov', 'wmv', 'webm', 'mpeg', 'mpg'
        ]

async def remove_unwanted_parts(file_name, title):
    # Remove the title from the filename
    title = title.lower()
    try:
        title = re.sub(r"\(\d{4}\)", "", title).strip()
    except Exception as e:
        logger.info(f"😂Known Error : {e}")
        pass
    file_name = file_name.lower().replace(title, ' ')

    # Remove all unwanted words
    for word in unwanted_list:
        file_name = file_name.replace(word.lower(), ' ').strip()
    print(f"this is cleaned : {file_name} ")
    # Remove resolutions
    for res in resolutions:
        file_name = file_name.lower().replace(res, '')

    # Remove codecs
    for codec in codecs:
        file_name = file_name.lower().replace(codec, '')

    # Remove subtitles
    for subtitle in subtitles:
        file_name = file_name.lower().replace(subtitle, '')

    # Remove any other known unwanted elements like season/episode patterns, extra spaces, special characters
    file_name = re.sub(r'[^\w\s]', '', file_name)  # Remove special characters

    # Clean extra spaces
    file_name = ' '.join(file_name.split())  # Remove extra spaces
    
    return file_name.strip()

# Function to extract season, episode, resolution, quality, and languages
async def extract_movie_details(filenmx, title):
    # Resolution
    file_name = filenmx
    if "." in file_name:
        file_name = file_name.replace(".", " ")
    if "_" in file_name:
        file_name = file_name.replace("_", " ")
    logger.info(f"📽 ORG Name : {file_name}")
    cleaned_file_name = await remove_unwanted_parts(file_name, title)
    logger.info(f"🧩Cleaned file name = {cleaned_file_name}")
    resolution = None
    for key in resolutions:
        if key.lower() in file_name.lower():
            resolution = resolutions[key]
            break
    
    # codec
    codec = None 
    for key in codecs:
        if key.lower() in file_name.lower():
            codec = codecs[key]
            if key.lower() == "h.265" or key.lower() == "hevc":
                break

    # Quality
    quality = None
    for key in qualities:
        if key.lower() in file_name.lower():
            quality = qualities[key]
            break

    audio = None
    for key in audios:
        if key.lower() in file_name.lower():
            audio = audios[key]
            break
    
    #subtitle
    subtitle = None
    for key in subtitles:
        if key.lower() in file_name.lower():
            subtitle = subtitles[key]
            break

# =================== little complex =========================== 

    # Languages
    detected_languages = []
    for key in languages:
        if key.lower() in cleaned_file_name.lower():
            language_name = languages[key]
            if "fandub" in cleaned_file_name.lower():
                language_name += "(fanDub)"
            elif "org" in cleaned_file_name.lower():
                language_name += "(org)"

            detected_languages.append(language_name)
    
    languages_list = "-".join(detected_languages) if detected_languages else None
    # print(languages_list)

    return resolution, quality, subtitle, audio, languages_list, codec

# Renaming logic
async def rename_movie_file(file_name, title):
    resolution, quality, subtitle, audio, languages_list, codec = await extract_movie_details(file_name, title)
    
    n_title = title if title is not None else ""  # Placeholder for extracting title (can enhance this further)
    n_resolution = f"{resolution} •" if resolution is not None else ""
    r_resolution = f"{resolution}" if resolution is not None else ""
    n_quality = f"{quality}" if quality is not None else ""
    n_languages = f"[{languages_list}]" if languages_list is not None else ""
    n_subtitle = f"{subtitle}" if subtitle is not None else ""
    n_codec = f"{codec}" if codec is not None else ""
    n_audio = f"{audio}" if audio is not None else ""

    new_name = f"{n_resolution} {n_title} - {r_resolution} {n_codec} {n_quality} {n_audio} {n_languages} {n_subtitle}"
    clean_new_name = re.sub(r'\s+', ' ', new_name).strip()

    return clean_new_name

# ========================== for webseries 👇 ==========================
# Function to extract type, season, episode, resolution, quality, and languages

async def is_webseries(file_name, title):
    if "." in file_name:
        file_name = file_name.replace(".", " ")
    if "_" in file_name:
        file_name = file_name.replace("_", " ")
    cleaned_file_name = await remove_unwanted_parts(file_name, title)

    # Patterns to match web series characteristics
    season_regex = r"S(\d{1,3})"  # Matches season numbers like "S01"
    episode_regex = r"(EP|\bE)(\d{1,3})"  # Matches episode numbers like "E01"
    # complete_regex = r"Complete"  # Detects the word "Complete"
    season_keyword_regex = r"Season\s*\d{1,3}"  # Matches "Season 1", "Season01", etc.

    # Check for any match
    if (
        re.search(season_regex, cleaned_file_name, re.IGNORECASE) or
        re.search(episode_regex, cleaned_file_name, re.IGNORECASE) or
        # re.search(complete_regex, file_name, re.IGNORECASE) or
        re.search(season_keyword_regex, cleaned_file_name, re.IGNORECASE)
    ):
        return True  # File is part of a web series
    return False  # Not a web series file

async def extract_details(filenmx, title):
    file_name = filenmx
    # Season and Episode
    if "." in file_name:
        file_name = file_name.replace(".", " ")
    if "_" in file_name:
        file_name = file_name.replace("_", " ")
    print(file_name)
    cleaned_file_name = await remove_unwanted_parts(file_name, title)
    logger.info(cleaned_file_name)
    
    season_match = re.search(season_regex, cleaned_file_name, re.IGNORECASE)
    multi_episode_match1 = re.search(multi_episode_regex1, cleaned_file_name, re.IGNORECASE)
    multi_episode_match2 = re.search(multi_episode_regex2, cleaned_file_name, re.IGNORECASE)
    episode_match1 = re.search(episode_regex1, cleaned_file_name, re.IGNORECASE)
    episode_match2 = re.search(episode_regex2, cleaned_file_name, re.IGNORECASE)
    special_match = re.search(special_episode_regex, cleaned_file_name, re.IGNORECASE)
    complete_match = re.search(complete_regex, cleaned_file_name, re.IGNORECASE)  # Case-insensitive matching for "Complete"

    # getting values
    season = f"S{int(season_match.group(1)):02}" if season_match else None
    full_season = f"Season {int(season_match.group(1)):02}" if season_match else None
    if multi_episode_match1:
        episode = f"E{int(multi_episode_match1.group(1)):02}-{int(multi_episode_match1.group(2)):02}"
        fullepisode = f"Episode {int(multi_episode_match1.group(1)):02}-{int(multi_episode_match1.group(2)):02}"
    elif multi_episode_match2:
        episode = f"E{int(multi_episode_match2.group(1)):02}-{int(multi_episode_match2.group(2)):02}"
        fullepisode = f"Episode {int(multi_episode_match2.group(1)):02}-{int(multi_episode_match2.group(2)):02}"
    elif special_match:
        episode = "Special-Ep"
        fullepisode = "Special Episode"

    elif episode_match1:
        episode = f"E{int(episode_match1.group(1)):02}"
        fullepisode = f"Episode {int(episode_match1.group(1)):02}"
    elif episode_match2:
        episode = f"E{int(episode_match2.group(1)):02}"
        fullepisode = f"Episode {int(episode_match2.group(1)):02}"
    else:
        episode = None
        fullepisode = None
    
    complete = None
    if (season or episode) and complete_match:
        # "Complete" should appear after season or episode information
        if file_name.lower().find('complete') > (file_name.lower().find(season) if season else file_name.lower().find(episode)):
            complete = "Complete"

    # Resolution
    resolution = None
    for key in resolutions:
        if key.lower() in file_name.lower():
            resolution = resolutions[key]
            break
    
    # codec
    codec = None 
    for key in codecs:
        if key.lower() in file_name.lower():
            codec = codecs[key]
            if key.lower() == "h.265" or key.lower() == "hevc":
                break

    # Quality
    quality = None
    for key in qualities:
        if key.lower() in cleaned_file_name.lower():
            quality = qualities[key]
            break
    
    #subtitle
    subtitle = None
    for key in subtitles:
        if key.lower() in file_name.lower():
            subtitle = subtitles[key]
            break

    audio = None
    for key in audios:
        if key.lower() in cleaned_file_name.lower():
            audio = audios[key]
            break
    # Languages
    detected_languages = []
    for key in languages:
        if key.lower() in cleaned_file_name.lower():
            language_name = languages[key]
            if "fandub" in cleaned_file_name.lower():
                language_name += "(fanDub)"
            elif "org" in cleaned_file_name.lower():
                language_name += "(org)"

            detected_languages.append(language_name)
    
    languages_list = "-".join(detected_languages) if detected_languages else None
    print(languages_list)

    return season, full_season, episode, resolution, quality, subtitle, audio, languages_list, fullepisode, codec, complete

async def rename_file(file_name, title):
    season, full_season, episode, resolution, quality, subtitle, audio, languages_list, fullepisode, codec, complete = await extract_details(file_name, title)
    n_title = title if title is not None else ""  # Placeholder for extracting title (can enhance this further)
    # n_title = extract_title(file_name)   # Placeholder for extracting title (can enhance this further)

    n_season = f"{season} •" if season is not None else ""
    n_episode = f"{episode} •" if episode is not None else ""
    n_audio = f"{audio}" if audio is not None else ""
    n_fullepisode = f"[{fullepisode}]" if fullepisode is not None else ""
    n_resolution = f"{resolution}" if resolution is not None else ""
    n_quality = f"{quality}" if quality is not None else ""
    n_languages = f"[{languages_list}]" if languages_list is not None else ""
    n_fullseason = f"[{full_season}]" if full_season is not None else ""
    n_subtitle = f"{subtitle}" if subtitle is not None else ""
    n_codec = f"{codec}" if codec is not None else ""
    n_complete = f"{complete} •" if complete is not None else ""
    new_name = f"{n_season} {n_complete} {n_episode} {n_title} {n_fullseason} {n_fullepisode} {n_resolution} {n_codec} {n_quality} {n_audio} {n_languages} {n_subtitle}"
    clean_new_name = re.sub(r'\s+', ' ', new_name).strip()
    return clean_new_name
# ========================== for webseries 👆 ==========================

async def check_extension_and_watermark(file, new_file_name):
    try:
        if not "." in new_file_name:
            if "." in file.file_name:
                extn = file.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
        # watermark = "@real_MoviesAdda6"
        new_lazy_name = new_file_name + " @real_MoviesAdda6." + extn
    except Exception as e:
        new_lazy_name = new_file_name + " @real_MoviesAdda6.mkv"
        print(e)
        pass
    return new_lazy_name

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def auto_rename(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    title = message.caption
    print(title)
    if title is None:
        return message.reply("😕 ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜ ʜᴀᴠᴇ ᴍᴇɴᴛɪᴏɴᴇᴅ sᴇʀɪᴇs ɴᴀᴍᴇ ɪɴ ғɪʟᴇ...")

    lazymsg = await message.reply(f"<b>🤞 ʟᴇᴛ ᴛʜᴇ ᴍᴀɢɪᴄ ʙᴇɢɪɴ... ❤</b>", parse_mode=enums.ParseMode.HTML)
    if await is_webseries(filename, title):
        print("Detected webseries")
        new_file_name = await rename_file(filename, title)

        new_lazy_name = await check_extension_and_watermark(file, new_file_name)
    else:
        new_file_name = await rename_movie_file(filename, title)
        new_lazy_name = await check_extension_and_watermark(file, new_file_name)
    # finally calling renamer logic // adding task
    await lazydevelopertaskmanager(client, message, new_lazy_name, lazymsg)







    # await client.send_message(
    #     chat_id=message.from_user.id, 
    #     text=f"<blockquote>📌ᴏʀɪɢɪɴᴀʟ : {filename}</blockquote>\n<blockquote>🤞ʀᴇɴᴀᴍᴇᴅ : <code>{new_lazy_name}</code></blockquote>",
    #     parse_mode=enums.ParseMode.HTML
    #     )




# ===========================================================================
                    ### ./ AUTO RENAME = STEP 1
# ===========================================================================
# ===========================================================================



# @Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
# async def rename_start(client, message):
#     file = getattr(message, message.media.value)
#     filename = file.file_name
#     filesize = humanize.naturalsize(file.file_size) 
#     fileid = file.file_id
#     try:
#         text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
#         buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
#                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
#         await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
#         await sleep(FLOOD)
#     except FloodWait as e:
#         await sleep(e.value)
#         text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
#         buttons = [[ InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename") ],
#                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
#         await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
#     except:
#         pass

# @Client.on_message(filters.private & filters.command(["start"]))
# async def start(client, message):
#     user = message.from_user
#     if not await db.is_user_exist(user.id):
#         await db.add_user(user.id)     
#     txt=f"👋 Hey {user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ! 🍟"
#     button=InlineKeyboardMarkup([[
#         InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
#         ],[
#         InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs', url='https://t.me/LazyDeveloper'),
#         InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ', url='https://t.me/LazyDeveloper')
#         ],[
#         InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ', callback_data='about'),
#         InlineKeyboardButton('ℹ ʜᴇʟᴘ', callback_data='help')
#         ]])
#     if START_PIC:
#         await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
#     else:
#         await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"""👋 Hey {query.from_user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ғɪʟᴇ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴛʜᴜᴍʙɴᴀɪʟ & ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ sᴜᴘᴘᴏʀᴛ! 🍟""",
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
                ],[
                InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs ', url='https://t.me/LazyDeveloper'),
                InlineKeyboardButton('🍂 sᴜᴘᴘᴏʀᴛ ', url='https://t.me/LazyDeveloper')
                ],[
                InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ ', callback_data='about'),
                InlineKeyboardButton('ℹ ʜᴇʟᴘ ', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=mr.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=mr.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=mr.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()
