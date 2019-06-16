import datetime
from dateutil.parser import parse
import re

class demandperiod(object):

    def __init__(self):
        self.demandperiod={}
        self.months={1:'JAN',2:'FEB',3:'MAR',4:'APR',
                     5:'MAY',6:'JUN',7:'JUL',8:'AUG',
                     9:'SEP',10:'OCT',11:'NOV',12:'DEC'}
        
    def testdate(text):
        regex = r'[0-9]{4}(-[0-9]{2})?(-[0-9]{2})?'
        a=re.match(regex,text)
        if a != None:
            return True,a.string[0:4]
        return False,''
    
    def generateperiods(year):
        weekperiods={}
        for i in range(1,datetime.date(year,12,28).isocalendar()[1]+1):
            weekperiods[i]={}

        for i in range(1,13):
            date=datetime.date(year,i,1)
            isoyear,isoweek,isoday=date.isocalendar()
            if i==1:
                if (isoyear==year and isoday<=4):
                    weekperiods[isoweek]['period']=i
                    weekperiods[isoweek]['periodweek']='a'
                else:
                    weekperiods[isoweek]={}
                    prev=demandperiod.generateperiods(year-1)
                    weekperiods[isoweek]['period']=prev[isoweek]['period']
                    weekperiods[isoweek]['periodweek']=prev[isoweek]['periodweek']
                    weekperiods[1]['period']=i
                    weekperiods[1]['periodweek']='a'
            else:
                if isoday<=3:
                    weekperiods[isoweek]['period']=i
                    weekperiods[isoweek]['periodweek']='a'
                elif isoyear == year:
                    weekperiods[isoweek+1]['period']=i
                    weekperiods[isoweek+1]['periodweek']='a'
                else:
                    weekperiods[1]['period']=i
                    weekperiods[1]['periodweek']='a'
        for i in range(2,datetime.date(year,12,28).isocalendar()[1]+1):
            if len(weekperiods[i])==0 and len(weekperiods[i-1])!=0:
                weekperiods[i]['period']=weekperiods[i-1]['period']
                weekperiods[i]['periodweek']=chr(ord(weekperiods[i-1]['periodweek'])+1)
        return weekperiods
    
    def generate(self,year):
        self.demandperiod={}
        self.demandperiod[year]={}
        self.year=year # next(iter(self.demandperiod))
        for month in range(1,13):
            self.demandperiod[year][month]=[]

        d=datetime.date(int(year),1,1)
        dayofyear=1
        while d<datetime.date(int(year)+1,1,1):
            dateinfo={}
            dateinfo['day']=d.isoformat()
            isoyear,isoweek,isoday=d.isocalendar()
            dateinfo['isoyear']=str(isoyear)
            dateinfo['isoweek']=str(isoweek)
            dateinfo['isoday']=str(isoday)
            dateinfo['dayofyear']=str(dayofyear)
            dateinfo['period']=demandperiod.generateperiods(int(year))[isoweek]['period']
            dateinfo['periodweek']=demandperiod.generateperiods(int(year))[isoweek]['periodweek']
         
            self.demandperiod[year][d.month].append(dateinfo)
            #self.demandperiod[year].append(dateinfo)
            d=d+datetime.timedelta(days=1)
            dayofyear+=1

    
    def returnyeardemanperiods(self):
        return self.demandperiod
        
    def returnyearmonthdemanperiods(self,month):
        demandperiodmonth={}
        demandperiodmonth[self.year]={}
        demandperiodmonth[self.year][int(month)]=self.demandperiod[self.year][int(month)]
        return demandperiodmonth
    
    def returndaydemanperiods(self,day):
        demandperiodday={}
        demandperiodday[self.year]={}
        month=day[5:7]
        demandperiodday[self.year][int(month)]=[]
        for i in self.demandperiod[self.year][int(month)]:
            if i['day']==day:
                demandperiodday[self.year][int(month)].append(i)
        return demandperiodday
    
    
    