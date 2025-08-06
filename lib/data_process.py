import configparser
import pandas as pd
import csv
from tkinter import filedialog
import os,sys
from datetime import datetime as dt

mapping = configparser.ConfigParser()
mapping.read('D:\develop\django\project\python\etc\mapping.ini')

def read_folders():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    if iDirPath != '':
        return iDirPath
    else:
        return None

def read_files(path):

    # 指定したフォルダ直下に存在するファイル名をすべて取得
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]

def set_param(formats,df:pd):
    
    if formats['campaign_id'] is not None:
        df['campaign_id'] = formats['campaign_id']
    if formats['rewardname_description'] is not None:
        df['rewardname_description'] = formats['rewardname_description']
    if formats['useby_date'] is not None:
        df['useby_date'] = formats['useby_date']
    
def move_data(mapping_rule,df:pd):

    # [mapping.ini]の設定に従って、データを移行
    if(not(mapping.has_section(mapping_rule))):
        return
    
    src_col=mapping[mapping_rule]['src']
    format=mapping[mapping_rule]['format']
    dtype=mapping[mapping_rule]['dtype']

    if(dtype=='str'):
        return df[src_col]
    elif(dtype=='datetime'):
        return [s.strftime(format) for s in pd.to_datetime(df[src_col])]

def shuffle_date(df:pd):
    return df.sample(frac=1,ignore_index=True)

def export_data(formats,df:pd):
    
    if not(os.path.isdir(formats['dest_path'])):
        os.makedirs(formats['dest_path'])

    # csv形式で出力する
    # 出力形式は「UTF-8」、ダブルクォートは最小限
    df.to_csv(os.path.join(formats['dest_path'],formats['dest_file']),index=False,encoding="utf-8",quoting=0)
    