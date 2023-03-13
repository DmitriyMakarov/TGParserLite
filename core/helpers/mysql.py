import logging

import pymysql
from pymysql.cursors import DictCursor
import datetime

con = pymysql.connect(host='95.214.63.160', user='bot_test', password='120984', database='test_bot',
                      cursorclass=DictCursor)


def check_user_exist(user_id):
    try:
        query = f'SELECT user_id FROM `users` WHERE user_id="{user_id}"'
        cursor = con.cursor()
        cursor.execute(query)
        return len(cursor.fetchall())
    except Exception:
        logging.exception(Exception)


def add_user(user_id):
    try:
        now_date = datetime.datetime.today().strftime("%Y.%m.%d")
        query = f'INSERT INTO users (user_id, data_reg) VALUES ({user_id}, "{now_date}")'
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        con.close()
    except Exception:
        logging.exception(Exception)


def get_user_balance(user_id):
    try:
        query = f'SELECT balance FROM users WHERE user_id="{str(user_id)}"'
        cursor = con.cursor()
        cursor.execute(query)
        balance = cursor.fetchone()[0]
        con.close()
    except pymysql.Error as e:
        logging.exception(e)
    return balance


def set_user_balance(user_id):
    try:
        query_get_pays = f'SELECT sum FROM bills WHERE user_id=(SELECT id FROM users WHERE user_id="{user_id}" AND payd=1)'
        query_order_count = f'SELECT count(*) FROM orders WHERE user_id=(SELECT id FROM users WHERE user_id="{str(user_id)}")'
        cursor = con.cursor()
        cursor.execute(query_get_pays)
        pay_sum = 0
        for pay in cursor.fetchall():
            pay_sum = pay_sum + int(pay[0])
        cursor.execute(query_order_count)
        orders_count = cursor.fetchall()[0][0]
        balance = pay_sum - int(orders_count) * 10
        query_set_balance = f'UPDATE users SET balance={balance} WHERE user_id="{str(user_id)}"'
        cursor.execute(query_set_balance)
        con.commit()
    except pymysql.Error as e:
        logging.exception(e)
