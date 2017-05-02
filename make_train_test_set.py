#!/usr/bin/python
# -*- coding: UTF-8 -*-
from gen_action_fea import *
from gen_sku_fea import *
from gen_user_fea import *
from make_label import *
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def make_train_set(sku_fea, user_fea, train_start_time, train_end_time, test_start_time, test_end_time):
    start_days = "2016-02-01"
    labels = get_labels(test_start_time, test_end_time)

    # generate 时间窗口
    # actions = get_accumulate_action_feat(train_start_date, train_end_date)
    actions = None
    for i in (1, 2, 3, 5, 7, 10, 15, 21, 30):
        start_time = train_end_time - pd.to_timedelta(str(i)+' days')
        if actions is None:
            actions = get_action_feat(start_time, train_end_time)
        else:
            actions = pd.merge(actions, get_action_feat(start_time, train_end_time), how='left',
                               on=['user_id', 'sku_id'])

    actions = pd.merge(actions, user_fea, how='left', on='user_id')
    actions = pd.merge(actions, sku_fea, how='left', on='sku_id')
    actions = pd.merge(actions, labels, how='left', on=['user_id', 'sku_id'])
    actions = actions.fillna(0)
    actions = actions[actions['cate'] == 8]

    user_sku_pair = actions[['user_id', 'sku_id']].copy()
    labels = actions['label'].copy()
    del actions['user_id']
    del actions['sku_id']
    del actions['label']
    # train_set_file = "train_set_" + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # actions.to_csv(FilePath + train_set_file, index=False)
    return user_sku_pair, actions, labels

def make_test_set(sku_fea, user_fea, train_start_date, train_end_time):
    start_days = "2016-02-01"
    # generate 时间窗口
    # actions = get_accumulate_action_feat(train_start_date, train_end_date)
    actions = None
    for i in (1, 2, 3, 5, 7, 10, 15, 21, 30):
        start_time = train_end_time - pd.to_timedelta(str(i)+' days')
        if actions is None:
            actions = get_action_feat(start_time, train_end_time)
        else:
            actions = pd.merge(actions, get_action_feat(start_time, train_end_time), how='left',
                               on=['user_id', 'sku_id'])

    actions = pd.merge(actions, user_fea, how='left', on='user_id')
    actions = pd.merge(actions, sku_fea, how='left', on='sku_id')
    actions = actions.fillna(0)
    actions = actions[actions['cate'] == 8]

    user_sku_pair = actions[['user_id', 'sku_id']].copy()
    del actions['user_id']
    del actions['sku_id']
    # test_set_file = "train_set_" + STARTdt_str + 'to' + ENDdt_str + '.csv'
    # actions.to_csv(FilePath + test_set_file, index=False)
    return user_sku_pair, actions