import logging,unittest,time
from HTMLReport import no_retry,ddt

from common.parameter import ParameTestCase
from common.tools import swithToRightWeb,keyboardInput,myAddScreen

from business.logInOut import login,logout
from business.others import reOpenApp

from page.navBar import PageBar
from page.alert import PageAlert
from page.trade.trade import PageTrade
from page.trade.fund import PageFund

from testData.data import accountPool

# @unittest.skip('跳过')
@ddt.ddt
class TestTradeFund(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 基金交易测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageTrade=PageTrade(cls.driver)
		cls.pageFund=PageFund(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.acc_pwd=(cls.args.account,accountPool[cls.args.account][0])
		cls.nickName=accountPool[cls.args.account][1]

	def setUp(self):
		if self.args.debug:return
		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
		self.__class__.pageBar.clickTrade()
		# self.__class__.pageAlert.clickAlert()
		self.__class__.pageTrade.clickFund()
		# self.__class__.pageAlert.clickAlert()

	# @no_retry
	# @unittest.skip('跳过')
	@ddt.data(*['HKD','USD'])
	def test_01_CMBI_5507(self,currency):
		'''申购基金'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-5507 {currency} 申购基金 ========== ')
		self.__class__.pageFund.clickFundMarket()
		# self.__class__.pageAlert.clickAlert()
		self.__class__.pageFund.clickIknow()
		swithToRightWeb(self.driver,'/fund-sys/fund')
		self.__class__.pageFund.clickAllfund() # 点击全部基金
		
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.__class__.pageFund.clickFilter()
		self.__class__.pageFund.clickReset()
		# swithToRightWeb(self.driver,0)
		if currency=='HKD':
			self.__class__.pageFund.clickFilterHK()
		elif currency=='USD':
			self.__class__.pageFund.clickFilterUS()
		self.__class__.pageFund.clickFilterLowRisk()
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.__class__.pageFund.clickComfirm(js=1)
		self.__class__.pageFund.clickFundOne()# 点击列表里的第一个
		swithToRightWeb(self.driver,'/fundDetail')
		# /fund-sys/fundDetail
		# 点击认购
		self.__class__.pageFund.clickBuy()
		swithToRightWeb(self.driver,'/apply')
		buyMoney=self.__class__.pageFund.getMinMoney()

		self.__class__.pageFund.clickInputAmount()
		keyboardInput(self.driver,buyMoney)
		time.sleep(2)

		fundName=self.__class__.pageFund.textFundisin()
		self.__class__.pageFund.clickAgree()
		# self.__class__.pageFund.clickAgree1()
		self.__class__.pageFund.clickBuy2()
		self.__class__.pageFund.clickComfirmBuy()
		self.__class__.pageFund.clickIknow_web()

		# self.__class__.pageFund.clickComfirm()
		time.sleep(3)
		self.assertEqual(fundName,self.__class__.pageFund.textOrderName())
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'截图')
		self.__class__.pageBar.goBack(3)
		logging.info(f' ========== 测试结束 CMBI-5507 {currency} 申购基金 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_02_CMBI_5542(self):
		'''赎回基金'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(' ========== 测试开始 CMBI-5542 赎回基金 ========== ')
		self.__class__.pageFund.clickRedeem()
		swithToRightWeb(self.driver,'/redeem')
		self.__class__.pageFund.clickAgree()

		self.__class__.pageFund.clickInputAmount()
		keyboardInput(self.driver,'500')
		time.sleep(2)
		self.__class__.pageFund.clickRedeem1()
		self.__class__.pageFund.clickComfirmBuy()
		self.__class__.pageFund.clickIknow_web()

		# self.assertEqual(1,self.__class__.pageFund.successMsg1Exists())
		# self.__class__.pageFund.clickComfirm()
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'截图')
		# swithToRightWeb(self.driver,'fund-sys/records')
		# self.assertEqual('赎回',self.__class__.pageFund.textRedeemFlag())
		self.__class__.pageFund.goBack(1)
		logging.info(' ========== 测试结束 CMBI-5542 赎回基金 ========== ')

	# @no_retry
	# @unittest.skip('跳过')
	def test_03_CMBI_0000(self):
		'''基金定投'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-0000 基金定投 ========== ')
		self.__class__.pageFund.clickFundMarket()
		# self.__class__.pageAlert.clickAlert()
		self.__class__.pageFund.clickIknow()
		swithToRightWeb(self.driver,'/fund-sys/fund')
		self.__class__.pageFund.clickAllfund() # 点击全部基金
		
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.__class__.pageFund.clickFilter()
		self.__class__.pageFund.clickReset()
		# swithToRightWeb(self.driver,0)
		self.__class__.pageFund.clickFilterHK()
		self.__class__.pageFund.clickFilterLowRisk()
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.__class__.pageFund.clickComfirm(js=1)
		self.__class__.pageFund.clickFundOne()# 点击列表里的第一个
		swithToRightWeb(self.driver,'/fundDetail')
		
		self.__class__.pageFund.clickBuyPlan()# 点击定投
		swithToRightWeb(self.driver,'/fund-sys/castSurely')

		buyMoney=self.__class__.pageFund.getMinMoney()
		self.__class__.pageFund.clickInputAmount()
		keyboardInput(self.driver,buyMoney)
		time.sleep(2)

		fundName=self.__class__.pageFund.textFundisin()
		self.__class__.pageFund.clickAgree()
		# self.__class__.pageFund.clickAgree1()
		self.__class__.pageFund.clickBuyPlan2()
		self.__class__.pageFund.clickComfirmBuy()
		self.__class__.pageFund.clickCheckPlan()
		swithToRightWeb(self.driver,'/fund-sys/castSurelyList')
		myAddScreen(self,'截图')
		self.__class__.pageFund.clickplanItems()
		self.__class__.pageFund.clickstopPlan()
		self.__class__.pageFund.clickComfirmBuy()
		self.assertTrue(self.__class__.pageFund.flag_stopedPlan())
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'截图')
		self.__class__.pageBar.goBack(4)
		logging.info(f' ========== 测试结束 CMBI-0000 基金定投 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_04_CMBI_5523(self):
		'''基金页户口切换'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(' ========== 测试开始 CMBI-5523 基金页户口切换 ========== ')
		try:
			self.__class__.pageFund.clickAccount()
			accountM=self.__class__.pageFund.clickAccount1(self.args.account)
			self.__class__.pageFund.inputPwd(accountPool[accountM][0])
			self.__class__.pageFund.clickLogin()
			time.sleep(3)
			self.assertEqual(0,self.__class__.pageFund.loginExists(5))
			reOpenApp(self.driver)
		except:
			reOpenApp(self.driver)
			raise Exception('切换户口失败')
		finally:
			logout(self.driver)
		logging.info(' ========== 测试结束 CMBI-5523 基金页户口切换 ========== ')

	def tearDown(self):
		if self.args.debug:return
		self.__class__.pageBar.goBack()
		# swithToRightWeb(self.driver,0)

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 基金交易测试结束！ ########## ')

if __name__=='__main__':
	# unittest.main()
	pass