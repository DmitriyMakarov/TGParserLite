import sqlite3
import configparser
import os
import datetime

base_path = (os.environ['VIRTUAL_ENV'] + '/../' + 'res/db/db.sqlite')
connect_base = sqlite3.connect(base_path, check_same_thread=False)
cursor = connect_base.cursor()


def check_user_exist(user_id):
    query = f'SELECT user_id FROM users WHERE user_id="{str(user_id)}"'
    try:
        if cursor.execute(query).fetchall()[0][0] == str(user_id):
            result = 200
        else:
            result = 400
    except Exception as e:
        result = 400
        print(e, 'check_user_exist()')
    return result


def add_new_user(user_id):
    query = f'INSERT INTO users (user_id, data_reg) VALUES ("{str(user_id)}","{str(datetime.datetime.today())}")'
    try:
        cursor.execute(query)
        connect_base.commit()
    except Exception as e:
        print(e, 'add_new_user()')


def get_user_balance(user_id):
    query = f'SELECT balance FROM users WHERE user_id="{str(user_id)}"'
    try:
        result = cursor.execute(query).fetchall()[0][0]
    except Exception as e:
        print(e, 'get_user_balance()')
        result = 'err'
    return result


def set_user_balance(user_id):
    query_get_pays = f'SELECT sum FROM bills WHERE user_id=(SELECT id FROM users WHERE user_id="{str(user_id)}" AND payd=1)'
    query_order_count = f'SELECT count(*) FROM orders WHERE user_id=(SELECT id FROM users WHERE user_id="{str(user_id)}")'
    sum_order = 0
    try:
        pays_cursor = cursor.execute(query_get_pays)
        for pay in pays_cursor:
            sum_order = sum_order + int(pay[0])
        count_cursor = cursor.execute(query_order_count).fetchall()[0][0]
        summ = sum_order - int(count_cursor) * 10
        query_set_balance = f'UPDATE users SET balance={summ} WHERE user_id="{str(user_id)}"'
        cursor.execute(query_set_balance)
        connect_base.commit()
    except Exception as e:
        print(e, 'set_user_balance()')
    return summ


