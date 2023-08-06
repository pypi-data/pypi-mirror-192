from .base_model import BaseModel
from ..helpers import RedisCacheConfig
from ..helpers.redis_helper import RedisClient


class AddressMappingStructure:
    ID = "_id"
    MERCHANT_ID = "merchant_id"
    ADDRESS_ID = "address_id"
    MAPPING_VALUE = "mapping_value"
    RANK = "rank"
    TYPE = "type"


class AddressMappingModel(BaseModel):
    MERCHANT_DEFAULT = "SYSTEM_CONFIG"

    def __init__(self):
        super().__init__()
        self.collection = "address_mapping"

    def find_mapping(self, merchant_id, mapping_value, location_type):
        # cache redis
        key_cache = RedisCacheConfig.MERCHANT_ADDRESS_MAPPING_KEY.format(
            merchant_id=merchant_id, mapping_value=mapping_value, location_type=location_type
        )
        value_cache = RedisClient().get(key=key_cache)
        if value_cache:
            return value_cache
        data = self.find_one(query={
            AddressMappingStructure.MERCHANT_ID: {
                "$in": [merchant_id, self.MERCHANT_DEFAULT]
            },
            AddressMappingStructure.MAPPING_VALUE: mapping_value,
            AddressMappingStructure.TYPE: location_type
        }, sort=[(AddressMappingStructure.ID, -1)])
        if data:
            data = RedisClient().set(key=key_cache, value=data)
        return data
