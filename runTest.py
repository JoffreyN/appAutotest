import HTMLReport,time,os,logging,argparse,traceback,threading
from uuid import uuid4
from testSuite.suite import *

from common.tools import getDriver,sendMail,moveFiles,getCapability,replaceVideolog
from common.apiCenter import login_acc,cardOperate,signAgreement,openMarket
from common.dbOperation import reset_certifi
from business.checkVerEnv import checkVerEnv
from business.others import reOpenApp
from testData.data import accountPool
from config import *

def getParser():
	parser=argparse.ArgumentParser(description='壹隆环球APP自动化测试',formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-ip',dest='appiumHost',help="指定appium服务地址(默认 127.0.0.1)",required=False,default='127.0.0.1')
	parser.add_argument('-p',dest='appiumPort',help="指定appium服务端口(默认 4723)",required=False,default='4723')
	parser.add_argument('-WDAP',help="[iOS专用]指定WebDriverAgent服务端口",required=False,default=None)
	parser.add_argument('-iosAppPath',help="[iOS专用]指定app路径",required=False,default=None)
	# parser.add_argument('-bundleId',help="[iOS专用]指定app的bundleId",required=False,default='com.cmbi.zytxEt')
	parser.add_argument('-platformVersion',help="[iOS专用]指定iOS版本(默认 13.7)",required=False,default='13.7')
	parser.add_argument('-i',dest='deviceName',help="指定测试设备:\n\t192.168.56.104:5555\n\t192.168.56.105:5555\n\t192.168.56.106:5555\n\tiPhone 11 Pro Max\n\tiPhone 11 Pro\n\tiPhone 11",required=True)
	parser.add_argument('-a',dest='account',help="指定测试现金账户号",required=False,default=None)
	parser.add_argument('-v',dest='cusVer',help="指定需要测试的APP版本号，未指定则用当前版本",required=False)
	parser.add_argument('-e',dest='env',help="指定运行环境(默认 UAT)：\n\tUAT\tUAT环境\n\tTEST\tTEST环境",required=False,default='uat')
	parser.add_argument('-s',dest='suite',help="指定需要执行的用例集(默认 all):\n\tall\t\t所有用例集\n\tlogin\t\t登录用例集\n\ttradeFund\t基金交易用例集\n\ttrade\t\t股票交易用例集\n\tcurrExchange\t货币兑换用例集\n\tmore\t业务办理用例集\n\tmy\t\t我的模块用例集\n\tregister\t开户注册用例集\n\thomeNews\t首页相关用例集\n\tmarket\t\t行情相关用例集\n\taccUIview\t账户UI总览",required=False,default='all')
	# parser.add_argument('--skip',help="指定跳过用例或用例集",required=False,default='')
	parser.add_argument('--sendMail',help="自动发送邮件",action='store_true',required=False)
	parser.add_argument("--receiver",help=argparse.SUPPRESS,required=False)
	parser.add_argument("--fromInfo",help=argparse.SUPPRESS,required=False)
	# parser.add_argument('--autoUpdate',help="自动更新最新版app",action='store_true',required=False)
	# parser.add_argument("--skipCurBoss",help='跳过货币兑换boss部分',action='store_true',required=False)
	# parser.add_argument("--skipRegweb",help='跳过站外开户部分',action='store_true',required=False)
	parser.add_argument("--ttl",help='账户类型为TTL',action='store_true',required=False)
	parser.add_argument("--debug",help='debug模式',action='store_true',required=False)
	args=parser.parse_args()
	return args

def main():
	for i in range(100):
		try:
			sessionDic=login_acc(args.account,accountPool[args.account][0],env=args.env,ttl=args.ttl)
			break
		except:
			if i==99:raise Exception(f'登录失败！')
	threading.Thread(target=cardOperate,args=(sessionDic,args.env,)).start()#港股行情卡
	threading.Thread(target=signAgreement,args=(sessionDic,args.env,)).start()#美股行情卡
	threading.Thread(target=openMarket,args=(sessionDic,args.env,)).start()#开通市场

	reset_certifi(args.account,args.env)

	_s=args.deviceName[7:].replace(' ','_') if 'iPhone' in args.deviceName else args.deviceName[11:14]
	args.timeStr=f"{time.strftime('%Y%m%d%H%M%S')}_{str(uuid4())[:6]}_{_s}"
	capability=getCapability(args)
	appiumUrl=f'http://{args.appiumHost}:{args.appiumPort}/wd/hub'
	driver=getDriver(capability,appiumUrl);reopen=0

	for i in range(5):
		try:
			args.appVersion,reopen=checkVerEnv(driver,capability,args)
			break
		except TimeoutError:
			logging.info(f'检测环境及版本失败，1秒后开始第 {i+1} 次重试...')
			time.sleep(1)
		except AttributeError:
			logging.info(f'检测环境及版本失败，1秒后重启并开始第 {i+1} 次重试...')
			time.sleep(1)
			reOpenApp(driver)
	if reopen:reOpenApp(driver)
	suites=loadSuite(driver,args)
	print(suites)
	# sys.exit(0)

	platformName=driver.capabilities['platformName']
	reportURL=f'{host}/{args.timeStr}'
	HTMLReport.TestRunner(
		title="壹隆环球APP自动化测试报告",
		description=f'运行环境: <span class="info">{args.env.upper()}</span><br/>app版本: <span class="info">{platformName} {args.appVersion}</span><br/>设备信息: <span class="info">{args.deviceName}</span><br/>使用账户: <span class="info">{args.account}</span>',
		output_path=f'report/{args.timeStr}',
		report_file_name='index',
		sequential_execution=True,#按照套件添加(addTests)顺序执行
		tries=2,delay=3,retry=1,
	).run(suites)
	driver.terminate_app(driver.capabilities['app_id'])
	driver.quit()

	replaceVideolog(args.timeStr)
	try:
		moveFiles(args.timeStr,'copy')
	except:
		traceback.print_exc()

	print('报告链接：',reportURL)
	# if platform=='darwin':
	# 	os.system(f'open {reportURL}')
	# elif platform=='win32':
	# 	os.system(f'start {reportURL}')
	# else:
	# 	print('platform:',platform)

	if args.sendMail:
		# <p style="font-size:x-small;text-align:right;">本邮件由appAutoTest自动发送</p><br/>
		foot=f'<p>网页版请<a href="{reportURL}">点击这里</a>查看(提示：请用 CMBI 网络访问)</p><br/>'
		text=open(os.path.expanduser(os.path.join(webPath,args.timeStr,'index.html')),'r',encoding='utf-8').read()
		sendMail(f'{foot}{text}',platformName,fromInfo=args.fromInfo,cusReceiver=args.receiver)
	return reportURL,args.timeStr

if __name__=='__main__':
	args=getParser()
	args.env=args.env.lower()
	# logging.info(f'{args.sendMail}')
	reportURL,timeStr=main()
