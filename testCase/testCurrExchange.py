import time,logging,traceback,re,unittest
from random import uniform
from HTMLReport import no_retry,ddt

from page.navBar import PageBar
from page.mine.my import PageMy
from page.alert import PageAlert
from page.home.home import PageHome
from page.alertLogin import PageAlertLogin
from page.mine.businesWeek.currExchange import PageCurrExchange

from common.parameter import ParameTestCase
from common.tools import isTradeTime,swithToRightWeb,start_recording,stop_recording
from business.logInOut import login,logout

from testData.data import accountPool,accBinding,currExchange_Data

# @unittest.skip('跳过')
@ddt.ddt
class TestCurrExchange(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 货币兑换测试开始 ########## ')
		cls.acc_pwd=(cls.args.account,accountPool[cls.args.account][0])
		nickName=accountPool[cls.args.account][1]
		login(cls.driver,cls.acc_pwd,forceLogout=1,cusNickName=nickName,args=cls.args)
		cls.pageBar=PageBar(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageAlertLogin=PageAlertLogin(cls.driver)
		cls.pageMy=PageMy(cls.driver)
		cls.pageHome=PageHome(cls.driver)
		cls.pageCurrExchange=PageCurrExchange(cls.driver)

	def setUp(self):
		pass


	# @no_retry
	# @unittest.skip('跳过')
	@ddt.data(*currExchange_Data)
	@ddt.unpack
	def test_CMBI_9999(self,in_out,cur_L,cur_R):
		'''货币兑换测试'''
		in_out_Dic={'in':'兑入','out':'兑出'}
		logging.info(f' ========== 测试开始 CMBI-9999 货币兑换 {in_out_Dic[in_out]} {cur_L}-->{cur_R} ========== ')
		self.__class__.pageBar.clickHome()
		self.__class__.pageAlert.clickAlert()
		# self.__class__.pageHome.clickReload()
		swithToRightWeb(self.__class__.driver,'index.html#/home')
		self.__class__.pageHome.clickCurrExchange()
		self.__class__.pageAlertLogin.inputPwordIFneeded(self.__class__.acc_pwd[1])
		start_recording(self.__class__.driver)
		swithToRightWeb(self.__class__.driver,'#/currency?')
		self.__class__.pageCurrExchange.clickAlert_confirm()
		videoName=f"{time.strftime('%H%M%S')}_{cur_L}_{cur_R}"
		try:
			self.__class__.pageCurrExchange.clickChangeCurr(in_out)
			self.__class__.pageCurrExchange.chooseCurr(cur_L,cur_R)
			amount=round(uniform(100,1000),2)
			self.__class__.pageCurrExchange.inputAmount(amount)
			self.__class__.pageCurrExchange.clickkbConfirm()
			self.__class__.pageCurrExchange.clicksubmit()
			time.sleep(1)
			self.__class__.pageCurrExchange.clickconfirm()
			time.sleep(1)
			self.__class__.pageCurrExchange.clickdone()
			
			self.__class__.pageBar.goBack()
		except Exception:
			logging.error(traceback.format_exc())
			raise Exception
		finally:
			stop_recording(self.__class__.driver,self.__class__.args.timeStr,videoName)
		logging.info(f' ========== 测试结束 CMBI-9999 货币兑换 {in_out_Dic[in_out]} {cur_L}-->{cur_R} ========== ')

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 货币兑换测试结束 ########## ')
		logout(cls.driver)

if __name__=='__main__':
	unittest.main()