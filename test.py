import sys,os,HTMLReport
# from common.CMSsystem import *
# from common.system_boss import *
# from common.system_openbo import loginBO

# from common.dbOperation import del_pwdHistory
# from common.dbOperation import del_market
# from common.CMS_ttl_system import *
# from business.changePwd import resetpwd_ttl
# from common.apiCenter import *
# from common.system_appadmin import *
# from business.reg_futures_api import reg_futures_api
# from business.reg_api import reg_api_second
# from common.system_openbo import checkBO,manualActivate,getCheckID,sendWelcome
# getPfundList('uat')
# getPfundList('uat','bondOrder')
# getPfundList('uat','spOrder')
# print(getSwitchStatus('USER_LOGIN_PRIVACY_SWITCH'))

# addBankcard('292232',93783537596268128,env='uat')

# fundPool=[
# 'P202108231190HKD','P202108231191HKD','P202201101233HKD','P202201131237HKD','P202201131238HKD','P202201131241HKD','P202201121235HKD','P202201121236HKD','P202201131239HKD','P202201121234HKD','P202108231189HKD','P20220222P321HKD','P20220222P322HKD','P20220222P323HKD','P202202231243HKD','P202202231244HKD','P202202241245HKD','P202202241246HKD','P202202251248HKD','P202202251250HKD','P202202251251HKD','P202202251252HKD','P202202281254HKD','P202202281253HKD','P202202251247HKD','P202203011255USD','P202203011256USD','P202203011257USD','P202202251249HKD','P202201131242JPY','P202112281232USD','P202201131240HKD','P202108231182HKD','P202108231089HKD','P202107261022USD','P202107261012USD','P202107261010USD','P202112141223HKD','P202112131213USD','P202112131215USD','P202112141219HKD','P202112141225HKD','P202112151226HKD','P202112281227HKD','P202112281228USD','P202112281229USD','P202112281230HKD','P202112281231USD','P202108231126HKD','P202108231127HKD','P202108231128HKD','P202108231129HKD','P202108231130HKD','P202108231131HKD','P202108231132HKD','P202108231133HKD','P202108231134HKD','P202108231135HKD','P202108231136HKD','P202108231137HKD','P202108231138HKD','P202108231139HKD','P202108231140HKD','P202108231141HKD','P202108231142HKD','P202108231143HKD','P202108231144HKD','P202108231145HKD','P202108231146HKD','P202108231147HKD','P202108231148HKD','P202108231149HKD','P202108231150HKD','P202108231151HKD','P202108231152HKD','P202108231153HKD','P202108231154HKD','P202108231155HKD','P202108231156HKD','P202108231157HKD','P202108231158HKD','P202108231159HKD','P202108231160HKD','P202108231161HKD','P202108231162HKD','P202108231163HKD','P202108231164HKD','P202108231165HKD','P202108231166HKD','P202108231167HKD','P202108231168HKD','P202108231169HKD','P202108231170HKD','P202108231171HKD','P202108231172HKD','P202108231173HKD','P202108231174HKD','P202108231175HKD','P202108231176HKD','P202108231177HKD','P202108231178HKD','P202108231181HKD','P202108231179HKD','P202108231183HKD','P202108231180HKD','P202108231184HKD','P202108231185HKD','P202108231186HKD','P202108231187HKD','P202108231188HKD','P202107261034USD','P202107261032USD','P202107261033USD','P202107261035USD','P202107261036USD','P202107261037USD','P202107261038USD','P202107261039USD','P202107261040HKD','P202107261041USD','P202107261042USD','P202107301072USD','P202108231094HKD','P202108231095HKD','P202111241195HKD','P202111291201USD','P202111291203USD','P202112031207HKD','P202108231096HKD','P202108231116HKD','P202108231117HKD','P202112041210USD','P202112061211HKD','P202107301066USD','P202108031077HKD','P202108201079USD','P202108201081HKD','P202108231109HKD','P202108231110HKD','P202108231111HKD','P202108231112HKD','P202112141218HKD','P202112141220HKD','P202112141221HKD','P202112141222HKD','P202112141224HKD','P202107291057USD','P202107291058USD','P202107291059USD','P202107291060USD','P202107291061USD','P202108201078USD','P202108201082HKD','P202108231083CNY','P202112031205HKD','P202112031206HKD','P202112131214USD','P202112141216HKD','P202108031074CNY','P202108031076HKD','P202108231084CNY','P202108231085CNY','P202108231086CNY','P202108231087CNY','P202108231088CNY','P202108231090HKD','P202108231091HKD','P202108231092HKD','P202108231093HKD','P202111301204USD','P202108231113HKD','P202108231114HKD','P202108231115HKD','P202107291052USD','P202107291053USD','P202107291054USD','P202107291055USD','P202107291056USD','P202112081212HKD','P202112141217HKD','P202108231118HKD','P202108231119HKD','P202108231120HKD','P202108231121HKD','P202108231122HKD','P202108231123HKD','P202108231124HKD','P202108231125HKD','P202108031075USD','P202108201080USD','P202108231097HKD','P202108231098HKD','P202108231099HKD','P202108231100HKD','P202108231101HKD','P202108231102HKD','P202108231103HKD','P202108231104HKD','P202108231105HKD','P202107301063USD','P202107301064USD','P202107301065USD','P202108021073USD','P202108231106HKD','P202108231107HKD','P202108231108HKD','P202112031208HKD','P202107261000USD','P202107261001USD','P202107261002USD','P202107261003USD','P202107261004USD','P202107261005USD','P202107261006USD','P202107261008USD','P202107261009USD','P202107261011USD','P202107261014USD','P202107261015USD','P202107261016USD','P202107261017USD','P202107261018USD','P202107261019USD','P202107261043USD','P202107261044USD','P202111291202USD','P202107261013USD','P202107261045USD','P202107281046CNY','P202107291047USD','P202107291048USD','P202107291049USD','P202107291050USD','P202107291051USD','P202110131194HKD','P202111261196HKD','P202111261197HKD','P202111261198HKD','P202111261199HKD','P202111261200HKD','P202112041209USD','P202107261020USD','P202107261021USD','P202107261023USD','P202107261024USD','P202107261025USD','P202107261026USD','P202107261029USD','P202107261030USD','P202107261031USD','P202107301062USD','P202107301067USD','P202107301068USD','P202107301069USD','P202107261027USD','P202107261028USD','P202107301070USD','P202107301071USD',

# 'P202107261039USD',
# 'P20220222P321HKD','P20220222P322HKD','P20220222P323HKD','P202202231243HKD','P202202231244HKD','P202202241245HKD','P202202241246HKD','P202202251248HKD','P202202251250HKD','P202202251251HKD','P202202251252HKD','P202202281254HKD','P202202281253HKD','P202202251247HKD','P202203011255USD','P202203011256USD','P202203011257USD','P202202251249HKD',
# ]
# print(getOrderToken('917876','P202108231190HKD'))
# for fund in fundPool:
# 	try:
# 		pFundOrder('917876',fund)
# 	except KeyboardInterrupt:
# 		sys.exit(0)
# 	except:
# 		logging.info(f'异常: {fund}')

# pFundOrder('917876','P202107261039USD')
# print(getInitialPwd('8xn63kcjtevhlayrdmi2@zvm3wqtg5u9op8k.com','test'))

# loginBO('uat')

for i in range(10):
	print(f'第 {i+1} 个')
	os.system('python3 regWeb.py -e uat --margin --check --active --ttl --regbyapi')# TTL开户
	# os.system('python regWeb.py --margin --check --active --setPwd -e uat --headless')# 一般投资者
	# os.system('python regWeb.py --margin --check --active --setPwd -e uat --pi --headless')# 专业投资者



# accPool=['292232'
# ]
# conn=None
# env='uat'
# for acc in accPool:
# 	conn=del_market(acc,env=env,conn=conn)
# 	openMarket_boss(acc,env=env)

# del_pwdHistory('290525')

# card_id=get_cardID('706158','uat')[0][0]
# print(card_id)
# print(getCheckID(search2='18953052903',getAcclist=1,env='test',ttl=1))

# approveIdList=getCasherDeposite('918770')
# print(approveIdList)
# approve_submit(approveIdList)

# print(resetpwd_ttl('918795','aaaa1111',env='test'))

# # cancelFinance('M706159','aaaa1111',env='uat',ttl=1)

# sessionDic=login_acc('706159','aaaa1111','uat')
# print(sessionDic)

# preTradeOrderId=preOrderDetail(sessionDic,'uat')
# print(preTradeOrderId)
# preOrderCancel(sessionDic,preTradeOrderId,'uat')
# tradeOrderId=orderSubmitIPO(sessionDic)
# cancelOrderIPO(sessionDic,'TC163772412019372299')
# cardOperate(sessionDic,'uat')
# signAgreement(sessionDic,'uat')
# print(resetpwd('290525','aaaa1111',env='uat',ttl=0))
# resetAccountPwdSendCode('292232')
# unlockAcc('292232')
# login_acc('292233','aaaa1112',env='uat',ttl=1)



# changeChannel()
# print(getInfoJSON('292233',env='uat'))
# ableBalance=getAvailableBalance('292233',env='uat')
# money=100000000-float(ableBalance['data']['HKD'].replace(',',''))
# print(ableBalance)
# bankCardInfo=getSettlementAccount('292232','HKD',env='uat')
# print(bankCardInfo)
# print(getCompanyBankInfo('HKD',bankCardInfo['data'][0]['bank_code'],env='uat'))

# stopAllApprove('292233','uat')
# approveId=withdrawalSave('292232','HKD',None,'uat')
# print(approveId)
# approveId=approveId['data']['id']
# result=money_check(approveId,bigMoney=1)
# print(f'审核提取结果: {result}')

# inmoney_CMS('803203','HKD',money,env='uat')


# print(cmsClientPhone('292233',env='uat'))
# account='290522';env='uat'
# cms_resetpwd(account,env=env)# 重置密码
# del_pwdHistory(account,env=env)# 删除曾经用过的密码
# mailid=getMailRecord(account,env=env,keyword='密码已重置')
# print(f'邮件ID: {mailid}')
# newpwd=getPwd_from_mail(mailid[0][-1],env=env)# 查询重置后的密码
# print(newpwd)


# accInfo=getAccountinfo('292232')
# print(accInfo)
# eipoOrder_save('M706160','uat')
# eipoOrder_cancel('TC163773705775111925','uat')

# print(queryIPOorder('M292233','uat'))
# print(eipoOrder_save('M292233','uat'))

# class Args():
# 	def __init__(self):
# 		pass
# args=Args()
# args.env='uat'
# args.acc='803387'
# args.tel='15313039267'
# reg_api_second(args)
# args.tel=None
# args.email=None
# reg_futures_api(args)



# for i in range(1,5):
# 	checkID=checkBO(args.tel,i,env=args.env,futures=1)

# manualActivate(checkID,env=args.env)
# sendWelcome(checkID,env=args.env)
# accList=getCheckID(search2=args.tel,getAcclist=1,env=args.env,futures=1)

# print(f'{args.tel} 对应户口号 {" ".join(accList)}')





