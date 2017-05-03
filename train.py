#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def train_and_predict(train_set,train_label,preds,predict_set):
    FilePath = "../JData/"
    train_set = train_set.values
    predict_set = predict_set.values
    train_set = xgb.DMatrix(train_set,label=train_label)
    predict_set = xgb.DMatrix(predict_set)

    params={'booster':'gbtree',
            'objective': 'rank:pairwise',
            'eval_metric':'auc',
            'gamma':0.1,
            'min_child_weight':1.1,
            'max_depth':5,
            'lambda':10,
            'subsample':0.7,
            'colsample_bytree':0.7,
            'colsample_bylevel':0.7,
            'eta': 0.01,
            'tree_method':'exact',
            'seed':0
            }

    model = xgb.train(params,train_set,num_boost_round=3500)
    preds['label'] = model.predict(predict_set)
    preds.label = MinMaxScaler().fit_transform(preds.label)
    #preds.to_csv("xgb_preds.csv",index=None)

    feature_score = model.get_fscore()
    feature_score = sorted(feature_score.items(), key=lambda x:x[1],reverse=True)
    fs = []

    for (key, value) in feature_score:
        fs.append("{0},{1}\n".format(key, value))
    with open(FilePath+'fea_score.csv', 'w') as f:
        f.writelines("feature,score\n")
        f.writelines(fs)
    return preds