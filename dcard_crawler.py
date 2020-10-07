# coding: utf-8
import requests
import time
import json
import sqlite3

tableName = 'trending'

sql = '''CREATE  TABLE  IF NOT EXISTS "main"."{}" 
("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "articleID" INTEGER, "forumName" VARCHAR, "forumAlias" VARCHAR, "title" VARCHAR, "school" VARCHAR, 
"department" VARCHAR, "gender" VARCHAR, "createdAt" VARCHAR, "updatedAt" VARCHAR, "commentCount" INTEGER, 
"likeCount" INTEGER, "excerpt" VARCHAR, "path" VARCHAR)'''.format(tableName)

try:
    conn = sqlite3.connect('dcard_db.sqlite')
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    jData = {}
    # 下列網址會向Dcard要求「article ID」之前的文章資訊，一次提供30筆資料
    prefix = 'https://www.dcard.tw/_api/forums/trending/posts?popular=false&before='
    articleID = '234506405'  # 目前最新的文章
    rs = requests.session()
    while True:
        res = rs.get(prefix + str(articleID))
        if str(res) == '<Response [200]>':
            data = res.text
            jData = json.loads(data)
            for i in range(jData.__len__()):
                articleID = jData[i]['id']
                title = jData[i]['title'].replace("'", "''")  # 置換單引號成雙單引號
                print(jData[i])
                if jData[i]['anonymousSchool'] == False:
                    if jData[i]['school']:
                        school = jData[i]['school'].replace("'", "''")
                    else:
                        school = 'None'
                else:
                    school = 'anonymousSchool'
                if jData[i]['anonymousDepartment'] == False:
                    department = jData[i]['department']
                else:
                    department = 'anonymousDepartment'
                gender = jData[i]['gender']
                createdAt = jData[i]['createdAt']
                updatedAt = jData[i]['updatedAt']
                commentCount = jData[i]['commentCount']
                likeCount = jData[i]['likeCount']
                excerpt = jData[i]['excerpt'].replace("'", "''")
                forumName = jData[i]['forumName']
                forumAlias = jData[i]['forumAlias']
                prePath = 'https://www.dcard.tw/f/{}/p/'.format(forumAlias)
                path = prePath + str(articleID)
                print('ID: {}'.format(articleID))
                print('title: {}'.format(title))
                print('school: {}'.format(school))
                print('department: {}'.format(department))
                print('gender: {}'.format(gender))
                print('created at: {}'.format(createdAt))
                print('update at: {}'.format(updatedAt))
                print('commentCount: {}'.format(commentCount))
                print('likeCount: {}'.format(likeCount))
                print('excerpt: {}'.format(excerpt))
                print('URL: {}'.format(path))
                print('forumName: {}'.format(forumName))
                print('forumAlias: {}'.format(forumAlias))
                print('-----')
                # print(sql)
                sql = '''
                INSERT INTO `{}`(`articleID`, `forumName`, `forumAlias`, `title`, `school`, `department`, `gender`, `createdAt`, `updatedAt`,
                 `commentCount`, `likeCount`, `excerpt`, `path`)  
                 VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                '''.format(tableName, articleID, forumName, forumAlias, title, school, department, gender, createdAt,
                           updatedAt, commentCount, likeCount, excerpt, path)
                c.execute(sql)
                conn.commit()
                print('success')
                print('-----')
            else:
                print('status code = {}'.format(res))
        time.sleep(1)  # 等待一秒再要求新資料，避免快速存取會被擋IP
        if jData.__len__() < 30:  # 一次請求30筆資料，當文章不足30筆資料表示到達最底層。
            print(jData.__len__())
            print('文章全數存取完畢')
            break
except Exception as e:
    print(e)
conn.close()
