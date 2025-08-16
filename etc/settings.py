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
    "Manual@プロモコード":['campaign_flg','rewardname','rewardname_description','PortInOnly','MaxLimit','useby_date']
    ,"Voucher@プロモコード":['campaign_flg','promocode']
    ,"Manual@他社特典／デジタルコード":['campaign_flg','rewardname','rewardname_description','useby_date']
}