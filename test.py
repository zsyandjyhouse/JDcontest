#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np

FilePath = "../JData/"
ActionAllFile = "JData_Action_All.csv"
action_all = pd.read_csv(FilePath + ActionAllFile)
start_time = '2016-03-27'
end_time = '2016-04-16'
action_all.time = pd.to_datetime(action_all['time'],format='%Y-%m-%d %H:%M:%S')
actions = action_all[(action_all.time >= start_time) & (action_all.time <= end_time)]
actions.to_csv('JData_Action_before_327.csv',index=None)