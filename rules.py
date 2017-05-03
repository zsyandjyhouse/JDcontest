#!/usr/bin/python
# -*- coding: UTF-8 -*-
from get_actions import *


def addcart_without_buy(start_time,end_time):
    actiondata = get_actions(start_time,end_time)
    actiondata = actiondata[actiondata['cate']==8]
    actiondata = actiondata[(actiondata['type']==4)|(actiondata['type']==2)]
    print actiondata
    df = pd.get_dummies(actiondata['type'], prefix='type')
    actions = pd.concat([actiondata, df], axis=1)
    print actions
    actions.drop(['time', 'model_id', 'brand','type'],inplace=True)
    actions = actions.groupby(['user_id','sku_id','cate'],as_index=False).sum()
    predict_buy = actions[(actions['type_4']==0) &(actions['type_2']!=0)]
    predict_buy = predict_buy[['user_id','sku_id']]
    return predict_buy


def gen_result_with_rules(start_time,end_time):
    predict_buy = addcart_without_buy(start_time,end_time)
    return predict_buy

if __name__ == '__main__':
    end_time = pd.to_datetime('2016-04-15 23:59:59', format='%Y-%m-%d %H:%M:%S')
    start_time = end_time-pd.to_timedelta('1 days')

    predict_buy = gen_result_with_rules(start_time, end_time)
    print predict_buy