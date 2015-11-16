#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from config.config import CONFIG
from pymongo import MongoClient


client = MongoClient(CONFIG.MONGO.HOST, CONFIG.MONGO.PORT)


def get_collection(db_name, collection_name):
    db = getattr(client, db_name, None)
    return getattr(db, collection_name, None)
