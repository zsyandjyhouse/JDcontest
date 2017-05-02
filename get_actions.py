#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
#获取时间段内的行为数据

def get_actions(start_time, end_time):
    """
    :param start_date:
    :param end_date:
    :return: actions: pd.Dataframe
    """
    FilePath = "../JData/"
    ActionAllFile = "JData_Action_All.csv"
    action_all = pd.read_csv(FilePath + ActionAllFile)
    action_all.time = pd.to_datetime(action_all['time'],format='%Y-%m-%d %H:%M:%S')
    actions = action_all[(action_all.time >= start_time) & (action_all.time <= end_time)]
    return actions

if __name__ == '__main__':
    print 'get_action'