#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import sys
from get_actions import *
reload(sys)
sys.setdefaultencoding('utf-8')

FilePath = "../JData/"
ActionFiles = ["JData_Action_201602.csv", "JData_Action_201603.csv", "JData_Action_201604.csv"]
CommentFile = "JData_Comment.csv"
ProductFile = "JData_Product.csv"
UserFile = "JData_User.csv"
ActionAllFile = "JData_Action_All.csv"
ProductBasicFeaFile = "JData_Product_Basic_Fea.csv"
skuFeaInCommentFile = "sku_fea_in_comment_ultimate.csv"

#获取时间段内的行为数据
# def get_actions(start_time, end_time):
#     """
#     :param start_date:
#     :param end_date:
#     :return: actions: pd.Dataframe
#     """
#     action_all = pd.read_csv(FilePath + ActionAllFile)
#     action_all.time = pd.to_datetime(action_all['time'],format='%Y-%m-%d %H:%M:%S')
#     actions = action_all[(action_all.time >= start_time) & (action_all.time <= end_time)]
#     return actions

def convert_age(age_str):
    if age_str == u'-1':
        return 0
    elif age_str == u'15岁以下':
        return 1
    elif age_str == u'16-25岁':
        return 2
    elif age_str == u'26-35岁':
        return 3
    elif age_str == u'36-45岁':
        return 4
    elif age_str == u'46-55岁':
        return 5
    elif age_str == u'56岁以上':
        return 6
    else:
        return -1

def get_basic_user_fea():
    user = pd.read_csv(FilePath+UserFile, encoding='gbk')
    user['age'] = user['age'].map(convert_age)
    age_df = pd.get_dummies(user["age"], prefix="age")
    sex_df = pd.get_dummies(user["sex"], prefix="sex")
    user_lv_df = pd.get_dummies(user["user_lv_cd"], prefix="user_lv_cd")
    user = pd.concat([user['user_id'], age_df, sex_df, user_lv_df], axis=1)
    user.to_csv(FilePath + 'user_basic_fea.csv',index=False)
    return user

def get_user_fea_in_action(start_time, end_time):
    actions = get_actions(start_time, end_time)
    df = pd.get_dummies(actions['type'], prefix='type')
    actions = pd.concat([actions['user_id'], df], axis=1)
    actions = actions.groupby(['user_id'], as_index=False).sum()
    # actions['user_action_1_ratio'] = actions['action_4'] / actions['action_1']
    # actions['user_action_2_ratio'] = actions['action_4'] / actions['action_2']
    # actions['user_action_3_ratio'] = actions['action_4'] / actions['action_3']
    # actions['user_action_5_ratio'] = actions['action_4'] / actions['action_5']
    # actions['user_action_6_ratio'] = actions['action_4'] / actions['action_6']
    print actions
    user_sku_in_action = actions[['user_id','type_1','type_2','type_3','type_4','type_5','type_6']]
    # user_sku_in_action.to_csv(FilePath+'user_dku_in_action.csv',index=False)
    return user_sku_in_action

def gen_user_fea(start_time, end_time):
    user_basic_fea = get_basic_user_fea()
    user_fea_in_action = get_user_fea_in_action(start_time, end_time)
    user_fea = pd.merge(user_fea_in_action, user_basic_fea, on='user_id', how='left')
    user_fea.fillna(0, inplace=True)
    # user_fea_file = "user_fea_" + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # user_fea.to_csv(FilePath + user_fea_file, index=False)
    return user_fea

if __name__ == '__main__':
    STARTdt_str = '2016-03-01'
    ENDdt_str = '2016-03-01'
    STARTdt = pd.to_datetime(STARTdt_str, format='%Y-%m-%d')
    ENDdt = pd.to_datetime(ENDdt_str, format='%Y-%m-%d')
    STARTtime = pd.to_datetime(STARTdt_str + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')
    ENDtime = pd.to_datetime(ENDdt_str + ' 23:59:59', format='%Y-%m-%d %H:%M:%S')

    user_basic_fea = get_basic_user_fea()
    user_fea_in_action = get_user_fea_in_action(STARTtime, ENDtime)
    user_fea = pd.merge(user_fea_in_action, user_basic_fea, on='user_id',how='left')
    user_fea_file = "sku_fea_"+STARTdt_str+'to'+ENDdt_str+'.csv'
    user_fea.to_csv(FilePath+user_fea_file,index=False)
    user_fea.fillna(0, inplace=True)
    print user_fea
    print user_fea.dtypes

