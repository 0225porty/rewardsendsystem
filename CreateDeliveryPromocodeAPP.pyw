import configparser
import pandas as pd
import etc.settings as myrules
import lib.data_process as myfunc
import tkinter as tk
from tkinter import ttk
import os,sys
import datetime
from tkinter import ttk
from etc import common
from tkinter import messagebox

prm = myrules.params[os.path.basename(__file__)]

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
        self.sent_type_combo = ttk.Combobox(master,values=common.sent_type_option,textvariable=tk.StringVar,width=38,state="readonly")
        self.sent_type_combo.bind("<<ComboboxSelected>>",self.update_combo_reward_type)
        self.reward_type_lb = tk.Label(master,text="特典種別")
        self.reward_type_combo = ttk.Combobox(master,textvariable=tk.StringVar,width=38,state="readonly")
        self.reward_type_combo.bind("<<ComboboxSelected>>",self.switching_entry)
        self.main_func = tk.Button(master,text='Start',width=40,command=self.main)

        ## GUI画面に各項目を配置 ##
        # ラベル
        self.tilte_lb_01.grid(common.grid_param["title"],row=0)
        self.folder_lb.grid(common.grid_param["left"],row=1)
        self.folder_button.grid(common.grid_param["right"],row=1)
        self.tilte_lb_02.grid(common.grid_param["title"],row=2)
        self.sent_type_lb.grid(common.grid_param["left"],row=3)
        self.reward_type_lb.grid(common.grid_param["left"],row=4)
        self.cpid_lb.grid(common.grid_param["left"],row=5)
        self.description_lb.grid(common.grid_param["left"],row=6)
        
        # 設定項目
        self.folder_entry.grid(common.grid_param["center"],row=1)
        self.sent_type_combo.grid(common.grid_param["center"],row=3)
        self.reward_type_combo.grid(common.grid_param["center"],row=4)
        self.cpid_entry.grid(common.grid_param["center"],row=5)
        self.description_entry.grid(common.grid_param["center"],row=6)
        self.main_func.grid(common.grid_param["center"],row=9)

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
        self.reward_type_combo['values'] = common.reward_type_option[selected]
        self.reward_type_combo.set('')  # 初期値をリセット

        if selected == 'Manual':
            self.cpid_lb.grid(common.grid_param["left"],row=5)
            self.cpid_entry.grid(common.grid_param["center"],row=5)
            self.description_lb.grid(common.grid_param["left"],row=6)
            self.description_entry.grid(common.grid_param["center"],row=6)
        else:
            self.cpid_lb.grid_forget()
            self.cpid_entry.grid_forget()
            self.description_lb.grid_forget()
            self.description_entry.grid_forget()
        
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
            self.valid_lb.grid(common.grid_param["left"],row=7)
            self.valid_entry.grid(common.grid_param["center"],row=7)
            self.valid_bikou.grid(common.grid_param["right"],row=7)
            self.valid_entry.delete(0,tk.END)
            self.valid_entry.insert(0,f"{datetime.date.today().strftime('%Y-%m-%d')}")
    
    def setting_rule(self,prm):
        
        # 入力したパラメータ値を取得
        prm['mode'] = self.sent_type_combo.get() + "@" + self.reward_type_combo.get()
        prm['campaign_id'] = self.cpid_entry.get()
        prm['rewardname_description'] = self.description_entry.get()
        prm['sent_type'] = self.sent_type_combo.get()
        prm['reward_type'] = self.reward_type_combo.get()
        prm['useby_date'] = self.valid_entry.get()
        
    def main(self):

        ### メインの処理 ###
        # 01 元ファイルの読み込み
        self.setting_rule(prm)
        myfunc.create_base_path(prm)
        
        # DeliveryPromocodeの作成開始を宣言
        myfunc.output_log(prm,1,"Delivery_promocodes作成開始")
        
        # 指定したフォルダから元ファイルを読み込み
        rewards = myfunc.read_files(prm,self.folder_entry.get())

        try:
            for file in rewards:
                
                #元ファイルを「src」にコピーする

                # dataframeの初期化
                df = pd.DataFrame(columns=myrules.default_coloms[prm['mode']])
                myfunc.output_log(prm,1,f"データフレーム初期化完了／カラム名：{df.columns}")

                # 元ファイルを1ファイルずつdataframeへ格納
                df_src = pd.read_csv(os.path.join(self.folder_entry.get(),file), sep=',', encoding="UTF-8")
                myfunc.set_params(prm,df_src)

                for col_name in df.columns:
                    strValue = prm['target'] + ':' + col_name

                    # データ移行
                    df[col_name] = myfunc.move_data(prm,strValue,df_src)

                # データの編集
                myfunc.output_log(prm,1,f"データ編集開始")
                df = myfunc.format_data(prm,strValue,df)

                # データのシャッフル
                myfunc.output_log(prm,1,f"データシャッフル開始")
                df = myfunc.shuffle_date(prm,df)
                
                # データのエクスポート
                myfunc.output_log(prm,1,f"csv出力開始")
                myfunc.export_data(prm,df,file)

            messagebox.showinfo('メッセージ', '特典作成が完了しました。') 

        except Exception as e:

            messagebox.showinfo('メッセージ', '特典作成中にエラーが発生しました。') 
            myfunc.output_log(prm,3,f"予期せぬエラーが発生しました。")
            myfunc.output_log(prm,3,f"エラークラス：{e.__class__.__name__}／エラー内容：{e.args[0]}／詳細：{e}")
        finally:
            myfunc.output_log(prm,1,"処理完了")
        


if __name__ == "__main__":
    root = tk.Tk()
    root = CreateDeliveryPromocodeAPP(master=root)
    
    #GUI画面の起動
    root.mainloop()