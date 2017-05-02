#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import sys
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

#获取时间段内的行为数据user,sku,actioncount
def get_action_feat(start_time, end_time):
    actions = get_actions(start_time, end_time)
    actions = actions[['user_id', 'sku_id', 'type']]
    df = pd.get_dummies(actions['type'], prefix='%s-%s-action' % (start_time, end_time))
    actions = pd.concat([actions, df], axis=1)  # type: pd.DataFrame
    actions = actions.groupby(['user_id', 'sku_id'], as_index=False).sum()
    del actions['type']
    # action_fea_file = 'action_fea_' + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # action_fea.to_csv(FilePath + action_fea_file, index=False)
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