from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemes import Asset

class AssetModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client)

        self.collection = self.db_client[ DataBaseEnum.COLLECTION_ASSET_NAME.value ]
    
    @classmethod
    async def create_instance(cls, db_client: object):

        instance = cls(db_client)
        await instance.init_collection()

        return instance

    async def init_collection(self):
        
        all_collections = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[ DataBaseEnum.COLLECTION_ASSET_NAME.value ]
            indexes = Asset.get_indexes()

            for index in indexes:        
                await self.collection.create_index(
                    keys = index["key"],
                    name = index["name"],
                    unique = index["unique"]
                )
    async def create_asset(self, project_id: str):

        self.collection.create_one