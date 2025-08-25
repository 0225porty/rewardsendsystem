# grid配置の定義
grid_param = {
    "left" :{"column":0,"padx":2,"pady":4,"ipadx":20,"ipady":5,"sticky":"e"}
    ,"center" :{"column":1,"padx":2,"pady":4,"ipadx":20,"ipady":5}
    ,"right" :{"column":2,"ipadx":2,"ipady":5,"sticky":"w"}
    ,"title" :{"column":0,"ipadx":2,"ipady":5,"sticky":"w","columnspan":2}
}
# GUI画面の設定
sent_type_option = ["Manual","Voucher"]
reward_type_option = {
             "Manual"    :["プロモコード","他社特典／デジタルコード","他社特典／URL","他社特典／ローソンお買物券","リマインド配信","auPAY残高還元リマインド"]
            ,"Voucher"   :["プロモコード","他社特典／コード","他社特典／URL（単一）","他社特典／URL（複数）","他社特典／ローソンお買物券"]
}

# 環境設定
env_setting = {
    
    # 共通の設定
    "CreateDeliveryPromocodeAPP.pyw":{
        "target":"promocode"
        ,"env_path":"{base}/etc/env_settings.py"
        ,"setting_path":"{base}/etc/settings.py"
        ,"mapping_path":"{base}/etc/mapping.ini"
        ,"edit_path":"{base}/etc/edit.ini"
        ,"module_path":"{base}/lib/data_process.py"
        ,"export_path":"D:/work/python/{campaign_flg}_promocode/"
        ,"upload_path":"{export_path}upload/"
        ,"src_path":"{export_path}src/"
        ,"log_path":"{base}/mst/"
        ,"export_file":"No.8_{filename}.csv"
        ,"log_name":"execelog.xlsx"
        ,"sheet_name":"log"
    }
    ,"CreateSendDataAPP.pyw":{
        "target":"senddata"
        ,"env_path":"{base}/etc/env_settings.py"
        ,"setting_path":"{base}/etc/settings.py"
        ,"mapping_path":"{base}/etc/mapping.ini"
        ,"edit_path":"{base}/etc/edit.ini"
        ,"module_path":"{base}/lib/data_process.py"
        ,"export_path":"D:/work/python/{campaign_flg}_senddata/"
        ,"upload_path_01":"{export_path}upload/snowflake/"
        ,"upload_path_02":"{export_path}upload/clevertap/"
        ,"src_path":"{export_path}src/"
        ,"log_path":"{base}/mst/"
        ,"export_file_01":"No.5_{campaign_flg}_RSH.csv"
        ,"export_file_02":"{campaign_flg}.csv"
        ,"log_name":"execelog.xlsx"
        ,"sheet_name":"log"
    }
}

# ログファイル名の定義
check_file = {
    "Manual@プロモコード":"チェックファイル_M_#10.xlsx"
    ,"Manual@他社特典／デジタルコード":"チェックファイル_M_#11.xlsx"
    ,"Voucher@プロモコード":"チェックファイル_V_#10.xlsx"
}