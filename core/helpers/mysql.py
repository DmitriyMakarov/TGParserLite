import pymysql
import datetime

con = pymysql.connect(host='йцукен', user='bot_test', password='йцукен', database='test_bot')


def check_user_exist(user_id):
    query = f'SELECT user_id FROM `users` WHERE user_id="{user_id}"'
    try:
        cursor = con.cursor()
        cursor.execute(query)
        try:
            if cursor.fetchall()[0][0] == str(user_id):
                result = 200
            else:
                result = 400
        except IndexError:
            result = 400
        cursor.close()
        con.close()
    except Exception as e:
        print(e, "Error")
        result = 400
    return result


def add_user(user_id):
    now_date = datetime.datetime.today().strftime("%Y-%m-%d")
    print(now_date)
    query = f'INSERT INTO users (user_id, data_reg) VALUES ({user_id}, "{now_date}")'
    cursor = con.cursor()
    print('add_user')
    try:
        print('add user try')
        cursor.execute(query)
        con.commit()
        con.close()
    except pymysql.MySQLError as e:
        print(e)


def get_user_balance(user_id):
    query = f'SELECT balance FROM users WHERE user_id="{str(user_id)}"'
    cursor = con.cursor()
    try:
        cursor.execute(query)
        balance = cursor.fetchone()[0]
        con.close()
    except pymysql.Error as balance:
        print(balance)
    return balance


def set_user_balance(user_id):
    query_get_pays = f'SELECT sum FROM bills WHERE user_id=(SELECT id FROM users WHERE user_id="{user_id}" AND payd=1)'
    query_order_count = f'SELECT count(*) FROM orders WHERE user_id=(SELECT id FROM users WHERE user_id="{str(user_id)}")'
    try:
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
        print(e)
