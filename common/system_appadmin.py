import requests,logging,time,re,base64,simplejson
from bs4 import BeautifulSoup
from .tools import saveCookie,readCookie

def getConfig_appadmin(env):
	global host,head,uname,pwd
	host=f'http://{env}-****'
	uname_dict={'test':'****','uat':'****'}
	uname=uname_dict[env]
	pwd='Cmbi@2021'
	head={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
		'Cookie':'',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Connection':'close',
		'X-Requested-With':'XMLHttpRequest',
	}

def login_appadmin(env):
	global host,head,uname,pwd
	getConfig_appadmin(env)
	url=f'{host}/admin/adminUser/login'
	keys={"account":uname,"password":pwd,"vcode":""}
	for i in range(3):
		resp=requests.post(url,headers=head,data=keys,timeout=30)
		try:
			respJson=resp.json()
		except json.decoder.JSONDecodeError:
			logging.error(f'自动登录appadmin系统失败，登录接口返回异常: {resp.text}')
			continue
		if respJson['result']=='1':
			try:
				head['Cookie']=resp.headers['set-cookie']
			except KeyError:
				logging.info(f'debug: {resp.headers}')
				head['Cookie']='0'
			saveCookie(head['Cookie'],f'appadmin_{env}')
			return head['Cookie']
		else:
			logging.error(f'自动登录appadmin系统失败: {respJson}')
			logging.info(f'2秒后开始第 {i+1} 次重试...')
			time.sleep(2);head['Cookie']=''
	raise

def requests_appadmin(methmod,path,backType='json',env='uat',**kwargs):
	global host,head,uname,pwd
	getConfig_appadmin(env.lower())
	cookieLogined=readCookie(f'appadmin_{env}')
	for i in range(5):
		head['Cookie']=cookieLogined
		resp=requests.request(methmod,f'{host}{path}',headers=head,timeout=30,**kwargs)
		if 'admin/AdminUser' in resp.text or 'redirect' in resp.text:
			logging.info(f'appadmin后台cookie失效，重新登录…')
			cookieLogined=login_appadmin(env)
			continue
		else:
			if backType=='json':
				try:
					result=resp.json()
				except:
					logging.error(f'{path}返回数据不是json {resp.text}')
					result=resp.text
					continue
			elif backType=='text':
				result=resp.text
			elif backType=='soup':
				# with open('temp.html','w',encoding='utf-8') as f:f.write(resp.text)
				result=BeautifulSoup(resp.text,'lxml')
			return result

########################################################################################################################################
def getSwitchStatus(switchName,env='uat'):
	# 查询app设置 系统开关状态
	logging.info(f'查询{env}环境 {switchName} 开关状态')
	path=f'/admin/systemSwitch/edit?code={switchName}'
	soup=requests_appadmin('GET',path,backType='soup',env=env)
	try:
		status=soup.select_one('select').select_one("[selected='']").text.strip()
		logging.info(f'{env}环境 {switchName} 开关状态: {status}')
		return status
	except:
		return '开启'

def getMailRecord_appadmin(account,env='uat',start_date=None,end_date=None,keyword='登录通知',timeLimit=180):
	date=time.strftime("%Y-%m-%d")
	if not start_date:start_date=date
	if not end_date:end_date=date
	param={
		'type':'3',
		'key':'account',
		'search':account,
		'status':'',
		'begin_date':start_date,
		'end_date':end_date,
	}

	path='/admin/appSendRecord/list'
	respJson=requests_appadmin('GET',path,backType='json',env=env,params=param)
	mailRecord=[]
	if len(respJson['data']['dataList']['list'])>0:
		for item in respJson['data']['dataList']['list']:
			acc=item['account']
			mailTxt=item['emailTitle']
			sendTime=item['sendTime']
			mailid=item['id']
			if (keyword in mailTxt) and (acc==account) and (int(time.time())-time.mktime(time.strptime(sendTime,'%Y-%m-%d %X'))<timeLimit):#3分钟内的:
				mailRecord.append((acc,mailTxt,sendTime,mailid))
	return mailRecord

########################################### 新股认购相关 ###################################################################################
def getAccountinfo(account,env='uat'):
	# 查询用户信息
	path=f'/admin/eipoOrder/accountinfo?accountid={account}'
	respJson=requests_appadmin('GET',path,backType='json',env=env)
	return respJson

def ipoBuyDetail(account,aecode,accountType,env='uat'):
	# 查询新股详情及购买力
	path=f'/admin/eipoOrder/ipoBuyDetail?stockCode=989450&accountid={account}&publishId=2022032211210696&accountId={account}&aecode={aecode}&accountType={accountType}'
	respJson=requests_appadmin('GET',path,backType='json',env=env)
	return respJson

def eipoOrder_save(account,env='uat'):
	# 新股认购
	oldOrderNo=queryIPOorder(account,env)
	if oldOrderNo:eipoOrder_cancel(oldOrderNo,env)
	accInfo=getAccountinfo(account,env)
	path='/admin/eipoOrder/save'
	acctype_dict={'MRGN':'保证金账户','CUST':'现金账户'}
	data={
		'programId':'',
		'tokenId':'',
		'cancelDeadline':'2123-03-27 00:00',
		'singleFinLimit':'',
		'accountId':account,
		'channelType':'',
		'accountType':accInfo['data']['acctType'],
		'acctType':acctype_dict[accInfo['data']['acctType']],
		'accountName':accInfo['data']['name'],
		'aeCode':accInfo['data']['aecode'],
		'department':'EQU',
		'gmIdNumber':'',
		'gmAccountId':'',
		'accClass':'',
		'stockCode':'989450',
		'stockName':'AUTO(自动化)',
		'leftTotalUsedAmount':'(HKD)0.00',
		'selectType':'cash',
		'subscribeEndDate':'2123-03-22 16:00',
		'applySubscribeNum':'500,9999.77',
		'financingScale':'',
		'financingRate':'',
		'useCash':'9999.77',
		'financingScaleMoney':'',
		'useFinancing':'',
		'subscribeFee':'30.00',
		'currency':'HKD',
		'cashFee':'30.00',
		'financingFee':'100.00',
		'freezeAmount':'10,029.77 HKD',
		'recordNo':'123',
	}
	respJson=requests_appadmin('POST',path,backType='json',env=env,data=data)
	logging.info(f'新股认购结果: {respJson}')
	return respJson.get('result').get('tradeOrderId')

def eipoOrder_cancel(orderNo,env='uat'):
	# 新股认购 取消认购
	path=f"/admin/eipoOrder/cancel"
	data={
		'orderNo':orderNo,
		'stockCode':'989450',
		'reason':'ForAutoTest',
	}
	# print(data)
	respJson=requests_appadmin('POST',path,backType='json',env=env,data=data)
	logging.info(f'取消认购结果: {respJson}')

def queryIPOorder(account,env='uat'):
	path=f'/admin/eipoOrder/list'
	status=['INIT','ACCEPT_SUCCESS']
	param={
		'stockCode':'989450',
		'publishId':'2022032211210696',
		'key':'accountid',
		'search':account,
		'order_type':'',
		'captial_type':'',
		'order_status':'',
	}
	for s in status:
		param['order_status']=s
		respJson=requests_appadmin('GET',path,backType='json',env=env,params=param)
		logging.info(respJson)
		if respJson['data']['dataList']['list']:
			return respJson['data']['dataList']['list'][0]['orderNo']

#####################################################################################################################
def getOrderInfo(account,productCode,env='test'):
	path=f'/admin/pFundOrder/placeOrder?side=1&accountid={account}&productCode={productCode}&currency={productCode[-3:]}'
	respJson=requests_appadmin('GET',path,backType='json',env=env)
	return respJson

def pFundOrder(account,productCode,env='test'):
	# 私募基金下单
	orderInfo=getOrderInfo(account,productCode,env)
	logging.info(f'orderInfo: {orderInfo}')
	path='/admin/pFundOrder/exchangeOrder'
	data={
		'side':'1',
		'accountid':account,
		'aecode':'655',
		'vulnerableFlag':'',
		'orderToken':orderInfo['data']['preCheck']['orderToken'],
		'productCode':productCode,
		'nobuy':'N',
		'isContinue':'N',
		'currency':'',
		'miniAmount':orderInfo['data']['preCheck']['miniAmount'],
		'powerAmount':orderInfo['data']['buyPower']['powerAmount'],
		'buyAmount':orderInfo['data']['preCheck']['miniAmount'],
		'subscriptionFeeRate':'0',
		'manageFeeRate':'0',
		'totalAmount':orderInfo['data']['preCheck']['miniAmount'],
		'agreeCcCompliance':'on',
		'agreeRiskStatement':'on',
		'agreeDda':'on',
		'recordInfo':'default',
		'vcWitness':'',
		'concentration_prod':'25%',
		'holdingSum':'0',
		'miniRenewalAmount':'1000',
		'cashSum':orderInfo['data']['preCheck']['cashSum'],
		'complexFund':'Y',
		'riskRating':orderInfo['data']['preCheck']['riskRating'],
		'checkItemRes':'1',
		'checkItemList': str([{"checkResult":"1","custInfo":"0.0003","itemCode":"CONCENTRATION_RATIO","itemName":"集中度","productInfo":"0.25"}]).replace("'",'"'),
		'concentration_cust_num':'0.0003',
		'concentration_res':'1',
		'clarification':''
	}
	logging.info(f'data: {data}')
	respJson=requests_appadmin('POST',path,backType='json',env=env,data=data)
	# respJson=requests_appadmin('POST',path,backType='json',env=env,data=data,proxies={"http":"http://10.0.2.83:8079"})
	logging.info(f'基金 {productCode} 下单结果: {respJson}')

def getPfundList(env,product='pFundOrder',side='1'):
	# 查询 私募基金产品列表
	itemName={'pFundOrder':'pfundP','bondOrder':'p','spOrder':'p'}
	productName={'pFundOrder':'私募基金','bondOrder':'债券','spOrder':'结构化'}
	# allowTrade={'pFundOrder':'','bondOrder':'S','spOrder':'T'}

	path=f'/admin/{product}/prodListCheck'
	data={'page':'1','side':side}
	respJson=requests_appadmin('POST',path,backType='json',env=env,data=data)
	pages=int(respJson['result']['pages'])
	total=int(respJson['result']['total'])
	logging.info(f'总个数:{total} 总页数:{pages}')
	productList=[]
	for i in range(1,pages+1):
		logging.info(f'第{i}页')
		data['page']=i
		respJson=requests_appadmin('POST',path,backType='json',env=env,data=data)
		for item in respJson['result'][f'{itemName[product]}roductInfoList']:
			if product=='pFundOrder':
				pass
			elif product=='bondOrder':
				if item['status']!='S':
					continue
			elif product=='spOrder':
				if item['status']!='T':
					continue
			productList.append(item['productCode'])

	logging.info(f'查询 {productName[product]}产品列表: {productList}')