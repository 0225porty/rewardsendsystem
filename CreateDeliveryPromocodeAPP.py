import configparser
import pandas as pd
import etc.settings as myrules
import lib.data_process as myfunc
import tkinter as tk
from tkinter import ttk
import os,sys
import datetime

target = 'promocode'
mapping = configparser.ConfigParser()
mapping.read('D:\develop\django\project\python\etc\mapping.ini')

class CreateDeliveryPromocodeAPP(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        master.geometry("600x400")
        master.title("Delivery_promocodes作成ツール")
        s = ttk.Style()
        s.theme_use('default')

        # GUI画面の各項目
        self.tilte_lb_01 = tk.Label(master,text="■特典が保存されているフォルダを選択してください。")
        self.tilte_lb_02 = tk.Label(master,text="■パラメータを指定してください。")
        self.folder_lb = tk.Label(master,text="対象パス")
        self.folder_entry = tk.Entry(master,width=40,state='readonly')
        self.folder_button = tk.Button(master,text="参照",command=self.selected_dirpath)
        self.cpid_lb = tk.Label(master,text="キャンペーンID")
        self.cpid_entry = tk.Entry(master,width=40)
        self.description_lb = tk.Label(master,text="特典の説明")
        self.description_entry = tk.Entry(master,width=40)
        self.valid_lb = tk.Label(master,text="有効期限")
        self.valid_bikou = tk.Label(master,text="(形式：YYYY-MM-DD)")
        self.valid_entry = tk.Entry(master,width=40)
        self.sent_type_lb = tk.Label(master,text="配信種別")
        self.sent_type_combo = ttk.Combobox(master,values=myrules.sent_type_option,textvariable=tk.StringVar,width=38,state="readonly")
        self.sent_type_combo.bind("<<ComboboxSelected>>",self.update_combo_reward_type)
        self.reward_type_lb = tk.Label(master,text="特典種別")
        self.reward_type_combo = ttk.Combobox(master,textvariable=tk.StringVar,width=38,state="readonly")
        self.reward_type_combo.bind("<<ComboboxSelected>>",self.switching_entry)
        self.main_func = tk.Button(master,text='Start',width=40,command=self.main)

        ## GUI画面に各項目を配置 ##
        # ラベル
        self.tilte_lb_01.grid(myrules.grid_param["title"],row=0)
        self.folder_lb.grid(myrules.grid_param["left"],row=1)
        self.folder_button.grid(myrules.grid_param["right"],row=1)
        self.tilte_lb_02.grid(myrules.grid_param["title"],row=2)
        self.cpid_lb.grid(myrules.grid_param["left"],row=3)
        self.description_lb.grid(myrules.grid_param["left"],row=4)
        self.sent_type_lb.grid(myrules.grid_param["left"],row=5)
        self.reward_type_lb.grid(myrules.grid_param["left"],row=6)
        
        # 設定項目
        self.folder_entry.grid(myrules.grid_param["center"],row=1)
        self.cpid_entry.grid(myrules.grid_param["center"],row=3)
        self.description_entry.grid(myrules.grid_param["center"],row=4)
        self.sent_type_combo.grid(myrules.grid_param["center"],row=5)
        self.reward_type_combo.grid(myrules.grid_param["center"],row=6)
        self.main_func.grid(myrules.grid_param["center"],row=9)

    def selected_dirpath(self):
        dirpath: str = myfunc.read_folders()
        if dirpath is not None:
            self.folder_entry.configure(state='normal')
            self.folder_entry.delete(0,tk.END)
            self.folder_entry.insert(tk.END,dirpath)
            self.folder_entry.configure(state='readonly')

    def update_combo_reward_type(self,event):

        ## 配信種別がManual／Voucherによって特典種別の値を切り替える
        selected = self.sent_type_combo.get()
        self.reward_type_combo['values'] = myrules.reward_type_option[selected]
        self.reward_type_combo.set('')  # 初期値をリセット

    def switching_entry(self,event):

        ## 有効期限が不要な特典種別の場合に、入力項目の表示／非表示を切り替える
        selected = self.reward_type_combo.get()
        if selected == 'プロモコード' or selected == 'リマインド配信' or selected == 'auPAY残高還元':
            ## 非表示
            self.valid_lb.grid_forget()
            self.valid_entry.grid_forget()
            self.valid_bikou.grid_forget()
        else:
            ## 表示
            self.valid_lb.grid(myrules.grid_param["left"],row=7)
            self.valid_entry.grid(myrules.grid_param["center"],row=7)
            self.valid_bikou.grid(myrules.grid_param["right"],row=7)
    
    def setting_rule(self,formats):
        
        formats['target'] = target
        formats['src_path'] = self.folder_entry.get()
        formats['date_6'] = datetime.date.today().strftime('%y%m%d')

        type1 = self.sent_type_combo.get()
        type2 = self.reward_type_combo.get()
        str = type1 + "@" + type2
        formats['columns'] = myrules.format_col[str]
        formats['campaign_id'] = self.cpid_entry.get() + '_' + formats['date_6']
        formats['rewardname_description'] = self.description_entry.get()
        formats['sent_type'] = self.sent_type_combo.get()
        formats['reward_type'] = self.reward_type_combo.get()
        formats['useby_date'] = self.valid_entry.get()
        formats['dest_path'] = formats['dest_path'] + formats['campaign_id'] + formats['dirname']
        formats['dest_file'] = formats['prefix'] + formats['campaign_id'] + '.csv'
        
    
    def main(self):

        ### メインの処理 ###
        # 01 元ファイルの読み込み
        fpath = self.folder_entry.get()
        rewards = myfunc.read_files(fpath)

        # 02 特典の作成定義を設定
        formats = myrules.default_rule
        self.setting_rule(formats)

        # 03 出力用ファイルの宣言
        df = pd.DataFrame(columns=formats["columns"])

        # 04 データの移行
        for file in rewards:
            
            df_src = pd.read_csv(os.path.join(fpath,file), sep=',', encoding="UTF-8")
            myfunc.set_param(formats,df_src)

            for col_name in df.columns:
                strValue = formats['target'] + ':' + col_name
                df[col_name] = myfunc.move_data(strValue,df_src)
        
        # 05 データのシャッフル
        df = myfunc.shuffle_date(df)

        # 06 データのエクスポート
        myfunc.export_data(formats,df)
        


if __name__ == "__main__":
    root = tk.Tk()
    root = CreateDeliveryPromocodeAPP(master=root)
    
    #GUI画面の起動
    root.mainloop()