#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from requests import Session

class IGService:
    
    D_BASE_URL = {
        'live': 'https://api.ig.com/gateway/deal',
        'demo': 'https://demo-api.ig.com/gateway/deal'
    }

    HEADERS = {}
    API_KEY = None
    IG_USERNAME = None
    IG_PASSWORD = None
    CLIENT_TOKEN = None
    SECURITY_TOKEN = None
    session = None

    
    def __init__(self, username, password, api_key, acc_type):
        """Constructor, calls the method required to connect to the API (accepts acc_type = LIVE or DEMO)"""
        self.API_KEY = api_key
        self.IG_USERNAME = username
        self.IG_PASSWORD = password
        self.BASE_URL = self.D_BASE_URL[acc_type.lower()]
        
        self.HEADERS['BASIC'] = {
            'X-IG-API-KEY': self.API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json; charset=UTF-8'
        }
                                        
        self.parse_response = self.parse_response_with_exception
                
                
    def parse_response_with_exception(self, *args, **kwargs):
        """ *args will give you all function parameters as a tuple:
            **kwargs will give you all keyword arguments except for those corresponding to a formal parameter as a dictionary.
            http://stackoverflow.com/questions/36901/what-does-double-star-and-star-do-for-parameters
        """
        
        """Parses JSON respons  returns dict
        exception raised when error occurs"""
        response = json.loads(*args, **kwargs)
        if 'errorCode' in response:
            raise(Exception(response['errorCode']))
        return(response)   
              
        
    def create_session(self):
        """Creates a trading session, obtaining session tokens for subsequent API access"""
        params = { 
            'identifier': self.IG_USERNAME, 
            'password': self.IG_PASSWORD 
        }

        response = requests.post(self.BASE_URL  + '/session', data=json.dumps(params), headers=self.HEADERS['BASIC'])
        self._set_headers(response.headers, True)
        data = self.parse_response(response.text)
        self.session = Session()
        return(data)
                
    def _set_headers(self, response_headers, update_cst):
        """Sets headers"""
        if update_cst == True:
            self.CLIENT_TOKEN = response_headers['CST']

        if 'X-SECURITY-TOKEN' in response_headers:
            self.SECURITY_TOKEN = response_headers['X-SECURITY-TOKEN']
        else:
            self.SECURITY_TOKEN = None

        self.HEADERS['LOGGED_IN'] = {
            'X-IG-API-KEY': self.API_KEY,
            'X-SECURITY-TOKEN': self.SECURITY_TOKEN,
            'CST': self.CLIENT_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json; charset=UTF-8'
        }

        self.HEADERS['DELETE'] = {
            'X-IG-API-KEY': self.API_KEY,
            'X-SECURITY-TOKEN': self.SECURITY_TOKEN,
            'CST': self.CLIENT_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json; charset=UTF-8',
            '_method': 'DELETE'
        }
        
    def fetch_accounts(self):
        """Returns a list of accounts belonging to the logged-in client"""
        response = self.session.get(self.BASE_URL + '/accounts', headers=self.HEADERS['LOGGED_IN'])
        return self.parse_response(response.text)
        

    def fetch_transaction_history(self, trans_type, start_date, end_date):
        
        url_params = {
            'trans_type': trans_type,
            'start_date': start_date,
            'end_date': end_date
        }
        
        url = self.BASE_URL + '/history/transactions/{trans_type}/{start_date}/{end_date}'.format(**url_params)
        response = self.session.get(url, headers=self.HEADERS['LOGGED_IN'])    
        return self.parse_response(response.text)
        

    def search_trade_ID(self, search_term):

        params = {
            'searchTerm': search_term
        }
        
        url = self.BASE_URL + '/markets?searchTerm={searchTerm}'.format(**params)
        response = self.session.get(url, headers=self.HEADERS['LOGGED_IN']) 
        return self.parse_response(response.text)

    def check_histoical_price(self,epic_id,resolution,start_date,end_date):
        
        params = {
            'epic_id':epic_id,
            'resolution': resolution,
            'start_date':start_date,
            'end_date':end_date
        }
        
        url = self.BASE_URL + '/prices/{epic_id}?resolution={resolution}&from={start_date}&to={end_date}'.format(**params)

        # change the API version to 3 in order to make it run
        self.HEADERS['LOGGED_IN']['Version'] = str(3)
        response = self.session.get(url, headers=self.HEADERS['LOGGED_IN']) 
        return self.parse_response(response.text)
        
        