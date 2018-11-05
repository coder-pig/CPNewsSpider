"""
MySQL数据库操作工具类
"""
import pymysql


# 新闻类
class News:
    def __init__(self, title, abstract, url, create_time, category, origin):
        self.title = title
        self.abstract = abstract
        self.url = url
        self.create_time = create_time
        self.category = category
        self.origin = origin

    def to_dict(self):
        return {'title': self.title, 'abstract': self.abstract, 'url': self.url, 'create_time': self.create_time, 'category': self.category, 'origin': self.origin}


# MySQL数据库操作类
class DBHelper:

    def __init__(self):
        self.db = pymysql.connect('localhost', user='root', password='Jay12345', port=3306)
        self.news_column_list = ['title', 'abstract', 'url', 'create_time', 'category', 'origin']

    # 创建数据库
    def create_db(self):
        cursor = self.db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS news CHARACTER SET UTF8MB4")
        cursor.close()

    # 创建表
    def create_table(self):
        self.db = pymysql.connect('localhost', user='root', password='Jay12345', port=3306, db='news')
        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF Not Exists news("
                       "id INT AUTO_INCREMENT PRIMARY KEY,"
                       "title TEXT NOT NULL,"
                       "abstract TEXT,"
                       "url TEXT NOT NULL,"
                       "create_time TEXT NOT NULL,"
                       "category TEXT NOT NULL,"
                       "origin  TEXT NOT NULL)")
        cursor.close()

    # 删除表
    def delete_table(self):
        self.db = pymysql.connect('localhost', user='root', password='Jay12345', port=3306, db='news')
        cursor = self.db.cursor()
        cursor.execute("")
        cursor.close()

    # 插入一条新闻
    def insert_news(self, news):
        cursor = self.db.cursor()
        try:
            keys = ','.join(self.news_column_list)
            values = ','.join(['%s'] * len(self.news_column_list))
            sql = 'INSERT INTO news ({keys}) VALUES ({values})'.format(keys=keys, values=values)
            cursor.execute(sql, tuple(news.to_dict().values()))
            self.db.commit()
        except Exception as e:
            print(str(e))
            self.db.rollback()
        finally:
            cursor.close()

    # 插入多条新闻
    def insert_some_news(self, some_news):
        cursor = self.db.cursor()
        try:
            keys = ','.join(self.news_column_list)
            values = ','.join(['%s'] * len(self.news_column_list))
            sql = 'INSERT INTO news ({keys}) VALUES ({values})'.format(keys=keys, values=values)
            for news in some_news:
                cursor.execute(sql, tuple(news.to_dict().values()))
            self.db.commit()
        except Exception as e:
            print(str(e))
            self.db.rollback()
        finally:
            cursor.close()


if __name__ == '__main__':
    helper = DBHelper()
    helper.create_db()
    helper.create_table()
