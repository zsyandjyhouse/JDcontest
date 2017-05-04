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

    #获取user基本属性（age,sex...)
def get_basic_user_fea():
    user = pd.read_csv(FilePath+UserFile, encoding='gbk')
    # user['age'] = user['age'].map(convert_age)
    user['age']=user['age'].replace([u'16-25岁',u'26-35岁',u'36-45岁',u'46-55岁',u'56岁以上'],[1,2,3,4,5])
    user=user[((user['age']==1) |
                (user['age']==2) |
                ( user['age']==3) |
                (user['age']==4) |
                (user['age']==5)|
                (user['age']==-1))]
    age_df = pd.get_dummies(user["age"], prefix="age")
    sex_df = pd.get_dummies(user["sex"], prefix="sex")
    user_lv_df = pd.get_dummies(user["user_lv_cd"], prefix="user_lv_cd")
    user = pd.concat([user['user_id'], age_df, sex_df, user_lv_df], axis=1)
    user.to_csv(FilePath + 'user_basic_fea.csv',index=False)
    return user

    #获取时间段内的操作行为个数统计
def get_user_fea_in_action(start_time, end_time,action_data):
    actions=action_data[(action_data['time']>=start_time)&(action_data['time']<=end_time)]
    #actions = get_actions(start_time, end_time)
    df = pd.get_dummies(actions['type'], prefix='type')
    actions = pd.concat([actions['user_id'], df], axis=1)
    actions = actions.groupby(['user_id'], as_index=False).sum()
    # actions['user_action_1_ratio'] = actions['action_4'] / actions['action_1']
    # actions['user_action_2_ratio'] = actions['action_4'] / actions['action_2']
    # actions['user_action_3_ratio'] = actions['action_4'] / actions['action_3']
    # actions['user_action_5_ratio'] = actions['action_4'] / actions['action_5']
    # actions['user_action_6_ratio'] = actions['action_4'] / actions['action_6']
    user_sku_in_action = actions[['user_id','type_1','type_2','type_3','type_4','type_5','type_6']]
    # user_sku_in_action.to_csv(FilePath+'user_dku_in_action.csv',index=False)
    return user_sku_in_action

#统计用户分别对某商品type12/type2的次数
def type1to2(action_before,type1_int,type2_int):
    type12=action_before[(action_before['type']==type1_int)|(action_before['type']==type2_int)]
    type1='type_'+str(type1_int)
    type2='type_'+str(type2_int)
    temp=pd.get_dummies(type12['type'],prefix='type')
    temp=pd.concat([type12[['user_id','sku_id']],temp],axis=1)
    temp=temp.groupby(['user_id','sku_id'],as_index=False).agg('sum')
    temp=temp[(temp[type1]>0)]

    # 操作次数变购比
    type12=temp
    del type12['sku_id']
    type12d2='type'+str(type1_int)+'_d_'+str(type2_int)
    type12=type12.groupby(['user_id'],as_index=False).agg('sum')
    type12[type12d2]=type12[type2]/type12[type1]
    type12=type12[['user_id',type12d2]]

    #操作商品个数变购比
    type12d2_sku=type12d2+'_sku'
    type12_sku=temp
    type12_sku[type1]=type12_sku[type1].apply(lambda x: 1 if x>0 else 0)
    type12_sku[type2]=type12_sku[type2].apply(lambda x: 1 if x>0 else 0)
    type12_sku=type12_sku.groupby(['user_id'],as_index=False).agg('sum')
    type12_sku[type12d2_sku]=type12_sku[type2]/type12_sku[type1]
    type12_sku=type12_sku[['user_id',type12d2_sku]]

    type12=pd.merge(type12,type12_sku,on=['user_id'],how='outer')
    type12=type12[(type12[type12d2]>0)|(type12[type12d2_sku]>0)]
    return type12


#统计用户从第一次看到下单所需的天数
def days(action_before):
    temp=action_before[(action_before.type==4)]
    temp=temp[['user_id','sku_id','time']]
    temp.rename(columns={'time':'time_4'},inplace=True)
    first=action_before[['user_id','sku_id','time']]
    first=first.groupby(['user_id','sku_id'])['time'].min().reset_index()

    temp=pd.merge(temp,first,on=['user_id','sku_id'],how='left')
    
    temp['gap']=temp['time_4']-temp['time']
    temp['gap']=temp['gap'].dt.seconds
    temp=temp[['user_id','gap']]

    temp['count']=1
    temp=temp.groupby(['user_id'],as_index=False).agg('sum')
    #print temp.dtypes
    temp['ava_gap']=temp['gap']/temp['count']
    temp['ava_gap']=temp['ava_gap']/86400
    temp=temp[['user_id','ava_gap']]
    temp=temp[temp['ava_gap']>0]
    return temp
    
#获取全局特征
def get_user_acc(starttime,endtime,action_data):
    action=action_data[(action_data['time']>=starttime)&(action_data['time']<=endtime)]
    #action=get_actions(start,end)
    #购物车变购物比
    type2to4=type1to2(action,2,4)
    #关注变购比
    type5to4=type1to2(action,5,4)
    #点击变购比
    type6to4=type1to2(action,6,4)
    #浏览变购比
    type1to4=type1to2(action,1,4)
    
    res=type1to4
    res=pd.merge(res,type2to4,on=['user_id'],how='outer')
    res=pd.merge(res,type5to4,on=['user_id'],how='outer')
    res=pd.merge(res,type6to4,on=['user_id'],how='outer')
    res.fillna(0,inplace=True)
    #print res.dtypes
    #type1256变购比
    res['type1256to4']=res['type1_d_4']+res['type2_d_4']+res['type5_d_4']+res['type6_d_4']
    res['type1256to4']=res['type1256to4']/4.0
    res['type1256to4_sku']=res['type1_d_4_sku']+res['type2_d_4_sku']+res['type5_d_4_sku']+res['type6_d_4_sku']
    res['type1256to4_sku']=res['type1256to4_sku']/4.0
    #用户购买所需天数
    user_gap_ava=days(action)
    res=pd.merge(res,user_gap_ava,on=['user_id'],how='outer')
    res.fillna(0,inplace=True)
    return res


#main
def gen_user_fea(start_time, end_time,action_data):
    user_basic_fea = get_basic_user_fea()

    #局部特征
    #获取时间段内的操作行为个数统计
    user_fea_in_action = get_user_fea_in_action(start_time, end_time,action_data)
    user_fea = pd.merge(user_fea_in_action, user_basic_fea, on='user_id', how='left')
    
    #print user_fea
    # user_fea_file = "user_fea_" + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # user_fea.to_csv(FilePath + user_fea_file, index=False)

    #全局特征
    #start='2016-01-31'
    #start = pd.to_datetime(start + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')
    #end=end_time
    #user_acc=get_user_acc(start,end,action_data)
    #user_fea=pd.merge(user_fea,user_acc,on=['user_id'],how='left')
    user_fea.fillna(0, inplace=True)
    print user_fea.dtypes

    return user_fea

if __name__ == '__main__':
    STARTdt_str = '2016-03-31'
    ENDdt_str = '2016-04-01'

    STARTtime = pd.to_datetime(STARTdt_str + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')
    ENDtime = pd.to_datetime(ENDdt_str + ' 23:59:59', format='%Y-%m-%d %H:%M:%S')

    user_fea = gen_user_fea(STARTtime,ENDtime)

