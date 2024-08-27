#!/usr/bin/env python3
""""sumary_line"""


def top_students(mongo_collection):
    """Returns Top Student"""
    return mongo_collection.aggregate([
        {'$project': {
            'name': '$name',
            'averageScore': {'$avg': '$topics.score'}
        }},

        {'$sort': {'averageScore': -1}}
    ])
