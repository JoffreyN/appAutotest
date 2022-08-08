from HTMLReport import ddt
import time,logging,unittest

from page.navBar import PageBar
from page.alert import PageAlert
from page.trade.buy import PageBuy
from page.trade.sell import PageSell
from page.trade.fund import PageFund
from page.home.appMore import PageMore
from page.trade.trade import PageTrade
from page.market.stock import PageStock
from page.trade.orders import PageOrders
from page.trade.trade_alert import PageTradeAlert
from page.mine.staticAssets import PageStaticAssets
from page.mine.businesWeek.statement import PageStatement

from business.logInOut import login
from common.tools import swithToRightWeb,myAddScreen
from common.parameter import ParameTestCase

from testData.data import tradeData,accountPool

# @unittest.skip('跳过')
@ddt.ddt
class TestAccUIview(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 账户UI总览 模块测试开始 ########## ')
		cls.acc_pwd=(cls.args.account,accountPool[cls.args.account][0])
		cls.pageStaticAssets=PageStaticAssets(cls.driver)
		cls.nickName=accountPool[cls.args.account][1]
		cls.pageTradeAlert=PageTradeAlert(cls.driver)
		cls.pageStatement=PageStatement(cls.driver)
		cls.pageOrders=PageOrders(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageTrade=PageTrade(cls.driver)
		cls.pageStock=PageStock(cls.driver)
		cls.pageMore=PageMore(cls.driver)
		cls.pageFund=PageFund(cls.driver)
		cls.pageSell=PageSell(cls.driver)
		cls.pageBar=PageBar(cls.driver)
		cls.pageBuy=PageBuy(cls.driver)
		cls.pageBuy=PageBuy(cls.driver)
		cls.ordersURL='/appweb/trade'

	def setUp(self):
		if self.args.debug:return
		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
		self.__class__.pageBar.clickTrade()
		# self.__class__.pageAlert.clickAlert()
		
	# @unittest.skip('跳过')
	@ddt.data('股票交易跳转','订单查询跳转','静态资产跳转','结单查询跳转','更多跳转')
	def test_CMBI_22440(self,types):
		'''港股市场功能入口'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22440 港股市场功能入口 ========== ')
		self.__class__.pageTrade.clickStockHK()
		# self.__class__.pageAlert.clickAlert()
		if types=='股票交易跳转':
			myAddScreen(self,'点击港股后截图')
			self.__class__.pageTrade.clickTrade()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,self.__class__.ordersURL)
			myAddScreen(self,'点击股票交易后截图')
			self.assertTrue(self.__class__.pageBuy.flagExists())
		elif types=='订单查询跳转':
			self.__class__.pageTrade.clickOrder()
			swithToRightWeb(self.driver,self.__class__.ordersURL)
			self.assertTrue(self.__class__.pageOrders.flagExists())
		elif types=='静态资产跳转':
			self.__class__.pageTrade.clickStaticAssets()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,'/trade_v2.html#/StaticPortfolio')
			self.assertTrue(self.__class__.pageStaticAssets.flagExists())
		elif types=='结单查询跳转':
			self.__class__.pageTrade.clickInquire()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,'/index.html#/checkInquire')
			self.assertTrue(self.__class__.pageStatement.flagExists())
		elif types=='更多跳转':
			self.__class__.pageTrade.clickMore()
			swithToRightWeb(self.driver,'/appMap')
			self.assertTrue(self.__class__.pageMore.flagExists())
		swithToRightWeb(self.driver,0)
		# self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-22440 港股市场功能入口 ========== ')

	# @unittest.skip('跳过')
	@ddt.data('股票交易跳转','订单查询跳转','静态资产跳转','结单查询跳转','更多跳转')
	def test_CMBI_22441(self,types):
		'''美股市场功能入口'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22441 美股市场功能入口 ========== ')
		self.__class__.pageTrade.clickStockUS()
		# self.__class__.pageAlert.clickAlert()
		if types=='股票交易跳转':
			myAddScreen(self,'点击美股后截图')
			self.__class__.pageTrade.clickTrade()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,self.__class__.ordersURL)
			myAddScreen(self,'点击股票交易后截图')
			self.assertTrue(self.__class__.pageBuy.flagExists())
		elif types=='订单查询跳转':
			self.__class__.pageTrade.clickOrder()
			swithToRightWeb(self.driver,self.__class__.ordersURL)
			self.assertTrue(self.__class__.pageOrders.flagExists())
		elif types=='静态资产跳转':
			self.__class__.pageTrade.clickStaticAssets()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,'/trade_v2.html#/StaticPortfolio')
			self.assertTrue(self.__class__.pageStaticAssets.flagExists())
		elif types=='结单查询跳转':
			self.__class__.pageTrade.clickInquire()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,'/index.html#/checkInquire')
			self.assertTrue(self.__class__.pageStatement.flagExists())
		elif types=='更多跳转':
			self.__class__.pageTrade.clickMore()
			swithToRightWeb(self.driver,'/appMap')
			self.assertTrue(self.__class__.pageMore.flagExists())
		swithToRightWeb(self.driver,0)
		# self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-22441 美股市场功能入口 ========== ')

	# @unittest.skip('跳过')
	@ddt.data('订单查询跳转','静态资产跳转','结单查询跳转','更多跳转')
	def test_CMBI_22442(self,types):
		'''中华通市场功能入口'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22442 中华通市场功能入口 ========== ')
		self.__class__.pageTrade.clickStockA()
		# self.__class__.pageAlert.clickAlert()
		if types=='股票交易跳转':
			myAddScreen(self,'截图')
			self.__class__.pageTrade.clickTrade()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,self.__class__.ordersURL)
			self.assertTrue(self.__class__.pageBuy.flagExists())
		elif types=='订单查询跳转':
			self.__class__.pageTrade.clickOrder()
			swithToRightWeb(self.driver,self.__class__.ordersURL)
			self.assertTrue(self.__class__.pageOrders.flagExists())
		elif types=='静态资产跳转':
			self.__class__.pageTrade.clickStaticAssets()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,'/trade_v2.html#/StaticPortfolio')
			self.assertTrue(self.__class__.pageStaticAssets.flagExists())
		elif types=='结单查询跳转':
			self.__class__.pageTrade.clickInquire()
			# self.__class__.pageAlert.clickAlert()
			swithToRightWeb(self.driver,'/index.html#/checkInquire')
			self.assertTrue(self.__class__.pageStatement.flagExists())
		elif types=='更多跳转':
			self.__class__.pageTrade.clickMore()
			swithToRightWeb(self.driver,'/appMap')
			self.assertTrue(self.__class__.pageMore.flagExists())
		swithToRightWeb(self.driver,0)
		# self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-22442 中华通市场功能入口 ========== ')

	# # @unittest.skip('跳过')
	# @ddt.data('基金市场','基金自选','订单查询','更多跳转')
	# def test_CMBI_22443(self,types):
	# 	'''基金市场功能入口'''
	# 	if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-22443 基金市场功能入口 ========== ')
	# 	self.__class__.pageTrade.clickFund()
	# 	# self.__class__.pageAlert.clickAlert()
	# 	if types=='基金市场':
	# 		self.__class__.pageFund.clickFundMarket()
	# 		# self.__class__.pageAlert.clickAlert()
	# 		swithToRightWeb(self.driver,'/fund')
	# 		# self.assertTrue(self.__class__.pageFund.flagExists())
	# 	elif types=='基金自选':
	# 		self.__class__.pageFund.clickOptionalFund()
	# 		self.assertTrue(self.__class__.pageFund.flagExists_mine())
	# 	elif types=='订单查询':
	# 		self.__class__.pageFund.clickFundorderquery()
	# 		swithToRightWeb(self.driver,'/fund-sys/records')
	# 		self.assertTrue(self.__class__.pageFund.flagExists_fundOrders())
	# 	elif types=='更多跳转':
	# 		self.__class__.pageTrade.clickMore()
	# 		swithToRightWeb(self.driver,'/appMap')
	# 		self.assertTrue(self.__class__.pageMore.flagExists())
	# 	swithToRightWeb(self.driver,0)
	# 	# self.__class__.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-22443 基金市场功能入口 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22458(self):
		'''验证点击持仓数据，打开功能抽屉'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:self.skipTest('ttl账户无持仓')
		logging.info(f' ========== 测试开始 CMBI-22458 验证点击持仓数据，打开功能抽屉 ========== ')
		logging.info(f'该条用例已包含于 CMBI-22459、CMBI-22460、CMBI-22461')
		logging.info(f' ========== 测试结束 CMBI-22458 验证点击持仓数据，打开功能抽屉 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22459(self):
		'''验证点击功能抽屉行情入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:self.skipTest('ttl账户无持仓')
		logging.info(f' ========== 测试开始 CMBI-22459 验证点击功能抽屉行情入口跳转正常 ========== ')
		self.__class__.pageTrade.clickStockHK()
		# self.__class__.pageAlert.clickAlert()
		stockName=self.__class__.pageTrade.getStockNameOne()
		self.__class__.pageTrade.clickHoldOne()
		self.__class__.pageTrade.clickDrawerMarket()
		# self.__class__.pageAlert.clickAlert()
		self.assertIn(stockName,self.__class__.pageStock.getStockName())
		self.assertTrue(self.__class__.pageStock.flagExists())
		logging.info(f' ========== 测试结束 CMBI-22459 验证点击功能抽屉行情入口跳转正常 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22460(self):
		'''验证点击功能抽屉买入入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:self.skipTest('ttl账户无持仓')
		logging.info(f' ========== 测试开始 CMBI-22460 验证点击功能抽屉买入入口跳转正常 ========== ')
		self.__class__.pageTrade.clickStockUS()
		# self.__class__.pageAlert.clickAlert()
		stockName=self.__class__.pageTrade.getStockNameOne()
		self.__class__.pageTrade.clickHoldOne()
		self.__class__.pageTrade.clickDrawerBuy()
		swithToRightWeb(self.driver,self.__class__.ordersURL)
		self.assertTrue(self.__class__.pageBuy.flagExists())
		swithToRightWeb(self.driver,0)
		logging.info(f' ========== 测试结束 CMBI-22460 验证点击功能抽屉买入入口跳转正常 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22461(self):
		'''验证点击功能抽屉卖出入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:self.skipTest('ttl账户无持仓')
		logging.info(f' ========== 测试开始 CMBI-22461 验证点击功能抽屉卖出入口跳转正常 ========== ')
		self.__class__.pageTrade.clickStockHK()
		# self.__class__.pageAlert.clickAlert()
		stockName=self.__class__.pageTrade.getStockNameOne()
		self.__class__.pageTrade.clickHoldOne()
		self.__class__.pageTrade.clickDrawerSell()
		swithToRightWeb(self.driver,self.__class__.ordersURL)
		self.assertTrue(self.__class__.pageSell.flagExists())
		swithToRightWeb(self.driver,0)
		logging.info(f' ========== 测试结束 CMBI-22461 验证点击功能抽屉卖出入口跳转正常 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22477(self):
		'''验证点击今日订单打开功能抽屉'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22477 验证点击今日订单打开功能抽屉 ========== ')
		logging.info(f'该条用例已包含于 CMBI-22478 ~ CMBI-22485')
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-22477 验证点击今日订单打开功能抽屉 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22478(self):
		'''验证点击今日订单功能抽屉行情入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22478 验证点击今日订单功能抽屉行情入口跳转正常 ========== ')
		self.__class__.pageTrade.clickStockHK()
		# self.__class__.pageAlert.clickAlert()
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.driver,self.__class__.ordersURL)
		stockCode=self.__class__.pageOrders.getStockCode()
		stockName=self.__class__.pageOrders.getStockName()
		self.__class__.pageOrders.clickStockInfo()
		swithToRightWeb(self.driver,0)
		self.__class__.pageStock.clickTrade()
		swithToRightWeb(self.driver,'appweb/trade/?productNo')
		self.assertIn(stockName,self.__class__.pageBuy.getstockName())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-22478 验证点击今日订单功能抽屉行情入口跳转正常 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22479(self):
		'''验证点击今日订单功能抽屉中"修改"入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22479 验证点击今日订单功能抽屉中"修改"入口跳转正常 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.driver,self.__class__.ordersURL)
		# self.__class__.pageOrders.openPYPL()
		self.__class__.pageOrders.clickChangeOrder()
		swithToRightWeb(self.driver,'/trade/modify')
		self.assertTrue(self.__class__.pageSell.flagExists())
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-22479 验证点击今日订单功能抽屉中"修改"入口跳转正常 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22482(self):
		'''验证点击今日订单功能抽屉中"撤销"入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22482 验证点击今日订单功能抽屉中"撤销"入口跳转正常 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickCancelOrder()
		self.assertTrue(self.__class__.pageTradeAlert.flagExists())
		self.__class__.pageTradeAlert.clickCancel()
		logging.info(f' ========== 测试结束 CMBI-22482 验证点击今日订单功能抽屉中"撤销"入口跳转正常 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_22485(self):
		'''验证点击今日订单功能抽屉中"详情"入口跳转正常'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-22485 验证点击今日订单功能抽屉中"详情"入口跳转正常 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickOrderDetail()
		swithToRightWeb(self.driver,'trade/about?orderId')
		self.assertTrue(self.__class__.pageOrders.detilFlagExists())
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-22485 验证点击今日订单功能抽屉中"详情"入口跳转正常 ========== ')

	# @unittest.skip('跳过，无基金持仓')
	# def test_CMBI_22496(self):
	# 	'''验证点击基金持仓打开功能抽屉'''
	# 	logging.info(f' ========== 测试开始 CMBI-22485 验证点击基金持仓打开功能抽屉 ========== ')
	# 	logging.info(f'该条用例已包含于 CMBI-22497 ~ CMBI-22499')
	# 	# self.__class__.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-22485 验证点击基金持仓打开功能抽屉 ========== ')

	# @unittest.skip('跳过，无基金持仓')
	# def test_CMBI_22497(self):
	# 	'''验证点击基金持仓功能抽屉"行情"入口跳转正常'''
	# 	logging.info(f' ========== 测试开始 CMBI-22497 验证点击基金持仓功能抽屉"行情"入口跳转正常 ========== ')
	# 	self.__class__.pageTrade.clickFund()
		# self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageFund.clickOpen()
	# 	self.__class__.pageFund.clickDetail()
	# 	swithToRightWeb(self.driver,'fund-sys/fundDetail')
	# 	self.assertTrue(self.__class__.pageFund.flag_DetailsExists())
	# 	logging.info(f' ========== 测试结束 CMBI-22497 验证点击基金持仓功能抽屉"行情"入口跳转正常 ========== ')

	# @unittest.skip('跳过，无基金持仓')
	# def test_CMBI_22498(self):
	# 	'''验证点击基金持仓功能抽屉"申购"入口跳转正常'''
	# 	logging.info(f' ========== 测试开始 CMBI-22498 验证点击基金持仓功能抽屉"申购"入口跳转正常 ========== ')
	# 	self.__class__.pageTrade.clickFund()
		# self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageFund.clickOpen()
	# 	self.__class__.pageFund.clickApplyBuy()
	# 	swithToRightWeb(self.driver,'fund-sys/apply')
	# 	self.assertTrue(self.__class__.pageFund.flag_applyBuyExists())
	# 	logging.info(f' ========== 测试结束 CMBI-22498 验证点击基金持仓功能抽屉"申购"入口跳转正常 ========== ')

	# @unittest.skip('跳过，无基金持仓')
	# def test_CMBI_22499(self):
	# 	'''验证点击基金持仓功能抽屉"赎回"入口跳转正常'''
	# 	logging.info(f' ========== 测试开始 CMBI-22499 验证点击基金持仓功能抽屉"赎回"入口跳转正常 ========== ')
	# 	self.__class__.pageTrade.clickFund()
		# self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageFund.clickOpen()
	# 	self.__class__.pageFund.clickRedeem()
	# 	swithToRightWeb(self.driver,'fund-sys/redeem')
	# 	self.assertTrue(self.__class__.pageFund.flag_redeemExists())
	# 	logging.info(f' ========== 测试结束 CMBI-22499 验证点击基金持仓功能抽屉"赎回"入口跳转正常 ========== ')

	def tearDown(self):
		if self.args.debug:return
		self.__class__.pageBar.goBack()

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 账户UI总览 模块测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass
