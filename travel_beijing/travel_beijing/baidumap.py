#coding=utf-8

import urllib2
import urllib
import httplib
import json


class BaiduMap:
    precision = None
    host = 'http://api.map.baidu.com'
    path = '/geocoder/v2/?'
    param = {
              'address' : None,
              'output' : 'json',
              'ak' : 'rBHgzWXGwp7M0w0E8MSUUzrr',
              'location' : None,
              'city' : None
            }


    def __init__(self):
        self.setPercision(50)
    
    def __init__(self, city, precision=50):
        self.setCity(city)
        self.setPrecision(precision)

    #设置城市
    def setCity(self, city):
        if city != None:
            self.param['city'] = city

    #设置精度
    def setPrecision(self, precision):
        if precision > 0 and precision <= 100:
            self.precision = precision


    #根据地址得到经纬度
    def getLocation(self, address, city=None):
        self.setParam("address", address, city)
        result = self.sendAndRec()
        #for key in sorted(result):
            #print(key, '=======>', result[key])

        return result


    #设置字典参数param
    def setParam(self, key, value, city):
        #根据所传地址设置内容参数
        if key == "address":
            if 'location' in self.param:
                del self.param['location']
            if city == None and 'city' in self.param and self.param['city'] == None:
                del self.param['city']
            else:
                self.param['city'] = city
        #根据所传经纬度设置内容参数
        elif key == "location":
            if 'city' in self.param:
                del self.param['city']
            if 'address' in self.param:
                del self.param['address']
        
        self.param[key] = value
 
   
    #发送请求
    def sendAndRec(self):
        url = self.host + self.path + urllib.urlencode(self.param)
        r = urllib.urlopen(url)

        return r.read()


    #对返回结果的状态进行判断
    def checkStatus(self, status):
        #正确
        if status == 0:
            return None

        #对错误结果分情况判断
        error = None
        if status == 1:
            error = "服务器内部错误"
        elif status == 2:
            error = "请求参数非法"
        elif status == 3:
            error = "权限校验失败"
        elif status == 4:
            error = "配额校验失败"
        elif status == 5:
            error = "ak不存在或者非法"
        elif status == 101:
            error = "服务禁用"
        elif status == 102:
            error = "不通过白名单或者安全码不对"
        else:
            error = "其他错误"
        return error
