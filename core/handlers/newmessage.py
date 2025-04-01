from .imports import (
    bot, 
    message, 
    messageDecorator, 
    db, 
    checkJoin, 
    getJoinText,
    submit,
    menu,
    edit,
    panel,
    channelString,
    back_admin,
    cfg,
    yes_no
)

@bot.on(message(incoming=True))
@messageDecorator
async def MessageHandler(text, user, message_id, is_admin, user_info, channels, e):
    if e.is_private:
        if not user_info:
            await db.addUser(user)

        if text.startswith('/start'):
            data = text.split()
            if len(data) == 1:
                mess = await e.reply('👇🏼 از دکمه های زیر استفاده کن', buttons=menu)
                await db.setMessage(user, mess.id)
                await db.setStep(user, str())
            else:
                try:
                    chat, message = data[1].split('_')
                    if '@'+chat in channels and message in (await db.getPosts('@'+chat)).values():
                        ch = checkJoin(user, '@'+chat)
                        if ch:
                            mess = await e.reply(getJoinText(ch), buttons=submit('@'+chat))
                            await db.setMessage(user, mess.id)
                            return
                        await bot.forward_messages(user, int(message), chat)
                except:
                    pass
        else:
            await e.delete()

        if is_admin and user_info:
            if text.lower() in ('panel', '/panel', 'پنل'):
                await edit(user, user_info[2], '📍 سلام ادمین ، با استفاده از پنل زیر میتونی ربات رو کنترل کنی :', panel)
            elif user_info[1] == 'addchannel':
                ch, ad = text.split()
                if ch not in channels:
                    await db.addChannel(ch.lower(), ad)
                    await db.setStep(user, str())
                    await edit(user, user_info[2], f'✅ کانال {ch} با موفقیت اضافه شد.', panel)
                else:
                    await edit(user, user_info[2], '❗️ این کانال از قبل وجود داشت', back_admin)
            elif user_info[1] == 'removechannel':
                if text not in channels:
                    chs = channelString(channels)
                    await edit(user, user_info[2], '❗️ کانال رو از لیست پایین انتخاب کن :\n'+chs, back_admin)
                else:
                    await db.deleteChannel(text)
                    await edit(user, user_info[2], f'✅ کانال {text} با موفقیت حذف شد', panel)
                    await db.setStep(user, str())
    else:
        username = ('@'+str(e.sender.username)).lower()
        sub = '<b>'+text.splitlines()[0]+'</b>'
        if username in channels:
            admin = await db.getAdmin(username)
            await bot.send_message(admin, f'‼️ <a href="https://t.me/{username[1:]}/{message_id}">پیام جدیدی</a>  از کانال {username} تشخیص داده شد\n👇🏼 برای اضافه کردنش به پست ها از دکمه های زیر استفاده کن.\nعنوان : {sub}', buttons=yes_no(username, message_id), link_preview=False)