import time,logging,unittest
from HTMLReport import no_retry

from common.parameter import ParameTestCase
from common.tools import swithToRightWeb

from page.navBar import PageBar
from page.trade.fund import PageFund
from page.home.home import PageHome
from page.news.news import PageNews
from page.alert import PageAlert

# from config import reLoginAcc

# @unittest.skip('跳过')
class TestHomeNews(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 首页/资讯 模块测试开始 ########## ')
		cls.pageBar=PageBar(cls.driver)
		cls.pageHome=PageHome(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)

	def setUp(self):
		pass

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_CMBI_156(self):
	# 	'''热门基金跳转'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-156 热门基金跳转 ========== ')
	# 	self.pageFund=PageFund(self.driver)
	# 	self.pageBar.clickHome()
	# 	self.pageAlert.clickAlert()
	# 	swithToRightWeb(self.driver,'news/index.html#/home')
	# 	fundOneName=self.pageHome.textFund1()
	# 	self.pageHome.clickFund1()
	# 	swithToRightWeb(self.driver,'/index.html#/fundDetail?')
	# 	self.pageFund.clickIknow()
	# 	self.assertIn(fundOneName,self.pageFund.textFundName2())
	# 	self.pageBar.goBack()
	# 	swithToRightWeb(self.driver,'news/index.html#/home')
	# 	self.pageHome.clickFundMore()
	# 	self.pageFund.clickIknow()
	# 	swithToRightWeb(self.driver,'news/index.html#/fund')
	# 	self.assertEqual(1,self.pageFund.flagExists())

	# 	logging.info(f' ========== 测试结束 CMBI-156 热门基金跳转 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_157(self):
		'''深度推荐跳转'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-157 深度推荐跳转 ========== ')
		self.__class__.pageBar.clickHome()
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.driver,'news/index.html#/home')
		articleTitle=self.__class__.pageHome.textArticleOne()
		self.__class__.pageHome.clickArticleOne()
		swithToRightWeb(self.driver,'/news/index.html#/detail/')
		self.assertEqual(articleTitle,self.__class__.pageHome.textArticleTitle())
		self.__class__.pageBar.goBack(n=2)
		logging.info(f' ========== 测试结束 CMBI-157 深度推荐跳转 ========== ')

	# # @unittest.skip('跳过')
	# # @no_retry
	# def test_CMBI_161(self):
	# 	'''资讯分享'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-161 资讯分享 ========== ')
	# 	self.pageBar.clickNews()
	# 	self.pageNews=PageNews(self.driver)

	# 	self.pageNews.clickArticleOne()
	# 	swipeUp(self.driver,n=10)
	# 	self.pageNews.clickShare1()
	# 	self.assertEqual(1,self.pageNews.weChatExists())
	# 	self.pageBar.goBack()
	# 	self.pageNews.clickShare2()
	# 	self.assertEqual(1,self.pageNews.weChatExists())
	# 	self.pageBar.goBack()
	# 	# self.pageNews.clickMore()
	# 	# self.pageNews.clickShare3()
	# 	# self.assertEqual('微信登录',self.pageNews.textWeChat())
	# 	# self.pageBar.goBack()
	# 	# self.pageNews.clickMore()
	# 	# self.pageNews.clickShare4()
	# 	# self.assertEqual('微信登录',self.pageNews.textWeChat())
	# 	self.pageBar.goBack()
		
	# 	logging.info(f' ========== 测试结束 CMBI-161 资讯分享 ========== ')

	# # @unittest.skip('跳过')
	# @no_retry
	# def test_CMBI_162(self):
	# 	'''热门推荐跳转'''
	# if self.args.debug:self.skipTest('debug跳过')
	# 	logging.info(f' ========== 测试开始 CMBI-162 热门推荐跳转 ========== ')
	# 	self.pageBar.clickMy()
	# 	self.pageBar.clickHome()
	# 	self.pageAlert.clickAlert()
	# 	self.pageNews=PageNews(self.driver)
	# 	swithToRightWeb(self.driver,'news/index.html#/home')
	# 	self.pageHome.clickArticleOne()
	# 	swithToRightWeb(self.driver,'/news/index.html#/detail/')
	# 	url=self.driver.current_url
	# 	title=self.pageNews.textHotTitle1()
	# 	self.pageNews.clickHotArticle1()
	# 	swithToRightWeb(self.driver,'/news/index.html#/detail/')
	# 	# swithToRightWeb(self.driver,'/news/index.html#/detail/',url)
	# 	self.assertEqual(title,self.pageNews.textHotTitle2())
	# 	self.pageBar.goBack()
	# 	logging.info(f' ========== 测试结束 CMBI-162 热门推荐跳转 ========== ')

	def tearDown(self):
		if self.args.debug:return
		self.__class__.pageBar.goBack()

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 首页/资讯 模块测试开始 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass
