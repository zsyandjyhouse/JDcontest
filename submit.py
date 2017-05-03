#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pandas import Series,DataFrame
import pandas as pd
import sys
reload(sys)
def submit(xgb_preds,value):
    result = xgb_preds[xgb_preds.label >= value]
    submit = result.groupby(['user_id'],as_index = False).last()
    submit = submit[['user_id','sku_id']]
    return submit

FilePath = "../JData/"
resultFile = FilePath+"xgb_preds_2016-04-05to2016-04-15.csv"
submitFile = FilePath+"submit_0503.csv"
xgb_preds=pd.read_csv(resultFile)
res=submit(xgb_preds,0.77)
res=res.astype(int)
print res.shape
res.to_csv(submitFile,index=None,encoding='utf-8')
