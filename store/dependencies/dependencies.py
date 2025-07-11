from store.db.mongo import db_client
from store.usecases.product import ProductUsecases


async def get_product_usecase() -> ProductUsecases:
    """
    Função de dependência que fornece uma instância de ProductUsecases.
    """
    # db_client é o seu singleton MongoClient, que já tem o cliente Motor inicializado.
    # get_client() retorna o AsyncIOMotorClient.
    return ProductUsecases(client=db_client.get())
