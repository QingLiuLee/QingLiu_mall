# -*- coding: utf-8 -*-
# @Time     : 4/24/19 8:00 PM
# @Author   : Lee才晓
# @Describe :
from motor.motor_asyncio import AsyncIOMotorClient

from system.base_config import MONGODB
from utils.singleton import singleton


@singleton
class MotorBase:
    """
    更改mongodb连接方式 单例模式下支持多库操作
    About motor's doc: https://github.com/mongodb/motor
    """
    # _db = {}
    # _collection = {}

    __slots__ = {
        'motor_uri', '_db', '_collection','MONGODB'
    }

    def __init__(self):
        self.motor_uri = ''
        self._collection = {}
        self._db = {}
        self.MONGODB = MONGODB

    def client(self, db):
        # motor
        self.motor_uri = 'mongodb://{account}{host}:{port}/'.format(
            account='{username}:{password}@'.format(
                username=self.MONGODB['MONGO_USERNAME'],
                password=self.MONGODB['MONGO_PASSWORD']) if self.MONGODB['MONGO_USERNAME'] else '',
            host=self.MONGODB['MONGO_HOST'] if self.MONGODB['MONGO_HOST'] else 'localhost',
            port=self.MONGODB['MONGO_PORT'] if self.MONGODB['MONGO_PORT'] else 27017,
            )
        return AsyncIOMotorClient(self.motor_uri)

    def get_db(self, db=MONGODB['DATABASE']):
        """
        获取一个db实例
        :param db: database name
        :return: the motor db instance
        """
        if db not in self._db:
            self._db[db] = self.client(db)[db]

        return self._db[db]

    def get_collection(self, db_name, collection):
        """
        获取一个集合实例
        :param db_name: database name
        :param collection: collection name
        :return: the motor collection instance
        """
        collection_key = db_name + collection
        if collection_key not in self._collection:
            self._collection[collection_key] = self.get_db(db_name)[collection]

        return self._collection[collection_key]

    ######################################################################################
    # def connect_db(self, db=MONGODB):
    #     self.motor_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
    #         account='{username}:{password}@'.format(
    #             username=db['MONGO_USERNAME'],
    #             password=db['MONGO_PASSWORD']) if db['MONGO_USERNAME'] else '',
    #         host=db['MONGO_HOST'] if db['MONGO_HOST'] else 'localhost',
    #         port=db['MONGO_PORT'] if db['MONGO_PORT'] else 27017,
    #         database=db['DATABASE'])
    #     self._db = AsyncIOMotorClient(self.motor_uri)
    #     return self._db
    #
    # def connect_mongo(self,mongo=MONGODB):
    #     pass
    #
    # def get_collection(self, collection):
    #
    #     if collection not in self._collection:
    #         self._collection[collection] = self._db['qingliu'][collection]
    #
    #     return self._collection[collection]
    #
    # def test_get_data(self, collection):
    #     return self._collection[collection]