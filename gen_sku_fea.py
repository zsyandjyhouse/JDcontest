#!/usr/bin/python
# -*- coding: UTF-8 -*-
from get_actions import *
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

#获得基础商品特征，来自product表里
def get_basic_product_fea():
    product = pd.read_csv(FilePath+ProductFile)
    attr1_df = pd.get_dummies(product["a1"], prefix="a1")
    attr2_df = pd.get_dummies(product["a2"], prefix="a2")
    attr3_df = pd.get_dummies(product["a3"], prefix="a3")
    product = pd.concat([product[['sku_id', 'cate', 'brand']], attr1_df, attr2_df, attr3_df], axis=1)
    product.to_csv(FilePath+ProductBasicFeaFile,index=False)
    return product

# 计算截止enddt之前商品的品论数据
def get_comment_product_fea(endtime):
    enddt = pd.to_datetime(endtime,format = '%Y-%m-%d')
    if enddt == pd.to_datetime('2016-04-15',format = '%Y-%m-%d'):
        commentdata = pd.read_csv(FilePath + CommentFile)
        commentdata = commentdata[(commentdata["dt"] == "2016-04-15")]
        commentdata = commentdata.sort_values(by="sku_id").reset_index()[["sku_id", "comment_num", "has_bad_comment", "bad_comment_rate"]]
        return commentdata
    else:
        startdt = enddt - pd.Timedelta(days=7)
        commentpath = FilePath + CommentFile
        commentdata_ALL = pd.read_csv(commentpath)  # 吧Jdatya_comment.csv全部读出来了
        commentdata_ALL.dt = pd.to_datetime(commentdata_ALL.dt, format='%Y-%m-%d')  # 吧dt列转化成date格式
        comment = commentdata_ALL[(commentdata_ALL.dt <= enddt) & (commentdata_ALL.dt > startdt)]
        df = pd.get_dummies(comment['comment_num'], prefix='comment_num')
        comment = pd.concat([comment, df], axis=1)
        comment = comment[['sku_id', 'has_bad_comment', 'bad_comment_rate', 'comment_num_1', 'comment_num_2', 'comment_num_3','comment_num_4']]
        sorted_comment = comment.sort_values(by=['sku_id']).reset_index().drop('index',1)
        #sorted_comment.to_csv(FilePath + 'skuFeaInComment_before'+str(enddt), index=False)
        return sorted_comment

# # comment数据里每一个商品的最终评论数据，4-15,46545个商品
# def cal_sku_fea_in_comment_ultimate():
#     commentdata = pd.read_csv(FilePath + CommentFile)
#     commentdata = commentdata[(commentdata["dt"] == "2016-04-15")]
#     commentdata = commentdata.sort_values(by="sku_id").reset_index()[
#         ["sku_id", "comment_num", "has_bad_comment", "bad_comment_rate"]]
#     commentdata.to_csv(FilePath + skuFeaInCommentFile, index=False)

# 获得商品的操作数
def get_sku_fea_in_action(starttime, endtime):
    ActionData = get_actions(starttime, endtime)

    skuinActionData = ActionData[['sku_id', 'cate', 'brand']].drop_duplicates()
    skuinActionData = skuinActionData.sort_values(by=['sku_id'])
    skuinActionData = skuinActionData.reset_index().drop('index', 1)

    # 计算action中商品的操作总数
    ActionData_sortbysku = ActionData.sort_values(by=['sku_id'])
    All_ActionSumofSku_id = ActionData_sortbysku.groupby(ActionData_sortbysku['sku_id'], as_index=False).size()
    All_ActionSumofSku_id = All_ActionSumofSku_id.reset_index()
    All_ActionSumofSku_id.columns = ['sku_id', 'All_Action_count']
    skuFeainActionData = pd.merge(skuinActionData, All_ActionSumofSku_id, on='sku_id', how='left')
    skuFeainActionData.fillna(0, inplace=True)

    # 计算商品的所有操作涉及到的用户的数量
    ActionData_sku_user_pair = ActionData[['sku_id', 'user_id']].sort_values(by=['sku_id', 'user_id']).drop_duplicates()
    ActionData_sku_user_pair = ActionData_sku_user_pair.groupby([ActionData_sku_user_pair['sku_id']],
                                                                as_index=False).size()
    ActionData_sku_user_pair = ActionData_sku_user_pair.reset_index()
    ActionData_sku_user_pair.columns = ['sku_id', 'All_Action_user_count']
    skuFeainActionData = pd.merge(skuFeainActionData, ActionData_sku_user_pair, on='sku_id', how='left')
    skuFeainActionData.fillna(0, inplace=True)

    # 计算商品平均每个用户的操作数
    # skuFeainActionData['All_Action_Count_per_user'] = skuFeainActionData['All_Action_count']/skuFeainActionData['All_Action_user_count']

    # 计算商品6种操作对应的操作总数、用户总数、占总操作数占比、占总用户数占比、用户的平均行为数
    for i in range(6):
        # 操作类型为i+1的所有数据
        type_ActionData = ActionData[ActionData.type == (i + 1)]

        # 操作类型为i+1的所有商品
        type_skuinActionData = type_ActionData[['sku_id']].drop_duplicates()
        type_skuinActionData = type_skuinActionData.reset_index()[['sku_id']]
        type_skuinActionData = type_skuinActionData.sort_values(by=['sku_id'])
        type_skuinActionData = type_skuinActionData.reset_index().drop('index', 1)

        # 计算typeactiondata中商品对应的操作总数
        type_ActionData_sortbysku = type_ActionData.sort_values(by=['sku_id'])
        type_ActionSumofSku_id = type_ActionData_sortbysku.groupby(type_ActionData_sortbysku['sku_id'],
                                                                   as_index=False).size()
        type_ActionSumofSku_id = type_ActionSumofSku_id.reset_index()
        type_ActionSumofSku_id.columns = ['sku_id', 'type' + str(i + 1) + '_Action_count']
        skuFeainActionData = pd.merge(skuFeainActionData, type_ActionSumofSku_id, on='sku_id', how='left')
        skuFeainActionData.fillna(0, inplace=True)
        # 计算商品type=i+1操作占总操作数的比例
        # skuFeainActionData['type'+str(i+1)+'_Action_count_in_All_Action'] = skuFeainActionData['type'+str(i+1)+'_Action_count']/skuFeainActionData['All_Action_count']#type=1的行为占行为总数的比例

        # 计算typeactiondata中商品对应的操作涉及用户数
        type_ActionData_sku_user_pair = type_ActionData[['sku_id', 'user_id']].sort_values(
            by=['sku_id', 'user_id']).drop_duplicates()
        type_All_ActionuserSumofSku_id = type_ActionData_sku_user_pair.groupby(
            [type_ActionData_sku_user_pair['sku_id']], as_index=False).size()
        type_All_ActionuserSumofSku_id = type_All_ActionuserSumofSku_id.reset_index()
        type_All_ActionuserSumofSku_id.columns = ['sku_id', 'type' + str(i + 1) + '_Action_user_count']
        skuFeainActionData = pd.merge(skuFeainActionData, type_All_ActionuserSumofSku_id, on='sku_id', how='left')
        skuFeainActionData.fillna(0, inplace=True)
    # skuFeainActionData['type'+str(i+1)+'_Action_user_count_in_All_Action'] = skuFeainActionData['type'+str(i+1)+'_Action_user_count']/skuFeainActionData['All_Action_user_count']#type=1的用户占行为用户总数的比例
    # skuFeainActionData['type'+str(i+1)+'_Action_Count_per_user'] = skuFeainActionData['type'+str(i+1)+'_Action_count']/skuFeainActionData['type'+str(i+1)+'_Action_user_count']#用户平均行为（type=1）数

    skuFeainActionData.fillna(0, inplace=True)
    skuFeainActionData['type1256_Action_count'] = skuFeainActionData['type1_Action_count'] + skuFeainActionData[
        'type2_Action_count'] + skuFeainActionData['type5_Action_count'] + skuFeainActionData['type6_Action_count']
    skuFeainActionData['type1256_Action_user_count'] = skuFeainActionData['type1_Action_user_count'] + \
                                                       skuFeainActionData['type2_Action_user_count'] + \
                                                       skuFeainActionData['type5_Action_user_count'] + \
                                                       skuFeainActionData['type6_Action_user_count']

    # print skuFeainActionData

    # #计算商品点击变购率：总购买数/总点击数，总购买用户/总点击用户
    # skuFeainActionData['buy_click_all'] = skuFeainActionData['type4_Action_count']/skuFeainActionData['type6_Action_count']
    # skuFeainActionData['buy_click_user'] = skuFeainActionData['type4_Action_user_count']/skuFeainActionData['type6_Action_user_count']

    # #计算商品浏览变购率：总购买数/总浏览数，总购买用户/总浏览用户
    # skuFeainActionData['buy_browse_all'] = skuFeainActionData['type4_Action_count']/skuFeainActionData['type1_Action_count']
    # skuFeainActionData['buy_browse_user'] = skuFeainActionData['type4_Action_user_count']/skuFeainActionData['type1_Action_user_count']

    # #计算商品加购物车变购率：总购买数/总点击数，总购买用户/总点击用户
    # skuFeainActionData['buy_add_all'] = skuFeainActionData['type4_Action_count']/skuFeainActionData['type2_Action_count']
    # skuFeainActionData['buy_add_user'] = skuFeainActionData['type4_Action_user_count']/skuFeainActionData['type2_Action_user_count']

    # #计算商品收藏变购率：总购买数/总点击数，总购买用户/总点击用户
    # skuFeainActionData['buy_attention_all'] = skuFeainActionData['type4_Action_count']/skuFeainActionData['type5_Action_count']
    # skuFeainActionData['buy_attention_user'] = skuFeainActionData['type4_Action_user_count']/skuFeainActionData['type5_Action_user_count']


    return skuFeainActionData

# 算的有问题，重算！！！！！！！！！！！！！
# 计算关注变购率:总关注购买数/总关注数~=总关注购买用户数/总关注用户数
def cal_buy_attention_pro():
    attentionData = pd.read_csv(FilePath + 'cleaned_ActionAllType5.csv')
    buyData = pd.read_csv(FilePath + 'cleaned_ActionAllType4.csv')
    attention_user_sku_pair = attentionData[['user_id', 'sku_id']].drop_duplicates()
    buyData = pd.merge(attention_user_sku_pair, buyData, on=['user_id', 'sku_id'], how='left').dropna()
    buy_attention_data = pd.concat([buyData, attentionData]).sort_values(by=['sku_id', 'user_id', 'time'])

    # buy_attention_data.to_csv(FilePath+'buy_attention_data.csv',index=False)
    attention_sku = attentionData['sku_id'].drop_duplicates()  # 被关注的商品集合
    # 计算被关注的商品下单的次数
    sku_buysum = buy_attention_data[buy_attention_data.type == 4]
    sku_buysum = sku_buysum.groupby(sku_buysum['sku_id'], as_index=False).size()
    sku_buysum = sku_buysum.reset_index()
    sku_buysum.columns = ['sku_id', 'numofbuy']
    # 计算被关注的商品被关注的次数
    sku_attsum = buy_attention_data[buy_attention_data.type == 5]
    sku_attsum = sku_attsum.groupby(sku_attsum['sku_id'], as_index=False).size()
    sku_attsum = sku_attsum.reset_index()
    sku_attsum.columns = ['sku_id', 'numofatt']
    # 计算商品的关注变购比：总购买数/总关注数
    buy_attention_pro = pd.merge(sku_attsum, sku_buysum, on='sku_id', how='left')
    buy_attention_pro['buy_attention_pro'] = buy_attention_pro['numofbuy'] / buy_attention_pro['numofatt']
    buy_attention_pro = buy_attention_pro.fillna(0)[['sku_id', 'buy_attention_pro']]

    # print buy_attention_pro#[sku_id,关注变购比]
    return buy_attention_pro

# # 拼接商品特征
# def concat_sku_fea(starttime, endtime, enddt, STARTdt_str, ENDdt_str):
#     skuFeainActionData = getActionNumInActionData(starttime, endtime)
#     skuFeainActionData8 = skuFeainActionData[skuFeainActionData.cate == 8]
#     # buy_attention_pro = cal_buy_attention_pro()
#     proFea = pd.read_csv(FilePath + ProductFile)
#     commentFea = makeComment(enddt)
#     commentFea['has_comment'] = 1
#     # skuFeaInActon = pd.merge(skuFeainActionData,buy_attention_pro,on='sku_id',how='left')
#
#     skuFea = pd.merge(skuFeainActionData8, commentFea, on='sku_id', how='left')
#     skuFea = pd.merge(skuFea, proFea, on=['sku_id', 'cate', 'brand'], how='left')
#     skuFea.fillna(0, inplace=True)
#     skuFea.to_csv(FilePath + 'sku_Fea' + 'from' + STARTdt_str + 'to' + ENDdt_str + '.csv', index=False)

def gen_sku_fea(starttime, endtime):
    sku_basic_fea = get_basic_product_fea()
    sku_fea_in_comment = get_comment_product_fea(endtime)
    sku_fea_in_action = get_sku_fea_in_action(starttime, endtime)
    sku_fea = pd.merge(sku_fea_in_action, sku_fea_in_comment, on='sku_id', how='left')
    sku_fea = pd.merge(sku_fea, sku_basic_fea, on=['sku_id', 'cate', 'brand'], how='left')
    sku_fea.fillna(0, inplace=True)
    # sku_fea_file = "sku_fea_" + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # sku_fea.to_csv(FilePath + sku_fea_file, index=False)
    return sku_fea

if __name__ == '__main__':
    STARTdt_str = '2016-03-01'
    ENDdt_str = '2016-03-01'
    STARTdt = pd.to_datetime(STARTdt_str, format='%Y-%m-%d')
    ENDdt = pd.to_datetime(ENDdt_str, format='%Y-%m-%d')
    STARTtime = pd.to_datetime(STARTdt_str + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')
    ENDtime = pd.to_datetime(ENDdt_str + ' 23:59:59', format='%Y-%m-%d %H:%M:%S')

    sku_basic_fea = get_basic_product_fea()
    sku_fea_in_comment = get_comment_product_fea(ENDdt)
    sku_fea_in_action = get_sku_fea_in_action(STARTtime,ENDtime)
    sku_fea = pd.merge(sku_fea_in_action,sku_fea_in_comment,on='sku_id', how='left')
    sku_fea = pd.merge(sku_fea, sku_basic_fea, on=['sku_id','cate','brand'], how='left')
    sku_fea.fillna(0,inplace=True)
    print sku_fea
    print sku_fea.dtypes
    sku_fea_file = "sku_fea_"+STARTdt_str+'to'+ENDdt_str+'.csv'
    sku_fea.to_csv(FilePath+sku_fea_file,index=False)