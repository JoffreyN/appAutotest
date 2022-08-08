import time,logging,traceback,unittest
from HTMLReport import ddt,no_retry
from page.navBar import PageBar
from page.alert import PageAlert
from page.mine.my import PageMy
from page.mine.login_uname import PageLogin_u
from page.mine.login_pword import PageLogin_p
from page.mine.logined import PageLogined
from page.mine.lingpai import PageLingpai
from page.mine.findPwd import PageFindPwd
from business.logInOut import logout
from common.parameter import ParameTestCase
from common.system_boss import getSMScode
from common.tools import swithToRightWeb
from common.dbOperation import get_cardID

from testData.data import accountPool,accBinding

# @unittest.skip('跳过')
# @ddt.ddt
class TestLogin(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 登录测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageMy=PageMy(cls.driver)
		cls.pageLogin_u=PageLogin_u(cls.driver)
		cls.pageLogin_p=PageLogin_p(cls.driver)
		cls.pageLogined=PageLogined(cls.driver)
		cls.pageLingpai=PageLingpai(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageFindPwd=PageFindPwd(cls.driver)

	def setUp(self):
		if self.args.debug:return
		self.__class__.pageBar.clickMy()
		# self.__class__.pageAlert.clickAlert()
		for i in range(3):
			try:
				self.__class__.pageMy.clickLogin()
				break
			except AttributeError:
				if self.__class__.pageMy.textNick():
					logout(self.driver)

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_133(self):
		'''手机号+密码 登录'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-133 手机号+密码 登录 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		phone=accBinding[self.args.account][1]
		pwd=accountPool[phone][0]
		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname(phone)
		self.__class__.pageLogin_u.clickLogin()

		self.__class__.pageLogin_p.inputPword(pwd)
		self.__class__.pageLogin_p.clickConfirm()

		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')
		logging.info(f' ========== 测试结束 CMBI-133 手机号+密码 登录 ========== ')

	# @unittest.skip('跳过')
	@no_retry
	def test_CMBI_134(self):
		'''手机号+验证码 登录'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-134 手机号+验证码 登录 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		phone=accBinding[self.args.account][1]
		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname(phone)
		self.__class__.pageLogin_u.clickLogin()

		self.__class__.pageLogin_p.clickSMS()
		time.sleep(1)
		# code=getSMScode(phone,self.args.env,0)
		code=getSMScode(phone,self.args.env,4)
		logging.info(f'手机号 {phone} 验证码 {code}')
		self.__class__.pageLogin_p.inputSMS(code)

		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')
		logging.info(f' ========== 测试结束 CMBI-134 手机号+验证码 登录 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_134_1(self):
		'''手机号+验证码 找回密码'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-134 手机号+验证码 找回密码 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		phone=accBinding[self.args.account][1]
		pwd=accountPool[phone][0]
		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname(phone)
		self.__class__.pageLogin_u.clickLogin()

		self.__class__.pageLogin_p.clickForgetpwd()
		swithToRightWeb(self.driver,'/settle/reset')
		time.sleep(1)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(1)
		self.__class__.pageFindPwd.inputSMScode('8888',self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit(self.args.ttl)
		time.sleep(5)
		self.__class__.pageFindPwd.inputPassword(pwd,self.args.ttl)
		self.__class__.pageFindPwd.inputPassword2(pwd,self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit2(self.args.ttl)
		self.__class__.pageFindPwd.clickDone(self.args.ttl)
		
		swithToRightWeb(self.driver,0)
		self.__class__.pageLogin_p.inputPword(pwd)
		self.__class__.pageLogin_p.clickConfirm()
		# self.__class__.pageLogined.clickIknow()
		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')
		logging.info(f' ========== 测试结束 CMBI-134_1 手机号+验证码 找回密码 ========== ')

	# @no_retry
	# @unittest.skip('跳过')
	def test_CMBI_135(self):
		'''证券号+密码 登录'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-135 证券号+密码 登录 ========== ')
		if self.args.env=='prod':
			self.__class__.pageLogin_u.inputUname(self.args.account)
			self.__class__.pageLogin_u.clickLogin()
			if self.__class__.pageLogin_u.unCheckFlagExists():
				self.__class__.pageLogin_u.clickConfirm()
				self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env,only=1)
				self.__class__.pageLogin_u.clickLogin()

		else:
			self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
			self.__class__.pageLogin_u.inputUname(self.args.account)
			self.__class__.pageLogin_u.clickLogin()

		self.__class__.pageLogin_p.inputPword(accountPool[self.args.account][0])
		self.__class__.pageLogin_p.clickConfirm()
		# toast=self.__class__.pageLogin_p.getToast()
		# if toast:
		# 	logging.info("toast:",toast)
		# 	self.assertNotIn('密码不正确',toast,'密码错误，测试失败！')
		try:
			text=self.__class__.pageLogined.textSMS()
			if text:flag=1;logging.info(text)
			# else:logging.info(text);flag=0;logging.info('未要求输入验证码')
		except AttributeError:
			flag=0;logging.info('未要求输入验证码')
		if flag:
			if self.args.env=='prod':
				self.__class__.pageLogined.clickLingpai()
				self.__class__.pageLogined.clickOpenLPapp()

				self.__class__.pageLingpai.inputUnlockpwd()
				self.__class__.pageLingpai.clickGetLP(self.args.account)
				token=self.__class__.pageLingpai.getToken()
				logging.info('返回3次')
				self.__class__.pageBar.goBack(3)
				time.sleep(5)

				self.__class__.pageLogined.inputlingpai(token)
				self.__class__.pageLogined.clickConfirm()
			else:
				self.__class__.pageLogined.clickSMS()
				self.__class__.pageLogined.clickConfirm(ignoreError=1)
				time.sleep(2)
				# code=getCodeLog(account[0])
				# if self.driver.capabilities['platformName']=='Android':
				# 	phone=self.__class__.pageLogined.textPhone()
				# else:
				phone=accBinding[self.args.account][1]
				code=getSMScode(phone,self.args.env,6)
				self.__class__.pageLogined.inputSMS(code)
				self.__class__.pageLogined.clickConfirm()
		# msg=self.__class__.pageLogined.textEleMsg()
		# self.assertEqual('使用手机号登录更便捷',msg,'测试失败，引导提示信息与预期不符！')
		self.__class__.pageLogined.clickIknow()

		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')
		logging.info(f' ========== 测试结束 CMBI-135 证券号+密码 登录 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_135_1(self):
		'''证券号+验证码 找回密码'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-134 证券号+验证码 找回密码 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		pwd=accountPool[accBinding[self.args.account][1]][0]
		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname(self.args.account)
		self.__class__.pageLogin_u.clickLogin()
		self.__class__.pageLogin_p.clickForgetpwd()
		swithToRightWeb(self.driver,'settle/reset/account')
		
		card_id=get_cardID(self.args.account,self.args.env)[0][0]
		self.__class__.pageFindPwd.inputcard_id(card_id,self.args.ttl)
		self.__class__.pageFindPwd.clickNext()
		self.__class__.pageFindPwd.inputSMScode('8888',self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit(self.args.ttl)
		time.sleep(5)
		self.__class__.pageFindPwd.inputPassword(pwd,self.args.ttl)
		self.__class__.pageFindPwd.inputPassword2(pwd,self.args.ttl)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(3)
		self.__class__.pageFindPwd.clickDone(self.args.ttl)
		swithToRightWeb(self.driver,0)
		self.__class__.pageLogin_p.inputPword(pwd)
		self.__class__.pageLogin_p.clickConfirm()
		self.__class__.pageLogined.clickIknow()
		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')
		logging.info(f' ========== 测试结束 CMBI-135_1 证券号+验证码 找回密码 ========== ')


	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_136(self):
		'''邮箱+密码 登录'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-136 邮箱+密码 登录 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname('694080632@qq.com')
		self.__class__.pageLogin_u.clickLogin()

		self.__class__.pageLogin_p.inputPword('123456')
		self.__class__.pageLogin_p.clickConfirm()

		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')
		logging.info(f' ========== 测试结束 CMBI-136 邮箱+密码 登录 ========== ')
	
	def tearDown(self):
		if self.args.debug:return
		logout(self.driver)

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 登录测试结束 ########## ')

if __name__=='__main__':
	unittest.main()