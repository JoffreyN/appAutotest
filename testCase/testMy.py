import time,logging,unittest
from HTMLReport import no_retry

from common.parameter import ParameTestCase
from common.tools import swithToRightWeb
from common.dbOperation import get_cardID,del_pwdHistory
from common.system_boss import cms_resetpwd,getMailRecord,getPwd_from_mail
from common.apiCenter import resetpwd,login_acc,unlockAcc

from business.logInOut import login,logout

from page.navBar import PageBar
from page.alert import PageAlert
from page.mine.my import PageMy
from page.mine.set import PageSet
from page.mine.login_uname import PageLogin_u
from page.mine.login_pword import PageLogin_p
from page.mine.logined import PageLogined
from page.mine.changePwd import PageChangePwd
from page.mine.findPwd import PageFindPwd
from page.mine.findAcc import PageFindAcc
# from page.mine.commonProb import PageCommonProb
# from page.mine.cusManage import PageCusManage
# from page.mine.feedback import PageFeedback
from page.mine.unlockAcc import PageUnlockAcc

from testData.data import accountPool,accBinding,UnionAcc

# @unittest.skip('跳过')
class TestMy(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 我的 模块测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageMy=PageMy(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageLogin_u=PageLogin_u(cls.driver)
		cls.pageLogin_p=PageLogin_p(cls.driver)
		cls.pageLogined=PageLogined(cls.driver)
		cls.pageFindPwd=PageFindPwd(cls.driver)
		cls.pageFindAcc=PageFindAcc(cls.driver)
		# cls.pageFeedback=PageFeedback(cls.driver)
		cls.pageUnlockAcc=PageUnlockAcc(cls.driver)
		# cls.pageCommonProb=PageCommonProb(cls.driver)
		# cls.pageCusManage=PageCusManage(cls.driver)
		cls.pageSet=PageSet(cls.driver)
		cls.pageChangePwd=PageChangePwd(cls.driver)
		cls.acc_pwd=(cls.args.account,accountPool[cls.args.account][0])
		cls.nickName=accountPool[cls.args.account][1]

	def setUp(self):
		pass

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_001(self):
		'''忘记证券账户'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.env=='prod':self.skipTest('跳过')

		logging.info(f' ========== 测试开始 CMBI-001 忘记证券账户 ========== ')
		self.__class__.pageBar.clickMy()
		self.__class__.pageMy.clickLogin()
		self.__class__.pageLogin_u.clickForgetAcc()

		time.sleep(2)
		swithToRightWeb(self.driver,'/settle/query')
		card_id=get_cardID(self.args.account,self.args.env)[0][0]
		self.__class__.pageFindAcc.inputCardId(card_id)
		self.__class__.pageFindAcc.click_next()
		time.sleep(1)
		try:
			self.__class__.pageFindAcc.click_next()
			time.sleep(1)
		except:pass
		
		time.sleep(3)
		self.__class__.pageFindAcc.inputSmscode('8888')
		self.__class__.pageFindAcc.click_yes()
		time.sleep(1)
		# myAddScreen(self,'截图')
		# self.assertIn(self.args.account,self.__class__.pageFindAcc.getAccInfo())
		self.__class__.pageFindAcc.click_goToLogin()

		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-001 忘记证券账户 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_149(self):
		'''忘记证券账户密码'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.env=='prod':self.skipTest('跳过')

		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
		self.__class__.pageBar.clickMy()
		# self.__class__.pageAlert.clickAlert()
		logging.info(f' ========== 测试开始 CMBI-149 忘记证券账户密码 ========== ')
		self.__class__.pageMy.clickSet()
		pwd=accountPool[accBinding[self.args.account][1]][0]
		self.__class__.pageSet.clickChangePwd()
		time.sleep(3)
		swithToRightWeb(self.driver,'/reset/account')

		self.__class__.pageFindPwd.inputaccountid(self.args.account,self.args.ttl)
		card_id=get_cardID(self.args.account,self.args.env)[0][0]
		self.__class__.pageFindPwd.inputcard_id(card_id,self.args.ttl)
		# self.__class__.pageFindPwd.clickNext(1)
			
		if self.args.ttl:
			self.__class__.pageFindPwd.clickNext()
		else:
			self.__class__.pageFindPwd.clickNext_postResetApply()
		self.__class__.pageFindPwd.inputSMScode('8888',self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit(self.args.ttl)
		time.sleep(5)
		self.__class__.pageFindPwd.inputPassword(pwd,self.args.ttl)
		self.__class__.pageFindPwd.inputPassword2(pwd,self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit2(self.args.ttl)
		time.sleep(3)
		self.__class__.pageFindPwd.clickDone()
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-149 忘记证券账户密码 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_149_1(self):
		'''联名账户重置密码'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.env=='prod':self.skipTest('跳过')
		union_acc_info=UnionAcc[self.args.account]
		login(self.driver,(union_acc_info[0],union_acc_info[1]),forceLogout=1,args=self.args)#验证2FA
		logout(self.driver)
		logging.info(f' ========== 测试开始 CMBI-149_1 联名账户重置密码 ========== ')
		self.__class__.pageBar.clickMy()
		self.__class__.pageMy.clickLogin()

		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname(union_acc_info[0])
		self.__class__.pageLogin_u.clickLogin()
		self.__class__.pageLogin_p.clickForgetpwd()
		swithToRightWeb(self.driver,'settle/reset/account')

		logging.info('只输入第1个证件号')
		self.__class__.pageFindPwd.inputcard_id(union_acc_info[2][0],self.args.ttl)
		time.sleep(2)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(2)
		self.assertTrue(self.__class__.pageFindPwd.alertMsgExists())
		self.__class__.pageFindPwd.click_alertYes()
		time.sleep(2)

		logging.info('只输入第2个证件号')
		self.__class__.pageFindPwd.inputcard_id(union_acc_info[2][1],self.args.ttl)
		time.sleep(2)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(2)
		self.assertTrue(self.__class__.pageFindPwd.alertMsgExists())
		self.__class__.pageFindPwd.click_alertYes()
		time.sleep(2)

		logging.info('输入2个证件号')
		self.__class__.pageFindPwd.inputcard_id(''.join(union_acc_info[2]),self.args.ttl)
		time.sleep(2)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(2)

		self.__class__.pageFindPwd.inputSMScode('8888',self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit(self.args.ttl)
		time.sleep(5)
		self.__class__.pageFindPwd.inputPassword(union_acc_info[1],self.args.ttl)
		self.__class__.pageFindPwd.inputPassword2(union_acc_info[1],self.args.ttl)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(3)
		self.__class__.pageFindPwd.clickDone(self.args.ttl)
		swithToRightWeb(self.driver,0)
		self.__class__.pageLogin_p.inputPword(union_acc_info[1])
		self.__class__.pageLogin_p.clickConfirm()
		self.__class__.pageLogined.clickIknow()
		# time.sleep(1)
		nickName=self.__class__.pageMy.textNick()
		self.assertIsNotNone(nickName,'无法获取用户昵称，测试失败！')

		# swithToRightWeb(self.driver,0)
		# self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-149_1 联名账户重置密码 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_151(self):
		'''邮箱找回密码'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-151 邮箱找回密码 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		logout(self.driver)
		self.__class__.pageBar.clickMy()
		self.__class__.pageAlert.clickAlert()
		self.__class__.pageMy.clickLogin()
		self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
		self.__class__.pageLogin_u.inputUname('694080632@qq.com')
		self.__class__.pageLogin_u.clickLogin()
		self.__class__.pageLogin_p.clickForgetpwd()
		time.sleep(5)
		# self.__class__.pageBar.goBack()
		swithToRightWeb(self.driver,'/settle/reset')

		time.sleep(1)
		self.__class__.pageFindPwd.clickNext()
		time.sleep(1)
		self.__class__.pageFindPwd.inputSMScode('8888',self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit(self.args.ttl)
		time.sleep(5)
		self.__class__.pageFindPwd.inputPassword('aaaa1111',self.args.ttl)
		self.__class__.pageFindPwd.inputPassword2('aaaa1111',self.args.ttl)
		self.__class__.pageFindPwd.clickSubmit2(self.args.ttl)
		self.__class__.pageFindPwd.clickDone(self.args.ttl)

		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-151 邮箱找回密码 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_152(self):
		'''boss重置密码后修改密码'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-152 boss重置密码后修改密码 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		del_pwdHistory(self.args.account,env=self.args.env)# 删除曾经用过的密码
		try:
			logout(self.driver)
			cms_resetpwd(self.args.account,env=self.args.env)# 重置密码
			mailid=getMailRecord(self.args.account,env=self.args.env,keyword='密码已重置|密碼已重置|password has been reset')
			logging.info(f'邮件ID: {mailid}')
			newpwd=getPwd_from_mail(mailid[0][-1],env=self.args.env)# 查询重置后的密码
			logging.info(f'重置后的密码: {newpwd}')
			# 登录并修改密码
			login(self.driver,(self.args.account,newpwd),args=self.args,acc=0,needNickname=0)
			time.sleep(3)
			swithToRightWeb(self.driver,'/settle/firstLogin')
			self.__class__.pageChangePwd.inputOldPwd(newpwd,self.args.ttl)
			self.__class__.pageChangePwd.inputNewPwd(self.__class__.acc_pwd[1],self.args.ttl)
			self.__class__.pageChangePwd.inputConfirmPwd(self.__class__.acc_pwd[1],self.args.ttl)
			self.__class__.pageChangePwd.clickSetPassword(self.args.ttl)
			self.__class__.pageChangePwd.clickDone(self.args.ttl)
			swithToRightWeb(self.driver,0)
			self.__class__.pageBar.goBack()
		except Exception as err:
			raise err
		finally:
			resetpwd(self.args.account,self.__class__.acc_pwd[1],env=self.args.env,ttl=self.args.ttl)

		logging.info(f' ========== 测试结束 CMBI-152 boss重置密码后修改密码 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_153(self):
		'''账户解锁后登陆成功'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-153 账户解锁后登陆成功 ========== ')
		if self.args.env=='prod':self.skipTest('跳过')
		logout(self.driver)

		for i in range(11):
			try:login_acc(self.args.account,'****',env=self.args.env,ttl=self.args.ttl)
			except:pass
		try:
			self.__class__.pageBar.clickMy(timeout=5,screen=False)
			self.__class__.pageMy.clickLogin()
			self.__class__.pageLogin_u.clickCheckView(self.args.appVersion,env=self.args.env)
			self.__class__.pageLogin_u.inputUname(self.__class__.acc_pwd[0])
			self.__class__.pageLogin_u.clickLogin()
			self.__class__.pageLogin_p.inputPword(self.__class__.acc_pwd[1])
			self.__class__.pageLogin_p.clickConfirm()
			
			card_id=get_cardID(self.args.account,self.args.env)[0][0]
			time.sleep(5)
			swithToRightWeb(self.driver,'/settle/unlock')
			self.__class__.pageUnlockAcc.click_confirm()
			time.sleep(5)
			self.__class__.pageUnlockAcc.input_cardid(card_id)
			self.__class__.pageUnlockAcc.click_next()
			time.sleep(5)
			self.__class__.pageUnlockAcc.input_smscode('8888')
			self.__class__.pageUnlockAcc.click_unlock()
			self.__class__.pageUnlockAcc.click_done()
			swithToRightWeb(self.driver,0)
			self.__class__.pageBar.goBack(2)

			login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
			nickName=self.__class__.pageMy.textNick()
			logging.info(f'用户昵称: {nickName}')
			self.assertIsNotNone(nickName)
		except Exception as err:
			raise err
		finally:
			unlockAcc(self.args.account,self.args.env)


		logging.info(f' ========== 测试结束 CMBI-153 账户解锁后登陆成功 ========== ')



	def tearDown(self):
		time.sleep(1)
		# self.__class__.pageBar.goBack()

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 我的 模块测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass