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
# パラメータ変数
params = {
    "CreateDeliveryPromocodeAPP.pyw":{
        "mode":None
        ,"target":"promocode"
        ,"campaign_id":None
        ,"rewardname_description":None
        ,"sent_type":None
        ,"reward_type":None
        ,"useby_date":None
    }
}

# カラム名の定義
default_coloms = {
    "Manual@プロモコード":['campaign_flg','rewardname','rewardname_description','MaxLimit','useby_date']
    ,"Voucher@プロモコード":['campaign_flg','promocode']
    ,"Manual@他社特典／デジタルコード":['campaign_flg','rewardname','rewardname_description','useby_date']
}