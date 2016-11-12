# -*- coding: utf-8 -*-
import urllib2
import urllib
from bs4 import BeautifulSoup
import MySQLdb


def getContent(url):
    '''获取网页信息'''

    # url = 'http://s.visitbeijing.com.cn/html/j-117873.shtml'
    # url = 'http://s.visitbeijing.com.cn/html/j-101407.shtml'
    response = urllib2.urlopen(url)

    the_page = response.read()
    # save2file(the_page, 'page.txt')
    # print the_page
    return the_page


def parseContent(url, content):
    '''解析网页'''
    soup = BeautifulSoup(content, "lxml")
    # name = soup.select('div.banTitle > p')[0].get_text()
    name = url

    conn = conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    if cur.execute("select name from scenes_info where name='"+name+"'") > 0:
        print "here"
        return


    tipsList = soup.select('div.open')
    # save2file(scenceList)
    # print scenceList
    danSeason = wangSeson = tip = phone = besttime = visittime = facilities = ""
    for i in tipsList:
        para = i.select('div.op01 > p')
        danSeasonNode = i.select('p.p01')
        if danSeasonNode:
            danSeason = danSeasonNode[0].get_text()
        else:
            danSeason = ""

        wangSeasonNode = i.select('p.p02')
        if wangSeasonNode:
            wangSeason=wangSeasonNode[0].get_text()
        else:
            wangSeason = ""

        # textNode =
        try:
            text = para[2].get_text()
            if u'提示' in text:
                tip = text
            else:
                tip = ""
        except:
            continue


        phoneNode = i.select('p.p03')
        if phoneNode:
            phone = phoneNode[0].get_text()
        else:
            phone = ""

        besttimeNode = i.select('p.p04')
        if besttimeNode:
            besttime = besttimeNode[0].get_text()
        else:
            besttime = ""

        visittimeNode = i.select('p.p05')
        if visittimeNode:
            visittime = visittimeNode[0].get_text()
        else:
            visittime = ""

        sheshis = i.select('span.gou')
        facilities = ""
        if sheshis:
            for sheshi in sheshis:
                facilities = facilities + sheshi.get_text()
    print danSeason + '--' + wangSeason + '--' + tip + '--' + phone + '--' + besttime + '--' + visittime
    print facilities
    print '--' * 15

    ticketList = soup.select('div.ticket')
    if ticketList:
        for t in ticketList:
            paras = t.select('p')
            info = ''
            for pa in paras:
                info = info + ' '+ pa.get_text()
    print info

        # for index, p in enumerate(para):
        #     if len(para) == 6:
        #         tmptx = p.get_text()
        #         if index == 0:
        #             danSeason = tmptx
        #         if index == 1:
        #             wangSeason = tmptx
        #         if index == 2:
        #             tip = tmptx
        #         if index == 3 and u'电话' in tmptx:
        #             phone = tmptx
        #         if index == 4 and u'时间' in tmptx:
        #             besttime = tmptx
        #         if index == 5 and u'时间' in tmptx:
        #             visittime = tmptx

    save2db(name, danSeason, wangSeason, tip, phone, besttime, visittime, facilities, info)


def spider():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    cur.execute("select url from scenes_list")
    result = cur.fetchall()
    for res in result:
        url = res[0]
        content = getContent(url)
        parseContent(url, content)

    conn.commit()
    cur.close()
    conn.close()


def save2db(name, danSeason, wangSeason, tip, phone, besttime, visittime, facilities, info):
    '''保存到数据库'''
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    # cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat + 1, tmplng + 1, float(distance)))
    cur.execute("insert into sns.scenes_info(name, danSeason, wangSeason, tips, phone, besttime, visittime, facilities, ticket) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(name, danSeason, wangSeason, tip, phone, besttime, visittime, facilities, info))
    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    '''主函数'''
    # content = getContent()
    # parseContent(content)
    spider()