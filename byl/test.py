# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request,redirect,make_response,session
import os,MySQLdb
from flask import jsonify
import json
import sys
from repeatGames import RepeatGames

reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
#app.secret_key='afjlsjfowflajflkajfkjfkaljf'
#user_list = ['jim','max','py']
imagepath = os.path.join(os.getcwd(),"static/images")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next', methods=['GET','POST'])
def nextpage():
    if request.method=='POST':
        print 'success'
        data = request.json
        print data
        people=int(data['people'])
        time=int(data['time'])
        responsedata={'people':'',
                      'time':''
                      }
        if people<2:
            responsedata['people']="参数人数至少为2人"


        if time<10:
            responsedata['time']='比赛轮数最少为10轮'



        return jsonify(responsedata)


    #elif request.method=='GET':
@app.route('/strategy')
def strategy():
    people=request.args.get('people')
    time=request.args.get('time')
    strategys=['']
    print people
    strategy=["一直合作","一直背叛","随机策略","一直抱复","仁爱型","犹大型","乔斯策略","道宁策略","怪异型策略","哈灵顿策略","两报还一报","一报还两报","三报还一报","一报还三报","一报换一报","x报还一报","一报还x报",'M报还N报']
    return render_template('next.html',people=int(people),time=int(time),strategy=strategy,strategycount=len(strategy),firstgroup=int(len(strategy)/2+1))

@app.route('/output' ,methods=['GET','POST'])
def output():
    if request.method=='POST':
        people=int(request.form.get('people'))
        rounds=int(request.form.get('rounds'))
        print people
        strategys=[]
        need_args=[]
       # strategy=["一直合作","一直背叛","随机策略","一直抱复","两报还一报","一报还两报","三报还一报","一报还三报","一报换一报","x报还一报","一报还x报"]
        for i in range(1,int(people)+1):
            strategys.append(int(request.form.get('people'+str(i))))
            if int(request.form.get('people'+str(i)))==18:
                need_args.append(i)
        if not 18 in strategys:
            repeatgames=RepeatGames()
            result=repeatgames.main(people,rounds,strategys)
            print result
            keys=[]
            values=[]
            competitors=[]
            for i in range(0,len(result)):
                keys.append(result[i][0])
                competitors.append(result[i][1]+1)
                values.append(result[i][2])
            return render_template('output.html',keys=keys,values=values,competitors=competitors,len=len(keys))
        else:
            strategys=" ".join([str(x) for x in strategys])
            argpeople=" ".join([str(x) for x in need_args])
            return render_template('choosearg.html',strategys=strategys,needargs=need_args,argpeople=argpeople,people=int(people),time=int(rounds))



@app.route('/output_args' ,methods=['GET','POST'])
def output_args():
    if request.method=='POST':
        people=int(request.form.get('people'))
        rounds=int(request.form.get('rounds'))
        print people
        strategys=request.form.get('strategys').split(' ')
        argpeople=request.form.get('argpeople').split(' ')

        strategys=[int(x) for x in strategys]
        argpeople=[int(x) for x in argpeople]
        args={}
        print argpeople
        for i in argpeople:
            print i
            print request.form.get(str(i)+'M')

            args[i]=[int(request.form.get(str(i)+'M')),int(request.form.get(str(i)+'N'))]
        print args
        repeatgames=RepeatGames()
        result=repeatgames.main_args(people,rounds,strategys,args)
        print result
        keys=[]
        values=[]
        competitors=[]
        for i in range(0,len(result)):
            keys.append(result[i][0])
            competitors.append(result[i][1]+1)
            values.append(result[i][2])
        return render_template('output.html',keys=keys,values=values,competitors=competitors,len=len(keys))

@app.route('/output_random')
def output_random():
    people=int(request.args.get('people'))
    time=int(request.args.get('time'))
    repeatgames=RepeatGames()
    result=repeatgames.main_random(people,time)
    print result
    keys=[]
    values=[]
    competitors=[]
    for i in range(0,len(result)):
        keys.append(result[i][0])
        competitors.append(result[i][1]+1)
        values.append(result[i][2])
    return render_template('output.html',keys=keys,values=values,competitors=competitors,len=len(keys))


@app.route('/map')
def createmap():

    conn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('atmo')
    site=[u"东城东四",u"西城官园",u"西城万寿西宫",u"朝阳农展馆",u"东城天坛",u"海淀万柳",u"朝阳奥体中心",u"海淀北部新区",u"海淀北京植物园",u"北京美国大使馆",u"东四环北路",
        u"南三环西路",u"西直门北大街",u"永定门内大街",u"前门东大街",u"丰台花园",u"石景山古城",u"丰台云岗"]
    site2=[u"顺义新城",u"通州新城",u"亦庄开发区",u"大兴黄村镇",u"房山良乡",u"昌平镇",u"门头沟龙泉镇",u"京南榆垡",u"京东南永乐店",u"京西南琉璃河",u"京东东高村",u"京东北密云水库",u"怀柔镇",u"昌平定陵",
        u"密云镇",u"延庆镇",u"平谷镇"]
    siteinfo={}
    for i in range(0,len(site)):
        cur.execute('select centerlat,centerlng from atmo.aqicnsiteangle where center="'+site[i]+'"')
        lat=float(cur.fetchone()[0])
        lng=float(cur.fetchone()[1])
        siteinfo[site[i]]=[lat,lng,1]



    for i in range(0,len(site2)):
        cur.execute('select centerlat,centerlng from atmo.aqicnsiteangle where center="'+site2[i]+'"')
        lat=float(cur.fetchone()[0])
        lng=float(cur.fetchone()[1])
        siteinfo[site2[i]]=[lat,lng,2]
    return render_template('map.html',siteinfo=siteinfo)



if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)