from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from threading import Thread

# Mandatory join button
join_check = InlineKeyboardMarkup(
    [

        [InlineKeyboardButton('عضویت در کانال', url="*************")],
    ]
)


# mandatory join
def joined_handler(_, client, message):
    try:
        user_obj = client.get_chat_member(chat_id="*************", user_id=message.from_user.id)
        return True  # who are in channel
    except Exception as e:
        message.reply_text('برای استفاده از ربات ابتدا عضو کانال شوید.پس از عضویت مجدد ربات را استارت کنید.',
                           reply_markup=join_check)
        return False  # who are not in channel


join_filter = filters.create(joined_handler)


# /start
@Client.on_message(filters.command("start") & join_filter)
async def start(client, message):
    await message.reply_text(
        "سلام به ربات شورای صنفی دانشکده پرستاری و مامایی حضرت فاطمه (س) خوش آمدید .لطفا از گزینه های زیر انتخاب کنید.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("ارتباط با ما", callback_data="contact"),
            InlineKeyboardButton("امکانات", callback_data="options")
        ]]))


# function to contact admin and head
@Client.on_callback_query(filters.regex("contact"))
async def handle_contact(client, callback_query):
    await callback_query.message.edit_text("با ما در ارتباط باشید.",
                                           reply_markup=InlineKeyboardMarkup([[
                                               InlineKeyboardButton("ارتباط با دبیر",
                                                                    url="*************")
                                           ], [InlineKeyboardButton("بازگشت", callback_data="back")]]))


# handle options button
@Client.on_callback_query(filters.regex("options"))
async def handle_options(client, callback_query):
    await callback_query.message.edit_text("برای دریافت اخبار و اعلانات گزینه Reminder را انتخاب کنید.\n"
                                           "برای آشنایی با اعضای شورای صنفی گزینه معرفی اعضا را انتخاب کنید.",

                                           reply_markup=InlineKeyboardMarkup([[
                                               InlineKeyboardButton("Reminder", callback_data="Reminder"),
                                               InlineKeyboardButton("معرفی اعضا", callback_data="members")
                                           ], [InlineKeyboardButton("بازگشت", callback_data="back")]]))


# handle members button
@Client.on_callback_query(filters.regex("members"))
async def handle_members(client, callback_query):
    await callback_query.message.reply_photo(
        "photo_2024-08-22_17-03-29.jpg",
        caption="اعضای شورای صنفی دانشکده پرستاری و مامایی حضرت فاطمه (س)")
    await callback_query.message.edit_text("برای بازگشتن به قسمت اول گزینه بازگشت را انتخاب کنید.",
                                           reply_markup=InlineKeyboardMarkup([
                                               [InlineKeyboardButton("بازگشت", callback_data="back")]]))


# handle back button
@Client.on_callback_query(filters.regex("back"))
async def handle_back(client, callback_query):
    await callback_query.message.edit_text("لطفا از گزینه های زیر انتخاب کنید.",
                                           reply_markup=InlineKeyboardMarkup([[
                                               InlineKeyboardButton("ارتباط با ما", callback_data="contact"),

                                               InlineKeyboardButton("امکانات", callback_data="options")
                                           ]]))


# permission to send message
allowed_users = set()


# function to send that news button is activated
@Client.on_callback_query(filters.regex("Reminder"))
async def allow_callback(client, callback_query):
    user_id = callback_query.from_user.id
    allowed_users.add(user_id)
    await callback_query.answer("شما اخبار و اعلانات را دریافت خواهید کرد")


# function to send admin message to users
@Client.on_message(filters.user("*************") & filters.text)
async def admin_message(client, message):
    text = message.text
    for user_id in allowed_users:
        try:
            await client.send_message(user_id, text)
        except Exception as e:
            print(f"خطا در ارسال پیام به کاربر {user_id}: {e}")
