# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request,redirect,make_response,session
import os,MySQLdb
from flask import jsonify
import json
import sys
from recommend2 import recommend


reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
#app.secret_key='afjlsjfowflajflkajfkjfkaljf'
#user_list = ['jim','max','py']
imagepath = os.path.join(os.getcwd(),"static/images")

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/recommend' ,methods=['GET','POST'])
def recommend1():
    if request.method=='POST':
        day=int(request.form.get('day'))
        month=request.form.get('month')
        cost= int(request.form.get('cost'))
        rec=recommend()
        paths,paths_by_day=rec.start(day,cost,month)
        return render_template('recommend.html',path=paths,path_by_day=paths_by_day,day=day)


@app.route('/detail' ,methods=['GET','POST'])
def detail():
    if request.method=='POST':
        path=request.form.get('path')

        rec=recommend()
        pathdict=rec.showdetail(path)
        print pathdict
        name=pathdict['name']
        price=pathdict['price']
        intro=pathdict['intro']
        special=pathdict['special']
        pic=pathdict['pic']
        address=pathdict['address']
        len1=len(pathdict['name'])
        len2=len1/3
        len3=len1%3
        return render_template('detail.html',name=name,price=price,intro=intro,special=special,pic=pic,address=address,len=len1,len2=len2,len3=len3)



if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)