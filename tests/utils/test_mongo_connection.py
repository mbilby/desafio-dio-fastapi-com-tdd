# async def test_mongo():
#     # Use a URL que você usa no seu projeto, com usuário e senha corretos
#     mongo_url = "mongodb://root:mongodb@localhost:27017/store?authSource=admin"
#     client = AsyncIOMotorClient(mongo_url)
#     db = client.get_default_database()

#     collections = await db.list_collection_names()
#     print("Coleções encontradas:", collections)

#     client.close()
