import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Db:
    def __init__(self, uri: str, database_name: str):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.bot = self.db.bots
        self.userbot = self.db.userbot 
        self.col = self.db.users
        self.nfy = self.db.notify
        self.chl = self.db.channels

    # ----------------- User Management -----------------
    def new_user(self, id: int, name: str) -> dict:
        """Create a new user document."""
        return dict(
            id=id,
            name=name,
            ban_status=dict(
                is_banned=False,
                ban_reason=""
            ),
            log_enabled=True
        )

    async def add_user(self, id: int, name: str) -> None:
        """Add a new user to database."""
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id: int) -> bool:
        """Check if a user exists."""
        user = await self.col.find_one({'id': id})
        return bool(user)

    async def total_users_count(self) -> int:
        """Get total number of users."""
        return await self.col.count_documents({})

    async def delete_user(self, user_id: int) -> None:
        """Delete a user."""
        await self.col.delete_many({'id': user_id})

    async def get_all_users(self):
        """Fetch all users."""
        return self.col.find({})

    # ----------------- Ban Management -----------------
    async def ban_user(self, user_id: int, ban_reason: str = "No Reason") -> None:
        """Ban a user with optional reason."""
        ban_status = dict(is_banned=True, ban_reason=ban_reason)
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def remove_ban(self, id: int) -> None:
        """Remove ban from a user."""
        ban_status = dict(is_banned=False, ban_reason="")
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id: int) -> dict:
        """Get ban status of a user."""
        default = dict(is_banned=False, ban_reason="")
        user = await self.col.find_one({'id': id})
        return user.get('ban_status', default) if user else default

    async def get_banned(self) -> list:
        """Get all banned users."""
        users = self.col.find({'ban_status.is_banned': True})
        return [user['id'] async for user in users]

    # ----------------- Config Management -----------------
    async def update_configs(self, id: int, configs: dict) -> None:
        """Update user configs."""
        await self.col.update_one({'id': id}, {'$set': {'configs': configs}})

    async def get_configs(self, id: int) -> dict:
        """Get user configs."""
        default = {
            'caption': None,
            'duplicate': True,
            'forward_tag': False,
            'min_size': 0,
            'max_size': 0,
            'extension': None,
            'keywords': None,
            'protect': None,
            'button': None,
            'db_uri': None,
            'filters': {
                'poll': True,
                'text': True,
                'audio': True,
                'voice': True,
                'video': True,
                'photo': True,
                'document': True,
                'animation': True,
                'sticker': True
            }
        }
        user = await self.col.find_one({'id': id})
        return user.get('configs', default) if user else default

    async def get_filters(self, user_id: int) -> list:
        """Get disabled filters for a user."""
        filters_ = []
        user_filters = (await self.get_configs(user_id))['filters']
        for k, v in user_filters.items():
            if v is False:
                filters_.append(str(k))
        return filters_

    # ----------------- Link Removal Management -----------------
    async def is_link_removal_enabled(self, chat_id: int) -> bool:
        """Check if link removal is enabled for a chat."""
        doc = await self.col.find_one({"id": chat_id})
        return doc.get("remove_links", False) if doc else False

    async def toggle_link_removal(self, chat_id: int, enable: bool) -> None:
        """Enable or disable link removal for a chat."""
        await self.col.update_one(
            {"id": chat_id},
            {"$set": {"remove_links": enable}},
            upsert=True
        )

    # ----------------- Bot Management -----------------
    async def add_bot(self, datas: dict) -> None:
        """Add a new bot."""
        if not await self.is_bot_exist(datas['user_id']):
            await self.bot.insert_one(datas)

    async def remove_bot(self, user_id: int) -> None:
        """Remove a bot."""
        await self.bot.delete_many({'user_id': user_id})

    async def get_bot(self, user_id: int) -> dict | None:
        """Get a bot details."""
        return await self.bot.find_one({'user_id': user_id})

    async def is_bot_exist(self, user_id: int) -> bool:
        """Check if a bot exists."""
        bot = await self.bot.find_one({'user_id': user_id})
        return bool(bot)

    async def total_users_bots_count(self) -> tuple:
        """Get total count of users and bots."""
        users = await self.col.count_documents({})
        bots = await self.bot.count_documents({})
        return users, bots

    # ----------------- Userbot Management -----------------
    async def add_userbot(self, datas: dict) -> None:
        """Add a userbot."""
        if not await self.is_userbot_exist(datas['user_id']):
            await self.userbot.insert_one(datas)

    async def remove_userbot(self, user_id: int) -> None:
        """Remove a userbot."""
        await self.userbot.delete_many({'user_id': user_id})

    async def get_userbot(self, user_id: int) -> dict | None:
        """Get a userbot."""
        return await self.userbot.find_one({'user_id': user_id})

    async def is_userbot_exist(self, user_id: int) -> bool:
        """Check if a userbot exists."""
        bot = await self.userbot.find_one({'user_id': user_id})
        return bool(bot)

    # ----------------- Channel Management -----------------
    async def in_channel(self, user_id: int, chat_id: int) -> bool:
        """Check if a channel exists."""
        channel = await self.chl.find_one({"user_id": user_id, "chat_id": chat_id})
        return bool(channel)

    async def add_channel(self, user_id: int, chat_id: int, title: str, username: str) -> bool:
        """Add a channel."""
        if await self.in_channel(user_id, chat_id):
            return False
        await self.chl.insert_one({"user_id": user_id, "chat_id": chat_id, "title": title, "username": username})
        return True

    async def remove_channel(self, user_id: int, chat_id: int) -> bool:
        """Remove a channel."""
        if not await self.in_channel(user_id, chat_id):
            return False
        await self.chl.delete_many({"user_id": user_id, "chat_id": chat_id})
        return True

    async def get_channel_details(self, user_id: int, chat_id: int) -> dict | None:
        """Get channel details."""
        return await self.chl.find_one({"user_id": user_id, "chat_id": chat_id})

    async def get_user_channels(self, user_id: int) -> list:
        """Get all channels of a user."""
        channels = self.chl.find({"user_id": user_id})
        return [channel async for channel in channels]

    # ----------------- Notify (Forward) Management -----------------
    async def add_frwd(self, user_id: int) -> None:
        """Add a user for forwarding notifications."""
        await self.nfy.insert_one({'user_id': user_id})

    async def rmve_frwd(self, user_id: int = 0, all: bool = False) -> None:
        """Remove a forwarding user or all users."""
        query = {} if all else {'user_id': user_id}
        await self.nfy.delete_many(query)

    async def is_forwad_exit(self, user_id: int) -> bool:
        """Check if forwarding settings exist."""
        u = await self.nfy.find_one({'user_id': user_id})
        return bool(u)

    async def get_all_frwd(self):
        """Get all forwarding users."""
        return self.nfy.find({})

    async def forwad_count(self) -> int:
        """Get forwarding users count."""
        return await self.nfy.count_documents({})

    async def get_forward_details(self, user_id: int) -> dict:
        """Get forwarding details of a user."""
        default = {
            'chat_id': None,
            'forward_id': None,
            'toid': None,
            'last_id': None,
            'limit': None,
            'msg_id': None,
            'start_time': None,
            'fetched': 0,
            'offset': 0,
            'deleted': 0,
            'total': 0,
            'duplicate': 0,
            'skip': 0,
            'filtered': 0
        }
        user = await self.nfy.find_one({'user_id': user_id})
        return user.get('details', default) if user else default

    async def update_forward(self, user_id: int, details: dict) -> None:
        """Update forwarding details of a user."""
        await self.nfy.update_one({'user_id': user_id}, {'$set': {'details': details}})

# Create DB instance
db = Db(Config.DATABASE_URI, Config.DATABASE_NAME)
