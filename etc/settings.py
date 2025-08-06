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
            "Manual"    :["プロモコード","他社特典／デジタルコード","他社特典／URL","リマインド配信","auPAY残高還元"],
            "Voucher"   :["プロモコード","他社特典／コード","他社特典／URL（単一）","他社特典／URL（複数）"]
        }

# 作成定義
default_rule = {
    "src_path":None
    ,"dest_path":"D:/work/python/"
    ,"dirname":"/upload"
    ,"log_path":None
    ,"target":None
    ,"columns":None
    ,"campaign_id":None
    ,"rewardname_description":None
    ,"sent_type":None
    ,"reward_type":None
    ,"useby_date":None
    ,"prefix":"No.8_"
    ,"date_6":None
    ,"dest_file":None

}

# カラム名の定義
format_col = {
    "Manual@プロモコード":['campaign_flg','rewardname','rewardname_description','useby_date']
    ,"Voucher@プロモコード":['campaign_flg','promocode']
}