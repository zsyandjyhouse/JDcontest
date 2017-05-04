#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pandas import Series,DataFrame
import pandas as pd
import sys
reload(sys)

FilePath = "../JData/"
resultFile = "xgb_preds_0426.csv"
submitFile = "submit_0426.csv"

def submit(xgb_preds,value):
    result = xgb_preds[xgb_preds.label >= value]
    submit = result.groupby(['user_id'],as_index = False).last()
    submit = submit[['user_id','sku_id']]
    return submit