 # importing libraries
from pytrends.request import TrendReq
import pandas as pd
import time
import os

# opening the file to read the ticker
f = open(r'C://Users/Hi/Desktop/ticker_ra.csv')
lines = f.readlines()
lines[:] = [line.rstrip('\n') for line in lines]

# storing the category in the list  i
#i = ['1283', '107', '278']
i = ['1283']

# creating a new folder 
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)    

#iterating it over loop line by line
count = 0
for j in lines:
    #count = count+29
    print("count is", count)
    time.sleep(.001)
    for k in i:
        
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = j
        #print(kw_list)
        pytrends.build_payload(kw_list, cat=k, timeframe='2004-01-01 2017-12-31', geo='US', gprop='')
        data = pytrends.interest_over_time()
        count = count+1
        #print(data)
        df = pd.DataFrame(data)
        createFolder('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/')
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_monthly.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2004-01-01 2004-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2004.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2004-07-01 2004-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2004.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2005-01-01 2005-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2005.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2005-07-01 2005-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2005.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2006-01-01 2006-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2006.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2006-07-01 2006-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2006.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2007-01-01 2007-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2007.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2007-07-01 2007-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2007.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2008-01-01 2008-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2008.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2008-07-01 2008-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2008.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2009-01-01 2009-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2009.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2009-07-01 2009-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2009.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2010-01-01 2010-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2010.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2010-07-01 2010-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2010.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2011-01-01 2011-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2011.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2011-07-01 2011-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2011.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2012-01-01 2012-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2012.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2012-07-01 2012-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2012.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2013-01-01 2013-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2013.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2013-07-01 2013-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2013.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2014-01-01 2014-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2014.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2014-07-01 2014-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2014.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2015-01-01 2015-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2015.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2015-07-01 2015-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2015.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2016-01-01 2016-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2016.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2016-07-01 2016-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2016.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2017-01-01 2017-06-30', geo='US', gprop='')
        fst = pytrends.interest_over_time()
        count = count+1
        #print(fst)
        df = pd.DataFrame(fst)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_fsthalf_2017.csv')
        pytrends.build_payload(kw_list, cat=k, timeframe='2017-07-01 2017-12-31', geo='US', gprop='')
        last = pytrends.interest_over_time()
        count = count+1
        #print(last)
        df = pd.DataFrame(last)
        df.to_csv('C:/Users/Hi/Dropbox/Saranya/'+k+'/'+j+'_'+k+'/'+j+'_'+k+'_daily_secondhalf_2017.csv')
        
