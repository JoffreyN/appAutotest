import HTMLReport,logging,time,faker,requests,string
from random import sample,randint
from common.tools import saveFile,encryption
from .reg_api import sign_img,openStatus,checkTable,save_first,checkEmail,save,createNotice,sign

newPwd='aaaa1111'
head={
	'Content-Type':'application/json;charset=UTF-8',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}

head_urlencode={
	'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
}


def sendSmsCode(args):
	url=f'/gateway/operator/sendSmsCode'
	data={
		"areaCode":"86",
		"codeType":"normal",
		"mobile":args.tel,
		"traceLogId":f"fromTestservices{time.time()}",
		"signatureApp":True,
		"lang":"cn"
	}
	logging.info(f'请求URL: {url}')
	logging.info(f'请求数据: {data}')
	timestamp,signature=encryption(data)

	head["TIMESTAMP"]=timestamp
	head["SIGNATURE"]=signature
	resp=requests.post(url,headers=head,json=data,timeout=30)
	del head["SIGNATURE"]
	del head["TIMESTAMP"]

	respJson=resp.json()
	logging.info(f'响应数据: {respJson}')
	if not respJson['success']:
		raise Exception(f'/gateway/operator/sendSmsCode 返回数据异常')

def smsCodeLogin(args):
	url=f'/gateway/operator/smsCodeLogin'
	data={
		"areaCode":"86",
		"mobile":args.tel,
		"channel":"OUTER_H5",
		"code":"8888",
		"traceLogId":f"fromTestservices{time.time()}",
		"signatureApp":True,
		"lang":"cn"
	}
	logging.info(f'请求URL: {url}')
	logging.info(f'请求数据: {data}')
	timestamp,signature=encryption(data)

	head["TIMESTAMP"]=timestamp
	head["SIGNATURE"]=signature
	resp=requests.post(url,headers=head,json=data,timeout=30)
	del head["SIGNATURE"]
	del head["TIMESTAMP"]

	respJson=resp.json()
	logging.info(f'响应数据: {respJson}')
	try:
		args.operatorNo=respJson['result']['operatorNo']
		args.token=respJson['result']['loginToken']
	except:
		raise Exception(f'/gateway/operator/smsCodeLogin 返回数据异常')

	
####################################################################################################
def reg_futures_api(args):
	args.sign_img=sign_img
	fake=faker.Faker('zh_CN')
	fakeEn=faker.Faker('en')
	if not args.tel:args.tel=fake.phone_number()
	if not args.email:args.email=f"{''.join(sample(string.ascii_lowercase+string.digits,20))}@{''.join(sample(string.ascii_lowercase+string.digits,15))}.com"
	args.cnName=args.name_cn=f'{fake.name()}{fake.first_name()}{fake.word()}{fake.first_name()}'
	args.enName=args.name_en=f"{args.env}{fakeEn.name()} {fakeEn.first_name()} {fakeEn.first_name()} {fakeEn.word()}".replace('.','')
	args.cardID=args.card_id=fake.ssn()
	# args.address='香港'
	args.address=fake.address()
	args.com_name=fake.company()
	args.home_tel=f'0{randint(10,99)}-{randint(10000000,99999999)}'

	saveFile(f"----- {args.env.upper()}环境 期货开户 {time.strftime('%Y-%m-%d %X')} -----")
	saveFile(f'手机号： {args.tel}')
	saveFile(f'中文名: {args.name_cn}')
	saveFile(f'英文名: {args.name_en}')
	saveFile(f'证件ID: {args.card_id}')
	saveFile(f'出生地址: {args.address}')
	saveFile('出生日期： 1984-06-01')
	saveFile(f'联系地址: {args.address}')
	saveFile(f'邮箱号： {args.email}')
	saveFile(f'公司名称: {args.com_name}')

	sendSmsCode(args)
	smsCodeLogin(args)
	openStatus(args,'futures')
	checkTable(args,'futures')

	args.table_status='card'
	args.aecode='988'
	data_first={
		'noLoading':'1','skipResponseErrorToast':'true','table_type':'1','card_type':'PN','address_as_card':'0','email':'','contact_address':'','mobcountry':'86','op_purpose':'1','op_purpose_due':'','publish_1':'1','publish_2':'1','publish_3':'1','publish_4':'1','publish_5':'1','publish_6':'1','publish_7':'1','publish_8':'1','publish_9':'1','publish_9_1':'1','publish_9_2':'1','publish_9_3':'1','publish_10':'1','education':'2','asset_liquid':'11','source_fund':'1','source_wealth':'1','monthly_invest_amount':'1','ac_cash':'1','ac_margin':'0','der_1':'','der_2':'','der_3':'','der_4':'1','q1':'','q2':'','q3':'','q4':'','q5':'','q6':'','q7':'','q8':'','q9':'','q10':'','q11':'','q12':'','sign_method':'online','is_know_risk':'','aum_card':'','aum_mobile':'','ac_futures':'1','aum_account':'','card_photo1':'202112/20211208309225163893450136.jpg','card_photo2':'','sex':'1','nationality':'1','nationality_other':'','card_issue':'HKG','card_address':'','address_certify':'','card_org':'','card_expires_begin':'1984-06-01','card_expires_end':'2051-01-01','birthday':'1984-06-01','op':'h5','channel':'','table_class':'futures','lang':'cn','birth_place':'中国','address_country':'HKG',
		'invite_code':args.aecode,
		'mobile':args.tel,
		'address':args.address,
		'name_cn':args.name_cn,
		'name_en':args.name_en,
		'card_id':args.card_id,
		'table_status':args.table_status,
		'token':args.token,
		'serial_num':f'FromAutoTest_{str(time.time())}',
	}
	args=save_first(args,data_first)

	data_full={
		'table_type':'1','card_type':'PN','address_as_card':'0','mobcountry':'86','op_purpose':'1','op_purpose_due':'','publish_1':'1','publish_2':'1','publish_3':'1','publish_4':'1','publish_5':'1','publish_6':'1','publish_7':'1','publish_8':'1','publish_9':'1','publish_9_1':'1','publish_9_2':'1','publish_9_3':'1','publish_10':'1','education':'2','asset_liquid':'11','source_fund':'1','source_wealth':'1','monthly_invest_amount':'1','ac_cash':'1','ac_margin':'0','der_1':'','der_2':'','der_3':'','der_4':'1','q1':'','q2':'','q3':'','q4':'','q5':'','q6':'','q7':'','q8':'','q9':'','q10':'','q11':'1','q12':'4','sign_method':'online','is_know_risk':'1','aum_card':'','aum_mobile':'','ac_futures':'1','aum_account':'','card_photo1':'202112/20211208309225163893450136.jpg','card_photo2':'','sex':'1','nationality':'1','nationality_other':'','card_issue':'HKG','card_address':'','address_certify':'202112/20211208706665163893475167.jpg','card_org':'','card_expires_begin':'1984-06-01','card_expires_end':'2051-01-01','job_status':'1','job':'1','com_industry':'1','job_status_other':'','retired_reasons':'','publish_1_name':'','publish_1_card_id':'','publish_1_tel':'','publish_1_address':'','publish_1_us':'','publish_4_agency':'','publish_4_code':'','publish_2_name':'','publish_2_account':'','publish_3_name':'','publish_3_account':'','publish_7_name':'','publish_7_relation':'','revenue':'12','asset':'11','source_fund_note':'','source_wealth_note':'','settlement_notify_mail':'1','settlement_notify_postal':'0','q13':'4','q14':'4','q15':'2','q31':'5','q32':'5','q33[0]':'4','q33[1]':'3','q33[2]':'2','q34':'','binded_bankname':'','binded_bankcode':'','binded_cardno':'','binded_certify':'','channel':'','lang':'cn','birthday':'1984-06-01','birth_place':'中国','table_class':'futures','address_country':'HKG',
		'crs_array':'[{"crs_area":"HKG","crs_notin_type":"","crs_tin":"'+args.card_id+'","crs_notin_note":"","crs_certify":""}]',
		'binded_cardname':args.name_en,
		'home_tel':args.home_tel,
		'address':args.address,
		'email':args.email,
		'contact_address':args.address,
		'mobile':args.tel,
		'name_cn':args.name_cn,
		'name_en':args.name_en,
		'invite_code':args.aecode,
		'card_id':args.card_id,
		'com_name':args.com_name,
		'sign_img':args.sign_img,
		'table_status':args.table_status,
		'token':args.token,
		'table_no':args.table_no,
		'table_token':args.table_token,
	}

	checkEmail(args)
	table_status=('personal','background','marketchoose','der','simpleRpq','riskannounce','addHk','sign','handwrite')
	for i in table_status:
		args.table_status=i
		if i=='handwrite':sign(args)
		result=save(args,data_full)
	if result=='success':
		createNotice(args)
		return args
