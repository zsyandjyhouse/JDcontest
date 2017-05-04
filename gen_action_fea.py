#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import pandas as pd
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

# #获取时间段内的行为数据
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

#获取时间段内的行为数据user,sku,actioncount
def get_action_feat(start_time, end_time,action_data):
    actions=action_data[(action_data['time']>=start_time)&(action_data['time']<=end_time)]
    #actions = get_actions(start_time, end_time)
    #actions = actions[actions['cate'] == 8]
    actions = actions[['user_id', 'sku_id', 'type']]
    df = pd.get_dummies(actions['type'], prefix='%s-%s-action' % (start_time, end_time))
    actions = pd.concat([actions, df], axis=1)  # type: pd.DataFrame
    actions = actions.groupby(['user_id', 'sku_id'], as_index=False).sum()
    
    actions.fillna(0,inplace=True)
    name='%s-%s-action' % (start_time, end_time)
    actions[name+'_1256']=actions[name+'_1']+actions[name+'_2']+actions[name+'_5']+actions[name+'_6']
    actions[name+'_1256_d_4']=actions[name+'_4']/actions[name+'_1256']

    del actions['type']
    # action_fea_file = 'action_fea_' + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # action_fea.to_csv(FilePath + action_fea_file, index=False)
    return actions

#计算时间段内每一天行为乘上权重因子的特征
def get_accumulate_action_feat(start_time, end_time,action_data):
    actions=action_data[(action_data['time']>=start_time)&(action_data['time']<=end_time)]
    action_data['time'] = pd.to_datetime(action_data['time'],format='%Y-%m-%d %H:%M:%S')
    df = pd.get_dummies(actions['type'], prefix='action')
    actions = pd.concat([actions, df], axis=1) # type: pd.DataFrame
    #近期行为按时间衰减
    actions['weights'] = actions['time'].map(lambda x: pd.to_timedelta(end_time-x))
    #actions['weights'] = time.strptime(end_date, '%Y-%m-%d') - actions['datetime']
    actions['weights'] = actions['weights'].map(lambda x: math.exp(-x.days))
    print actions.head(10)
    actions['action_1'] = actions['action_1'] * actions['weights']
    actions['action_2'] = actions['action_2'] * actions['weights']
    actions['action_3'] = actions['action_3'] * actions['weights']
    actions['action_4'] = actions['action_4'] * actions['weights']
    actions['action_5'] = actions['action_5'] * actions['weights']
    actions['action_6'] = actions['action_6'] * actions['weights']
    del actions['model_id']
    del actions['time']
    del actions['weights']
    del actions['cate']
    del actions['brand']
    actions = actions.groupby(['user_id', 'sku_id'], as_index=False).sum()
    actions.fillna(0,inplace=True)

    actions['action_1256']=actions['action_1']+actions['action_2']+actions['action_5']+actions['action_6']
    actions['action_1256_d_4']=actions['action_4']/actions['action_1256']
    del actions['type']
    return actions

if __name__ == '__main__':
    STARTdt_str = '2016-03-01'
    ENDdt_str = '2016-03-01'
    STARTdt = pd.to_datetime(STARTdt_str, format='%Y-%m-%d')
    ENDdt = pd.to_datetime(ENDdt_str, format='%Y-%m-%d')
    STARTtime = pd.to_datetime(STARTdt_str + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')
    ENDtime = pd.to_datetime(ENDdt_str + ' 23:59:59', format='%Y-%m-%d %H:%M:%S')

    action_fea = get_action_feat(STARTtime,ENDtime)
    print action_fea
    print action_fea.dtypes
    action_fea_file = 'action_fea_'+STARTdt_str + 'to'+ENDdt_str + '.csv'
    action_fea.to_csv(FilePath+action_fea_file,index=False)