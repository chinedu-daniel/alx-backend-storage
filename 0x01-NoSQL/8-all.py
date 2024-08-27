#!/usr/bin/env python3
"""
List all documents in Python
""" 


def list_all(mongo_collection):
    """
    function that lists all collection
    """
    if mongo_collection is None:
        return []
    return mongo_collection.find()
