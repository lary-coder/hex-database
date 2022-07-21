#!/usr/bin/env python3
"""
Python function that changes all topics of a school
document based on the name
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
        - mongo_collection = pymongo collection object
        - name (string) = the school name to update
        - topics (list of strings) = the list of topics
            approached in the school
    """
    return mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
            )