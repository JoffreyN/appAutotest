import os,faker

accountPool={
	# '账号':['密码','用户昵称']
	# '511682':['****','0023'],'M511682':['****','5870'],'132******70':['****','5870'],
	# '700876':['****','6697'],'M700876':['****','6697'],'155******97':['****','6697'],
	# '700877':['****','王佳'],'M700877':['****','6795'],'150******95':['****','6795'],
	# '290522':['****','5966'],'M290522':['****','5966'],'138******66':['****','5966'],
	# '290523':['****','4377'],'M290523':['****','4377'],'155******77':['****','4377'],
	# '290525':['****','3282'],'M290525':['****','3282'],'132******82':['****','3282'],
	'694080632@qq.com':['****','BxxxcName'],
	# '705801':['****','8689'],'M705801':['****','8689'],'156******89':['****','8689'],
	# '705802':['****','4999'],'M705802':['****','4999'],'157******99':['****','4999'],
	# '705805':['****','7992'],'M705805':['****','7992'],'135******92':['****','7992'],
	# '292036':['****','8357'],'M292036':['****','8357'],'159******57':['****','8357'],
	# '292037':['****','4018'],'M292037':['****','4018'],'182******18':['****','4018'],
	# '292038':['****','9823'],'M292038':['****','9823'],'135******23':['****','9823'],
	## 用于bmp行情
	'802632':['****','9065'],'M802632':['****','9065'],'158******65':['****','9065'],
	'802650':['****','6152'],'M802650':['****','6152'],'181******52':['****','6152'],
	'802652':['****','8848'],'M802652':['****','8848'],'131******48':['****','8848'],

	#以下为TTL账户
	'706158':['****','0476'],'M706158':['****','0476'],'155******76':['****','0476'],
	'706159':['****','3085'],'M706159':['****','3085'],'185******85':['****','3085'],
	'706160':['****','2427'],'M706160':['****','2427'],'139******27':['****','2427'],
	'292231':['****','4267'],'M292231':['****','4267'],'138******67':['****','4267'],
	'292232':['****','1196'],'M292232':['****','1196'],'181******96':['****','1196'],
	'292233':['****','8800'],'M292233':['****','8800'],'180******00':['****','8800'],
	## 用于bmp行情
	'802523':['****','8803'],'M802523':['****','8800'],'181******03':['****','8803'],
	'802529':['****','0106'],'M802529':['****','8800'],'151******06':['****','0106'],
	'802588':['****','6607'],'M802588':['****','8800'],'152******07':['****','6607'],
	## 用于联名账户重置密码
	'999001':['****',''],
	'999002':['****',''],
	'999003':['****',''],
	'999004':['****',''],
	'999005':['****',''],
	'999006':['****',''],
	#以下为生产账户
	'132228':['Cmbi7788','陳廣豐']
}

#现金账户对应的孖仔账户、手机号
accBinding={
	# '511682':['M511682','132******70','2********4@qq.com'],
	# '700876':['M700876','155******97','1********0@qq.com'],
	# '700877':['M700877','150******95','********0@qq.com'],
	# '290522':['M290522','138******66','********2@qq.com'],
	# '290523':['M290523','155******77','2********3@qq.com'],
	# '290525':['M290525','132******82','2********7@qq.com'],
	# '705801':['M705801','156******89','ocwyixas67ldg40h2qz1@9txbrwnua2c36fh.com'],
	# '705802':['M705802','157******99','ivc7xeo8pdwufy0sg56m@ukws0mj9olyrc5z.com'],
	# '705805':['M705805','135******92','ghz3uqejl1t2kyr4mxai@65it2hrlz3c941b.com'],
	# '292036':['M292036','159******57','cl4ewhzyb6dr83ksf2xm@nr175a6pdmk8hb3.com'],
	# '292037':['M292037','182******18','5v3qsfem72otcxyh1djg@rd4t1biw75nfm9a.com'],
	# '292038':['M292038','135******23','bh8pkvsflezn036a9m5w@78at9goi3cn1u52.com'],
	#以下为TTL账户
	'706158':['M706158','155******76','shyudvew3m1kr2o504lz@ysk2wbvmou9n5xe.com'],
	'706159':['M706159','185******85','jslkz89qiwneyam6tuov@dnjetlvc0fpgw4y.com'],
	'706160':['M706160','139******27','2g96obvq13tfdu7ymphn@2xcn5bpr41gljo9.com'],
	'292231':['M292231','138******67','n3z1jirc0ydhw2qmxlaf@ayp5qziv8e2ns4u.com'],
	'292232':['M292232','181******96','3t2igle50fuynjdhpb7a@a27bt4fsylwzmek.com'],
	'292233':['M292233','180******00','w18obcsehv4x0djg3ik7@g721evchzdj6a3w.com'],
	## 用于bmp行情
	'802632':['M802632','158******65','z2mkgif63y1anx8rq7ub@sq79hmwrvkbfdzu.com'],
	'802650':['M802650','181******52','rm8ohl6e43x29sjynbdu@qjfe8x6zan2703v.com'],
	'802652':['M802652','131******48','hcbqsi8vor5l49gfn3e7@bkfuz7pswlm3t28.com'],
	'802523':['M802523','181******03','e2ty6c3lgjwm8hsb9urd@0p7qu9adgtihl3b.com'],
	'802529':['M802529','151******06','xnuce1ar7pljk9g5oz03@xg6zmolu4hceq8f.com'],
	'802588':['M802588','152******07','1kqzhj4iblyfu26w5e98@g4tj8c2we1nal3y.com'],
	## 用于联名账户重置密码
	'999001':['','13522221110',''],
	'999002':['','13522221112',''],
	'999003':['','13522221114',''],
	'999004':['','13522221116',''],
	'999005':['','13522221118',''],
	'999006':['','13522221100',''],
}

UnionAcc={
	'706158':['999001','****',['441422*********103','23060*********194X',]],
	'706159':['999002','****',['511101*********59X','65402*********6474',]],
	'706160':['999003','****',['510781*********942','53042*********7077',]],
	'292231':['999004','****',['530324*********699','37070*********2113',]],
	'292232':['999005','****',['540222*********344','41062*********466X',]],
	'292233':['999006','****',['61092**********997','65322**********81X','11011**********052',]],
}



#交易持仓 使用现金账户
tradeData={
	# '511682':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '700876':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '700877':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '290522':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '290523':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '290525':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '705801':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '705802':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '705805':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '292036':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '292037':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	# '292038':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
	#以下为TTL账户
	'706158':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['PG'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BABA'],}},
	'706159':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['PG'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BABA'],}},
	'706160':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['PG'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BABA'],}},
	'292231':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['PG'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BABA'],}},
	'292232':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['PG'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BABA'],}},
	'292233':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['PG'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BABA'],}},
	#以下为生产账户
	'132228':{'b':{'HK':['03968'],'SH':['600600'],'SZ':['000001'],'US':['BILI'],},'s':{'HK':['02018'],'SH':['601398'],'SZ':['002594'],'US':['BRK.B'],}},
}

regData = {
	'706158':{
		'regFirst':('130******71','****'),# 用于第一次开户(需要先手机号注册成功呢)
		'regSecond':{# 用于二次开户,需要先一次开户完成并激活
			'general':[('134******60','****'),('700786','****')],
			'pi':[('15771018619','****'),('290381','****')],
		},
		'bmp_acc':('802632','****'),
	},
	'706159':{
		'regFirst':('135******45','****'),
		'regSecond':{'general':[('145******36','****'),('700607','')],'pi':[('139******15','****'),('290288','')],},
		'bmp_acc':('802650','****'),
	},
	'706160':{
		'regFirst':('130******72','****'),
		'regSecond':{'general':[('189******07','****'),('700788','****')],'pi':[('180******81','****'),('290382','****')],},
		'bmp_acc':('802652','****'),
	},
	'292231':{
		'regFirst':('138******89','****'),
		'regSecond':{'general':[('133******74','****'),('700606','')],'pi':[('145******86','****'),('290287','')],},
		'bmp_acc':('802523','****'),
	},
	'292232':{
		'regFirst':('137******27','****'),
		'regSecond':{'general':[('136******02','****'),('700878','')],'pi':[('189******22','****'),('290526','')],},
		'bmp_acc':('802529','****'),
	},
	'292233':{
		'regFirst':('134******82','****'),
		'regSecond':{'general':[('137******21','****'),('700879','')],'pi':[('132******82','****'),('290527','')],},
		'bmp_acc':('802588','****'),
	},


}

currExchange_Data=[
	('in','美元','港币'),('in','港币','美元'),('in','港币','人民币'),('in','人民币','港币'),('in','美元','人民币'),('in','人民币','美元'),
	('out','美元','港币'),('out','港币','美元'),('out','港币','人民币'),('out','人民币','港币'),('out','美元','人民币'),('out','人民币','美元'),
]

BMP_account={
	
}



##################以下配置一般不用修改#################

#用于行情模块 股票搜索
searchData=[
	{'inputs':'招商银行','expect':['03968','600036']},
	{'inputs':'09988','expect':['09988','阿里巴巴']},
	{'inputs':'blbl','expect':['BILI','哔哩哔哩']},
]

#用于站外开户
# regURL='http://0.0.0.0/appkh/form'
# regURL={
# 	'dev':'http://0.0.0.0/appweb/appkh/form',
# 	'test':'http://0.0.0.0/appweb/appkh/form',
# 	'uat':'http://0.0.0.0/appweb/appkh/form',
# }
regURL_ttl={
	'dev':'http://0.0.0.0/appweb/appkh/form',
	'test':'http://0.0.0.0/appweb/appkh/form',
	'uat':'http://0.0.0.0/appweb/appkh/form'
}
fake=faker.Faker(locale='zh_CN')
regInfo={
	'realName':'AutoTest',
	'enName':'RegFor AutoTest',
	'cardID':fake.ssn(),
	'birthplace':'中国广州',
	'birthday':'1994-01-30',
	'address':'广东省香港市皇后大道东17号',
	'homeTel':'010-*********',
	'email':'10******88@qq.com',
	'company':fake.company(),
	'pic1':os.path.abspath('testData/pic/1.png'),
	'pic2':os.path.abspath('testData/pic/1.jpg'),
	'pic3':os.path.abspath('testData/pic/1.jpeg'),
	'pic4':os.path.abspath('testData/pic/2.jpg'),
}

'''
新增用于ui自动化账户的步骤：
	1、开户，勾选保证金和现金账户
	2、给账户充港元、人民币、美元、基金账户关联、基金购买力、基金持仓、股票持仓（四种类型的股票各1只）
	3、开通北向交易权限
	4、插入交易历史
	(已废弃)5、boss后台修改账户类型为客户经理，988;985 密码设置为 1234
	6、业务办理-香港银行卡 三种币种各新增一个
	7、完成风险测评、衍生品问卷
	8、模拟炒股页面，点击领取
	9. 修改资料-证件信息、地址信息 填写一遍然后撤回，财务状况、雇佣信息走一遍

新增用于ui自动化TTL账户的步骤：
	（自动开户完成）1、开户，勾选保证金和现金账户
	（自动开户完成）2、给账户充港元、人民币、美元、基金账户关联、基金购买力、基金持仓、股票持仓（四种类型的股票各1只）
	（废弃）3、开通北向交易权限
	4、插入交易历史
	(已废弃)5、boss后台修改账户类型为客户经理，988;985 密码设置为 1234
	（自动开户完成）6、业务办理-香港银行卡 三种币种各新增一个
	7、完成风险测评
	8、模拟炒股页面，点击领取
	9. 修改资料-证件信息、地址信息 填写一遍然后撤回，财务状况、雇佣信息走一遍
	10. 开通基金交易权限
	11. 升级美股L1串流 港股L2串流
'''
