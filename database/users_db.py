import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.bannedList = self.db.bannedList

    # User creation template
    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            is_active=True  # Default active status
        )

    # Add a new user to the database
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    # Check if user exists
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    # Get total number of users
    async def total_users_count(self):
        return await self.col.count_documents({})

    # Get total number of active users
    async def active_users_count(self):
        return await self.col.count_documents({"is_active": True})

    # Get total number of banned users
    async def banned_users_count(self):
        return await self.bannedList.count_documents({})

    # Get all users
    async def get_all_users(self):
        return self.col.find({})

    # Delete a user by ID
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    # Ban a user
    async def ban_user(self, user_id):
        user = await self.bannedList.find_one({'banId': int(user_id)})
        if user:
            return False
        await self.bannedList.insert_one({'banId': int(user_id)})
        await self.col.update_one({'id': int(user_id)}, {"$set": {"is_active": False}})
        return True

    # Unban a user
    async def is_unbanned(self, user_id):
        try:
            if await self.bannedList.find_one({'banId': int(user_id)}):
                await self.bannedList.delete_one({'banId': int(user_id)})
                await self.col.update_one({'id': int(user_id)}, {"$set": {"is_active": True}})
                return True
            return False
        except Exception as e:
            error_msg = f'Failed to unban. Reason: {e}'
            print(error_msg)
            return error_msg

    # Check if user is banned
    async def is_banned(self, user_id):
        user = await self.bannedList.find_one({'banId': int(user_id)})
        return True if user else False

    # Get detailed info of banned users
    async def get_banned_user_details(self):
        banned_users = await self.bannedList.find().to_list(length=None)
        details = []

        for user in banned_users:
            user_data = await self.col.find_one({"id": user["banId"]})
            if user_data:
                details.append((user_data["id"], user_data.get("name", "Unknown")))
            else:
                details.append((user["banId"], "Unknown"))

        return details


# Initialize Database instance
db = Database(DATABASE_URI, DATABASE_NAME)
