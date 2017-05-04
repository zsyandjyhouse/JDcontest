#!/usr/bin/python
# -*- coding: UTF-8 -*-
from get_actions import *

FilePath = "../JData/"
ActionFiles = ["JData_Action_201602.csv", "JData_Action_201603.csv", "JData_Action_201604.csv"]

# def addcart_without_buy(start_time,end_time):
#     actiondata = get_actions(start_time,end_time)
#     print actiondata
#     actiondata = actiondata[actiondata['cate']==8]
#     print actiondata
#     actiondata = actiondata[(actiondata['type']==4)|(actiondata['type']==2)]
#     print actiondata
#     df = pd.get_dummies(actiondata['type'], prefix='type')
#     actions = pd.concat([actiondata, df], axis=1)
#     print actions
#     actions.drop(['time', 'model_id', 'brand','type'],inplace=True)
#     actions = actions.groupby(['user_id','sku_id','cate'],as_index=False).sum()
#     predict_buy = actions[(actions['type_4']==0) &(actions['type_2']!=0)]
#     predict_buy = predict_buy[['user_id','sku_id']]
#     return predict_buy


# def gen_result_with_rules(start_time,end_time):
#     predict_buy = addcart_without_buy(start_time,end_time)
#     return predict_buy

# if __name__ == '__main__':
end_time = pd.to_datetime('2016-04-15 23:59:59', format='%Y-%m-%d %H:%M:%S')
start_time = pd.to_datetime('2016-04-15 00:00:00', format='%Y-%m-%d %H:%M:%S')

#     predict_buy = gen_result_with_rules(start_time, end_time)
#     print predict_buy

actiondata = pd.read_csv(FilePath+ActionFiles[2])
actiondata = actiondata[actiondata['cate']==8]
actiondata['time']=pd.to_datetime(actiondata['time'],format='%Y-%m-%d %H:%M:%S')
actiondata = actiondata[(actiondata.time >= start_time) & (actiondata.time <= end_time)]
print actiondata
actiondata = actiondata[(actiondata['type']==4)|(actiondata['type']==2)]
print actiondata
df = pd.get_dummies(actiondata['type'], prefix='type')
actions = pd.concat([actiondata, df], axis=1)
print actions
actions.drop(['time', 'model_id', 'brand','type'],axis=1)
actions = actions.groupby(['user_id','sku_id','cate'],as_index=False).sum()
predict_buy = actions[(actions['type_4']==0) &(actions['type_2']!=0)]
predict_buy = predict_buy[['user_id','sku_id']]
print predict_buy
xgbpredict = pd.read_csv(FilePath+'')
predict_buy = pd.merge(predict_buy,xgbpredict,on=['user_id','sku_id'],how='outer')
predict_buy.to_csv(FilePath+'resultfrom_rules.csv',index=False)