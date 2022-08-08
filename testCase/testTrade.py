import time,logging,traceback,re,unittest,threading
from HTMLReport import ddt,addImage,no_retry

from common.parameter import ParameTestCase
from common.apiCenter import addHOld_ttl
from common.tools import isTradeTime,ifskip,swithToRightWeb,myAddScreen,swipeUp
from common.dbOperation import insertMoney,insertStock,excuteSQL
from common.system_boss import inmoney_CMS
from business.logInOut import login,logout

from page.navBar import PageBar
from page.trade.trade import PageTrade
from page.trade.buy import PageBuy
from page.trade.sell import PageSell
from page.trade.trade_alert import PageTradeAlert
from page.trade.orders import PageOrders
from page.alert import PageAlert
from page.market.market import PageMarket
from page.market.stock import PageStock

from testData.data import tradeData,accountPool,accBinding

# @unittest.skip('跳过')
@ddt.ddt
class TestTrade(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 股票交易测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageTrade=PageTrade(cls.driver)
		cls.pageBuy=PageBuy(cls.driver)
		cls.pageSell=PageSell(cls.driver)
		cls.pageTradeAlert=PageTradeAlert(cls.driver)
		cls.pageOrders=PageOrders(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)

		cls.pageMarket=PageMarket(cls.driver)
		cls.pageStock=PageStock(cls.driver)

		cls.ordersURL='/appweb/trade'
		if cls.pageBar.PFN=='Android':
			cls.changeBack=3
			cls.tradeBack=4
		else:
			cls.changeBack=3
			cls.tradeBack=1

	def setUp(self):
		if self.args.debug:return
		acc_pwd=(self.args.account,accountPool[self.args.account][0])
		nickName=accountPool[self.args.account][1]
		login(self.__class__.driver,acc_pwd,cusNickName=nickName,args=self.args)
		self.__class__.pageBar.clickTrade()
		self.__class__.pageAlert.clickAlert()
		self.__class__.pageTrade.clickStockHK()
		self.__class__.pageAlert.clickAlert()

	def reOrder(self,side='s'):
		if self.__class__.pageTradeAlert.failedFlagExists():#不在价位范围内
			price=self.__class__.pageTradeAlert.getPrice()
			self.__class__.pageTradeAlert.clickIknow()
			self.__class__.pageBuy.inputPrice(price)
			self.__class__.pageOrders.clickPriceMinus_order(1)

			if side=='b':
				self.__class__.pageBuy.clickBuy()
				time.sleep(1)
				myAddScreen(self,'点击买入后截图')
				flag1=self.__class__.pageBuy.flag1Exists()
				self.__class__.pageTradeAlert.clickConfirm()
				time.sleep(1)
				myAddScreen(self,'买入确认后截图')
			else:
				self.__class__.pageSell.clickSell()
				time.sleep(1)
				myAddScreen(self,'点击卖出后截图')
				self.assertFalse(self.__class__.pageSell.flag1Exists())
				self.__class__.pageTradeAlert.clickConfirm()
				time.sleep(1)
				myAddScreen(self,'卖出确认后截图')
		else:
			pass

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['b']['HK'])
	@ddt.data(*['限价单','特殊限价单','竞价限价单','竞价单','增强限价单'])
	# @ddt.data(*['竞价单'])
	def test_01_CMBI_5215(self,panName):
		'''股票交易买入港股'''
		if self.args.debug:self.skipTest('debug跳过')
		# logging.info(f'debug: {self.args.env} \n\n\n\n\n')
		if self.args.env!='prod':
			threading.Thread(target=inmoney_CMS,args=(self.args.account,'HKD','20000',self.args.env,1,)).start()#资金存入

		stockCode=tradeData[self.args.account]['b']['HK'][0]
		logging.info(f' ========== 测试开始 CMBI-5215 {panName} 股票交易买入港股 {stockCode} ========== ')
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		# self.__class__.pageBuy.clickTradeBuy()
		self.__class__.pageBuy.clickInput()#点击输入框
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageBuy.inputStock(stockCode)#输入股票代码
		self.__class__.pageBuy.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		if panName=='增强限价单':
			orderTypeTxt=self.__class__.pageBuy.getorderType()
			logging.info(f'订单类型为: {orderTypeTxt}')
			myAddScreen(self,'判断订单类型是 增强限价单 或 竞价限价单')
			if isTradeTime(time.time(),'HK'):
				flag=1 if '增强限价单' in orderTypeTxt or 'Enhanced Limit' in orderTypeTxt else 0
				self.assertTrue(flag)
			else:
				flag=1 if '竞价限价单' in orderTypeTxt or 'At-auction Limit' in orderTypeTxt else 0
				self.assertTrue(flag)
		else:
			self.__class__.pageBuy.changePan(panName)

		self.__class__.pageBuy.clickBuyPriceOne()
		# self.__class__.pageBuy.inputNum(1000)
		self.__class__.pageBuy.clickBuy()
		time.sleep(1)
		myAddScreen(self,'点击买入后截图')
		flag1=self.__class__.pageBuy.flag1Exists()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'买入确认后截图')
		self.reOrder('b')
		self.assertFalse(flag1)

		resultStockCode=self.__class__.pageBuy.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5215 {panName} 股票交易买入港股 {stockCode} ========== ')


	# @unittest.skip('跳过')
	# @no_retry
	def test_02_CMBI_5295(self):
		'''股票交易港股改单'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-5295 股票交易港股改单 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		Price=self.__class__.pageOrders.getOrderPrice()
		self.__class__.pageOrders.clickChangeOrder()
		swithToRightWeb(self.__class__.driver,'/trade/modify?')
		self.__class__.pageOrders.clickPriceMinus_order()
		# self.__class__.pageBuy.inputPrice(Price)
		self.__class__.pageBuy.clickBuy()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'trade/entrust')
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickOrderDetail()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'/trade/about?')
		self.__class__.pageOrders.clickChangeRecords()
		self.assertEqual(1,self.__class__.pageOrders.changeDetailExists())
		self.__class__.pageBar.goBack(self.__class__.changeBack-1)
		logging.info(f' ========== 测试结束 CMBI-5295 股票交易港股改单 ========== ')

	# @unittest.skip('跳过')
	def test_03_CMBI_5282(self):
		'''股票交易港股撤单'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-5282 股票交易港股撤单 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickCancelOrder()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'trade/entrust')
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickOrderDetail()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'/trade/about?')
		self.__class__.pageOrders.clickChangeRecords()
		self.assertEqual(1,self.__class__.pageOrders.cancelDetailExists())
		self.__class__.pageBar.goBack(self.__class__.changeBack-1)
		logging.info(f' ========== 测试结束 CMBI-5282 股票交易港股撤单 ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['b']['US'])
	def test_04_CMBI_5216(self):
		'''股票交易买入美股'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.env!='prod':
			threading.Thread(target=inmoney_CMS,args=(self.args.account,'USD','20000',self.args.env,1,)).start()#资金存入
		stockCode=tradeData[self.args.account]['b']['US'][0]
		logging.info(f' ========== 测试开始 CMBI-5216 股票交易买入美股 {stockCode} ========== ')
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		# self.__class__.pageBuy.clickTradeBuy()
		self.__class__.pageBuy.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageBuy.inputStock(stockCode)
		self.__class__.pageBuy.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		# self.__class__.pageBuy.clickBuyPriceOne()
		# self.__class__.pageBuy.inputNum(1000)

		# myAddScreen(self,'最大可买、订单类型是 限价单')
		# orderTypeTxt=self.__class__.pageBuy.getorderType()
		# logging.info(f'订单类型为: {orderTypeTxt}')
		# self.assertGreater(self.__class__.pageBuy.getMaxBuyNum(),0)
		# self.assertEqual('限价单',orderTypeTxt)
		
		self.__class__.pageBuy.clickNumOne()
		self.__class__.pageBuy.clickBuy()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'买入确认后截图')
		self.reOrder('b')
		resultStockCode=self.__class__.pageBuy.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5216 股票交易买入美股 {stockCode} ========== ')

	# @unittest.skip('跳过')
	def test_05_CMBI_5296(self):
		'''股票交易美股改单'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-5296 股票交易美股改单 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		Price=self.__class__.pageOrders.getOrderPrice()
		self.__class__.pageOrders.clickChangeOrder()
		swithToRightWeb(self.__class__.driver,'/trade/modify?')
		self.__class__.pageOrders.clickPriceMinus_order()
		# self.__class__.pageBuy.inputPrice(Price)
		self.__class__.pageBuy.clickBuy()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'trade/entrust')
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickOrderDetail()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'/trade/about?')
		self.__class__.pageOrders.clickChangeRecords()
		self.assertEqual(1,self.__class__.pageOrders.changeDetailExists())
		self.__class__.pageBar.goBack(self.__class__.changeBack-1)
		logging.info(f' ========== 测试结束 CMBI-5296 股票交易美股改单 ========== ')

	# @unittest.skip('跳过')
	def test_06_CMBI_5283(self):
		'''股票交易美股撤单'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-5283 股票交易美股撤单 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickCancelOrder()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'trade/entrust')
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickOrderDetail()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'/trade/about?')
		self.__class__.pageOrders.clickChangeRecords()
		self.assertEqual(1,self.__class__.pageOrders.cancelDetailExists())
		self.__class__.pageBar.goBack(self.__class__.changeBack-1)
		logging.info(f' ========== 测试结束 CMBI-5283 股票交易美股撤单 ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['b']['SH'])
	def test_07_CMBI_5217(self):
		'''股票交易买入沪股通'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:
			self.skipTest('ttl账户跳过买入A股')
		elif self.args.env!='prod':
			# 加资金 
			sql=insertMoney(self.args.account,types='CNY',delOld=1)
			excuteSQL(sql,dbType='sqlserver',env=self.args.env)
		stockCode=tradeData[self.args.account]['b']['SH'][0]
		logging.info(f' ========== 测试开始 CMBI-5217 股票交易买入沪股通 {stockCode} ========== ')
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		# self.__class__.pageBuy.clickTradeBuy()
		self.__class__.pageBuy.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageBuy.inputStock(stockCode)
		self.__class__.pageBuy.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		self.__class__.pageBuy.clickBuyPriceOne()
		# self.__class__.pageBuy.inputNum(1000)

		self.__class__.pageBuy.clickBuy()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'买入确认后截图')
		self.reOrder('b')
		resultStockCode=self.__class__.pageBuy.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5217 股票交易买入沪股通 {stockCode} ========== ')

	# @unittest.skip('跳过')
	def test_08_CMBI_5284_1(self):
		'''股票交易沪股通撤单'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:self.skipTest('ttl账户跳过买入A股')
		logging.info(f' ========== 测试开始 CMBI-5284 股票交易沪股通撤单 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickCancelOrder()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickOrderDetail()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'/trade/about?')
		self.__class__.pageOrders.clickChangeRecords()
		self.assertEqual(1,self.__class__.pageOrders.changeDetailExists())
		self.__class__.pageBar.goBack(self.__class__.changeBack-1)
		logging.info(f' ========== 测试结束 CMBI-5284 股票交易沪股通撤单 ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['b']['SZ'])
	def test_09_CMBI_5218(self):
		'''股票交易买入深股通'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:
			self.skipTest('ttl账户跳过买入A股')
		elif self.args.env!='prod':
			# 加资金 
			sql=insertMoney(self.args.account,types='CNY',delOld=1)
			excuteSQL(sql,dbType='sqlserver',env=self.args.env)
		stockCode=tradeData[self.args.account]['b']['SZ'][0]
		logging.info(f' ========== 测试开始 CMBI-5218 股票交易买入深股通 {stockCode} ========== ')
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		# self.__class__.pageBuy.clickTradeBuy()
		self.__class__.pageBuy.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageBuy.inputStock(stockCode)
		self.__class__.pageBuy.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		self.__class__.pageBuy.clickBuyPriceOne()
		# self.__class__.pageBuy.inputNum(1000)

		self.__class__.pageBuy.clickBuy()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'买入确认后截图')
		self.reOrder('b')
		resultStockCode=self.__class__.pageBuy.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5218 股票交易买入深股通 {stockCode} ========== ')

	# @unittest.skip('跳过')
	def test_10_CMBI_5284_1(self):
		'''股票交易深股通撤单'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:self.skipTest('ttl账户跳过买入A股')
		logging.info(f' ========== 测试开始 CMBI-5284 股票交易深股通撤单 ========== ')
		self.__class__.pageTrade.clickOrder()
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickCancelOrder()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,self.__class__.ordersURL)
		self.__class__.pageOrders.clickTodayOrders()
		self.__class__.pageOrders.clickOrderDetail()
		time.sleep(3)
		swithToRightWeb(self.__class__.driver,'/trade/about?')
		self.__class__.pageOrders.clickChangeRecords()
		self.assertEqual(1,self.__class__.pageOrders.changeDetailExists())
		self.__class__.pageBar.goBack(self.__class__.changeBack-1)
		logging.info(f' ========== 测试结束 CMBI-5284 股票交易深股通撤单 ========== ')

	# @ddt.data(*tradeData[acc]['s']['US'])
	# @unittest.skip('跳过')
	def test_11_CMBI_5220(self):
		'''股票交易卖出美股'''
		if self.args.debug:self.skipTest('debug跳过')
		# if self.args.ttl:self.skipTest('ttl账户跳过卖出')
		if self.args.env=='prod':self.skipTest('跳过')
		stockCode=tradeData[self.args.account]['s']['US'][0]
		logging.info(f' ========== 测试开始 CMBI-5220 股票交易卖出美股 {stockCode} ========== ')
		addHOld_ttl(self.args.account,stockCode,100,'USA',DW='D',env=self.args.env)
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		self.__class__.pageSell.clickTradeSell()
		self.__class__.pageSell.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageSell.inputStock(stockCode)
		self.__class__.pageSell.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		# self.__class__.pageSell.clickPriceOne()
		# self.__class__.pageSell.inputNum(1000)

		# myAddScreen(self,'最大可卖、订单类型是 限价单')
		# orderTypeTxt=self.__class__.pageSell.getorderType()
		# logging.info(f'订单类型为: {orderTypeTxt}')
		# self.assertGreater(self.__class__.pageSell.getMaxSellNum(),0)
		# self.assertEqual('限价单',orderTypeTxt)

		self.__class__.pageSell.clickNumOne()
		self.__class__.pageSell.clickSell()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'卖出确认后截图')
		self.reOrder()
		resultStockCode=self.__class__.pageSell.textResultStockCode()
		# stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5220 股票交易卖出美股 {stockCode} ========== ')

	# @ddt.data(*tradeData[acc]['s']['SH'])
	# @unittest.skip('跳过')
	def test_12_CMBI_5221(self):
		'''股票交易卖出沪股通'''
		if self.args.debug:self.skipTest('debug跳过')
		# if self.args.ttl:self.skipTest('ttl账户跳过卖出')
		if self.args.env=='prod':self.skipTest('跳过')
		stockCode=tradeData[self.args.account]['s']['SH'][0]
		logging.info(f' ========== 测试开始 CMBI-5221 股票交易卖出沪股通 {stockCode} ========== ')
		addHOld_ttl(self.args.account,stockCode,500,'SHA',DW='D',env=self.args.env)
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		self.__class__.pageSell.clickTradeSell()
		self.__class__.pageSell.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageSell.inputStock(stockCode)
		self.__class__.pageSell.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		# self.__class__.pageSell.clickPriceOne()
		# self.__class__.pageSell.inputNum(1000)

		self.__class__.pageSell.clickSell()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'卖出确认后截图')
		self.reOrder()
		resultStockCode=self.__class__.pageSell.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5221 股票交易卖出沪股通 {stockCode} ========== ')

	# @ddt.data(*tradeData[acc]['s']['SZ'])
	# @unittest.skip('跳过')
	def test_13_CMBI_5222(self):
		'''股票交易卖出深股通'''
		if self.args.debug:self.skipTest('debug跳过')
		# if self.args.ttl:self.skipTest('ttl账户跳过卖出')
		if self.args.env=='prod':self.skipTest('跳过')
		stockCode=tradeData[self.args.account]['s']['SZ'][0]
		logging.info(f' ========== 测试开始 CMBI-5222 股票交易卖出深股通 {stockCode} ========== ')
		addHOld_ttl(self.args.account,stockCode,500,'SZA',DW='D',env=self.args.env)
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		self.__class__.pageSell.clickTradeSell()
		self.__class__.pageSell.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageSell.inputStock(stockCode)
		self.__class__.pageSell.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		# self.__class__.pageSell.clickPriceOne()
		# self.__class__.pageSell.inputNum(1000)

		self.__class__.pageSell.clickSell()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'卖出确认后截图')
		self.reOrder()
		resultStockCode=self.__class__.pageSell.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5222 股票交易卖出深股通 {stockCode} ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['s']['HK'])
	def test_14_CMBI_5202(self):
		'''股票交易卖出碎股'''
		if self.args.debug:self.skipTest('debug跳过')
		# if self.args.ttl:self.skipTest('ttl账户跳过卖出')
		if self.args.env=='prod':self.skipTest('跳过')
		stockCode=tradeData[self.args.account]['s']['HK'][0]
		logging.info(f' ========== 测试开始 CMBI-5202 股票交易卖出碎股 {stockCode} ========== ')
		addHOld_ttl(self.args.account,stockCode,7,'HKG',DW='D',env=self.args.env)
		# if self.__class__.pageTrade.PFN=='Android':self.skipTest('Genymotion模拟器无法切换碎骨单，点击无反应')
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		if isTradeTime(time.time()):
			start=time.perf_counter()
			swithToRightWeb(self.__class__.driver,'/trade')
			self.__class__.pageSell.clickTradeSell()
			self.__class__.pageSell.clickInput()
			swithToRightWeb(self.__class__.driver,'/trade/search-stock')
			self.__class__.pageSell.inputStock(stockCode)
			self.__class__.pageSell.clickStockOne(stockCode)
			# swithToRightWeb(self.__class__.driver,'/appweb/trade')
			self.__class__.pageSell.changePan('碎股单')
			# self.__class__.pageSell.clickPriceOne()
			# self.__class__.pageSell.inputNum(2)
			self.__class__.pageSell.clickNumOne()
			self.__class__.pageSell.clickSell()
			self.__class__.pageTradeAlert.clickConfirm()
			time.sleep(1)
			myAddScreen(self,'卖出确认后截图')
			self.reOrder()
			# resultStockCode=self.__class__.pageSell.textResultStockCode()
			# stockCode=stockCode.split('.')[0]
			# self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
			self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
			logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
			# logout(self.__class__.driver)
		else:
			self.skipTest('当前处于非交易时间段')
		logging.info(f' ========== 测试结束 CMBI-5202 股票交易卖出碎股 {stockCode} ========== ')

	# @ddt.data(*tradeData[acc]['s']['HK'])
	# @unittest.skip('跳过')
	@ddt.data(*['限价单','特殊限价单','竞价限价单','竞价单','增强限价单'])
	def test_15_CMBI_5219(self,panName):
		'''股票交易卖出港股'''
		if self.args.debug:self.skipTest('debug跳过')
		# if self.args.ttl:self.skipTest('ttl账户跳过卖出')
		if self.args.env=='prod':self.skipTest('跳过')
		stockCode=tradeData[self.args.account]['s']['HK'][0]
		if self.args.ttl:
			addHOld_ttl(self.args.account,stockCode,500,'HKG',DW='D',env=self.args.env)
		else:
			# 加持仓
			sql=insertStock(self.args.account,types='HK',delOld=1)
			excuteSQL(sql,dbType='sqlserver',env=self.args.env)

		logging.info(f' ========== 测试开始 CMBI-5219 {panName} 股票交易卖出港股 {stockCode} ========== ')
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		self.__class__.pageSell.clickTradeSell()
		self.__class__.pageSell.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageSell.inputStock(stockCode)
		self.__class__.pageSell.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		
		if panName=='增强限价单':
			orderTypeTxt=self.__class__.pageSell.getorderType()
			logging.info(f'订单类型为: {orderTypeTxt}')
			myAddScreen(self,'判断订单类型是 增强限价单 或 竞价限价单')
			if isTradeTime(time.time(),'HK'):
				flag=1 if '增强限价单' in orderTypeTxt or 'Enhanced Limit' in orderTypeTxt else 0
				self.assertTrue(flag)
			else:
				flag=1 if '竞价限价单' in orderTypeTxt or 'At-auction Limit' in orderTypeTxt else 0
				self.assertTrue(flag)
		else:
			self.__class__.pageSell.changePan(panName)


		# orderTypeTxt=self.__class__.pageSell.getorderType()
		# logging.info(f'订单类型为: {orderTypeTxt}')
		# myAddScreen(self,'判断订单类型是 增强限价单 或 竞价限价单')
		# if isTradeTime(time.time(),'HK'):
		# 	self.assertIn('增强限价单',orderTypeTxt)
		# else:
		# 	self.assertIn('竞价限价单',orderTypeTxt)

		self.__class__.pageSell.clickSell()
		time.sleep(1)
		myAddScreen(self,'点击卖出后截图')
		self.assertFalse(self.__class__.pageSell.flag1Exists())
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'卖出确认后截图')
		self.reOrder()
		resultStockCode=self.__class__.pageSell.textResultStockCode()
		stockCode=stockCode.split('.')[0]
		self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5219 {panName} 股票交易卖出港股 {stockCode} ========== ')

	# @ddt.data(*tradeData[acc]['s']['HK'])
	# @unittest.skip('跳过')
	def test_15_CMBI_5219_6(self):
		'''卖出港股 点击最大卖出'''
		if self.args.debug:self.skipTest('debug跳过')
		# if self.args.ttl:self.skipTest('ttl账户跳过卖出')
		if self.args.env=='prod':self.skipTest('跳过')
		stockCode=tradeData[self.args.account]['s']['HK'][0]
		if self.args.ttl:
			addHOld_ttl(self.args.account,stockCode,500,'HKG',DW='D',env=self.args.env)
		else:
			# 加持仓
			sql=insertStock(self.args.account,types='HK',delOld=1)
			excuteSQL(sql,dbType='sqlserver',env=self.args.env)
		
		logging.info(f' ========== 测试开始 CMBI-5219_6 卖出港股 点击最大卖出 {stockCode} ========== ')
		start=time.perf_counter()
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		self.__class__.pageSell.clickTradeSell()
		self.__class__.pageSell.clickInput()
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageSell.inputStock(stockCode)
		self.__class__.pageSell.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		max_sell=self.__class__.pageSell.getMaxSellNum()
		self.__class__.pageSell.clickmaxSell()
		time.sleep(3)
		# self.__class__.pageSell.clickPriceOne()
		# self.__class__.pageSell.inputNum(1000)
		orderTypeTxt=self.__class__.pageSell.getorderType()
		logging.info(f'订单类型为: {orderTypeTxt}')
		myAddScreen(self,'判断订单类型是 增强限价单 或 竞价限价单')
		self.assertEqual(self.__class__.pageSell.get_input_num(),max_sell)
		if isTradeTime(time.time(),'HK'):
			flag=1 if '增强限价单' in orderTypeTxt or 'Enhanced Limit' in orderTypeTxt else 0
			self.assertTrue(flag)
		else:
			flag=1 if '竞价限价单' in orderTypeTxt or 'At-auction Limit' in orderTypeTxt else 0
			self.assertTrue(flag)

		self.__class__.pageSell.clickSell()
		self.__class__.pageTradeAlert.clickConfirm()
		time.sleep(1)
		myAddScreen(self,'卖出确认后截图')
		self.reOrder()
		# resultStockCode=self.__class__.pageSell.textResultStockCode()
		# stockCode=stockCode.split('.')[0]
		# self.assertEqual(stockCode,resultStockCode,f'测试不通过！输入的股票代码与委托结果不一致：{stockCode} {resultStockCode}')
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f'交易耗时：{round(time.perf_counter()-start,2)} 秒')
		logging.info(f' ========== 测试结束 CMBI-5219_6 卖出港股 点击最大卖出 {stockCode} ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['b']['HK'])
	def test_16_CMBI_0000(self):
		'''非中华通没有买卖档'''
		if self.args.debug:self.skipTest('debug跳过')
		stockCode='000004'
		logging.info(f' ========== 测试开始 CMBI-0000 非中华通没有买卖档 {stockCode} ========== ')
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		# self.__class__.pageBuy.clickTradeBuy()
		self.__class__.pageBuy.clickInput()#点击输入框 tagname input
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageBuy.inputStock(stockCode)#输入股票代码
		self.__class__.pageBuy.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		
		# self.__class__.pageStock.clickTrade()
		myAddScreen(self,'买卖档情况截图')
		self.assertFalse(self.__class__.pageBuy.buyPriceOneExists())
		self.assertFalse(self.__class__.pageBuy.sellPriceOneExists())
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f' ========== 测试结束 CMBI-0000 非中华通没有买卖档 {stockCode} ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*tradeData[acc]['b']['HK'])
	@no_retry
	def test_17_CMBI_0001(self):
		'''美股交易/非交易时间内买卖档情况'''
		if self.args.debug:self.skipTest('debug跳过')
		stockCode='PG'
		logging.info(f' ========== 测试开始 CMBI-0001 美股交易/非交易时间内买卖档情况 {stockCode} ========== ')
		self.__class__.pageTrade.clickTrade()
		self.__class__.pageAlert.clickAlert_iKnow()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.__class__.driver,'/trade')
		# self.__class__.pageBuy.clickTradeBuy()
		self.__class__.pageBuy.clickInput()#点击输入框 tagname input
		swithToRightWeb(self.__class__.driver,'/trade/search-stock')
		self.__class__.pageBuy.inputStock(stockCode)#输入股票代码
		self.__class__.pageBuy.clickStockOne(stockCode)
		# swithToRightWeb(self.__class__.driver,'/appweb/trade')
		myAddScreen(self,'买卖档情况截图')
		if isTradeTime(time.time(),'US'):
			self.assertTrue(self.__class__.pageBuy.buyPriceOneExists())
			self.assertTrue(self.__class__.pageBuy.sellPriceOneExists())
		else:
			self.assertFalse(self.__class__.pageBuy.buyPriceOneExists())
			self.assertFalse(self.__class__.pageBuy.sellPriceOneExists())
		self.__class__.pageBar.goBack(self.__class__.tradeBack-1)
		logging.info(f' ========== 测试结束 CMBI-0001 美股交易/非交易时间内买卖档情况 {stockCode} ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_18_CMBI_5122(self):
		'''已有户口手机号进入交易页'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.env=='prod':self.skipTest('跳过')
		logging.info(f' ========== 测试开始 CMBI-5122 已有户口手机号进入交易页 ========== ')
		try:
			logout(self.__class__.driver)
			phone=accBinding[self.args.account][1]
			pwd=accountPool[phone][0]
			nickName=accountPool[self.args.account][1]
			login(self.__class__.driver,(phone,pwd),cusNickName=nickName,args=self.args,acc=0)
			self.__class__.pageBar.clickMarket()
			self.__class__.pageAlert.clickAlert()

			self.__class__.pageMarket.clickMarket()
			self.__class__.pageAlert.clickAlert()
			self.__class__.pageMarket.clickTabHK()
			self.__class__.pageAlert.clickAlert()
			self.__class__.pageMarket.clickStock2()
			self.__class__.pageAlert.clickAlert()
			self.__class__.pageStock.clickTrade()
			myAddScreen(self,'港股截图')
			self.assertEqual(1,self.__class__.pageBuy.isEditPwdExists())
			if self.__class__.pageBar.PFN=='iOS':
				self.__class__.pageBuy.clickClose()
			else:
				self.__class__.pageBar.goBack()
			time.sleep(1)
			self.__class__.pageBar.goBack()
			if self.__class__.pageBar.PFN=='Android':# ios 无法获取美股tab页面
				self.__class__.pageMarket.clickMarket()
				self.__class__.pageAlert.clickAlert()
				self.__class__.pageMarket.clickTabUS()
				self.__class__.pageAlert.clickAlert()
				self.__class__.pageMarket.clickStock2()
				self.__class__.pageAlert.clickAlert()
				self.__class__.pageStock.clickTrade()
				myAddScreen(self,'美股截图')
				self.assertEqual(1,self.__class__.pageBuy.isEditPwdExists())
				if self.__class__.pageBar.PFN=='iOS':
					self.__class__.pageBuy.clickClose()
				else:
					self.__class__.pageBar.goBack()
				time.sleep(1)
				self.__class__.pageBar.goBack()
			self.__class__.pageMarket.clickMarket()
			self.__class__.pageAlert.clickAlert()
			self.__class__.pageMarket.clickTabSHSZ()
			self.__class__.pageAlert.clickAlert()
			time.sleep(2)
			swipeUp(self.__class__.driver,n=2)
			self.__class__.pageMarket.clickStock2(t='AH')
			self.__class__.pageAlert.clickAlert()
			self.__class__.pageStock.clickTrade()
			myAddScreen(self,'A股截图')
			self.assertEqual(1,self.__class__.pageBuy.isEditPwdExists())
			if self.__class__.pageBar.PFN=='iOS':
				self.__class__.pageBuy.clickClose()
			else:
				self.__class__.pageBar.goBack()
			time.sleep(2)
			self.__class__.pageBar.goBack()
		except Exception as e:
			raise e
		finally:
			logout(self.__class__.driver)
		logging.info(f' ========== 测试结束 CMBI-5122 已有户口手机号进入交易页 ========== ')

	def tearDown(self):
		if self.args.debug:return
		self.__class__.pageBar.goBack()

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 交易测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass