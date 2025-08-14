import __main__
import configparser
import pandas as pd
import csv
from tkinter import filedialog
import os
from datetime import datetime as dt
from etc import common
import openpyxl
from openpyxl.styles import PatternFill
import inspect

myEnv = common.env_setting[os.path.basename(__main__.__file__)]
mapping = configparser.ConfigParser()
edit = configparser.ConfigParser()
mapping.read(str(myEnv['mapping_path']).replace("{base}",os.path.dirname(__main__.__file__)))
edit.read(str(myEnv['edit_path']).replace("{base}",os.path.dirname(__main__.__file__)))

def create_base_path(param):
    
    # log出力先ファイルを取得
    myEnv['log_name'] = common.log_files[param['mode']]
    wb = openpyxl.load_workbook(os.path.join(str(myEnv['log_path']).replace("{base}",os.path.dirname(__main__.__file__)),str(myEnv['log_name'])))
    
    base_path = str(myEnv['export_path']).replace("{campaign_id}",str(param['campaign_id']))
    if not(os.path.isdir(base_path)):
        os.makedirs(base_path)
    
    # log出力先ファイルをコピー
    myEnv['log_name'] = str(myEnv['log_name']).replace(".xlsx",f"_{dt.now().strftime('%Y%m%d%H%M%S')}.xlsx")
    wb.save(os.path.join(base_path,myEnv['log_name']))

def output_log(param,level,msg):

    base_path = str(myEnv['export_path']).replace("{campaign_id}",str(param['campaign_id']))
    wb = openpyxl.load_workbook(os.path.join(base_path,str(myEnv['log_name'])))
    ws = wb[str(myEnv['sheet_name'])]
    
    last_row = ws.max_row   # 最終行を取得
    if level == 1:
        ws.cell(row=last_row+1,column=2).value = "情報"
        ws.cell(row=last_row+1,column=3).value = f"{inspect.stack()[1].function}:{inspect.stack()[1].lineno}"
        ws.cell(row=last_row+1,column=4).value = msg
    elif level == 2:
        ws.cell(row=last_row+1,column=2).value = "注意"
        ws.cell(row=last_row+1,column=3).value = f"{inspect.stack()[1].function}:{inspect.stack()[1].lineno}"
        ws.cell(row=last_row+1,column=4).value = msg
    elif level == 3:
        ws.cell(row=last_row+1,column=2).value = "警告"
        ws.cell(row=last_row+1,column=3).value = f"{inspect.stack()[1].function}:{inspect.stack()[1].lineno}"
        ws.cell(row=last_row+1,column=4).value = msg
    
    # ログの保存
    wb.save(os.path.join(base_path,str(myEnv['log_name'])))

def read_folders():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    if iDirPath != '':
        return iDirPath
    else:
        return None

def read_files(formats,path):

    output_log(formats,1,f"ファイル読み込み開始：{path}")

    # 指定したフォルダ直下に存在するファイル名をすべて取得
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    output_log(formats,1,f"ファイル読み込み完了：{files}")
    
    return files

def set_param(formats,df:pd):
    
    output_log(formats,1,f"パラメータ設定開始")
    
    if str(formats['mode']).split('@')[1] != 'プロモコード':
        col_cnt = df.shape[1]
        new_col = ['column' + str(i) for i in range(col_cnt)]
        df.columns = new_col
        output_log(formats,1,f"元データのカラム名変更：{new_col}")

    if formats['campaign_id'] != "":
        df['campaign_id'] = formats['campaign_id']
        output_log(formats,1,f"キャンペーンID設定完了：{formats['campaign_id']}")
    if formats['rewardname_description'] != "":
        df['rewardname_description'] = formats['rewardname_description']
        output_log(formats,1,f"特典説明の設定完了：{formats['rewardname_description']}")
    if formats['useby_date'] != "":
        df['useby_date'] = formats['useby_date']
        output_log(formats,1,f"特典有効期限の設定完了：{formats['useby_date']}")
    
    output_log(formats,1,f"パラメータ設定完了")
    
def move_data(formats,mapping_rule,df:pd):

    output_log(formats,1,f"データ移行開始")
    
    # [mapping.ini]の設定に従って、データを移行
    if(not(mapping.has_section(mapping_rule))):
        output_log(formats,2,f"「mapping.ini」にセクション名なし：{mapping_rule}")
        return
    output_log(formats,1,f"セクション名：{mapping_rule}")
    
    src_col=mapping[mapping_rule]['src']
    format=mapping[mapping_rule]['format']
    dtype=mapping[mapping_rule]['dtype']
    output_log(formats,1,f"移行元カラム：{src_col}／データ型：{dtype}／データ形式：{format}")

    if(dtype=='str'):
        df_dest = df[src_col]
    elif(dtype=='datetime'):
        df_dest = [s.strftime(format) for s in pd.to_datetime(df[src_col])]
    
    output_log(formats,1,f"データ移行完了")
    return df_dest

def format_data(formats,edit_rule,df:pd.DataFrame):

    output_log(formats,1,f"データの編集開始")
    
    # [edit.ini]に該当セクションがあるかを確認
    if edit.has_section(edit_rule):
        
        output_log(formats,1,f"セクション名：{edit_rule}")        
        
        colname=edit[edit_rule]['col']
        add=edit[edit_rule]['add']
        substi=pd.DataFrame(data=eval(edit[edit_rule]['substi']))
        output_log(formats,1,f"対象カラム名：{colname}／追加文字：{add}／置換文字：{substi}")
    
        if add != 'none':
            pass
            output_log(formats,1,f"文字列の追加完了　対象カラム名:{colname}／追加文字:{add}")

        if not(substi.empty):
            for d in substi.values:
                df = [str(strdf).replace(d[0],d[1]) for strdf in df]
                output_log(formats,1,f"文字列の置換完了　対象カラム名：{colname}／置換文字:{d[0]} → {d[1]}")
    else:
        output_log(formats,2,f"「edit.ini」にセクション名なし：{edit_rule}")

    
    # for r in range(df.shape[0]):
    #     for c in range(df.shape[1]):
    #         if df.columns[c] == 'MaxLimit' and df.columns[c]:
    #             df[r][c] = df[r][c]
    
    # output_log(formats,1,f"特典名の利用回数の追記完了")

    print(df)
    # データフレーム内の全値の（先頭・末尾）の空白を削除
    df = pd.DataFrame([df.loc[i].str.strip() for i in range(df.shape[0])])
    output_log(formats,1,f"全データの先頭・末尾の空白削除完了")
    
    output_log(formats,1,f"データの編集完了")
    return df

def shuffle_date(formats,df:pd):
    
    output_log(formats,1,f"特典のシャッフル開始")
    df = df.sample(frac=1,ignore_index=True)
    output_log(formats,1,f"特典のシャッフル完了")
    return df

def export_data(formats,df:pd,filename):
    
    output_log(formats,1,f"特典のcsv出力開始")

    # 出力先のフォルダを指定
    src_dir = str(myEnv['src_path']).replace("{campaign_id}",formats['campaign_id'])
    upload_dir = str(myEnv['upload_path']).replace("{campaign_id}",formats['campaign_id'])
    
    if not(os.path.isdir(src_dir)):
        os.makedirs(src_dir)
        output_log(formats,1,f"元データ保存先のパス作成{src_dir}")

    if not(os.path.isdir(upload_dir)):
        os.makedirs(upload_dir)
        output_log(formats,1,f"出力先のパス作成{upload_dir}")

    # csv形式で出力する
    # 出力形式は「UTF-8」、ダブルクォートは最小限
    dest_filename = str(myEnv['export_file']).replace("{filename}",filename)
    df.to_csv(os.path.join(upload_dir,dest_filename),index=False,encoding="utf-8",quoting=0)
    output_log(formats,1,f"特典のcsv出力完了／出力先フォルダ：{upload_dir}／ファイル名：{dest_filename}")
    