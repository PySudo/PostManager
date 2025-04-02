from sqlite3 import connect
from aiosqlite import connect as connect2
from json import loads, dumps

class ManageDB:
    def __init__(self, db_name):
        self.db_name = db_name
        with connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, s TEXT, m INTEGER, notif TEXT)')
            cursor.execute('CREATE TABLE IF NOT EXISTS channels(id INTEGER, posts TEXT, notif TEXT, admin TEXT)')

    async def exec(self, query, p=None, fetch_one=False, fetch_all=False):
        async with connect2(self.db_name) as db:
            cursor  = await db.execute(query, p)
            if fetch_one:
                return await cursor.fetchone()
            if fetch_all:
                return await cursor.fetchall()
            await db.commit()

    async def addUser(self, user):
        return await self.exec("INSERT INTO users(id, notif) VALUES (?, '[]')", (user,))

    async def addChannel(self, username, admin):
        await self.exec('INSERT INTO channels VALUES (?, \'{}\', \'[]\', ?)', (username, admin,))

    async def deleteChannel(self, username):
        await self.exec('DELETE FROM channels WHERE id = ?', (username,))

    async def getAdmin(self, username):
        return (await self.exec('SELECT admin FROM channels WHERE id = ?', (username,), True))[0]

    async def getPosts(self, username):
        json = (await self.exec('SELECT posts FROM channels WHERE id = ?', (username,), True))
        print('jsonnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',json,username)
        return loads(json[0])

    async def addPost(self, channel, message_id, title):
        posts = await self.getPosts(channel)
        posts[title] = message_id
        await self.exec('UPDATE channels SET posts = ? WHERE id = ?', (dumps(posts), channel,))

    async def getChannels(self):
        return await self.exec('SELECT id FROM channels', fetch_all=True)

    async def getUserInfo(self, user):
        return (await self.exec('SELECT * FROM users WHERE id = ? LIMIT 1', (user,), True))

    async def setStep(self, user, newStep):
        await self.exec('UPDATE users SET s = ? WHERE id = ?', (newStep, user,))

    async def getMessage(self, user):
        return (await self.exec('SELECT m FROM users WHERE id = ?', (user,), True))

    async def setMessage(self, user, Message):
        await self.exec('UPDATE users SET m = ? WHERE id = ?', (Message, user,))
    
    async def getUserNotif(self, user):
        return await self.exec('SELECT notif FROM users WHERE id = ?', (user,), True)

    async def getChannelNotif(self, channel):
        return await self.exec('SELECT notif FROM channels WHERE id = ?', (channel,), True)

    async def setNotif(self, user, channel):
        user_json = loads(await self.getUserNotif(user))
        channel_json = loads(await self.getChannelNotif(channel))
        user_json.append(channel)
        channel_json.append(user)
        await self.exec('UPDATE users SET notif = ? WHERE id = ?', (dumps(user_json), user,))
        await self.exec('UPDATE channels SET notif = ? WHERE id = ?', (dumps(channel_json), channel,))
    
    async def delNotif(self, user, channel):
        user_json = loads(await self.getUserNotif(user))
        channel_json = loads(await self.getChannelNotif(channel))
        user_json.remove(channel)
        channel_json.remove(user)
        await self.exec('UPDATE users SET notif = ? WHERE id = ?', (dumps(user_json), user,))
        await self.exec('UPDATE channels SET notif = ? WHERE id = ?', (dumps(channel_json), channel,))