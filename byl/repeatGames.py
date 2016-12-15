# -*- coding: utf-8 -*-
import random
import numpy

class RepeatGames:
    #"一直合作","一直背叛","随机策略","一直抱复","两报还一报","一报还两报","三报还一报","一报还三报","一报换一报","x报还一报","一报还x报",'M报还N报'
    stgDct = {
        1:"一直合作",
        2:"一直背叛",
        3:"随机策略",
        4:"一直抱复",
        5:"仁爱型",
        6:"犹大型",
        7:"乔斯策略",
        8:"道宁策略",
        9:"怪异型策略",
        10:"哈灵顿策略",
        11:"两报还一报",
        12:"一报还两报",
        13:"三报还一报",
        14:"一报还三报",
        15:"一报还一报",
        16:"x报还一报(X:1-5)",
        17:"一报还x报(X:1-3)",
        18:"M报还N报"
    }
    def __init__(self):
        print 'hello'
    #一报还一报
    def strategy1(self,list1,list2):
        if len(list1)==0:
            return 0
        return list2[len(list2)-1]

    #随机策略
    def strategy2(self,list1,list2):
        if random.random()>0.5:
            return 1
        else:
            return 0
    #一次背叛则永久背叛，否则坚持合作
    def strategy3(self,list1,list2):
        if len(list1)==0:
            return 0
        if 1 in list2:
            return 1
        else:
            return 0
    #对方连续N次背叛，我方连续背叛M次
    ##需要注意，N和M为非负整数


    def strategy4(self,n, m, list1, list2):
        if n<=0:
            #连续背叛策略
            return 1
        elif m<=0:
            #连续合作策略
            return 0
        else:
            #n次背叛则m次背叛
            pos = len(list2)
            if pos<n:
                return 0
            else:
                for i in range(m):
                    #检查前m个N数组切片
                    if pos-n-i<0:
                        continue
                    slice = list2[pos-n-i:pos-i]
                    if 0 not in slice:
                        #print slice, n, m, pos
                        #print list1, list2
                        return 1
                return 0
#仁爱型策略
    def strategy5(self,list1,list2):
        count=0
        for i in list2:
            if i==1:
                count=count+1
        rate=1-float(count)/100
        if random.random()<rate:
            return 0
        else:
            return 1
#犹大型策略
    def strategy6(self,list1,list2):
        count=0
        for i in list2:
            if i==0:
                count=count+1
        rate=float(count)/100
        if random.random()<rate:
            return 0
        else:
            return 1

#乔斯策略
    def strategy7(self,list1,list2):
        if len(list1)==0:
            return 0
        elif list2[len(list2)-1]==1:
            return 1
        else:
            if random.random()<0.1:
                return 1
            else:
                return 0
#道宁策略
    def strategy8(self,list1,list2):
        if len(list1)==0:
            return 1
        else:
            rate0=0
            rate1=0
            for i in range(len(list1)-1):
                if list1[i]==1:
                    if list2[i+1]==0:
                        rate0=rate0+1
                    else:
                        rate1=rate1+1
            if rate0>rate1:
                return 1
            else:
                return 0
#奇异型策略
    def strategy9(self,list1,list2):
        if len(list1)==0:
            return 0
        return 1-list2[len(list2)-1]
#哈灵顿策略
    def strategy10(self,list1,list2):
        if len(list1)<3:
            return 0
        else:
            length=len(list1)
            if list2[length-1]==0 and list2[length-2]==0 and list2[length-3]==0:
                return 1
            else:
                return 0





    def choosestrategy(self,stg1,stg2,list1,list2,xarg,yarg):
        print xarg,yarg
        x = 0
        y = 0
        if stg1==1:
            #一直合作
            x = 0
        elif stg1==2:
            #一直背叛
            x= 1
        elif stg1==3:
            x=self.strategy2(list1,list2)
        elif stg1==4:
            x=self.strategy3(list1,list2)
        elif stg1==5:
            x=self.strategy5(list1,list2)
        elif stg1==6:
            x=self.strategy6(list1,list2)
        elif stg1==7:
            x=self.strategy7(list1,list2)
        elif stg1==8:
            x=self.strategy8(list1,list2)
        elif stg1==9:
            x=self.strategy9(list1,list2)
        elif stg1==10:
            x=self.strategy10(list1,list2)
        elif stg1==11:
            #2背叛则1背叛
            x = self.strategy4(2, 1, list1, list2)
        elif stg1==12:
            #1背叛则2背叛
            x = self.strategy4(1, 2, list1, list2)
        elif stg1==13:
            #3背叛则1背叛
            x = self.strategy4(3, 1, list1, list2)
        elif stg1==14:
            #1背叛则3背叛
            x = self.strategy4(1, 3, list1, list2)
        elif stg1==15:
            #1报还1报
            x = self.strategy1(list1,list2)
        elif stg1==16:
            #1报还X报（X为1-5随机数）
            rand = random.randint(1,5)
            x = self.strategy4(1,rand, list1,list2)
        elif stg1==17:
            #X报还1报（X为1-3随机数）
            rand = random.randint(1,3)
            x = self.strategy4(rand,1, list1,list2)
        elif stg1==18:
            x=self.strategy4(xarg[0],xarg[1],list1,list2)


        if stg2==1:
            y = 0
        elif stg2==2:
            y = 1
        elif stg2==3:
            y=self.strategy2(list2,list1)
        elif stg2==4:
            y=self.strategy3(list2,list1)
        elif stg2==5:
            y=self.strategy5(list2,list1)
        elif stg2==6:
            y=self.strategy6(list2,list1)
        elif stg2==7:
            y=self.strategy7(list2,list1)
        elif stg2==8:
            y=self.strategy8(list2,list1)
        elif stg2==9:
            y=self.strategy9(list2,list1)
        elif stg2==10:
            y=self.strategy10(list2,list1)
        elif stg2==11:
            y = self.strategy4(2, 1, list2, list1)
        elif stg2==12:
            y = self.strategy4(1, 2, list2, list1)
        elif stg2==13:
            y = self.strategy4(3, 1, list2, list1)
        elif stg2==14:
            y = self.strategy4(1, 3, list2, list1)
        elif stg2==15:
            y = self.strategy1(list2,list1)
        elif stg2==16:
            #1报还X报（X为1-5随机数）
            rand = random.randint(1,5)
            y = self.strategy4(1,rand, list2,list1)
        elif stg2==17:
            #X报还1报（X为1-3随机数）
            rand = random.randint(1,3)
            y = self.strategy4(rand,1, list2,list1)
        elif stg2==18:
            y=self.strategy4(yarg[0],yarg[1],list2,list1)

        return x,y



    def init(self,num_competitor,num_round,strategies,strarg={}):
        #num_competitor:total number of competitor
        #num_round:number of rounds for each two competitor
        #strategys:strategy number for each single competitor
        resDct = {}
        stepDct = {}
        scoreRank = {}
        score = []
        for i in range(num_competitor):
            for j in range(i,num_competitor):
                list1 = []
                list2 = []
                for round in range(num_round):
                    if strategies[i]==18 and strategies[j]==18:
                        x, y = self.choosestrategy(strategies[i], strategies[j], list1,list2,strarg[(i+1)],strarg[(j+1)])
                    elif strategies[i]==18:
                        x, y = self.choosestrategy(strategies[i], strategies[j], list1,list2,strarg[(i+1)],[])
                    elif strategies[j]==18:
                        x, y = self.choosestrategy(strategies[i], strategies[j], list1,list2,[],strarg[(j+1)])
                    else:
                        x, y = self.choosestrategy(strategies[i], strategies[j], list1,list2,[],[])
                    list1.append(x)
                    list2.append(y)
                score1, score2 = self.calScore(list1, list2)
                score.append(score1)
                resDct[(i,j)] = (score1,score2)
                resDct[(j,i)] = (score2,score1)#simple query
                stepDct[(i,j)] = zip(list1, list2)
                stepDct[(j,i)] = zip(list2, list1)
            scoreRank[i] = numpy.mean(score)
        print scoreRank
        scoreRank = sorted(scoreRank.iteritems(),
            key=lambda x:x[1], reverse=True)
        print scoreRank
        scoreRank = [(self.stgDct[strategies[item[0]]],item[0], item[1]) for item in scoreRank]

        print '*'*50
        #print "Steps:",stepDct
        #print "Scores of each step:",resDct
        #print "Strategies:",strategies
        print "Total Score Rank:"
        for item in scoreRank:
            print item
        print '*'*50
        return scoreRank

    def calScore(self,list1, list2):
        if len(list1)!=len(list2):
            print "Error Rounds!"
            exit(0)
        sum1 = 0
        sum2 = 0
        for x,y in zip(list1, list2):
            if x==0 and y==0:
                sum1+=3
                sum2+=3
            elif x==0 and y==1:
                sum2+=5
            elif x==1 and y==1:
                sum1+=1
                sum2+=1
            elif x==1 and y==0:
                sum1+=5
            else:
                print "Error Strategy!"
                exit(0)
        return sum1, sum2

    def randomStrategy(self,num_competitor, num_strategy):
        #每个参赛者随机选择一种策略
        strategies = []
        for i in range(num_competitor):
            rand = random.randint(1, num_strategy)
            strategies.append(rand)
            print strategies
        return strategies

    # num_strategy = 11
    # num_competitor = 55
    # rounds = 200

    #1.参赛者随机选择策略
    #strategies = randomStrategy(num_competitor,num_strategy)
    #2.(Only for test)每种策略出现一次
    def main(self,num_competitor, rounds, strategies):
    #strategies = range(11)*5
        return self.init(num_competitor, rounds, strategies)

    def main_args(self,num_competitor, rounds, strategies,strargs):
        return self.init(num_competitor, rounds, strategies,strargs)

    def main_random(self,num_competitor, rounds):
        strategies = self.randomStrategy(num_competitor,17)
        return self.init(num_competitor, rounds, strategies)
