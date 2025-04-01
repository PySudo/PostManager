from .imports import (
    callback,
    callbackDecorator,
    db,
    bot,
    checkJoin,
    edit,
    menu,
    back_admin,
    channelString,
    channelsButton,
    getLink,
    createPostButton,
    panel,
    channelsButtonUser,
    submit,
    getJoinText,
    getLinkUser
)

@bot.on(callback)
@callbackDecorator
async def Query(data, user, is_admin, user_info, channels, e):
    m = user_info[2]

    if is_admin:
        data_admin = data.split('_')
        match data_admin[0]:
            case 'backA':
                await db.setStep(user, str())
                await e.edit('👇🏼 برگشتیم ، از دکمه های زیر استفاده کن :', buttons=panel)
            case 'addchannel':
                await edit(user, m, '⚙️ یوزرنیم چنلی که میخوای اضافه کنی رو همراه با آیدی ادمین ارسال کن :\nمثال : @FuckingDaily @Py_Sudo', back_admin)
                await db.setStep(user, data)
            case 'removechannel':
                if channels:
                    ch = channelString(channels)
                    await edit(user, m, '👇🏼 آیدی کانالی که میخوای حذف کنی رو از بین کانال های زیر ارسال کن :\n'+ch, back_admin)
                    await db.setStep(user, data)
                else:
                    await e.answer('❗️ کانالی اضافه نکردی که بخوای حذفش کنی')
            case 'manageposts':
                await e.edit('👇🏼 کانال رو از لیست پایین انتخاب کن ', buttons=channelsButton(channels))
            case 'channel':
                posts = await db.getPosts(data_admin[1])
                if posts:
                    links = getLink(data_admin[1], posts)
                    await e.edit(f'⚙️ برای تنظیمات هر پست روش کلیک کن :', buttons=createPostButton(links, 1, data_admin[1]))
                else:
                    await e.answer('❗️ هنوز پستی اضافه نکردی')
            case 'page':
                page = int(data_admin[1])
                channel = data_admin[2]
                posts = await db.getPosts(channel)
                links = getLink(channel, posts)
                await e.edit(buttons=createPostButton(links, page, channel))

            case 'yes':
                sub = (await e.get_message()).message.splitlines()[-1].split(':')[1].strip()
                channel = data_admin[1]
                msid = data_admin[2]
                await db.addPost(channel, msid, sub)
                await e.answer('✅ پست اضافه شد')
                await e.delete()
            case 'no':
                await e.answer('❌ پست اضافه نشد')
                await e.delete()

    data_user = data.split('_')
    match data_user[0]:
        case 'submit':
            ch = checkJoin(user, data_user[1])
            if ch:
                await e.answer('❌ هنوز جوین نشدی')
            else:
                await e.edit('👇🏼 از دکمه های زیر استفاده کن', buttons=menu)
        
        case 'back':
            await db.setStep(user, str())
            await e.edit('برگشتیم ، از دکمه های زیر استفاده کن 👇🏼', buttons=menu)
        
        case 'getpost':
            await e.edit('👇🏼 کانالی که میخوای پست ازش بخونی رو از لیست پایین انتخاب کن', buttons=channelsButtonUser(channels))

        case 'uchannel':
            posts = await db.getPosts(data_user[1])
            if posts:
                links = getLinkUser(data_user[1], posts)
                await e.edit('👇🏼 از دکمه های پایین برای دریافت پست ها استفاده کن', buttons=createPostButton(links, 1, data_user[1], False))
            else:
                await e.answer('❗️ هنوز پستی وجود نداره')

        case 'upage':
            page = int(data_user[1])
            channel = data_user[2]
            posts = await db.getPosts(channel)
            links = getLinkUser(channel, posts)
            await e.edit(buttons=createPostButton(links, page, channel, False))

        case 'sendpost' | 'myposts' | 'notifaction':
            await e.answer('❗️ به زودی فعال میشن')