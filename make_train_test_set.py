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

def make_fea_set(sku_fea, user_fea, train_start_date, train_end_time):
    start_days = "2016-02-01"
    # generate 时间窗口
    actions = None
    for i in (1, 2, 3, 5, 7):
    #for i in (1, 2, 3, 5, 7, 10, 15, 21, 30):
        start_time = train_end_time - pd.to_timedelta(str(i)+' days')
        if actions is None:
            actions = get_action_feat(start_time, train_end_time)
        else:
            actions = pd.merge(actions, get_action_feat(start_time, train_end_time), how='left',
                               on=['user_id', 'sku_id'])

    actions = pd.merge(actions, user_fea, how='left', on='user_id')
    actions = pd.merge(actions, sku_fea, how='left', on='sku_id')

    actions = actions.fillna(0)
    print 'fea_weidu3',actions.shape
    actions.to_csv('test'+str(train_end_time).split(' ')[0]+'.csv')
    return actions