from common.dbOperation import *
import argparse,logging

def getParser():
	parser=argparse.ArgumentParser(description='本程序用于执行各种SQL',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="指定环境（默认 uat ）:\n\tuat\tUAT环境\n\ttest\tTEST环境",required=False,default='uat')
	parser.add_argument('-a',dest='action',help="指定需要执行的操作（默认 12346 ）:\n\t1\t加持仓\n\t2\t加资金\n\t3\t加基金持仓\n\t4\t加交易历史\n\t5\t插入新股IPO\n\t6\t删除ESOP或其它多余的账户\n\t7\t查询账户身份证\n\t8\t删除手机号对应的开户数据（使用-u参数指定手机号）\n\t9\t恢复账户静态表数据（目前仅支持 511682 700876 700877 511703 290522 290523 290525）\n\t0\t开通中华通交易权限",required=False,default="12346")
	parser.add_argument('-u',dest='uname',help='指定需要操作的账户号（默认 "511682 700876 700877 511703 290522 290523 290525 706158 706159 706160 292231 292232 292233" ）',required=False,default="511682 700876 700877 511703 290522 290523 290525 706158 706159 706160 292231 292232 292233")
	parser.add_argument('-stockName',help="指定新股名称，不指定则随机生成",required=False,default='')
	parser.add_argument('-stockCode',help="指定新股代码，不指定则随机生成",required=False,default='')
	args=parser.parse_args()
	return args

if __name__=='__main__':
	start=time.perf_counter()
	args=getParser()
	args.env=args.env.lower()
	sqlList_abc=[];sqlList_SZ=[]
	accounts=args.uname.split()
	##############################################################################################
	for acc in accounts:
		if '1' in args.action:sqlList_abc.extend(insertStock(acc))# 加持仓
		if '2' in args.action:sqlList_abc.extend(insertMoney(acc))# 加资金
		if '3' in args.action:sqlList_abc.extend(insertFund(acc))# 加基金持仓
		if '4' in args.action:sqlList_abc.extend(insertTradeHistory(acc))# 加交易历史
		if '6' in args.action:
			_abc,_SZ=delESOP(acc,args.env)# 删除ESOP或其它多余的账户
			sqlList_abc.extend(_abc);sqlList_SZ.extend(_SZ)
		if '9' in args.action:sqlList_abc.append(recoverStaticInfo(acc))
		if '0' in args.action:sqlList_abc.extend(setBCANID(acc))
	if '5' in args.action:
		fake=faker.Faker('zh-CN')
		if not args.stockCode:args.stockCode=f'98{fake.random_int()}'
		if not args.stockName:
			args.stockName=fake.company_prefix()
			if len(args.stockName)==2:
				suffix=['股份','集团','科技','医药','时代','数码']
				args.stockName=f'{args.stockName}{choice(suffix)}'
		publishId,cmbi_deadline,sqlList_SZ=insertIPO(args.stockCode,args.stockName,args.env)
	if args.action=='7':
		sql_abc=querySSN(accounts[0])
		result=excuteSQL(sql_abc,dbType='sqlserver',env=args.env)
		print(f"{accounts[0]} 的证件ID为: {result[0][0]}")
	elif args.action=='8':
		delRegisterInfo(accounts[0],env=args.env)
	##############################################################################################
	if sqlList_abc:excuteSQL(sqlList_abc,dbType='sqlserver',env=args.env)
	if sqlList_SZ:excuteSQL(sqlList_SZ,dbType='mysql',env=args.env)
	if '5' in args.action:
		print(f"{args.env} 环境添加新股: {args.stockCode} {args.stockName} 成功")
		
		# from common.getCode_boss import releaseIPO,eipoSavePool,savePoolGradient
		# if savePoolGradient(publishId,args.stockCode,args.stockName,args.env):
		# 	if eipoSavePool(publishId,f'{cmbi_deadline} 16:00',args.env):
		# 		if releaseIPO(publishId,args.stockCode,args.env):
		# 			print(f"{args.env} 环境新股: {args.stockCode} {args.stockName} 自动发布成功")

	t=round(time.perf_counter()-start,3)
	print(f'恭喜!操作成功! 用时 {t} 秒')