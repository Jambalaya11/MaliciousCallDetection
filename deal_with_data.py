# coding : utf-8
import os
import csv
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import numpy as np
import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class FeatureExtraction(object):

    def __init__(self, data):
        self.data = data

    def compute_useTime(self):
        '''
        extract useTime from openDate
        useTime : opendate to now
        '''
        self.data["openDate"] = [str(index) for index in self.data["openDate"]]
        self.data["openDate"] = pd.to_datetime(self.data["openDate"])
        now = datetime.datetime(2018, 5, 16)
        self.data["useTime"] = [
            (now-index).days for index in self.data["openDate"]]
        self.data.drop('openDate', 1, inplace=True)

    def deal_with_callTime(self):
        '''
        calltime std,mean
        extract from callTime
        '''
        callTimeGroup = data.groupby(data['calling'])['callTime']
        agg_callTime = callTimeGroup.agg(
            {"meancallTime": np.mean, "stdCallTime": np.std}).reset_index()
        self.data = pd.merge(self.data, agg_callTime, on='calling', how='left')
        self.data.drop('callTime', 1, inplace=True)

    def is_weekDay(self):
        '''
        restDay: holiday: 01-01,05-01
                 weekday: Saturday,Sunday
        workday: except restDay
        extract isRestDay from startTime
        '''
        holiday = ['01-01', '05-01']
        self.data["startTime"] = pd.to_datetime(
            [str(index) for index in self.data["startTime"]])
        month = self.data["startTime"].apply(lambda x: x.month)
        day = self.data["startTime"].apply(lambda x: x.day)
        weekDay = self.data["startTime"].apply(lambda x: x.weekday() + 1)
        isRest = ((weekDay == 6) | (weekDay == 7))
        self.data['isRestDay'] = isRest * 1
        for h in holiday:
            h_month, h_day = h.split('-')
            h_index = ((month == int(h_month)) & (day == int(h_day)))
            self.data.loc[h_index, 'isRestDay'] = 1

    def is_workTime(self):
        '''
        auto define workday 08:00-18:00
        extract isWorkTime from startTime
        '''
        start_hour = 8
        end_hour = 18
        self.data["startTime"] = pd.to_datetime(
            [str(index) for index in data["startTime"]])
        hour = self.data["startTime"].apply(lambda x: x.hour)
        w_time = (hour >= start_hour) & (hour <= end_hour)
        self.data.loc[w_time, 'isWorkTime'] = 1

    def feature_encode(self):
        one_hot_feature = ['planName', 'custCode', 'userType','commiucateType',
                           'sellProduct', 'callingArea', 'calledArea']
        vector_feature = ['useTime', 'meancallTime', 'stdcallTime']
        for feature in one_hot_feature:
            try:
                self.data[feature] = LabelEncoder().fit_transform(
                    res_data[feature].apply(int))
            except:
                self.data[feature] = LabelEncoder(
                ).fit_transform(res_data[feature])
        '''
        enc = OneHotEncoder()
        for feature in one_hot_feature:
            enc.fit(res_data[feature].values.reshape(-1,1))
            one_hot_res_data = enc.transform(res_data[feature].values.reshape(-1,1))
        '''

    def run(self):
        self.compute_useTime()
        self.deal_with_callTime()
        self.is_weekDay()
        self.is_workTime()
        self.data.drop('startTime', 1, inplace=True)
        self.feature_encode()
        self.data = self.data.fillna('-1')
        self.data.to_csv("encoded_label.csv", index=False, sep=',')


def read_bill():
    '''
    revert txt file to csv  file
    '''
    with open(os.path.join(CURRENT_DIR, 'bill.csv', 'w')) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["calling", "called", "chargeCalling", "startTime", "callTime",
                         "cost", "commiucateType", "callType", "talkType", "callingArea", "calledArea"])
        with open(os.path.join(CURRENT_DIR, 'M2test3.txt', 'r')) as f:
            lines = f.readlines()
            data = {}
            for line in lines:
                items = line.strip().split('|')
                calling = items[0]
                called = items[1]
                chargeCalling = items[2]
                startTime = items[3]
                callTime = items[4]
                cost = items[5]
                commiucateType = items[6]
                callType = items[7]
                talkType = items[8]
                callingArea = items[9]
                calledArea = items[10]
                writer.writerow([calling, called, chargeCalling, startTime, callTime,
                                 cost, commiucateType, callType, talkType, callingArea, calledArea])


if __name__ == '__main__':
    '''
    benignCall label : 0
    maliciousCall label : 1
    '''
    benignCall = pd.read_csv(os.path.join(CURRENT_DIR, 'benignCall.csv'))
    benignCall['label'] = 0
    maliciousCall = pd.read_csv(os.path.join(CURRENT_DIR, 'maliciousCall.csv'))
    maliciousCall['label'] = 1
    data = pd.concat([benignCall, maliciousCall])
    # read_bill()
    #data_in = data.copy()
    #data_in.rename(columns={'calling':'called'},inplace = True)
    bill = pd.read_csv(os.path.join(CURRENT_DIR, 'bill.csv'))
    data = pd.merge(bill, data, on='calling', how='left')
    #data_in = pd.merge(bill,data_in,on='called',how='left')
    # data=data.fillna('-1')
    data.to_csv("ori_label.csv", index=False, sep=',')
    res_data = data.copy()
    feature_extraction = FeatureExtraction(res_data)
    feature_extraction.run()
