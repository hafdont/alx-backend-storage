#!/usr/bin/env python3
"""
Topics module
"""

def update_topics(mongo_collection, name, topics):
    """
    functions docstring
    """
    mongo_collection.update_many(
            {'name':name},
            {'$set': {'topics': topics}}
    )
