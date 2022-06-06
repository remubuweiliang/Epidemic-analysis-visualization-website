import pymysql


# 返回链接对象
def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='flask',
        charset='utf8'
    )


# 创建数据库
def creat_database():
    conn = get_conn()
    cursor = conn.cursor()
    # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 定义要执行的SQL语句
    sql = """
    CREATE TABLE `users` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `user` varchar(16) NOT NULL,
    `sex` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
    `number` bigint NOT NULL,
    `pwd` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `position` varchar(8) DEFAULT NULL,
    PRIMARY KEY (`user`),
    KEY `id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """
    cursor.execute(sql)
    # 对数据库进行写操作要提交（建表不算）
    # conn.commit()
    cursor.close()
    conn.close()


# 查询数据库
def query_data():
    # 连接数据库
    conn = get_conn()
    # 不管数据库操作结果如何，都要关闭数据库
    try:
        # 结果集默认以元组显示，DictCursor返回字典形式，cursor链接上执行sql语句的对象得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 查询 SQL 语句
        sql = "select * from users;"
        cursor.execute(sql)
        # 执行 SQL 语句 返回值就是 SQL 语句在执行过程中影响的行数
        # row_count = cursor.execute(sql)
        # print("SQL 语句执行影响的行数%d" % row_count)
        # 取出结果集中一行数据,　例如:(1, '张三')
        # print(cursor.fetchone())
        # 取出结果集中的所有数据, 例如:((1, '张三'), (2, '李四'), (3, '王五'))
        data = []
        for line in cursor.fetchall():
            data.append(line)
        return data
    finally:
        conn.close()


# # 查询数据库
# def query_one_data(data):
#     # 连接数据库
#     conn = get_conn()
#     # 不管数据库操作结果如何，都要关闭数据库
#     try:
#         # 结果集默认以元组显示，DictCursor返回字典形式，cursor链接上执行sql语句的对象得到一个可以执行SQL语句的光标对象
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # 查询 SQL 语句
#         sql = "select * from users;"
#         cursor.execute(sql)
#         # 执行 SQL 语句 返回值就是 SQL 语句在执行过程中影响的行数
#         # row_count = cursor.execute(sql)
#         # print("SQL 语句执行影响的行数%d" % row_count)
#         # 取出结果集中一行数据,　例如:(1, '张三')
#         # print(cursor.fetchone())
#         # 取出结果集中的所有数据, 例如:((1, '张三'), (2, '李四'), (3, '王五'))
#         data = []
#         for line in cursor.fetchall():
#             data.append(line)
#         return data
#     finally:
#         conn.close()


# 插入数据
def insert_database(data):
    # data = ('zry5', '男', '15816543914', '12312312131231', '佛山')
    conn = get_conn()
    # 不管数据库操作结果如何，都要关闭数据库
    try:
        # username = request.POST.get('username')
        # pwd = request.POST.get('pwd')
        cursor = conn.cursor()
        sql = "insert into users(user,sex,number,pwd,position) values(%s,%s,%s,%s,%s);"
        res = cursor.execute(sql, data)
        conn.commit()  # 涉及写操作要注意提交
        # 获取最新的那一条数据的ID
        # last_id = cursor.lastrowid
        # print("最后一条数据的ID是:", last_id)
        cursor.close()
    finally:
        conn.close()


# 删除数据
def delete_database(name):
    # name = "zry"
    # 建立连接
    conn = get_conn()
    # 不管数据库操作结果如何，都要关闭数据库
    try:
        # 获取一个光标
        cursor = conn.cursor()
        # 定义将要执行的SQL语句
        sql = "delete from users where user=%s;"
        # 拼接并执行SQL语句
        cursor.execute(sql, [name])
        # 涉及写操作注意要提交
        conn.commit()
        # 关闭连接
        cursor.close()
    finally:
        conn.close()


# 更新数据
def change_database(data):
    # data = ('zry', 'zry123123')
    # 建立连接
    conn = get_conn()
    # 不管数据库操作结果如何，都要关闭数据库
    try:
        # 获取一个光标
        cursor = conn.cursor()
        # 定义将要执行的SQL语句
        sql = "update users set pwd=%s where user=%s;"
        # 拼接并执行SQL语句
        cursor.execute(sql, data)
        # 涉及写操作注意要提交
        conn.commit()
        # 关闭连接
        cursor.close()
    finally:
        conn.close()


# if __name__ == '__main__':
#     query_data()
