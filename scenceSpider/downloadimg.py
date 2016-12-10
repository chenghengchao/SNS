# -*- coding: utf-8 -*-
import urllib2
import cookielib
import MySQLdb
import os


def get_file(url):
    try:
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(url)
        operate = opener.open(req)
        data = operate.read()
        return data
    except BaseException, e:
        print e
        return None


def save_file(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()

def mkdir(path):
        # 去除左右两边的空格
        path=path.strip()
        # 去除尾部 \符号
        path=path.rstrip("\\")

        if not os.path.exists(path):
            os.makedirs(path)

        return path
#下载图片主程序
def downloadimg():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    # cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat + 1, tmplng + 1, float(distance)))
    cur.execute('select id,imgurl from modify_scenes_v1')
    results=cur.fetchall()
    for one in results:
        print one
        id=one[0]
        src=one[1]
        save_file('./scene_img/',str(id)+'.jpg',get_file(src))

    cur.close()
    conn.close()


if __name__ == '__main__':
    downloadimg()
