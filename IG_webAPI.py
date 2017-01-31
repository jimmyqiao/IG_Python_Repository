#!/usr/bin/env python
# -*- coding: utf-8 -*-


from IG_API_Library import IGService
import pandas as pd
import matplotlib.pyplot as plotlib

ig_service = IGService("user", "pass", "api key","demo")

ig_service.create_session()

account_response = ig_service.fetch_accounts()

accounts_info = {
    'account status': str(account_response['accounts'][0]['status']),
    'fund':account_response['accounts'][0]['balance']['available'],
    'balance':account_response['accounts'][0]['balance']['deposit'],
    'deposit':account_response['accounts'][0]['balance']['profitLoss'],
}

response = ig_service.fetch_transaction_history('ALL_DEAL','01-01-2014', '18-11-2017')

trading_data=[]
for i in response['transactions']:
    pair_name=i['instrumentName']
    trading_data.append({'trade date': pd.to_datetime(str(i['date']),format='%d/%m/%y'),
                         'trade pair': pair_name,
                         'profit/loss': float(str(i['profitAndLoss'])[2:].replace(',','')),
                         'open Level':i['openLevel'],
                         'close Level':i['closeLevel'],
                         'size':i['size']
                        })
   
trade_df = pd.DataFrame(trading_data)     
trade_df = trade_df.sort_values(by='trade date',ascending=True)

"""
needs to change the search string for this function
response = ig_service.search_trade_ID('usdjpy')
for i in response['markets']:
  print i['epic']
"""

response = ig_service.check_histoical_price('CS.D.USDJPY.CFD.IP','DAY','2016-05-01','2016-05-28')
usdjpy_hist=[]
for i in response['prices']: 
    usdjpy_hist.append({'trade date':pd.to_datetime(str(i['snapshotTime']),format='%Y/%m/%d %H:%M:%S'),
                        'closePrice':float(str(i['closePrice']['ask'])),
                        'TradedVolume': int(i['lastTradedVolume'])
                        })
USDJPY_df=pd.DataFrame(usdjpy_hist)

print USDJPY_df

plotlib.plot(USDJPY_df['trade date'],USDJPY_df['closePrice'],'--')

plotlib.show()


