import argparse,time,logging,traceback
from config import newPwd
from business.reg import regWeb
from business.reg_api import reg_api

from common.tools import saveFile
from common.dbOperation import excuteSQL
from common.system_boss import getCasherDeposite,approve_submit,changeChannel
from common.system_openbo import getCheckID,checkBO,manualActivate,amlTable,piDocument
from common.apiCenter import add_ttlhuidu,submitDeposite,login_acc,w8Submit,openMarket,setPwdTel,resetpwd

def getParserReg():
	parser=argparse.ArgumentParser(description='壹隆环球Web自动开户',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-e',dest='env',help="指定环境（默认uat）:\n\ttest\ttest环境\n\tuat\tuat环境",required=False,default='uat')
	parser.add_argument('-l',dest='location',help="指定地区（默认 zh_CN）:\n\tzh_CN\t中国内地\n\tzh_HK\t中国香港",required=False,default='zh_CN')
	parser.add_argument('-t',dest='tel',help="指定开户手机号（默认随机生成一个）",required=False,default='')
	parser.add_argument('--email',help="指定邮箱（默认随机生成一个）",required=False,default='')
	parser.add_argument('--pi',help="专业投资者开户",action='store_true',required=False)
	parser.add_argument('--margin',help="勾选保证金账户（可抵押融资买卖股票）",action='store_true',required=False)
	parser.add_argument('--check',help="自动审核",action='store_true',required=False)
	parser.add_argument('--active',help="审核完成后自动激活(专业投资者账户无需选此项，会自动激活)",action='store_true',required=False)
	parser.add_argument('--setPwd',help="激活后自动修改密码",action='store_true',required=False)
	parser.add_argument('--ttl',help="开ttl账户",action='store_true',required=False,default=1)
	parser.add_argument("--headless",help=argparse.SUPPRESS,action='store_true',required=False)
	parser.add_argument("--regbyapi",help=argparse.SUPPRESS,action='store_true',required=False)

	args=parser.parse_args()
	return args

def main(args):
	start=time.perf_counter()
	areaCodeDic={'zh_CN':'86','zh_HK':'852'}
	args.areaCode=areaCodeDic[args.location]
	args.margin=1 if args.margin else 0
	if args.regbyapi:
		args=reg_api(args)
	else:
		args=regWeb(args)
	acc_type='ttl' if args.ttl else 'abc'
	if args.check:
		logging.info('开始审核……')
		checkID=0
		end=4
		for i in range(1,end):
			if i==2:
				amlTable(checkID,args.env)#反洗钱表格
				if args.pi:piDocument(checkID,args.env)#补充PI资料
			if i==end-1:changeChannel(acc_type,args.env)
			checkID=checkBO(args.tel,i,checkID,args.env)
		saveFile('审核完成！')
		active=0
		if args.pi:
			#专业投资者无激活这一步骤，审核完就是已激活状态
			saveFile('激活完成！')
			active=1
		else:
			if args.active:
				manualActivate(checkID,args.env)
				saveFile('激活完成！')
				active=1
		if active:
			accList=getCheckID(search2=args.tel,getAcclist=1,env=args.env)
			saveFile(f'{args.tel} 对应户口号 {" ".join(accList)}')
			args.acc=[i for i in accList if 'M' not in i][0]
			try:args.Macc=[i for i in accList if 'M' in i][0]
			except IndexError:args.Macc=''
				
			if args.setPwd:
				for _acc in accList:
					for n in range(5):
						result=resetpwd(_acc,newPwd,args.env,args.ttl)
						if result['result']!='1':
							logging.info(f'{_acc} 第{n}次重置密码失败: {result}')
							if '不能为空' in str(result) or 'Invalid login ID or password' in str(result):
								time.sleep(10)
							else:
								time.sleep(1)
							continue
						try:
							sessionDic=login_acc(_acc,newPwd,args.env,args.ttl)
							if sessionDic:
								sessionDic['enName']=args.enName
								saveFile(f'{_acc} 已重置密码为 {newPwd}')
							break
						except Exception:
							logging.info(f'{_acc} 第{n}次重置密码后登陆失败')
							if n==4:raise Exception
					# if args.ttl:
					# 	# add_ttlhuidu(accList,args.env)# 添	加灰度
					# 	# 资金存入
					# 	for curr in ['HKD','USD','CNY']:
					# 		submitDeposite(sessionDic,curr,args.env)
					# 		saveFile(f'{_acc} 存入 {curr} 成功',0)
					# 	# 资金存入审核
					# 	approveIdList=getCasherDeposite(_acc,args.env)
					# 	approve_submit(approveIdList,args.env)
					# 提交w8
					w8Submit(sessionDic,args.env)
					saveFile(f'{_acc} 提交w8成功',0)
					# 开通市场
					openMarket(sessionDic,args.env)
					saveFile(f'{_acc} 开通市场成功',0)
				#设置手机账号 登录密码
				status,reason=setPwdTel(args,newPwd)
				if status:
					saveFile(f'{args.tel} 设置密码成功 新密码 {newPwd}')
				else:
					logging.info(f'{args.tel} 设置密码失败 {reason}')
		create_at=time.strftime('%Y-%m-%d %X')
		is_pi=1 if args.pi else 0
		saveSQL=f"INSERT INTO interfaceTest_data.regInfo (acc_type,create_at,env,is_pi,acc,acc_pwd,Macc,Macc_pwd,phone,email,cn_name,en_name,card_id,birth_date) VALUES ('{acc_type}','{create_at}','{args.env}',{is_pi},'{args.acc}','{newPwd}','{args.Macc}','{newPwd}','{args.tel}','{args.email}','{args.cnName}','{args.enName}','{args.cardID}','1984-06-01');"
		excuteSQL(sql=saveSQL,env='test')
	t=time.strftime('%M{m}%S{s}',time.gmtime(time.perf_counter()-start)).format(m='分',s='秒')
	saveFile(f"用时：{t}\n----- 开户完成! {time.strftime('%Y-%m-%d %X')} -----\n")
	return args



if __name__=="__main__":
	args=getParserReg()
	try:
		main(args)
	except:
		traceback.print_exc()
		saveFile('\n',0)
	# respJson=resetpwd('800395','aaaa1111',env='uat',types='abc')
	# print(respJson)
