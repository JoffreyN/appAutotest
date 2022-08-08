import time,logging,traceback,re,unittest
# from random import randint,sample
from HTMLReport import ddt,no_retry

from testData.data import accountPool,accBinding

from page.mine.my import PageMy
from page.navBar import PageBar
from page.alert import PageAlert
from page.flagExists import PageFlagExists
# from page.uploadPic import PageUploadPic
# from page.mine.businesWeek.CRS import PageCRS
# from page.mine.fakeTrade import PageFakeTrade
# from page.mine.businesWeek.IPO import PageIPO
from page.mine.busineManage import PageBusineManage
# from page.mine.businesWeek.bankCard import PageBankCard
# from page.mine.businesWeek.editInfo import PageEditInfo
# from page.mine.businesWeek.riskAssessment import PageRiskAss
# from page.mine.businesWeek.importMoney import PageImportMoney
# from page.mine.businesWeek.exportMoney import PageExportMoney
# from page.mine.businesWeek.tradeHistory import PageTradeHistory
# from page.mine.businesWeek.emailSetting import PageEmailSetting
# from page.mine.businesWeek.financingQuota import PageFinancingQuota
# from page.mine.businesWeek.imExportHistory import PageImExportHistory

# from business.others import reOpenApp
from business.logInOut import login,logout

from common.parameter import ParameTestCase
from common.tools import swithToRightWeb,myAddScreen
# from common.system_boss import getSMScode,editPhone,switch_ocr,getMailRecord
# from common.dbOperation import getEmailCode,insertMoney,excuteSQL
# from common.system_appadmin import getMailRecord_appadmin

# @unittest.skip('跳过')
# @ddt.ddt
class TestBusineManage_prod(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## PROD环境业务办理模块测试开始 ########## ')
		cls.acc_pwd=(cls.args.account,accountPool[cls.args.account][0])
		# cls.pageFinancingQuota=PageFinancingQuota(cls.driver)
		# cls.pageImExportHistory=PageImExportHistory(cls.driver)
		# cls.pageTradeHistory=PageTradeHistory(cls.driver)
		# cls.pageEmailSetting=PageEmailSetting(cls.driver)
		cls.pageBusineManage=PageBusineManage(cls.driver)
		# cls.pageImportMoney=PageImportMoney(cls.driver)
		# cls.pageExportMoney=PageExportMoney(cls.driver)
		cls.nickName=accountPool[cls.args.account][1]
		# cls.pageFakeTrade=PageFakeTrade(cls.driver)
		# cls.pageUploadPic=PageUploadPic(cls.driver)
		# cls.pageEditInfo=PageEditInfo(cls.driver)
		# cls.pageBankCard=PageBankCard(cls.driver)
		# cls.pageRiskAss=PageRiskAss(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageFlagExists=PageFlagExists(cls.driver)
		cls.pageBar=PageBar(cls.driver)
		# cls.pageIPO=PageIPO(cls.driver)
		# cls.pageCRS=PageCRS(cls.driver)
		cls.pageMy=PageMy(cls.driver)

	def setUp(self):
		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
		self.__class__.pageBar.clickMy()
		# self.__class__.pageAlert.clickAlert()
		self.__class__.pageMy.clickYWBL()
		# self.__class__.pageBusineManage.inputPwordIFneeded()
		# swithToRightWeb(self.driver,'helperpage/more?')
		swithToRightWeb(self.driver,'/appMap')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_01(self):
		'''股票交易页面'''
		logging.info(f' ========== 测试开始 MORE-01 股票交易页面 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('01')
		swithToRightWeb(self.driver,'appweb/trade')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('01'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'股票交易页面跳转截图')
		logging.info(f' ========== 测试结束 MORE-01 股票交易页面 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_02(self):
		'''订单查询页面'''
		logging.info(f' ========== 测试开始 MORE-02 订单查询页面 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('02')
		swithToRightWeb(self.driver,'trade/entrust')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('02'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'订单查询页面跳转截图')
		logging.info(f' ========== 测试结束 MORE-02 订单查询页面 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_MORE_03(self):
	# 	'''股票持仓'''
	# 	logging.info(f' ========== 测试开始 MORE-03 股票持仓 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('03')
	# 	swithToRightWeb(self.driver,' ')
	#	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('03'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'股票持仓跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-03 股票持仓 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_04(self):
		'''港股ETF'''
		logging.info(f' ========== 测试开始 MORE-04 港股ETF ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('04')
		swithToRightWeb(self.driver,'appweb/quote')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('04'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'港股ETF跳转截图')
		logging.info(f' ========== 测试结束 MORE-04 港股ETF ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_05(self):
		'''可融股票'''
		logging.info(f' ========== 测试开始 MORE-05 可融股票 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('05')
		swithToRightWeb(self.driver,'/quote/marginRatio')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('05'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'可融股票跳转截图')
		logging.info(f' ========== 测试结束 MORE-05 可融股票 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_06(self):
		'''轮证中心'''
		logging.info(f' ========== 测试开始 MORE-06 轮证中心 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('06')
		swithToRightWeb(self.driver,'/quote/demonstration')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('06'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'轮证中心跳转截图')
		logging.info(f' ========== 测试结束 MORE-06 轮证中心 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_07(self):
		'''我的行情'''
		logging.info(f' ========== 测试开始 MORE-07 我的行情 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('07')
		swithToRightWeb(self.driver,'/helperpage/market')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('07'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'我的行情跳转截图')
		logging.info(f' ========== 测试结束 MORE-07 我的行情 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_08(self):
		'''新股认购'''
		logging.info(f' ========== 测试开始 MORE-08 新股认购 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('08')
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('08'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'新股认购跳转截图')
		logging.info(f' ========== 测试结束 MORE-08 新股认购 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_09(self):
		'''新股订单'''
		logging.info(f' ========== 测试开始 MORE-09 新股订单 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('09')
		swithToRightWeb(self.driver,'/eipo/orderList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('09'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'新股订单跳转截图')
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 MORE-09 新股订单 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_10(self):
		'''上市申请'''
		logging.info(f' ========== 测试开始 MORE-10 上市申请 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('10')
		swithToRightWeb(self.driver,'/eipo/marketList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('10'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'上市申请跳转截图')
		logging.info(f' ========== 测试结束 MORE-10 上市申请 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_11(self):
		'''新股日历'''
		logging.info(f' ========== 测试开始 MORE-11 新股日历 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('11')
		swithToRightWeb(self.driver,'/eipo/calendar')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('11'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'新股日历跳转截图')
		logging.info(f' ========== 测试结束 MORE-11 新股日历 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_12(self):
		'''打新计算器'''
		logging.info(f' ========== 测试开始 MORE-12 打新计算器 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('12')
		swithToRightWeb(self.driver,'/eipo/ipoCounter')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('12'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'打新计算器跳转截图')
		logging.info(f' ========== 测试结束 MORE-12 打新计算器 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_13(self):
		'''基金订单'''
		logging.info(f' ========== 测试开始 MORE-13 基金订单 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('13')
		swithToRightWeb(self.driver,'/fund-sys/records')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('13'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'基金订单跳转截图')
		logging.info(f' ========== 测试结束 MORE-13 基金订单 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_MORE_14(self):
	# 	'''基金持仓'''
	# 	logging.info(f' ========== 测试开始 MORE-14 基金持仓 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('14')
	# 	swithToRightWeb(self.driver,' ')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('14'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'基金持仓跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-14 基金持仓 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_MORE_15(self):
	# 	'''基金市场'''
	# 	logging.info(f' ========== 测试开始 MORE-15 基金市场 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('15')
	# 	swithToRightWeb(self.driver,'   ')
	#	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('15'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'基金市场跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-15 基金市场 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_16(self):
		'''货币基金'''
		logging.info(f' ========== 测试开始 MORE-16 货币基金 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('16')
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('16'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'货币基金跳转截图')
		logging.info(f' ========== 测试结束 MORE-16 货币基金 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_17(self):
		'''债券基金'''
		logging.info(f' ========== 测试开始 MORE-17 债券基金 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('17')
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('17'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'债券基金跳转截图')
		logging.info(f' ========== 测试结束 MORE-17 债券基金 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_18(self):
		'''股票基金'''
		logging.info(f' ========== 测试开始 MORE-18 股票基金 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('18')
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('18'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'股票基金跳转截图')
		logging.info(f' ========== 测试结束 MORE-18 股票基金 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_19(self):
		'''配置基金'''
		logging.info(f' ========== 测试开始 MORE-19 配置基金 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('19')
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('19'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'配置基金跳转截图')
		logging.info(f' ========== 测试结束 MORE-19 配置基金 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_20(self):
		'''基金筛选'''
		logging.info(f' ========== 测试开始 MORE-20 基金筛选 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('20')
		swithToRightWeb(self.driver,'/fund-sys/fundList')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('20'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'基金筛选跳转截图')
		logging.info(f' ========== 测试结束 MORE-20 基金筛选 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_21(self):
		'''基金公司'''
		logging.info(f' ========== 测试开始 MORE-21 基金公司 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('21')
		swithToRightWeb(self.driver,'/fund-sys/fundCompany')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('21'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'基金公司跳转截图')
		logging.info(f' ========== 测试结束 MORE-21 基金公司 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_22(self):
		'''资金存入'''
		logging.info(f' ========== 测试开始 MORE-22 资金存入 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('22')
		swithToRightWeb(self.driver,'/deposit')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('22'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'资金存入跳转截图')
		logging.info(f' ========== 测试结束 MORE-22 资金存入 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_23(self):
		'''资金提取'''
		logging.info(f' ========== 测试开始 MORE-23 资金提取 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('23')
		swithToRightWeb(self.driver,'/withdraw')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('23'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'资金提取跳转截图')
		logging.info(f' ========== 测试结束 MORE-23 资金提取 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_24(self):
		'''货币兑换'''
		logging.info(f' ========== 测试开始 MORE-24 货币兑换 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('24')
		swithToRightWeb(self.driver,'/currency')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('24'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'货币兑换跳转截图')
		logging.info(f' ========== 测试结束 MORE-24 货币兑换 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_25(self):
		'''资金调拨'''
		logging.info(f' ========== 测试开始 MORE-25 资金调拨 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('25')
		swithToRightWeb(self.driver,'/capitalallocation')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('25'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'资金调拨跳转截图')
		logging.info(f' ========== 测试结束 MORE-25 资金调拨 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_26(self):
		'''资金记录'''
		logging.info(f' ========== 测试开始 MORE-26 资金记录 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('26')
		swithToRightWeb(self.driver,'/fundsHistory')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('26'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'资金记录跳转截图')
		logging.info(f' ========== 测试结束 MORE-26 资金记录 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_28(self):
		'''开户专区'''
		logging.info(f' ========== 测试开始 MORE-28 开户专区 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('28')
		swithToRightWeb(self.driver,'resource')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('28'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'开户专区跳转截图')
		logging.info(f' ========== 测试结束 MORE-28 开户专区 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_29(self):
		'''专业投资者'''
		logging.info(f' ========== 测试开始 MORE-29 专业投资者 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('29')
		swithToRightWeb(self.driver,'/piUpgrade')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('29'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'专业投资者跳转截图')
		logging.info(f' ========== 测试结束 MORE-29 专业投资者 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_30(self):
		'''港美开户'''
		logging.info(f' ========== 测试开始 MORE-30 港美开户 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('30')
		swithToRightWeb(self.driver,'/form/s_start')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('30'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'港美开户跳转截图')
		logging.info(f' ========== 测试结束 MORE-30 港美开户 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_31(self):
		'''期货开户'''
		logging.info(f' ========== 测试开始 MORE-31 期货开户 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('31')
		swithToRightWeb(self.driver,'/appkh/futures')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('31'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'期货开户跳转截图')
		logging.info(f' ========== 测试结束 MORE-31 期货开户 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_32(self):
		'''公司开户'''
		logging.info(f' ========== 测试开始 MORE-32 公司开户 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('32')
		swithToRightWeb(self.driver,'/open-propaganda')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('32'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'公司开户跳转截图')
		logging.info(f' ========== 测试结束 MORE-32 公司开户 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_33(self):
		'''股权激励'''
		logging.info(f' ========== 测试开始 MORE-33 股权激励 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('33')
		swithToRightWeb(self.driver,'/esop/promotion/app')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('33'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'股权激励跳转截图')
		logging.info(f' ========== 测试结束 MORE-33 股权激励 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_34(self):
		'''资产总览'''
		logging.info(f' ========== 测试开始 MORE-34 资产总览 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('34')
		swithToRightWeb(self.driver,'/staticPortfolio')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('34'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'资产总览跳转截图')
		logging.info(f' ========== 测试结束 MORE-34 资产总览 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_35(self):
		'''结单查询'''
		logging.info(f' ========== 测试开始 MORE-35 结单查询 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('35')
		swithToRightWeb(self.driver,'/checkInquire')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('35'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'结单查询跳转截图')
		logging.info(f' ========== 测试结束 MORE-35 结单查询 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_36(self):
		'''开通市场'''
		logging.info(f' ========== 测试开始 MORE-36 开通市场 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('36')
		swithToRightWeb(self.driver,'/openMarket')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('36'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'开通市场跳转截图')
		logging.info(f' ========== 测试结束 MORE-36 开通市场 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_37(self):
		'''银行卡管理'''
		logging.info(f' ========== 测试开始 MORE-37 银行卡管理 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('37')
		swithToRightWeb(self.driver,'/bankcard')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('37'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'银行卡管理跳转截图')
		logging.info(f' ========== 测试结束 MORE-37 银行卡管理 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_38(self):
		'''修改资料'''
		logging.info(f' ========== 测试开始 MORE-38 修改资料 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('38')
		swithToRightWeb(self.driver,'/profile')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('38'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'修改资料跳转截图')
		logging.info(f' ========== 测试结束 MORE-38 修改资料 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_39(self):
		'''风险测评'''
		logging.info(f' ========== 测试开始 MORE-39 风险测评 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('39')
		swithToRightWeb(self.driver,'/rpqTest')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('39'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'风险测评跳转截图')
		logging.info(f' ========== 测试结束 MORE-39 风险测评 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_40(self):
		'''衍生品问卷'''
		logging.info(f' ========== 测试开始 MORE-40 衍生品问卷 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('40')
		swithToRightWeb(self.driver,'/derTest')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('40'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'衍生品问卷跳转截图')
		logging.info(f' ========== 测试结束 MORE-40 衍生品问卷 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_41(self):
		'''资料年审'''
		logging.info(f' ========== 测试开始 MORE-41 资料年审 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('41')
		swithToRightWeb(self.driver,'/client-renew')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('41'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'资料年审跳转截图')
		logging.info(f' ========== 测试结束 MORE-41 资料年审 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_42(self):
		'''W8表格'''
		logging.info(f' ========== 测试开始 MORE-42 W8表格 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('42')
		swithToRightWeb(self.driver,'/w8Table')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('42'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'W8表格跳转截图')
		logging.info(f' ========== 测试结束 MORE-42 W8表格 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_43(self):
		'''CRS登记'''
		logging.info(f' ========== 测试开始 MORE-43 CRS登记 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('43')
		swithToRightWeb(self.driver,'/crsRegister')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('43'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'CRS登记跳转截图')
		logging.info(f' ========== 测试结束 MORE-43 CRS登记 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_44(self):
		'''公司行动'''
		logging.info(f' ========== 测试开始 MORE-44 公司行动 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('44')
		swithToRightWeb(self.driver,'/companyMovement')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('44'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'公司行动跳转截图')
		logging.info(f' ========== 测试结束 MORE-44 公司行动 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_45(self):
		'''壹隆小课堂'''
		logging.info(f' ========== 测试开始 MORE-45 壹隆小课堂 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('45')
		swithToRightWeb(self.driver,'/detail/1219739')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('45'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'壹隆小课堂跳转截图')
		logging.info(f' ========== 测试结束 MORE-45 壹隆小课堂 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_46(self):
		'''我的路演'''
		logging.info(f' ========== 测试开始 MORE-46 我的路演 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('46')
		swithToRightWeb(self.driver,'/myroadshowCore')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('46'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'我的路演跳转截图')
		logging.info(f' ========== 测试结束 MORE-46 我的路演 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_47(self):
	# 	'''路演中心'''
	# 	logging.info(f' ========== 测试开始 MORE-47 路演中心 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('47')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('47'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'路演中心跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-47 路演中心 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_48(self):
	# 	'''IPO路演'''
	# 	logging.info(f' ========== 测试开始 MORE-48 IPO路演 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('48')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('48'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'IPO路演跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-48 IPO路演 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_49(self):
	# 	'''业绩路演'''
	# 	logging.info(f' ========== 测试开始 MORE-49 业绩路演 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('49')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('49'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'业绩路演跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-49 业绩路演 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_50(self):
	# 	'''机构活动'''
	# 	logging.info(f' ========== 测试开始 MORE-50 机构活动 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('50')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('50'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'机构活动跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-50 机构活动 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_51(self):
	# 	'''大咖专栏'''
	# 	logging.info(f' ========== 测试开始 MORE-51 大咖专栏 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('51')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('51'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'大咖专栏跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-51 大咖专栏 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_52(self):
	# 	'''金融公司'''
	# 	logging.info(f' ========== 测试开始 MORE-52 金融公司 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('52')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('52'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'金融公司跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-52 金融公司 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_53(self):
	# 	'''科技公司'''
	# 	logging.info(f' ========== 测试开始 MORE-53 科技公司 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('53')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('53'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'科技公司跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-53 科技公司 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_54(self):
	# 	'''生物制药'''
	# 	logging.info(f' ========== 测试开始 MORE-54 生物制药 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('54')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('54'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'生物制药跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-54 生物制药 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_55(self):
	# 	'''热门媒体'''
	# 	logging.info(f' ========== 测试开始 MORE-55 热门媒体 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('55')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('55'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'热门媒体跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-55 热门媒体 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_MORE_56(self):
	# 	'''汽车能源'''
	# 	logging.info(f' ========== 测试开始 MORE-56 汽车能源 ========== ')
	# 	self.__class__.pageBusineManage.cilckCommon_more('56')
	# 	swithToRightWeb(self.driver,'/roadshowCore')
	# 	self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('56'))
	# 	swithToRightWeb(self.driver,0)
	# 	myAddScreen(self,'汽车能源跳转截图')
	# 	logging.info(f' ========== 测试结束 MORE-56 汽车能源 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_57(self):
		'''活动中心'''
		logging.info(f' ========== 测试开始 MORE-57 活动中心 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('57')
		swithToRightWeb(self.driver,'/act-center')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('57'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'活动中心跳转截图')
		logging.info(f' ========== 测试结束 MORE-57 活动中心 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_58(self):
		'''权益中心'''
		logging.info(f' ========== 测试开始 MORE-58 权益中心 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('58')
		swithToRightWeb(self.driver,'/act_award')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('58'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'权益中心跳转截图')
		logging.info(f' ========== 测试结束 MORE-58 权益中心 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_59(self):
		'''模拟炒股'''
		logging.info(f' ========== 测试开始 MORE-59 模拟炒股 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('59')
		swithToRightWeb(self.driver,'/simulate')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('59'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'模拟炒股跳转截图')
		logging.info(f' ========== 测试结束 MORE-59 模拟炒股 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_60(self):
		'''通知设置'''
		logging.info(f' ========== 测试开始 MORE-60 通知设置 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('60')
		swithToRightWeb(self.driver,'/emailSetting')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('60'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'通知设置跳转截图')
		logging.info(f' ========== 测试结束 MORE-60 通知设置 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_61(self):
		'''有效时长'''
		logging.info(f' ========== 测试开始 MORE-61 有效时长 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('61')
		swithToRightWeb(self.driver,'/effectiveDuration')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('61'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'有效时长跳转截图')
		logging.info(f' ========== 测试结束 MORE-61 有效时长 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_62(self):
		'''密码管理'''
		logging.info(f' ========== 测试开始 MORE-62 密码管理 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('62')
		swithToRightWeb(self.driver,'/reset')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('62'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'密码管理跳转截图')
		logging.info(f' ========== 测试结束 MORE-62 密码管理 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_MORE_99_27(self):
		'''融资申请'''
		logging.info(f' ========== 测试开始 MORE-27 融资申请 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more('27')
		swithToRightWeb(self.driver,'/settle/margin')
		self.assertTrue(self.__class__.pageFlagExists.moreTab_exists('27'))
		swithToRightWeb(self.driver,0)
		myAddScreen(self,'融资申请跳转截图')
		logging.info(f' ========== 测试结束 MORE-27 融资申请 ========== ')



	def tearDown(self):
		self.__class__.pageBar.goBack(2)

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## PROD环境业务办理模块测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass