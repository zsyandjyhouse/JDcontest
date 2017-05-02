#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pandas import Series,DataFrame
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

FilePath = "../JData/"
ActionFiles = ["JData_Action_201602.csv", "JData_Action_201603.csv",  "JData_Action_201604.csv"]
CommentFile = "JData_Comment.csv"
ProductFile = "JData_Product.csv"
UserFile = "JData_User.csv"
ActionAllFile = "JData_Action_All.csv"

def make_action_all():
    action_1 = pd.read_csv(FilePath + ActionFiles[0]).drop_duplicates()
    action_2 = pd.read_csv(FilePath + ActionFiles[1]).drop_duplicates()
    action_3 = pd.read_csv(FilePath + ActionFiles[2]).drop_duplicates()
    action_all = pd.concat([action_1, action_2, action_3]).drop_duplicates()
    action_all.to_csv(FilePath+ActionAllFile,index=False)

if __name__ == '__main__':
    make_action_all()