import mysql.connector

from mysql import connector
from mysql.connector import errorcode
from mysql.connector.constants import ClientFlag
from flask import jsonify
import os


def GetConnection():
    conn = mysql.connector.connect(host='localhost', port='3306', user='root', password='root',
                                   database='food',auth_plugin='mysql_native_password')
    return  conn;


