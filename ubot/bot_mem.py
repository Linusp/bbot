# -*- coding: utf-8 -*-
import jieba
import pymongo

from tools import text_clean, eng_clean, chi_clean, is_english, is_chinese

HOST = 'localhost'
PORT = 27017

class BotMemory(object):
    def __init__(self, host, port):
        """连接 mongodb"""
        self.db = pymongo.MongoClient(host=host, port=port).bot.memory


    def update(self, key, value, tags):
        """新增或更新记录"""
        if self.db.find_one({"key": key}) not in (None, {}):
            self.db.update({"key": key}, {"$set": {"val": value, "tag": tags}})
        else:
            self.db.insert({"key": key, "val": value, "tag": tags})


    def recall(self, query):
        """搜索"""
        query = text_clean(query)
        refs = []
        if is_english(query):
            query = eng_clean(query)
            word_list = query.split()
        elif is_chinese(query):
            query = chi_clean(query)
            word_list = jieba.cut_for_search(query)
        else:
            word_list = []

        for word in word_list:
            refs = self.associate(word)
            if refs not in ([], None):
                break

        if refs == []:
            return 'Not found.'
        else:
            val = ''
            tag_str = ''
            for row in refs:
                res = self.db.find_one({"key": row[0]})
                if res is not None:
                    val = res.get('val', 'Not found.')
                    tags = res.get('tag', [])
                    tag_str = ','.join(tags) + '\n' if tags != [] else ''
                    break

            return tag_str + val


    def associate(self, key):
        """联想"""
        result = []
        for row in self.db.find({"key": {"$regex": ".*" + key + ".*"}}, {"key": 1, "tag": 1, "_id": 0}):
            result.append((row.get("key"), ','.join(row.get("tag", []))))

        for row in self.db.find({"tag": {"$all": [key]}}, {"key": 1, "tag": 1, "_id": 0}):
            result.append((row.get("key"), ','.join(row.get("tag", []))))

        for row in self.db.find({"val": {"$regex": ".*" + key + ".*"}}, {"key": 1, "tag": 1, "_id": 0}):
            result.append((row.get("key"), ','.join(row.get("tag", []))))

        return result


    def associate_all(self):
        """无界限的联想"""
        farm = self.db.find({}, {"key": 1, "tag": 1, "_id": 0})
        result = []
        for row in farm:
            result.append((row.get("key"), ','.join(row.get("tag", []))))

        return result


bot_memory = BotMemory(HOST, PORT)
