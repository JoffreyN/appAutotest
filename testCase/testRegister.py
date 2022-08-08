import time,logging,unittest,traceback
from HTMLReport import no_retry

from page.mine.my import PageMy
from page.navBar import PageBar
from page.alert import PageAlert
from page.home.home import PageHome
from page.uploadPic import PageUploadPic
from page.register.register_web import PageRegisterWeb
from page.mine.businesWeek.riskAssessment import PageRiskAss
from page.mine.changePwd import PageChangePwd

from business.logInOut import login,logout
from business.reg_futures_api import reg_futures_api
from business.reg_api import reg_api_second

from common.tools import swithToRightWeb
from common.parameter import ParameTestCase
from common.apiCenter import setPwdTel
from common.system_boss import getSMScode,getMailRecord,getPwd_from_mail,login_boss
from common.system_openbo import delAccount,loginBO,checkBO,manualActivate,getCheckID,sendWelcome

from testData.data import regInfo,regData

from regWeb import main as regWeb_main

# @unittest.skip('跳过')
class TestRegister(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 开户注册 模块测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageChangePwd=PageChangePwd(cls.driver)
		loginBO(cls.args.env)
		login_boss(cls.args.env)

	def setUp(self):
		pass


	# @unittest.skip('跳过')
	# @no_retry
	def test_01_CMBI_241(self):
		'''开户后用初始密码登录并修改密码'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-241 开户后用初始密码登录并修改密码 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		self.args.margin=False
		self.args.check=True
		self.args.active=True
		self.args.headless=True
		self.args.regbyapi=True
		self.args.setPwd=False
		self.args.pi=False
		self.args.location='zh_CN'
		self.args.tel=None
		self.args.email=None
		self.args=regWeb_main(self.args)
		status,reason=setPwdTel(self.args,'****')
		
		logging.info(f'{self.args.tel}对应户口号: {self.args.acc}')
		# for account in [self.args.acc,self.args.Macc]:
		account=self.args.acc
		logout(self.driver)
		mailid=getMailRecord(account,env=self.args.env,keyword='默认激活码',timeLimit=18000)[0][-1]
		firstpwd=getPwd_from_mail(mailid,env=self.args.env,mod='first')
		logging.info(f'{account} 初始密码: {firstpwd}')

		login(self.driver,(account,firstpwd),args=self.args,acc=0,needNickname=0)
		time.sleep(3)
		swithToRightWeb(self.driver,'/settle/firstLogin')
		self.__class__.pageChangePwd.inputOldPwd(firstpwd,self.args.ttl)
		self.__class__.pageChangePwd.inputNewPwd('****',self.args.ttl)
		self.__class__.pageChangePwd.inputConfirmPwd('****',self.args.ttl)
		self.__class__.pageChangePwd.clickSetPassword(self.args.ttl)
		self.__class__.pageChangePwd.clickDone(self.args.ttl)
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack()

		logging.info(f' ========== 测试结束 CMBI-241 开户后用初始密码登录并修改密码 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	def test_02_CMBI_241(self):
		'''二次开户后用初始密码登录并修改密码'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-241 二次开户后用初始密码登录并修改密码 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		self.args=reg_api_second(self.args)
		logging.info(f'{self.args.tel}对应户口号: {self.args.Macc}')
		account=self.args.Macc
		logout(self.driver)

		mailid=getMailRecord(account,env=self.args.env,keyword='默认激活码',timeLimit=18000)[0][-1]
		firstpwd=getPwd_from_mail(mailid,env=self.args.env,mod='first')
		logging.info(f'{account} 初始密码: {firstpwd}')

		login(self.driver,(account,firstpwd),args=self.args,acc=0,needNickname=0)
		time.sleep(3)
		swithToRightWeb(self.driver,'/settle/firstLogin')
		self.__class__.pageChangePwd.inputOldPwd(firstpwd,self.args.ttl)
		self.__class__.pageChangePwd.inputNewPwd('****',self.args.ttl)
		self.__class__.pageChangePwd.inputConfirmPwd('****',self.args.ttl)
		self.__class__.pageChangePwd.clickSetPassword(self.args.ttl)
		self.__class__.pageChangePwd.clickDone(self.args.ttl)
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack()

		logging.info(f' ========== 测试结束 CMBI-241 二次开户后用初始密码登录并修改密码 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_03_CMBI_000(self):
		'''期货开户'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-000 期货开户 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		
		self.args.tel=None
		self.args.email=None
		self.args=reg_futures_api(self.args)

		for i in range(1,5):
			checkID=checkBO(self.args.tel,i,env=self.args.env,futures=1)
		manualActivate(checkID,env=self.args.env)
		sendWelcome(checkID,env=self.args.env)
		accList=getCheckID(search2=self.args.tel,getAcclist=1,env=self.args.env,futures=1)

		logging.info(f'{self.args.tel} 对应户口号 {" ".join(accList)}')
		logging.info(f' ========== 测试结束 CMBI-000 期货开户 ========== ')

	# @unittest.skip('跳过')
	# def test_01_CMBI_132(self):
	# 	'''手机号注册'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-132 手机号注册 ========== ')
	# 	if self.pageBar.PFN=='iOS':self.skipTest('iOS模拟器上传图片后无法获取元素，暂时跳过')
	# 	logging.info(f'该条用例已包含于 CMBI-238 和 CMBI-241 中')
	# 	logging.info(f' ========== 测试结束 CMBI-132 手机号注册 ========== ')

	# @unittest.skip('跳过')
	# def test_02_CMBI_236(self):
	# 	'''进入开户首页'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-236 进入开户首页 ========== ')
	# 	if self.pageBar.PFN=='iOS':self.skipTest('iOS模拟器上传图片后无法获取元素，暂时跳过')
	# 	logging.info(f'该条用例已包含于 CMBI-237 和 CMBI-240 中')
	# 	logging.info(f' ========== 测试结束 CMBI-236 进入开户首页 ========== ')

	# @unittest.skip('跳过')
	# def test_03_CMBI_237(self):
	# 	'''一般投资者 站内提交开户申请'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-237 一般投资者 站内开户 ========== ')
	# 	if self.pageBar.PFN=='iOS':self.skipTest('iOS模拟器上传图片后无法获取元素，暂时跳过')
	# 	login(self.driver,self.regFirst,forceLogout=1,acc=0,args=self.args)
	# 	logging.info('从交易页面进入开户页')
	# 	self.pageBar.clickTrade()
	# 	self.pageAlert.clickAlert()
	# 	from page.trade.trade import PageTrade
	# 	self.pageTrade=PageTrade(self.driver)
	# 	self.pageTrade.clickRegister()
	# 	swithToRightWeb(self.driver,'/form/start')
	# 	self.pageRegWeb.selectCardType()
	# 	self.pageRegWeb.clickReadme()
	# 	self.pageRegWeb.clickNext1()
	# 	swithToRightWeb(self.driver,'/form/card')
	# 	self.pageRegWeb.clickCardPic()
	# 	self.pageUploadPic.uploadPic()
	# 	self.pageRegWeb.inputRealName(regInfo['realName'])
	# 	self.pageRegWeb.inputREnName(regInfo['enName'])
	# 	self.pageRegWeb.inputCardId(regInfo['cardID'])
	# 	self.pageRegWeb.inputBirthPlace(regInfo['birthplace'])
	# 	# self.pageRegWeb.inputBirthday(regInfo['birthday'])
	# 	self.pageRegWeb.clickBirthDay()
	# 	self.pageRegWeb.clickBirthDayOK()
	# 	self.pageRegWeb.inputAddress(regInfo['address'])
	# 	self.pageRegWeb.clickCardExpire()
	# 	self.pageRegWeb.clickAddressUp()
	# 	self.pageUploadPic.uploadPic()
	# 	self.pageRegWeb.clickNext2()
	# 	swithToRightWeb(self.driver,'/form/personal')
	# 	self.pageRegWeb.inputHomeTel(regInfo['homeTel'])
	# 	self.pageRegWeb.inputEmail(regInfo['email'])
	# 	self.pageRegWeb.selectJobStatus()
	# 	self.pageRegWeb.selectJob()
	# 	self.pageRegWeb.selectIndustry()
	# 	self.pageRegWeb.inputCompanyName(regInfo['company'])
	# 	self.pageRegWeb.clickNext3()
	# 	self.pageRegWeb.clickCardBtnOk()
	# 	swithToRightWeb(self.driver,'/form/background')
	# 	self.pageRegWeb.clickBackgroundInfo()
	# 	swithToRightWeb(self.driver,'/form/marketchoose')
	# 	self.pageRegWeb.clickMarketChoose()
	# 	swithToRightWeb(self.driver,'/form/riskannounce')
	# 	self.pageRegWeb.clickNext4()
	# 	self.pageRegWeb.clickNext5()
	# 	swithToRightWeb(self.driver,'/form/addHk')
	# 	self.pageRegWeb.clickAddHkNext()
	# 	swithToRightWeb(self.driver,'/form/sign')
	# 	self.pageRegWeb.clickAgreeSign()
	# 	self.pageRegWeb.clickSignTable()
	# 	swithToRightWeb(self.driver,'/form/handwrite')
	# 	self.pageRegWeb.sign(0)
	# 	self.pageRegWeb.clickPaperDone()
	# 	swithToRightWeb(self.driver,'/form/done')
	# 	self.assertEqual('提交成功',self.pageRegWeb.textMsg())
	# 	self.pageBar.goBack()
	# 	logout(self.driver)
	# 	logging.info(f' ========== 测试结束 CMBI-237 一般投资者 站内开户 ========== ')

	# @unittest.skip('二次开户暂时跳过')
	# def test_04_CMBI_239(self):
	# 	'''一般投资者 站内二次开户'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-239 一般投资者 站内二次开户 ========== ')
	# 	if self.pageBar.PFN=='iOS':self.skipTest('iOS模拟器上传图片后无法获取元素，暂时跳过')
	# 	login(self.driver,self.regSecond['general'][0],forceLogout=1,acc=0,args=self.args)
	# 	self.pageBar.clickHome()
	# 	self.pageAlert.clickAlert()
	# 	swithToRightWeb(self.driver,'index.html#/home')
	# 	self.pageHome.clickRegister()
	# 	swithToRightWeb(self.driver,'/appkh/')
	# 	self.pageHome.clickRegisterNow()
	# 	try:
	# 		swithToRightWeb(self.driver,'/form/s_start')
	# 		self.pageRegWeb.clickNext1()# 点击下一步
	# 		swithToRightWeb(self.driver,'/form/s_info')
	# 		self.pageRegWeb.clickNext1()# 点击下一步
	# 		swithToRightWeb(self.driver,'/form/s_infob')
	# 		self.pageRegWeb.clickNext1()# 点击下一步
	# 		swithToRightWeb(self.driver,'/form/s_personal')
	# 		self.pageRegWeb.clickNext1()# 点击下一步
	# 		self.pageRegWeb.clickContinue()# 点击继续开户
	# 		swithToRightWeb(self.driver,'/form/s_marketchoose')
	# 		self.pageRegWeb.clickNext1()# 点击下一步
	# 		swithToRightWeb(self.driver,'/form/s_marketchoose')
	# 		self.pageRegWeb.clickNext1()# 点击下一步
	# 		swithToRightWeb(self.driver,'/form/s_riskannounce')
	# 		self.pageRegWeb.clickNext4()
	# 		self.pageRegWeb.clickNext5()
	# 		swithToRightWeb(self.driver,'/form/s_done')
	# 		self.assertEqual('成功',self.pageRegWeb.textMsg())
	# 		self.pageRegWeb.clickPaperDone()# 点击完成
	# 		# self.pageBar.goBack(n=2)
	# 		self.pageBar.clickMy()
	# 		self.pageAlert.clickAlert()
	# 		account=self.pageMy.textAcc()
	# 		logout(self.driver)
	# 		delAccount(account=account)
	# 	except Exception:
	# 		logging.error(traceback.format_exc())
	# 		delAccount(search2=self.regSecond['general'][0][0],protectID=self.regSecond['general'][1][0])
	# 		raise Exception
	# 	logging.info(f' ========== 测试结束 CMBI-239 一般投资者 站内二次开户 ========== ')			

	# @unittest.skip('跳过')
	# def test_05_CMBI_240(self):
	# 	'''专业投资者 站内提交开户申请'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-240 专业投资者 站内开户 ========== ')
	# 	if self.pageBar.PFN=='iOS':self.skipTest('iOS模拟器上传图片后无法获取元素，暂时跳过')
	# 	login(self.driver,self.regFirst,forceLogout=1,acc=0,args=self.args)
	# 	logging.info('从首页进入开户页')
	# 	self.pageBar.clickHome()
	# 	self.pageAlert.clickAlert()
	# 	swithToRightWeb(self.driver,'index.html#/home')
	# 	self.pageHome.clickRegister()
	# 	swithToRightWeb(self.driver,'/appkh/')
	# 	self.pageHome.clickRegisterNow()
	# 	swithToRightWeb(self.driver,'/form/start')
	# 	self.pageRegWeb.clickPI()
	# 	self.pageRegWeb.selectCardType()
	# 	self.pageRegWeb.clickReadme()
	# 	self.pageRegWeb.clickNext1()
	# 	swithToRightWeb(self.driver,'/form/card')
	# 	self.pageRegWeb.clickCardPic()
	# 	self.pageUploadPic.uploadPic()
	# 	self.pageRegWeb.inputRealName(regInfo['realName'])
	# 	self.pageRegWeb.inputREnName(regInfo['enName'])
	# 	self.pageRegWeb.inputCardId(regInfo['cardID'])
	# 	self.pageRegWeb.inputBirthPlace(regInfo['birthplace'])
	# 	# self.pageRegWeb.inputBirthday(regInfo['birthday'])
	# 	self.pageRegWeb.clickBirthDay()
	# 	self.pageRegWeb.clickBirthDayOK()
	# 	self.pageRegWeb.inputAddress(regInfo['address'])
	# 	self.pageRegWeb.clickCardExpire()
	# 	self.pageRegWeb.clickAddressUp()
	# 	self.pageUploadPic.uploadPic()
	# 	self.pageRegWeb.clickNext2()
	# 	swithToRightWeb(self.driver,'/form/personal')
	# 	self.pageRegWeb.inputHomeTel(regInfo['homeTel'])
	# 	self.pageRegWeb.inputEmail(regInfo['email'])
	# 	self.pageRegWeb.selectJobStatus()
	# 	self.pageRegWeb.selectJob()
	# 	self.pageRegWeb.selectIndustry()
	# 	self.pageRegWeb.inputCompanyName(regInfo['company'])
	# 	self.pageRegWeb.clickNext3()
	# 	self.pageRegWeb.clickCardBtnOk()
	# 	swithToRightWeb(self.driver,'/form/background')
	# 	self.pageRegWeb.clickPiPic()
	# 	self.pageUploadPic.uploadPic()
	# 	self.pageRegWeb.clickBackgroundInfo()
	# 	swithToRightWeb(self.driver,'/form/marketchoose')
	# 	self.pageRegWeb.clickMarketChoose()
	# 	#衍生品问卷
	# 	swithToRightWeb(self.driver,'/form/der')
	# 	self.pageRegWeb.derTest()
	# 	self.pageRegWeb.clickderTest()
	# 	#风险评测
	# 	swithToRightWeb(self.driver,'/form/rpq')
	# 	self.pageRegWeb.riskTest()
	# 	self.pageRegWeb.selectYears()
	# 	self.pageRegWeb.selectTimes()
	# 	self.pageRegWeb.clickRpqTest()
	# 	swithToRightWeb(self.driver,'/form/market')
	# 	self.pageRegWeb.clickAccountMarket()
	# 	swithToRightWeb(self.driver,'/form/riskannounce')
	# 	self.pageRegWeb.clickNext4()
	# 	self.pageRegWeb.clickNext5()
	# 	swithToRightWeb(self.driver,'/form/addHk')
	# 	self.pageRegWeb.clickAddHkNext()
	# 	swithToRightWeb(self.driver,'/form/method')
	# 	self.pageRegWeb.chooseSignType()
	# 	self.pageRegWeb.clickF2Fpic()
	# 	self.pageUploadPic.uploadPic()
	# 	self.pageRegWeb.clickNext6()
	# 	swithToRightWeb(self.driver,'/form/sign')
	# 	self.pageRegWeb.clickAgreeSign()
	# 	self.pageRegWeb.clickSignTable()
	# 	swithToRightWeb(self.driver,'/form/handwrite')
	# 	self.pageRegWeb.sign(0)
	# 	self.pageRegWeb.clickPaperDone()
	# 	swithToRightWeb(self.driver,'/form/done')
	# 	self.assertEqual('提交成功',self.pageRegWeb.textMsg())
	# 	self.pageBar.goBack(n=2)
	# 	logout(self.driver)
	# 	logging.info(f' ========== 测试结束 CMBI-240 专业投资者 站内开户 ========== ')

	# @unittest.skip('二次开户暂时跳过')
	# def test_06_CMBI_242(self):
	# 	'''专业投资者 站内二次开户'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-242 专业者 站内二次开户 ========== ')
	# 	if self.pageBar.PFN=='iOS':self.skipTest('iOS模拟器上传图片后无法获取元素，暂时跳过')
	# 	login(self.driver,self.regSecond['pi'][0],forceLogout=1,acc=0,args=self.args)
	# 	self.pageBar.clickHome()
	# 	self.pageAlert.clickAlert()
	# 	swithToRightWeb(self.driver,'index.html#/home')
	# 	self.pageHome.clickRegister()
	# 	swithToRightWeb(self.driver,'/appkh/')
	# 	self.pageHome.clickRegisterNow()
	# 	try:
	# 		swithToRightWeb(self.driver,'/form/start')
	# 		self.pageRegWeb.clickAccMargin()
	# 		self.pageRegWeb.clickReadme()
	# 		self.pageRegWeb.clickNext1()
	# 		swithToRightWeb(self.driver,'/form/card')
	# 		self.pageRegWeb.clickCardExpire()
	# 		self.pageRegWeb.clickNext2()
	# 		swithToRightWeb(self.driver,'/form/personal')
	# 		self.pageRegWeb.selectIndustry()
	# 		self.pageRegWeb.clickNext3()
	# 		self.pageRegWeb.clickCardBtnOk()
	# 		swithToRightWeb(self.driver,'/form/background')
	# 		self.pageRegWeb.clickBackgroundInfo()
	# 		swithToRightWeb(self.driver,'/form/marketchoose')
	# 		self.pageRegWeb.clickMarketChoose()
	# 		swithToRightWeb(self.driver,'/form/der')
	# 		self.pageRegWeb.clickderTest()
	# 		swithToRightWeb(self.driver,'/form/rpq')
	# 		self.pageRegWeb.clickRpqTest()
	# 		swithToRightWeb(self.driver,'/form/market')
	# 		self.pageRegWeb.clickAccountMarket()
	# 		swithToRightWeb(self.driver,'/form/riskannounce')
	# 		self.pageRegWeb.clickNext4()
	# 		self.pageRegWeb.clickNext5()
	# 		swithToRightWeb(self.driver,'/form/addHk')
	# 		self.pageRegWeb.clickAddHkNext()
	# 		swithToRightWeb(self.driver,'/form/method')
	# 		self.pageRegWeb.chooseSignType()
	# 		self.pageRegWeb.clickF2Fpic()
	# 		swithToRightWeb(self.driver,0)
	# 		self.pageUploadPic.uploadPic()
	# 		swithToRightWeb(self.driver,'/form/method')
	# 		self.pageRegWeb.clickNext6()
	# 		swithToRightWeb(self.driver,'/form/sign')
	# 		self.pageRegWeb.clickAgreeSign()
	# 		self.pageRegWeb.clickSignTable()
	# 		swithToRightWeb(self.driver,'/form/handwrite')
	# 		self.pageRegWeb.sign(0)
	# 		self.pageRegWeb.clickPaperDone()
	# 		swithToRightWeb(self.driver,'/form/done')
	# 		self.assertEqual('提交成功',self.pageRegWeb.textMsg())
	# 		self.pageBar.goBack(n=2)
	# 		self.pageBar.clickMy()
	# 		self.pageAlert.clickAlert()
	# 		account=self.pageMy.textAcc()
	# 		logout(self.driver)
	# 		delAccount(account=account)
	# 	except Exception:
	# 		logging.error(traceback.format_exc())
	# 		delAccount(search2=self.regSecond['pi'][0][0],protectID=self.regSecond['pi'][1][0])
	# 		raise Exception
	# 	logging.info(f' ========== 测试结束 CMBI-242 专业者 站内二次开户 ========== ')


	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_07_CMBI_238(self):
	# 	'''一般投资者 站外提交开户申请'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-238 站外开户 ========== ')
	# 	if self.args.skipRegweb:self.skipTest("跳过，不属于APP范围，无需重复执行")
	# 	from common.tools import getWebDriver

	# 	driverWeb=getWebDriver(headless=0)
	# 	driverWeb.get(regURL[self.args.env])
	# 	self.pageRegisterWeb=PageRegisterWeb(driverWeb)
		
	# 	#第一步
	# 	self.pageRegisterWeb.inputPhone(self.regFirst[0])
	# 	for i in range(20):
	# 		self.pageRegisterWeb.clickGetcode()
	# 		if not self.pageRegisterWeb.acceptAlert():break
	# 	time.sleep(3)
		
	# 	code=getSMScode(self.regFirst[0])
	# 	self.pageRegisterWeb.inputSMScode(code)
	# 	self.pageRegisterWeb.clickNext()
	# 	#第二步
	# 	self.pageRegisterWeb.selectCardType()
	# 	self.pageRegisterWeb.clickReadme()
	# 	self.pageRegisterWeb.clickNext1()
		
	# 	# 第三步
	# 	self.pageRegisterWeb.inputCardPic(regInfo['pic1'])
	# 	self.pageRegisterWeb.inputRealName(regInfo['realName'])
	# 	self.pageRegisterWeb.inputREnName(regInfo['enName'])
	# 	self.pageRegisterWeb.inputCardId(regInfo['cardID'])
	# 	self.pageRegisterWeb.inputBirthPlace(regInfo['birthplace'])
	# 	self.pageRegisterWeb.clickBirthDay()
	# 	self.pageRegisterWeb.clickBirthDayOK()
	# 	self.pageRegisterWeb.inputAddress(regInfo['address'])
	# 	self.pageRegisterWeb.clickCardExpire()
	# 	self.pageRegisterWeb.inputAddressPic(regInfo['pic2'])
	# 	self.pageRegisterWeb.clickNext2()
	# 	# 第四步
	# 	self.pageRegisterWeb.inputHomeTel(regInfo['homeTel'])
	# 	self.pageRegisterWeb.inputEmail(regInfo['email'])
	# 	self.pageRegisterWeb.selectJobStatus()
	# 	self.pageRegisterWeb.selectJob()
	# 	self.pageRegisterWeb.selectIndustry()
	# 	self.pageRegisterWeb.inputCompanyName(regInfo['company'])
	# 	self.pageRegisterWeb.clickNext3()
	# 	self.pageRegisterWeb.clickCardBtnOk()
	# 	# 第五步
	# 	self.pageRegisterWeb.clickBackgroundInfo()
	# 	self.pageRegisterWeb.clickMarketChoose()
	# 	self.pageRegisterWeb.clickNext4()
	# 	self.pageRegisterWeb.clickNext5()
	# 	#第六步
	# 	self.pageRegisterWeb.clickAddHkNext()
	# 	#第七步
	# 	self.pageRegisterWeb.clickAgreeSign()
	# 	self.pageRegisterWeb.clickSignTable()
	# 	#第八步
	# 	self.pageRegisterWeb.sign()
	# 	self.pageRegisterWeb.clickPaperDone()
	# 	self.assertEqual('提交成功',self.pageRegisterWeb.textMsg())
	# 	driverWeb.quit()

	# 	logging.info(f' ========== 测试结束 CMBI-238 站外开户 ========== ')

	# @unittest.skip('跳过')
	# # @no_retry
	# def test_08_CMBI_241(self):
	# 	'''专业投资者 站外提交开户申请'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-241 专业者 站外开户 ========== ')
	# 	if self.args.skipRegweb:self.skipTest("跳过，不属于APP范围，无需重复执行")
	# 	from common.tools import getWebDriver

	# 	driverWeb=getWebDriver(headless=0)
	# 	driverWeb.get(regURL[self.args.env])
	# 	self.pageRegisterWeb=PageRegisterWeb(driverWeb)
		
	# 	#第一步
	# 	self.pageRegisterWeb.inputPhone(self.regFirst[0])
	# 	for i in range(20):
	# 		self.pageRegisterWeb.clickGetcode()
	# 		if not self.pageRegisterWeb.acceptAlert():break
	# 	time.sleep(3)
		
	# 	code=getSMScode(self.regFirst[0])
	# 	self.pageRegisterWeb.inputSMScode(code)
	# 	self.pageRegisterWeb.clickNext()
	# 	#第二步
	# 	self.pageRegisterWeb.clickPI()
	# 	self.pageRegisterWeb.selectCardType()
	# 	self.pageRegisterWeb.clickReadme()
	# 	self.pageRegisterWeb.clickNext1()
	# 	# 第三步
	# 	self.pageRegisterWeb.inputCardPic(regInfo['pic1'])
	# 	self.pageRegisterWeb.inputRealName(regInfo['realName'])
	# 	self.pageRegisterWeb.inputREnName(regInfo['enName'])
	# 	self.pageRegisterWeb.inputCardId(regInfo['cardID'])
	# 	self.pageRegisterWeb.inputBirthPlace(regInfo['birthplace'])
	# 	self.pageRegisterWeb.clickBirthDay()
	# 	self.pageRegisterWeb.clickBirthDayOK()
	# 	self.pageRegisterWeb.inputAddress(regInfo['address'])
	# 	self.pageRegisterWeb.clickCardExpire()
	# 	self.pageRegisterWeb.inputAddressPic(regInfo['pic2'])
	# 	self.pageRegisterWeb.clickNext2()
	# 	# 第四步
	# 	self.pageRegisterWeb.inputHomeTel(regInfo['homeTel'])
	# 	self.pageRegisterWeb.inputEmail(regInfo['email'])
	# 	self.pageRegisterWeb.selectJobStatus()
	# 	self.pageRegisterWeb.selectJob()
	# 	self.pageRegisterWeb.selectIndustry()
	# 	self.pageRegisterWeb.inputCompanyName(regInfo['company'])
	# 	self.pageRegisterWeb.clickNext3()
	# 	self.pageRegisterWeb.clickCardBtnOk()
	# 	# 第五步
	# 	self.pageRegisterWeb.inputPiPic(regInfo['pic3'])
	# 	time.sleep(1)
	# 	self.pageRegisterWeb.clickBackgroundInfo()
	# 	self.pageRegisterWeb.clickMarketChoose()
	# 	#衍生品问卷
	# 	self.pageRegisterWeb.derTest()
	# 	self.pageRegisterWeb.clickderTest()
	# 	# 风险取向测评
	# 	self.pageRegisterWeb.riskTest()
	# 	self.pageRegisterWeb.selectYears()
	# 	self.pageRegisterWeb.selectTimes()
	# 	self.pageRegisterWeb.clickRpqTest()
	# 	self.pageRegisterWeb.clickAccountMarket()

	# 	self.pageRegisterWeb.clickNext4()
	# 	self.pageRegisterWeb.clickNext5()
	# 	#第六步
	# 	self.pageRegisterWeb.clickAddHkNext()
	# 	self.pageRegisterWeb.chooseSignType()
	# 	self.pageRegisterWeb.inputF2Fpic(regInfo['pic4'])
	# 	time.sleep(1)
	# 	self.pageRegisterWeb.clickNext6()
	# 	#第七步
	# 	self.pageRegisterWeb.clickAgreeSign()
	# 	self.pageRegisterWeb.clickSignTable()
	# 	#第八步
	# 	self.pageRegisterWeb.sign()
	# 	self.pageRegisterWeb.clickPaperDone()
	# 	self.assertEqual('提交成功',self.pageRegisterWeb.textMsg())
	# 	driverWeb.quit()
	
	# 	logging.info(f' ========== 测试结束 CMBI-241 专业者 站外开户 ========== ')

	def tearDown(self):
		pass
		# try:
		# 	delAccount(search2=self.regFirst[0])
		# 	delAccount(search2=regInfo['email'])
		# except IndexError:
		# 	pass
		# except:
		# 	logging.error(traceback.format_exc())
		# 	pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 开户注册 模块测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass