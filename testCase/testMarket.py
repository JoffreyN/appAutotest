import time,logging,unittest
from HTMLReport import ddt,no_retry

from common.parameter import ParameTestCase
from common.tools import swithToRightWeb,myAddScreen
from business.logInOut import login

from page.navBar import PageBar
from page.market.market import PageMarket
from page.market.stock import PageStock
from page.alert import PageAlert
from page.trade.trade import PageTrade
from page.trade.buy import PageBuy

from testData.data import accountPool,regData


# @unittest.skip('跳过')
@ddt.ddt
class TestMarket(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 行情 模块测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageMarket=PageMarket(cls.driver)
		cls.pageStock=PageStock(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageTrade=PageTrade(cls.driver)
		cls.pageBuy=PageBuy(cls.driver)
		cls.acc_pwd=regData[cls.args.account]['bmp_acc']
		cls.nickName=accountPool[cls.acc_pwd[0]][1]


	def setUp(self):
		if self.args.debug:return
		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
		self.__class__.pageBar.clickMarket()
		# self.__class__.pageAlert.clickAlert()

	# @unittest.skip('跳过')
	# @no_retry
	def test_market_01(self):
		'''BMP行情相关样式检查'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 market_01 BMP行情相关样式检查 ========== ')
		self.__class__.pageMarket.clickTabMY()
		self.__class__.pageMarket.clickTengxun()
		myAddScreen(self,'bmp横幅截图')
		self.assertTrue(self.__class__.pageStock.BMPflagExists())
		self.__class__.pageStock.clickTrade()
		swithToRightWeb(self.driver,'/appweb/trade')
		myAddScreen(self,'涨跌幅及现价、买卖盘及刷新按钮截图')
		price=self.__class__.pageBuy.getprice()
		increase=self.__class__.pageBuy.getincrease()
		self.assertIsNotNone(price)
		self.assertIsNotNone(increase)
		self.assertTrue(self.__class__.pageBuy.refreshIcon_exists())

		
		#断言买盘卖盘数据
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('b',1))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('b',2))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('b',3))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('b',4))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('b',5))
		
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('s',1))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('s',2))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('s',3))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('s',4))
		self.assertTrue(self.__class__.pageBuy.buy_sell_price_exists('s',5))

		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(3)

		logging.info(f' ========== 测试结束 market_01 BMP行情相关样式检查 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# @ddt.data(*searchData)
	# def test_CMBI_164(self,infoData):
	# 	'''股票搜索'''
	# 	logging.info(f' ========== 测试开始 CMBI-164 股票搜索 ========== ')
	# 	if self.__class__.pageBar.PFN=="Android":
	# 		self.skipTest('搜索结果出来后无法获取页面，页面卡死。 Original error: Timed out after 10000 milliseconds waiting for root AccessibilityNodeInfo')
	# 	else:
	# 		self.__class__.pageMarket.clickSearch()
	# 		self.__class__.pageMarket.inputSearch(infoData['inputs'])
	# 		self.assertEqual(1,self.__class__.pageMarket.textExists(infoData['expect']))
	# 		self.__class__.pageMarket.clickCancel()
	# 		# self.__class__.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-164 股票搜索 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_CMBI_165(self):
	# 	'''添加自选'''
	# 	logging.info(f' ========== 测试开始 CMBI-165 添加自选 ========== ')
	# 	if self.__class__.pageBar.PFN=="Android":
	# 		self.skipTest('搜索结果出来后无法获取页面，页面卡死。 Original error: Timed out after 10000 milliseconds waiting for root AccessibilityNodeInfo')
	# 	else:
	# 		self.__class__.pageMarket.clickSearch()
	# 		self.__class__.pageMarket.inputSearch('BILI')
	# 		self.__class__.pageMarket.clickCollect()
	# 		self.__class__.pageMarket.clickCancel()
	# 		self.__class__.pageMarket.clickTabMY()
	# 		self.assertEqual('哔哩哔哩',self.__class__.pageMarket.textStockName())
	# 		#删除自选
	# 		for i in range(3):
	# 			try:
	# 				self.__class__.pageMarket.clickStockEdit()
	# 				break
	# 			except AttributeError:
	# 				if i==2:raise AttributeError
	# 		self.__class__.pageMarket.clickSelectAll()
	# 		self.__class__.pageMarket.clickDelete()
	# 		self.__class__.pageMarket.clickDone()
	# 	logging.info(f' ========== 测试结束 CMBI-165 添加自选 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_CMBI_170(self):
	# 	'''港股跳转'''
	# 	logging.info(f' ========== 测试开始 CMBI-170 港股跳转 ========== ')
	# 	# if self.__class__.pageBar.PFN=="iOS":
	# 	# 	self.skipTest('无法获取市场-港股Tab页面')
	# 	self.__class__.pageMarket.clickMarket()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageMarket.clickTabHK()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageMarket.clickStock2()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.assertEqual(1,self.__class__.pageStock.flagExists())
	# 	self.__class__.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-170 港股跳转 ========== ')

	# # # @unittest.skip('跳过')
	# # def test_CMBI_172(self):
	# # 	'''港股新闻跳转'''
	# # 	logging.info(f' ========== 测试开始 CMBI-172 港股新闻跳转 ========== ')
	# # 	if self.__class__.pageBar.PFN=='Android':
	# # 		self.__class__.pageMarket.clickMarket()
	# #		self.__class__.pageAlert.clickAlert()
	# # 		self.__class__.pageMarket.clickTabHK()
	# #		self.__class__.pageAlert.clickAlert()
	# # 		self.__class__.pageMarket.clickStock2()
	# #		self.__class__.pageAlert.clickAlert()
	# # 	else:
	# # 		self.__class__.pageMarket.clickSearch()
	# # 		self.__class__.pageMarket.inputSearch('00700')
	# # 		self.__class__.pageMarket.clickSearchResult()
	# # 	swithToRightWeb(self.driver,'index.html#/individualStock')
	# # 	self.__class__.pageStock.clickNews()

	# # 	newsTitle=self.__class__.pageStock.listOneTitle()
	# # 	self.__class__.pageStock.clickListOne()
	# # 	swithToRightWeb(self.driver,'index.html#/detail')
	# # 	self.assertEqual(newsTitle,self.__class__.pageStock.getDetailTitle())
	# # 	swithToRightWeb(self.driver,0)
	# # 	self.__class__.pageBar.goBack(n=2)
	# # 	if self.__class__.pageBar.PFN=='iOS':self.__class__.pageMarket.clickCancel()
	# # 	logging.info(f' ========== 测试结束 CMBI-172 港股新闻跳转 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_CMBI_173(self):
	# 	'''港股公告跳转'''
	# 	logging.info(f' ========== 测试开始 CMBI-173 港股公告跳转 ========== ')
	# 	if self.__class__.pageBar.PFN=='Android':
	# 		self.__class__.pageMarket.clickMarket()
	# 		self.__class__.pageAlert.clickAlert()
	# 		self.__class__.pageMarket.clickTabHK()
	# 		self.__class__.pageAlert.clickAlert()
	# 		self.__class__.pageMarket.clickStock2()
	# 		self.__class__.pageAlert.clickAlert()
	# 	else:
	# 		self.__class__.pageMarket.clickSearch()
	# 		self.__class__.pageMarket.inputSearch('00700')
	# 		self.__class__.pageMarket.clickSearchResult()
	# 	swithToRightWeb(self.driver,'index.html#/individualStock')
	# 	self.__class__.pageStock.clickNotice()

	# 	newsTitle=self.__class__.pageStock.listOneTitle()
	# 	self.__class__.pageStock.clickListOne()
	# 	swithToRightWeb(self.driver,'index.html#/detail')
	# 	self.assertEqual(newsTitle,self.__class__.pageStock.getDetailTitle())
	# 	swithToRightWeb(self.driver,0)
	# 	self.__class__.pageBar.goBack(n=2)
	# 	if self.__class__.pageBar.PFN=='iOS':self.__class__.pageMarket.clickCancel()
	# 	logging.info(f' ========== 测试结束 CMBI-173 港股公告跳转 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_CMBI_180(self):
	# 	'''美股跳转'''
	# 	logging.info(f' ========== 测试开始 CMBI-178 美股跳转 ========== ')
	# 	if self.__class__.pageBar.PFN=="iOS":
	# 		self.skipTest('无法获取市场-美股Tab页面')
	# 	self.__class__.pageBar.clickMarket()
	# 	self.__class__.pageAlert.clickAlert()
		
	# 	self.__class__.pageMarket.clickMarket()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageMarket.clickTabUS()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageMarket.clickStock2()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.assertEqual(1,self.__class__.pageStock.flagExists())
	# 	self.__class__.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-178 美股跳转 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_CMBI_178(self):
	# 	'''沪深港通跳转'''
	# 	logging.info(f' ========== 测试开始 CMBI-180 沪深港通跳转 ========== ')
	# 	# if self.__class__.pageBar.PFN=="iOS":
	# 	# 	self.skipTest('无法获取市场-港股Tab页面')
	# 	self.__class__.pageMarket.clickMarket()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageMarket.clickTabSHHK()
	# 	self.__class__.pageAlert.clickAlert()
	# 	self.__class__.pageMarket.clickStock2('AH')
	# 	self.assertEqual(1,self.__class__.pageStock.flagExists())
	# 	self.__class__.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-180 沪深港通跳转 ========== ')

	# # # @unittest.skip('跳过')
	# # def test_CMBI_181(self):
	# # 	'''沪深股跳转'''
	# # 	logging.info(f' ========== 测试开始 CMBI-181 沪深股跳转 ========== ')
	# # 	self.__class__.pageMarket.clickMarket()
	# # 	self.__class__.pageAlert.clickAlert()
	# # 	self.__class__.pageMarket.clickTabSHSZ()
	# # 	self.__class__.pageMarket.clickStock2()
	# #	self.__class__.pageAlert.clickAlert()
	# # 	self.assertEqual(1,self.__class__.pageStock.flagExists())
	# # 	self.__class__.pageBar.goBack()
	# # 	logging.info(f' ========== 测试结束 CMBI-181 沪深股跳转 ========== ')


	def tearDown(self):
		pass
		# self.__class__.pageBar.goBack()

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 行情 模块测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass
