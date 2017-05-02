#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

FilePath = "../JData/"
ActionFiles = ["JData_Action_201602.csv", "JData_Action_201603.csv", "JData_Action_201604.csv"]
CommentFile = "JData_Comment.csv"
ProductFile = "JData_Product.csv"
UserFile = "JData_User.csv"
ActionAllFile = "JData_Action_All.csv"

#获取时间段内的行为数据
def get_actions(start_time, end_time):
    """
    :param start_date:
    :param end_date:
    :return: actions: pd.Dataframe
    """
    action_all = pd.read_csv(FilePath + ActionAllFile)
    action_all.time = pd.to_datetime(action_all['time'],format='%Y-%m-%d %H:%M:%S')
    actions = action_all[(action_all.time >= start_time) & (action_all.time <= end_time)]
    return actions

#获取时间段内购买行为的用户和商品对，label设为1
def get_labels(start_time, end_time):
    actions = get_actions(start_time, end_time)
    actions = actions[actions['type'] == 4]
    actions = actions[actions['cate'] == 8]
    actions = actions.groupby(['user_id', 'sku_id'], as_index=False).sum()
    actions['label'] = 1
    actions = actions[['user_id', 'sku_id', 'label']]
    return actions

if __name__ == '__main__':
    STARTdt_str = '2016-04-10'
    ENDdt_str = '2016-04-15'
    start_date = pd.to_datetime(STARTdt_str + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')
    end_date = pd.to_datetime(ENDdt_str + ' 23:59:59', format='%Y-%m-%d %H:%M:%S')
    labels = get_labels(start_date,end_date)
    print labels.shape