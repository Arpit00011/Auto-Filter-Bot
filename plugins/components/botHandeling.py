from pyrogram import Client, filters , enums
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from info import ADMINS, START_IMG, URL
import re
from database.users_chats_db import db
@Client.on_message(filters.command("post_mode") & filters.user(ADMINS))
async def update_post_mode(client, message):
    try:
        post_mode = await db.update_post_mode_handle()
        btn = [[
        InlineKeyboardButton("ᴘᴏsᴛ ᴍᴏᴅᴇ ➜", callback_data="update_post_mode"),
        InlineKeyboardButton(f"{'sɪɴɢʟᴇ' if post_mode.get('singel_post_mode', True) else 'ᴍᴜʟᴛɪ'} ᴍᴏᴅᴇ", callback_data="change_update_post_mode"),
    ],
    [
        InlineKeyboardButton("ᴜᴘʟᴏᴀᴅ ᴍᴏᴅᴇ ➜", callback_data="update_post_mode"),
        InlineKeyboardButton(f"{'ᴀʟʟ' if post_mode.get('all_files_post_mode', True) else 'ɴᴇᴡ'} ғɪʟᴇs", callback_data="all_files_post_mode"),
    ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await message.reply_photo(caption="<b>sᴇʟᴇᴄᴛ ᴘᴏsᴛ ᴍᴏᴅᴇ ғʀᴏᴍ ʙᴇʟᴏᴡ :</b>", photo=START_IMG, reply_markup=reply_markup)
    except Exception as e:
        print('Err in update_post_mode', e)

@Client.on_message(filters.command("set_muc") & filters.user(ADMINS))
async def set_muc_id(client, message):
    try:
        id = message.command[1]
        if id:
            is_suc = await db.movies_update_channel_id(int(id))
            if is_suc:
                await message.reply("Successfully set movies update  channel id : " + id)
            else:
                await message.reply("Failed to set movies update channel id : " + id)
        else:
            await message.reply("Invalid channel id : " + id)
    except Exception as e:
        print('Err in set_muc_id', e)
        await message.reply("Failed to set movies channel id!")

@Client.on_message(filters.command("del_muc") & filters.user(ADMINS))
async def del_muc_id(client, message):
    try:
        is_suc = await db.del_movies_channel_id()
        if is_suc:
            await message.reply("Successfully deleted movies channel id")
        else:
            await message.reply("Failed to delete movies channel id")
    except Exception as e:
        print('Err in del_muc_id', e)
        await message.reply("Failed to delete movies channel id!")

@Client.on_message(filters.command("url"))
async def give_url(bot, message):
    if URL != None:
        bot_url = URL
        await message.reply(f'Here is your Bot\'s URL {bot_url}')
    else:
        await message.reply(f'Bro you have not provided the URL in enviroment')

@Client.on_message(filters.command("vjcmds"))
async def give_vjcmds(bot, message):
    await message.reply('''VJ ki repo ke saare cmds yeh rahe\n
                            /index - 𝑖𝑛𝑑𝑒𝑥 𝑓𝑖𝑙𝑒 𝑓𝑟𝑜𝑚 𝑦𝑜𝑢𝑟 𝑐ℎ𝑎𝑛𝑛𝑒𝑙
                            /logs - 𝑡𝑜 𝑔𝑒𝑡 𝑡ℎ𝑒 𝑟𝑒𝑐𝑒𝑛𝑡 𝑒𝑟𝑟𝑜𝑟𝑠
                            /stats - 𝑡𝑜 𝑔𝑒𝑡 𝑠𝑡𝑎𝑡𝑢𝑠 𝑜𝑓 𝑓𝑖𝑙𝑒𝑠 𝑖𝑛 𝑑𝑏.
                            /connections - 𝑇𝑜 𝑠𝑒𝑒 𝑎𝑙𝑙 𝑐𝑜𝑛𝑛𝑒𝑐𝑡𝑒𝑑 𝑔𝑟𝑜𝑢𝑝𝑠
                            /settings - 𝑇𝑜 𝑜𝑝𝑒𝑛 𝑠𝑒𝑡𝑡𝑖𝑛𝑔𝑠 𝑚𝑒𝑛𝑢
                            /filter - 𝑎𝑑𝑑 𝑚𝑎𝑛𝑢𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠
                            /filters - 𝑣𝑖𝑒𝑤 𝑓𝑖𝑙𝑡𝑒𝑟𝑠
                            /connect - 𝑐𝑜𝑛𝑛𝑒𝑐𝑡 𝑡𝑜 𝑃𝑀.
                            /disconnect - 𝑑𝑖𝑠𝑐𝑜𝑛𝑛𝑒𝑐𝑡 𝑓𝑟𝑜𝑚 𝑃𝑀
                            /del - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎 𝑓𝑖𝑙𝑡𝑒𝑟
                            /delall - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎𝑙𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠
                            /deleteall - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎𝑙𝑙 𝑖𝑛𝑑𝑒𝑥𝑒𝑑 𝑓𝑖𝑙𝑒𝑠.
                            /delete - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎 𝑠𝑝𝑒𝑐𝑖𝑓𝑖𝑐 𝑓𝑖𝑙𝑒 𝑓𝑟𝑜𝑚 𝑖𝑛𝑑𝑒𝑥.
                            /info - 𝑔𝑒𝑡 𝑢𝑠𝑒𝑟 𝑖𝑛𝑓𝑜
                            /id - 𝑔𝑒𝑡 𝑡𝑔 𝑖𝑑𝑠.
                            /imdb - 𝑓𝑒𝑡𝑐ℎ 𝑖𝑛𝑓𝑜 𝑓𝑟𝑜𝑚 𝑖𝑚𝑑𝑏.
                            /search - 𝑇𝑜 𝑠𝑒𝑎𝑟𝑐ℎ 𝑓𝑟𝑜𝑚 𝑣𝑎𝑟𝑖𝑜𝑢𝑠 𝑠𝑜𝑢𝑟𝑐𝑒𝑠
                            /start - 𝑇𝑜 𝑠𝑡𝑎𝑟𝑡 𝑡ℎ𝑒 𝑏𝑜𝑡
                            /setskip - 𝑇𝑜 𝑠𝑘𝑖𝑝 𝑛𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑚𝑒𝑠𝑠𝑎𝑔𝑒𝑠 𝑤ℎ𝑒𝑛 𝑖𝑛𝑑𝑒𝑥𝑖𝑛𝑔 𝑓𝑖𝑙𝑒𝑠
                            /users - 𝑡𝑜 𝑔𝑒𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑚𝑦 𝑢𝑠𝑒𝑟𝑠 𝑎𝑛𝑑 𝑖𝑑𝑠.
                            /chats - 𝑡𝑜 𝑔𝑒𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑡ℎ𝑒 𝑚𝑦 𝑐ℎ𝑎𝑡𝑠 𝑎𝑛𝑑 𝑖𝑑𝑠 
                            /leave  - 𝑡𝑜 𝑙𝑒𝑎𝑣𝑒 𝑓𝑟𝑜𝑚 𝑎 𝑐ℎ𝑎𝑡.
                            /disable  -  𝑑𝑜 𝑑𝑖𝑠𝑎𝑏𝑙𝑒 𝑎 𝑐ℎ𝑎𝑡.
                            /enable - 𝑟𝑒-𝑒𝑛𝑎𝑏𝑙𝑒 𝑐ℎ𝑎𝑡.
                            /ban  - 𝑡𝑜 𝑏𝑎𝑛 𝑎 𝑢𝑠𝑒𝑟.
                            /unban  - 𝑡𝑜 𝑢𝑛𝑏𝑎𝑛 𝑎 𝑢𝑠𝑒𝑟.
                            /channel - 𝑡𝑜 𝑔𝑒𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑡𝑜𝑡𝑎𝑙 𝑐𝑜𝑛𝑛𝑒𝑐𝑡𝑒𝑑 𝑐ℎ𝑎𝑛𝑛𝑒𝑙𝑠
                            /broadcast - 𝑡𝑜 𝑏𝑟𝑜𝑎𝑑𝑐𝑎𝑠𝑡 𝑎 𝑚𝑒𝑠𝑠𝑎𝑔𝑒 𝑡𝑜 𝑎𝑙𝑙 𝑢𝑠𝑒𝑟𝑠
                            /grp_broadcast - 𝑇𝑜 𝑏𝑟𝑜𝑎𝑑𝑐𝑎𝑠𝑡 𝑎 𝑚𝑒𝑠𝑠𝑎𝑔𝑒 𝑡𝑜 𝑎𝑙𝑙 𝑐𝑜𝑛𝑛𝑒𝑐𝑡𝑒𝑑 𝑔𝑟𝑜𝑢𝑝𝑠.
                            /batch - 𝑡𝑜 𝑐𝑟𝑒𝑎𝑡𝑒 𝑙𝑖𝑛𝑘 𝑓𝑜𝑟 𝑚𝑢𝑙𝑡𝑖𝑝𝑙𝑒 𝑝𝑜𝑠𝑡𝑠
                            /link - 𝑡𝑜 𝑐𝑟𝑒𝑎𝑡𝑒 𝑙𝑖𝑛𝑘 𝑓𝑜𝑟 𝑜𝑛𝑒 𝑝𝑜𝑠𝑡
                            /status - 𝑌𝑜𝑢𝑟 𝐻𝑒𝑟𝑜𝑘𝑢 𝐴𝑃𝐼 𝐾𝑒𝑦 𝑡𝑜 𝑐ℎ𝑒𝑐𝑘 𝑑𝑦𝑛𝑜, 𝑏𝑜𝑡 𝑢𝑝𝑡𝑖𝑚𝑒 𝑎𝑛𝑑 𝑏𝑜𝑡 𝑤𝑜𝑟𝑘𝑖𝑛𝑔 𝑑𝑎𝑦 𝑝𝑟𝑒𝑑𝑖𝑐𝑡𝑖𝑜𝑛.
                            /set_template - 𝑇𝑜 𝑠𝑒𝑡 𝑎 𝑐𝑢𝑠𝑡𝑜𝑚 𝐼𝑀𝐷𝑏 𝑡𝑒𝑚𝑝𝑙𝑎𝑡𝑒 𝑓𝑜𝑟 𝑖𝑛𝑑𝑖𝑣𝑖𝑑𝑢𝑎𝑙 𝑔𝑟𝑜𝑢𝑝𝑠
                            /gfilter - 𝑇𝑜 𝑎𝑑𝑑 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠.
                            /gfilters - 𝑇𝑜 𝑣𝑖𝑒𝑤 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑎𝑙𝑙 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠.
                            /delg - 𝑇𝑜 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎 𝑠𝑝𝑒𝑐𝑖𝑓𝑖𝑐 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟.
                            /delallg - 𝑇𝑜 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎𝑙𝑙 𝑔𝑙𝑜𝑏𝑎𝑙 𝑓𝑖𝑙𝑡𝑒𝑟𝑠 𝑓𝑟𝑜𝑚 𝑡ℎ𝑒 𝑏𝑜𝑡'𝑠 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒.
                            /deletefiles - 𝑇𝑜 𝑑𝑒𝑙𝑒𝑡𝑒 𝑃𝑟𝑒𝐷𝑉𝐷 𝑎𝑛𝑑 𝐶𝑎𝑚𝑅𝑖𝑝 𝐹𝑖𝑙𝑒𝑠 𝑓𝑟𝑜𝑚 𝑡ℎ𝑒 𝑏𝑜𝑡'𝑠 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒.
                            /add_premium - 𝐴𝑑𝑑 𝑢𝑠𝑒𝑟 𝑡𝑜 𝑝𝑟𝑒𝑚𝑖𝑢𝑚 𝑙𝑖𝑠𝑡
                            /remove_premium - 𝑅𝑒𝑚𝑜𝑣𝑒 𝑢𝑠𝑒𝑟 𝑓𝑟𝑜𝑚 𝑝𝑟𝑒𝑚𝑖𝑢𝑚 𝑙𝑖𝑠𝑡
                            /plan - 𝐶ℎ𝑒𝑐𝑘 𝑝𝑙𝑎𝑛 𝑑𝑒𝑡𝑎𝑖𝑙𝑠
                            /myplan - 𝐶ℎ𝑒𝑐𝑘 𝑦𝑜𝑢𝑟 𝑝𝑙𝑎𝑛 𝑠𝑡𝑎𝑡𝑠
                            /shortlink - 𝑠𝑒𝑡 𝑦𝑜𝑢𝑟 𝑢𝑟𝑙 𝑠ℎ𝑜𝑟𝑡𝑛𝑒𝑟 𝑖𝑛 𝑦𝑜𝑢𝑟 𝑔𝑟𝑜𝑢𝑝
                            /setshortlinkoff  - 𝑜𝑓𝑓 𝑠ℎ𝑜𝑟𝑡𝑙𝑖𝑛𝑘 𝑖𝑛 𝑦𝑜𝑢𝑟 𝑔𝑟𝑜𝑢𝑝
                            /setshortlinkon - 𝑜𝑛 𝑠ℎ𝑜𝑟𝑡𝑙𝑖𝑛𝑘 𝑖𝑛 𝑦𝑜𝑢𝑟 𝑔𝑟𝑜𝑢𝑝
                            /shortlink_info - 𝑐ℎ𝑒𝑐𝑘 𝑦𝑜𝑢𝑟 𝑔𝑟𝑜𝑢𝑝 𝑎𝑙𝑙 𝑠ℎ𝑜𝑟𝑡𝑙𝑖𝑛𝑘 𝑎𝑛𝑑 𝑡𝑢𝑡𝑜𝑟𝑖𝑎𝑙 𝑙𝑖𝑛𝑘 𝑑𝑒𝑡𝑎𝑖𝑙𝑠
                            /set_tutorial - 𝑠𝑒𝑡 𝑦𝑜𝑢𝑟 𝑢𝑟𝑙 𝑠ℎ𝑜𝑟𝑡𝑛𝑒𝑟 ℎ𝑜𝑤 𝑡𝑜 𝑜𝑝𝑒𝑛 𝑙𝑖𝑛𝑘 𝑢𝑟𝑙
                            /remove_tutorial - 𝑟𝑒𝑚𝑜𝑣𝑒 𝑦𝑜𝑢𝑟 𝑡𝑢𝑡𝑜𝑟𝑖𝑎𝑙 𝑢𝑟𝑙
                            /restart  - 𝑟𝑒𝑠𝑡𝑎𝑟𝑡 𝑡ℎ𝑒 𝑏𝑜𝑡 𝑠𝑒𝑟𝑣𝑒𝑟
                            /fsub - 𝑎𝑑𝑑 𝑓𝑜𝑟𝑐𝑒 𝑠𝑢𝑏𝑠𝑐𝑟𝑖𝑏𝑒 𝑐ℎ𝑎𝑛𝑛𝑒𝑙 𝑖𝑛 𝑔𝑟𝑜𝑢𝑝
                            /nofsub - 𝑟𝑒𝑚𝑜𝑣𝑒 𝑜𝑟 𝑜𝑓𝑓 𝑓𝑜𝑟𝑐𝑒 𝑠𝑢𝑏𝑠𝑐𝑟𝑖𝑏𝑒 𝑖𝑛 𝑦𝑜𝑢𝑟 𝑔𝑟𝑜𝑢𝑝
                            /set_caption - 𝑎𝑑𝑑 𝑐𝑎𝑝𝑡𝑖𝑜𝑛 𝑓𝑜𝑟 𝑦𝑜𝑢𝑟 𝑟𝑒𝑛𝑎𝑚𝑒𝑑 𝑓𝑖𝑙𝑒
                            /see_caption - 𝑠𝑒𝑒 𝑦𝑜𝑢𝑟 𝑠𝑎𝑣𝑒𝑑 𝑐𝑎𝑝𝑡𝑖𝑜𝑛
                            /del_caption - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑦𝑜𝑢𝑟 𝑠𝑎𝑣𝑒𝑑 𝑐𝑎𝑝𝑡𝑖𝑜𝑛
                            /set_thumb - 𝑎𝑑𝑑 𝑡ℎ𝑢𝑚𝑏𝑛𝑎𝑖𝑙 𝑓𝑜𝑟 𝑦𝑜𝑢𝑟 𝑟𝑒𝑛𝑎𝑚𝑒𝑑 𝑓𝑖𝑙𝑒
                            /view_thumb - 𝑣𝑖𝑒𝑤 𝑦𝑜𝑢𝑟 𝑠𝑎𝑣𝑒𝑑 𝑡ℎ𝑢𝑚𝑏𝑛𝑎𝑖𝑙
                            /del_thumb - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑦𝑜𝑢𝑟 𝑠𝑎𝑣𝑒𝑑 𝑡ℎ𝑢𝑚𝑏𝑛𝑎𝑖𝑙
                            /stream - 𝑔𝑒𝑛𝑒𝑟𝑎𝑡𝑒 𝑠𝑡𝑟𝑒𝑎𝑚 𝑎𝑛𝑑 𝑑𝑜𝑤𝑛𝑙𝑜𝑎𝑑 𝑙𝑖𝑛𝑘 𝑜𝑓 𝑦𝑜𝑢𝑟 𝑓𝑖𝑙𝑒
                            /stickerid - 𝑡𝑜 𝑔𝑒𝑡 𝑖𝑑 𝑎𝑛𝑑 𝑢𝑛𝑖𝑞𝑢𝑒 𝐼'𝑑 𝑜𝑓 𝑠𝑡𝑖𝑐𝑘𝑒𝑟
                            /font - 𝑡𝑜 𝑔𝑒𝑡 𝑎𝑛𝑦 𝑡𝑦𝑝𝑒 𝑜𝑓 𝑓𝑜𝑛𝑡 𝑜𝑓 𝑎𝑛𝑦 𝑤𝑜𝑟𝑑
                            /purgerequests - 𝑑𝑒𝑙𝑒𝑡𝑒 𝑎𝑙𝑙 𝑗𝑜𝑖𝑛 𝑟𝑒𝑞𝑢𝑒𝑠𝑡𝑠 𝑓𝑟𝑜𝑚 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒
                            /totalrequests - 𝑔𝑒𝑡 𝑡𝑜𝑡𝑎𝑙 𝑛𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑗𝑜𝑖𝑛 𝑟𝑒𝑞𝑢𝑒𝑠𝑡 𝑓𝑟𝑜𝑚 𝑑𝑎𝑡𝑎𝑏𝑎𝑠𝑒''')

