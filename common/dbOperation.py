import time,traceback,sys,faker,datetime,logging
from random import choice

def getIP():
	ip=None
	import os
	try:ip=[a for a in os.popen('ifconfig en1').readlines() if 'inet' in a][1].split()[1]
	except:pass
	return ip

def getDBconn(dbType,env='uat',host=None,user=None,password=None,port=3306):
	# ip=getIP() # pymssql 不支持使用指定IP连接
	if dbType=='mysql':
		import pymysql
		hostDic={'uat':'0.0.0.0','test':'0.0.0.0'}
		if not user:user='****'
		if not password:password='****'
		if not host:host=hostDic[env]
		conn=pymysql.connect(host=host,port=port,user=user,password=password,charset='utf8')
		# conn=pymysql.connect(host=hostDic[env],user=user,password=password,charset='utf8',bind_address=ip)
	elif dbType=='sqlserver':#ABC 数据库
		user='****';password='****'
		hostDic={'uat':'0.0.0.0','test':'0.0.0.0'}
		import pymssql
		conn=pymssql.connect(server=hostDic[env],user=user,password=password)
	return conn

def excuteSQL(sql,dbType='mysql',env='uat',conn=None,keepLive=0):
	if not conn:conn=getDBconn(dbType,env)
	cursor=conn.cursor()
	try:
		if type(sql)==list:
			for s in sql:
				cursor.execute(s)
				logging.info(f'sql执行成功: {s}')
			results=1
		else:
			cursor.execute(sql)
			logging.info(f'执行成功: {sql}')
			results=cursor.fetchall() if sql.startswith('SELECT') else 1
		cursor.close()
		conn.commit()
	except Exception as e:
		conn.rollback() # 事务回滚
		logging.info(f'SQL执行失败 {sql}\n{traceback.format_exc()}')
		results=0
	finally:
		if keepLive:
			return conn
		else:
			conn.close()
			if results:return results
			else:
				logging.info(f'执行失败: {sql}')

def insertStock(account,types='all',delOld=1):
	# 插入持仓
	AcctType='MRGN' if 'M' in account.upper() else 'CUST'
	USinsql=[
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','BRK/B','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','BRK/B','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','AAPL','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','AAPL','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','MSFT','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','MSFT','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','TSLA','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','TSLA','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','BABA','USA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','BABA','USA','{AcctType}','03','50000','ST','','{account}')",
	]
	HKinsql=[
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','02018','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','02018','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','02888','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','02888','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','00005','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','00005','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','00700','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','00700','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','01810','HKG','{AcctType}','03','50099','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','01810','HKG','{AcctType}','03','50099','ST','','{account}')",
	]
	SZinsql=[
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','002594','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','002594','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','300750','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','300750','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','000858','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','000858','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','000651','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','000651','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','002475','SZA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','002475','SZA','{AcctType}','03','50000','ST','','{account}')",
	]
	SHinsql=[
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','601398','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','601398','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','600036','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','600036','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','600519','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','600519','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','600030','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','600030','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('L','601628','SHA','{AcctType}','03','50000','ST','','{account}')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,AcctType,Depot,Position,Location,SyncRef,ClntCode) VALUES ('O','601628','SHA','{AcctType}','03','50000','ST','','{account}')",
	]
	delSQL={
		'all':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}'",
		'US':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND Market='USA'",
		'HK':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND Market='HKG'",
		'SZ':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND Market='SZA'",
		'SA':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND Market='SHA'",
	}
	sqlDic={'US':USinsql,'HK':HKinsql,'SZ':SZinsql,'SH':SHinsql}
	if types=='all':
		sqlList=USinsql+HKinsql+SZinsql+SHinsql
	else:
		sqlList=sqlDic[types]
	if delOld:sqlList.insert(0,delSQL[types])
	return sqlList

def insertMoney(account,types='all',delOld=1):
	# 插入资金
	AcctType='MRGN' if 'M' in account.upper() else 'CUST'
	USinsql=[
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','USD','L','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','USD','O','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','USD','P','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
	]
	HKinsql=[
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','HKD','L','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','HKD','O','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','HKD','P','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
	]
	CNYinsql=[
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','CNY','L','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','CNY','O','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
		f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','CNY','P','HSBC',100000000,.00000000,.00000000,'',.00000000,.00000000,.00000000,.00000000)",
	]
	delSQL={
		'all':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}'",
		'USD':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND CCY='USD'",
		'HKD':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND CCY='HKD'",
		'CNY':f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}' AND CCY='CNY'",
	}
	sqlDic={'USD':USinsql,'HKD':HKinsql,'CNY':CNYinsql}
	if types=='all':
		sqlList=USinsql+HKinsql+CNYinsql
	else:
		sqlList=sqlDic[types]
	if delOld:sqlList.insert(0,delSQL[types])
	return sqlList

def insertFund(account):
	AcctType='MRGN' if 'M' in account.upper() else 'CUST'
	sqlList=[
		# 插入基金持仓
		# 516742 施罗德基金
		# 516749 霸凌环球资源基金
		f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}'",
		# f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,ClntCode,AcctType,Depot,Position,Location,SyncRef) VALUES ('L','516742','FUN','{account}','{AcctType}','03',100000,'ST','')",
		# f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,ClntCode,AcctType,Depot,Position,Location,SyncRef) VALUES ('O','516742','FUN','{account}','{AcctType}','03',100000,'ST','')",
		# f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,ClntCode,AcctType,Depot,Position,Location,SyncRef) VALUES ('P','516742','FUN','{account}','{AcctType}','03',100000,'ST','')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,ClntCode,AcctType,Depot,Position,Location,SyncRef) VALUES ('L','516749','FUN','{account}','{AcctType}','03',100000,'ST','')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,ClntCode,AcctType,Depot,Position,Location,SyncRef) VALUES ('O','516749','FUN','{account}','{AcctType}','03',100000,'ST','')",
		f"INSERT INTO ****.dbo.**** (BalanceType,Instrument,Market,ClntCode,AcctType,Depot,Position,Location,SyncRef) VALUES ('P','516749','FUN','{account}','{AcctType}','03',100000,'ST','')",
		# # 插入美元基金购买力
		# f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}'",
		# f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,TimeStamp,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','USD','L','HSBC',100000000.00000000,.00000000,.00000000,'',NULL,NULL,NULL,NULL,NULL)",
		# f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,TimeStamp,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','USD','O','HSBC',100000000.00000000,.00000000,.00000000,'',NULL,NULL,NULL,NULL,NULL)",
		# f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,TimeStamp,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','USD','P','HSBC',100000000.00000000,.00000000,.00000000,'',NULL,NULL,NULL,NULL,NULL)",
		# # 插入港元基金购买力
		# f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,TimeStamp,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','HKD','L','HSBC',100000000.00000000,.00000000,.00000000,'',NULL,NULL,NULL,NULL,NULL)",
		# f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,TimeStamp,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','HKD','O','HSBC',100000000.00000000,.00000000,.00000000,'',NULL,NULL,NULL,NULL,NULL)",
		# f"INSERT INTO ****.dbo.**** (ClntCode,AcctType,Market,CCY,BalanceType,Bank,Position,OpeningBalance,MTDInterest,SyncRef,TimeStamp,CreditInterest,DebitInterest,OverdueInterest,PenaltyInterest) VALUES ('{account}','{AcctType}','ALL','HKD','P','HSBC',100000000.00000000,.00000000,.00000000,'',NULL,NULL,NULL,NULL,NULL)",
	]
	return sqlList

def insertTradeHistory(account):
	# 插入交易历史
	AcctType='MRGN' if 'M' in account.upper() else 'CUST'
	sqlList=[f"DELETE FROM ****.dbo.**** WHERE ClntCode='{account}'"];BargainNo=11518850;Qty=600;Price=12.7;bs={0:'B',1:'S'}
	for i in range(5):
		date=time.strftime('%Y-%m-%d')
		sqlList.append(f"INSERT INTO ****.dbo.**** VALUES ('',{BargainNo},'','{bs[i%2]}','{account}','{AcctType}','{date} 00:00:00.000','{date} 00:00:00.000','00981','HKD','1.00000000','','HKG',{Qty},{Price},{Qty*Price},{Qty*Price+381},0.00000000,381.00000000,'',0.00000000,0.00000000,'616',0.05000000,'','','','SMIC')")
		BargainNo+=1;Qty+=100;Price+=1
	return sqlList

def delESOP(account,env='uat'):
	_dbName={'test':'test_****','uat':'****'}
	sqlList_abc=[
		f"DELETE FROM ****.dbo.Clnt WHERE ClntCode LIKE '%{account}%' AND ClntCode!='{account}' AND ClntCode!='M{account}'",#ABC数据库
		f"DELETE FROM ****.dbo.**** WHERE ClntCode LIKE '%{account}%' AND ClntCode!='{account}' AND ClntCode!='M{account}'",#ABC数据库
	]
	sqlList_SZ=[
		f"DELETE FROM {_dbName[env]}.T_CUSTOMER_ACCOUNT_INFO WHERE ACCOUNT_NO LIKE '%{account}%' AND ACCOUNT_NO!='{account}' AND ACCOUNT_NO!='M{account}'",#UAT数据库
	]
	return sqlList_abc,sqlList_SZ

def insertIPO(stockCode,stockName,env='uat'):
	try:
		int(stockCode)
	except ValueError:
		print(f'输入的股票代码有误: {stockCode}')
		sys.exit(0)
	id0=time.strftime('%Y%m%d%H%M%S')
	publishId=f'{id0}96'
	cmbi_deadline=(datetime.date.today()+datetime.timedelta(days=365)).isoformat()
	cancel_deadline=(datetime.date.today()+datetime.timedelta(days=370)).isoformat()
	stock_pub_date=(datetime.date.today()+datetime.timedelta(days=375)).isoformat()

	dbNameDic={'test':'test_cmbi_ipo','uat':'cmbi_ipo'}
	# ipoNo=str(int(getMaxStockpubNo(env,dbNameDic[env]))+1)

	sqlList=[
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PUBLISH_INFO (id,stock_code,stock_name,financing_fee,cash_fee,publish_status,is_sponsor,is_consignee,sort_weight,cmbi_deadline,cancel_deadline,broker_start_time,broker_end_time,stock_pub_eipo_no,result_pub_date,is_valid,created_by,created_at,updated_by,updated_at,publish_date) VALUES ({publishId},'{stockCode}','{stockName}','100.0000','30.0000','WAIT_PUB',NULL,NULL,NULL,'{cmbi_deadline} 16:00:00','{cancel_deadline} 00:00:00',NOW(),'{cancel_deadline} 00:00:00',NULL,'{cancel_deadline} 00:00:00','UP','SYSTEM',NOW(),'SYSTEM',NOW(),NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_DETAIL (id,stock_code,stock_name,currency_unit,trade_unit,subscribe_vol,subscribe_price,prospectus_pub_date,subscribe_start_date,subscribe_end_date,listed_date,entrance_fee,pricing_date,pay_end_date,result_pub_date,stock_pub_date,refundment_date,total_proceeds,pur_price_interval,over_allotment,over_allot_apply_mul,one_lot_winning_rate,event_procedure,issue_type,public_date,jy_update_date,website,is_valid,created_by,created_at,updated_by,updated_at) VALUES ({id0},'{stockCode}','{stockName}','HKD','2000','375000000',NULL,NOW(),NOW(),'{cmbi_deadline} 16:00:00','{cmbi_deadline}','7000.0000','{cmbi_deadline}','{cmbi_deadline} 12:00:00','{cancel_deadline}','{stock_pub_date}','{stock_pub_date}','134062500.00','3.5~4.0','6286600',NULL,NULL,'PREARRANGED','公开发售 配售新股',NOW(),NOW(),'http://10.0.2.83/index.html','Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_CAPITAL_POOL (id,publish_id,financing_program_id,stock_code,stock_name,currency_unit,total_amount,cmbi_financing_amount,used_amount,usage_alert_line,financing_scale_max,financing_scale_min,apply_end_date,reason,pool_status,is_app_fin,fin_limit,created_by,created_at,updated_by,updated_at) VALUES ({id0}95,'{publishId}',NULL,'{stockCode}','{stockName}','HKD','0.0000','0.0000','0.0000','95.0000','90.0000','5.0000','{cmbi_deadline} 16:00:00','INIT_CLOSE','CLOSE',1,NULL,'AutoTest',NOW(),'AutoTest',NOW());",
		# f"INSERT INTO {dbNameDic[env]}.T_EIPO_FINANCING_RATE_PROGRAM (id,program_name,program_desc,is_valid,created_by,created_at,updated_by,updated_at) VALUES ({id0}99,'{stockCode}','{stockName}','Y','148',NOW(),'148',NOW())",
		# f"INSERT INTO {dbNameDic[env]}.T_EIPO_FINANCING_RATE_PROGRAM_DETAIL (id,program_id,serial_no,financing_amount_min,financing_amount_max,financing_rate,created_by,created_at,updated_by,updated_at) VALUES ({id0}97,'{id0}99','1','0.0000','1000000.0000','2.0000','148',NOW(),'148',NOW())",
		# f"INSERT INTO {dbNameDic[env]}.T_EIPO_FINANCING_RATE_PROGRAM_DETAIL (id,program_id,serial_no,financing_amount_min,financing_amount_max,financing_rate,created_by,created_at,updated_by,updated_at) VALUES ({id0}98,'{id0}99','2','1000000.0000','999999999.9900','5.0000','148',NOW(),'148',NOW())",

		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}01','{stockCode}','{stockName}','1','2000.0000','0.0000','7000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}02','{stockCode}','{stockName}','2','4000.0000','0.0000','14000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}03','{stockCode}','{stockName}','3','8000.0000','0.0000','28000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}04','{stockCode}','{stockName}','4','16000.0000','0.0000','56000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}05','{stockCode}','{stockName}','5','32000.0000','0.0000','112000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}06','{stockCode}','{stockName}','6','64000.0000','0.0000','224000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}07','{stockCode}','{stockName}','7','128000.0000','0.0000','448000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}08','{stockCode}','{stockName}','8','256000.0000','0.0000','896000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}09','{stockCode}','{stockName}','9','512000.0000','0.0000','1792000.0000','HKD','N',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
		f"INSERT INTO {dbNameDic[env]}.T_EIPO_STOCK_SUBSCRIBE_PROGRAM (id,stock_code,stock_name,serial_number,apply_subscribe_num,apply_num_rate,pay_able,currency_unit,is_can_apply_max,public_date,jy_update_date,is_valid,created_by,created_at,updated_by,updated_at) VALUES ('{id0}10','{stockCode}','{stockName}','10','1024000.0000','0.0000','3584000.0000','HKD','Y',NOW(),NOW(),'Y','SYSTEM',NOW(),'SYSTEM',NOW());",
	]
	return publishId,cmbi_deadline,sqlList

def querySSN(account):
	return f"SELECT Residentid FROM ****.dbo.**** WHERE ClntCode='{account}'"

def getEmailCode(email,env='uat',n=None):
	if n:return '8'*n
	sql=f"SELECT code,create_time FROM zygj.msg_verify_code WHERE account='{email}' ORDER BY create_time DESC"
	for i in range(10):
		results=excuteSQL(sql,dbType='mysql',env=env)
		for item in results:
			if int(time.time())-time.mktime(time.strptime(item[1],'%Y-%m-%d %X'))<300:
				return item[0]
		print('数据库中未查询到验证码，1秒后重试')
		time.sleep(1)
	raise Exception(f'{email} 从数据库查询验证码失败！')

def delRegisterInfo(mobile,env='uat'):
	_dbName={'test':'test_base_plat','uat':'base_plat'}
	print(f'开始删库……')
	operator_no=excuteSQL(f'SELECT OPERATOR_NO FROM {_dbName[env]}.T_CUSTOMER_LOGIN_INFO WHERE  LOGIN_NAME={mobile}',env=env)[0][0]
	customer=excuteSQL(f'SELECT CUSTOMER_NO FROM {_dbName[env]}.T_CUSTOMER_OPERATOR t2 WHERE t2.OPERATOR_NO={operator_no}',env=env)[0][0]

	sqlDel_DataBase=[
		f'DELETE FROM ****.**** WHERE mobile={mobile}',
		f'DELETE FROM ****.**** WHERE mobile={mobile}'
	]
	sqlDels=[
		f'DELETE FROM {_dbName[env]}.T_CUSTOMER_OPERATOR_CONTACT WHERE tel={mobile}',
		f'DELETE FROM {_dbName[env]}.T_CUSTOMER_LOGIN_INFO WHERE OPERATOR_NO={operator_no}',
		f'DELETE FROM {_dbName[env]}.T_CUSTOMER_OPERATOR WHERE OPERATOR_NO={operator_no}',
	]
	if customer:
		account_no=excuteSQL(f'SELECT ACCOUNT_NO FROM {_dbName[env]}.T_CUSTOMER_ACCOUNT_INFO WHERE CUSTOMER_NO={customer}',env=env)[0][0]
		sqlDels=sqlDels+[
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_RECOMMEND_INFO WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_STATEMENT WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_TEST_RESULT WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_ACCOUNT_INFO WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_ATTACHMENT WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_BASE_INFO WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_CERTIFICATE WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_CONTACT WHERE CUSTOMER_NO={customer} ',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_CRS WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_STATEMENT WHERE CUSTOMER_NO={customer}',
			f'DELETE FROM {_dbName[env]}.T_CUSTOMER_RECOMMEND_INFO WHERE CUSTOMER_NO={customer}',
		]
		if account_no:sqlDels.append(f'DELETE FROM {_dbName[env]}.T_CUSTOMER_ACCOUNT_INFO_DETAIL WHERE ACCOUNT_NO={account_no}')
	excuteSQL(sqlDel_DataBase+sqlDels,env=env)
	print(f'删库完成')

def recoverStaticInfo(account):
	data={
		"290522":"UPDATE ****.dbo.**** SET Name='CATHERINE COLEMAN',CName=N'劉梅',AECode='636',Prefix='Mr',Mobile=N'13853535966',Email=N'760844602@qq.com',PB='Y',PI='Y',MobCountry=N'86',Residentid=N'350322196704250844',InternationalID=N'350322196704250844',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='CUST',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'湖南省秀榮縣和平北京街l座 847882' WHERE ClntCode='290522';",
		"290523":"UPDATE ****.dbo.**** SET Name='ADRIAN GOULD',CName=N'魏紅',AECode='636',Prefix='Mr',Mobile=N'15572374377',Email=N'2294579303@qq.com',PB='Y',PI='Y',MobCountry=N'86',Residentid=N'360601200108272049',InternationalID=N'360601200108272049',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='CUST',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'陝西省楊縣徐彙北京街I座 648467' WHERE ClntCode='290523';",
		"511682":"UPDATE ****.dbo.**** SET Name='AUTOTEST',CName=N'autoTest',AECode='988',Prefix='Mr',Mobile=N'13207165870',Email=N'2806646694@qq.com',PB='N',PI='N',MobCountry=N'86',Residentid=N'646xxxresidentid',InternationalID=N'xxxinternationalid',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2019-10-21 00:00:00.000',AcCategory='Individual',AcctType='CUST',ResidenceCnty='CHN',Birthday=N'30 Jan 1994',Address=N'XXXXXXXXX' WHERE ClntCode='511682';",
		"511703":"UPDATE ****.dbo.**** SET Name='autoTxxxename',CName=N'axxxcName',AECode='988',Prefix='Mr',Mobile=N'13207165871',Email=N'XXX@XXXX.XX',PB='N',PI='N',MobCountry=N'86',Residentid=N'216xxxresidentid',InternationalID=N'xxxinternationalid',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2019-10-29 00:00:00.000',AcCategory='Individual',AcctType='CUST',ResidenceCnty='CHN',Birthday=N'30 Jan 1994',Address=N'XXXXXXXXX' WHERE ClntCode='511703';",
		"700876":"UPDATE ****.dbo.**** SET Name='CHRISTINE DIAZ',CName=N'嚴偉',AECode='988',Prefix='Mr',Mobile=N'15541956697',Email=N'1455164180@qq.com',PB='N',PI='N',MobCountry=N'86',Residentid=N'542527200202039060',InternationalID=N'542527200202039060',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='CUST',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'山西省豔市雙灤施路v座 863441' WHERE ClntCode='700876';",
		"700877":"UPDATE ****.dbo.**** SET Name='TRACI KERR',CName=N'王佳',AECode='988',Prefix='Mr',Mobile=N'15006336797',Email=N'979632830@qq.com',PB='N',PI='N',MobCountry=N'86',Residentid=N'230602198306136811',InternationalID=N'230602198306136811',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='CUST',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'安徽省蘭州市清浦杭州街W座 652388' WHERE ClntCode='700877';",
		"M290522":"UPDATE ****.dbo.**** SET Name='CATHERINE COLEMAN',CName=N'劉梅',AECode='636',Prefix='Mr',Mobile=N'13853535966',Email=N'760844602@qq.com',PB='Y',PI='Y',MobCountry=N'86',Residentid=N'350322196704250844',InternationalID=N'350322196704250844',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='MRGN',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'湖南省秀榮縣和平北京街l座 847882' WHERE ClntCode='M290522';",
		"M290523":"UPDATE ****.dbo.**** SET Name='ADRIAN GOULD',CName=N'魏紅',AECode='636',Prefix='Mr',Mobile=N'15572374377',Email=N'2294579303@qq.com',PB='Y',PI='Y',MobCountry=N'86',Residentid=N'360601200108272049',InternationalID=N'360601200108272049',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='MRGN',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'陝西省楊縣徐彙北京街I座 648467' WHERE ClntCode='M290523';",
		"M511682":"UPDATE ****.dbo.**** SET Name='autoTxxxename',CName=N'axxxcName',AECode='988',Prefix='Mr',Mobile=N'13207165870',Email=N'2806646694@qq.com',PB='N',PI='N',MobCountry=N'86',Residentid=N'646xxxresidentid',InternationalID=N'xxxinternationalid',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2019-10-21 00:00:00.000',AcCategory='Individual',AcctType='MRGN',ResidenceCnty='CHN',Birthday=N'30 Jan 1994',Address=N'XXXXXXXXX' WHERE ClntCode='M511682';",
		"M511703":"UPDATE ****.dbo.**** SET Name='autoTxxxename',CName=N'axxxcName',AECode='988',Prefix='Mr',Mobile=N'13207165871',Email=N'XXX@XXXX.XX',PB='N',PI='N',MobCountry=N'86',Residentid=N'216xxxresidentid',InternationalID=N'xxxinternationalid',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2019-10-29 00:00:00.000',AcCategory='Individual',AcctType='MRGN',ResidenceCnty='CHN',Birthday=N'30 Jan 1994',Address=N'XXXXXXXXX' WHERE ClntCode='M511703';",
		"M700876":"UPDATE ****.dbo.**** SET Name='CHRISTINE DIAZ',CName=N'嚴偉',AECode='988',Prefix='Mr',Mobile=N'15541956697',Email=N'1455164180@qq.com',PB='N',PI='N',MobCountry=N'86',Residentid=N'542527200202039060',InternationalID=N'542527200202039060',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='MRGN',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'山西省豔市雙灤施路v座 863441' WHERE ClntCode='M700876';",
		"M700877":"UPDATE ****.dbo.**** SET Name='TRACI KERR',CName=N'王佳',AECode='988',Prefix='Mr',Mobile=N'15006336797',Email=N'979632830@qq.com',PB='N',PI='N',MobCountry=N'86',Residentid=N'230602198306136811',InternationalID=N'230602198306136811',RegistrationNo=N'xxxregistrationNo',Active='Yes',OpenDate='2020-03-23 00:00:00.000',AcCategory='Individual',AcctType='MRGN',ResidenceCnty='CHN',Birthday=N'01 Jun 1984',Address=N'安徽省蘭州市清浦杭州街W座 652388' WHERE ClntCode='M700877';",
	}
	try:
		return data[account]
	except KeyError:
		return ''

def getMaxStockpubNo(env,dbName):
	sql=f'SELECT stock_pub_eipo_no FROM {dbName}.T_EIPO_STOCK_SUBSCRIBE_PUBLISH_INFO ORDER BY stock_pub_eipo_no DESC LIMIT 1;'
	result=excuteSQL(sql,dbType='mysql',env=env)
	return result[0][0]

def setBCANID(account):
	#开通中华通交易权限
	sqls=[
		f"Delete from ****.dbo.DefinedSettings Where SettingName='BCAN ID' and TableName='Clnt' and TableKey1='{account}';",
		f"Insert into ****.dbo.DefinedSettings (TableName,SettingName,TableKey1,TableKey2,TableKey3,TableKey4,TableKey5,SettingValue,SyncRef) Values ('Clnt','BCAN ID','{account}','','','','','1000100107','Target');"
	]
	return sqls

def get_cardID(uname,env='test'):
	check_sql=f"SELECT Residentid FROM ****.dbo.**** WHERE ClntCode='{uname}';"
	result=excuteSQL(check_sql,dbType='sqlserver',env=env)
	return result
	
def changeChannel(env,channel='TTL'):
	tableName={'dev':'dev_cmbi_boss','test':'test_cmbi_boss','uat':'cmbi_boss'}
	conn=getDBconn('mysql',env=env,host='192.168.99.124',user='root',password='9d0vWBBo3MU14XS')
	now=time.strftime("%Y-%m-%d %X")
	sql=f"UPDATE {tableName[env]}.master_setting SET key_value='{channel.upper()}',update_time='{now}' WHERE id=14;"
	excuteSQL(sql,conn=conn)

def del_pwdHistory(account,env='uat'):
	sql=f"DELETE FROM ****.dbo.ClntPasswordsReuseHistory WHERE ClntCode='{account}';"
	result=excuteSQL(sql,dbType='sqlserver',env=env)
	return result

def del_market(account,env='test',conn=None):
	if not conn:conn=getDBconn('mysql',env=env,host='192.168.99.147',user='cms',password='RviKVewmNsN2Xnt',port=8066)
	tableName={'dev':'dev_cmbi_boss','test':'test_cmbi_boss','uat':'cmbi_boss'}
	sql=f"DELETE FROM {tableName[env]}.cms_account_market WHERE accountid='{account}' AND market!='HKG';"
	conn=excuteSQL(sql,conn=conn,keepLive=1)
	return conn

def get_cifNo(account,env='uat'):
	conn=getDBconn('mysql',env=env,host='192.168.99.65',user='root',password='9d0vWBBo3MU14XS')
	sql=f'SELECT cif_no FROM cmbi_boss.cms_client WHERE client_code="{account}";'
	result=excuteSQL(sql,conn=conn,keepLive=0)
	return result[0][0]

def reset_certifi(account,env='uat'):
	certifi_dic={
		'706158':'B9612632',
		'706159':'U7213236',
		'706160':'X6166062',
		'292231':'Z1295641',
		'292232':'H9214854',
		'292233':'X7251772',
	}
	cif_no=get_cifNo(account,env)
	sql=f"UPDATE cmbi_boss.cms_client_certificate SET certificate_no='{certifi_dic[account]}' WHERE cif_no='{cif_no}' AND certificate_type='Hongkong ID';"
	conn=getDBconn('mysql',env=env,host='192.168.99.65',user='root',password='9d0vWBBo3MU14XS')
	excuteSQL(sql,conn=conn,keepLive=0)


# UPDATE ****.dbo.**** SET AcCategory='Individual' WHERE ClntCode='511682';
if __name__=='__main__':
	# changeChannel('test',channel='ABC')
	# del_market('801150',env='uat',conn=None)
	# print(get_cifNo('292233'))
	print(reset_certifi('292233'))