#!/usr/bin/env python3
"""
8-all.py
"""



def list_all(mongo_collection):
    """
    The documentation
    """
    return list(mongo_collection.find())
