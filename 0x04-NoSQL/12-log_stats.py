#!/usr/bin/env python3
"""
Python script that provides some stats about
Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def logs(nginx):
    '''
    Prints Nginx request logs.
    '''
    print(f'{nginx.count_documents({})} logs')
    print('Methods:')
    reqs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for req in reqs:
        print(f'\tmethod {req}: {nginx.count_documents({"method": req})}')
    print(f'{nginx.count_documents({"path": "/status"})} status check')


def conn():
    '''
    Establish a connection with MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    logs(nginx)


if __name__ == '__main__':
    conn()