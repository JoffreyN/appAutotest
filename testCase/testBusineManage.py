import time,logging,traceback,re,unittest,threading
from random import randint,sample,random
from HTMLReport import ddt,no_retry

from testData.data import accountPool,accBinding

from page.mine.my import PageMy
from page.navBar import PageBar
from page.alert import PageAlert
from page.uploadPic import PageUploadPic
from page.register.register_web import PageRegisterWeb
from page.mine.businesWeek.CRS import PageCRS
from page.mine.fakeTrade import PageFakeTrade
from page.mine.businesWeek.IPO import PageIPO
from page.mine.busineManage import PageBusineManage
from page.mine.businesWeek.bankCard import PageBankCard
from page.mine.businesWeek.editInfo import PageEditInfo
from page.mine.businesWeek.statement import PageStatement
from page.mine.businesWeek.riskAssessment import PageRiskAss
from page.mine.businesWeek.clientRenew import PageClientrenew
from page.mine.businesWeek.importMoney import PageImportMoney
from page.mine.businesWeek.importStock import PageImportStock
from page.mine.businesWeek.exportMoney import PageExportMoney
from page.mine.businesWeek.tradeHistory import PageTradeHistory
from page.mine.businesWeek.emailSetting import PageEmailSetting
from page.mine.businesWeek.financingQuota import PageFinancingQuota
from page.mine.businesWeek.imExportHistory import PageImExportHistory

from business.others import reOpenApp
from business.logInOut import login,logout

from common.parameter import ParameTestCase
from common.tools import swithToRightWeb,keyboardInput,myAddScreen,ftp_store_file
from common.system_boss import *
from common.dbOperation import getEmailCode,insertMoney,excuteSQL
from common.system_appadmin import getMailRecord_appadmin,eipoOrder_save,eipoOrder_cancel,queryIPOorder
from common.apiCenter import cancelFinance,preOrderDetail,preOrderCancel,login_acc,resetpwd_ttl

# @unittest.skip('跳过')
@ddt.ddt
class TestBusineManage(ParameTestCase):
	@classmethod
	def setUpClass(cls):
		logging.info(' ########## 业务办理模块测试开始 ########## ')
		cls.acc_pwd=(cls.args.account,accountPool[cls.args.account][0])
		cls.pageFinancingQuota=PageFinancingQuota(cls.driver)
		cls.pageImExportHistory=PageImExportHistory(cls.driver)
		cls.pageRegisterWeb=PageRegisterWeb(cls.driver)
		cls.pageTradeHistory=PageTradeHistory(cls.driver)
		cls.pageEmailSetting=PageEmailSetting(cls.driver)
		cls.pageBusineManage=PageBusineManage(cls.driver)
		cls.pageImportMoney=PageImportMoney(cls.driver)
		cls.pageClientrenew=PageClientrenew(cls.driver)
		cls.pageImportStock=PageImportStock(cls.driver)
		cls.pageExportMoney=PageExportMoney(cls.driver)
		cls.nickName=accountPool[cls.args.account][1]
		cls.pageStatement=PageStatement(cls.driver)
		cls.pageFakeTrade=PageFakeTrade(cls.driver)
		cls.pageUploadPic=PageUploadPic(cls.driver)
		cls.pageEditInfo=PageEditInfo(cls.driver)
		cls.pageBankCard=PageBankCard(cls.driver)
		cls.pageRiskAss=PageRiskAss(cls.driver)
		cls.pageAlert=PageAlert(cls.driver)
		cls.pageBar=PageBar(cls.driver)
		cls.pageIPO=PageIPO(cls.driver)
		cls.pageCRS=PageCRS(cls.driver)
		cls.pageMy=PageMy(cls.driver)

		sessionDic=login_acc(cls.acc_pwd[0],cls.acc_pwd[1],env=cls.args.env,ttl=cls.args.ttl)
		preTradeOrderId=preOrderDetail(sessionDic,cls.args.env)
		if preTradeOrderId:threading.Thread(target=preOrderCancel,args=(sessionDic,preTradeOrderId,cls.args.env,)).start()#通过聆讯取消预约

	def setUp(self):
		if self.args.debug:return
		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args)
		self.__class__.pageBar.clickMy()
		self.__class__.pageAlert.clickAlert()
		self.__class__.pageMy.clickYWBL()
		self.__class__.pageBusineManage.inputPwordIFneeded()
		# swithToRightWeb(self.driver,'helperpage/more?')
		swithToRightWeb(self.driver,'/appMap')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_143(self):
		'''资料年审'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-143 资料年审 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(41)
		swithToRightWeb(self.driver,'static/client-renew.html')
		try:
			self.__class__.pageClientrenew.myClick('撤回申请',self.__class__.pageClientrenew.withdraw)
			time.sleep(2)
			self.__class__.pageClientrenew.clickYes()
		except:
			pass
		self.__class__.pageClientrenew.myClick('开始确认更新表格',self.__class__.pageClientrenew.start)
		self.__class__.pageClientrenew.myClick('护照有效期',self.__class__.pageClientrenew.passport,until='located',scroll=1)
		self.__class__.pageClientrenew.myClick('护照有效期关闭',self.__class__.pageClientrenew.closepicker)
		self.__class__.pageClientrenew.myClick('下一步，个人资料',self.__class__.pageClientrenew.next1)
		time.sleep(3)
		self.__class__.pageClientrenew.myInput('邮箱',self.__class__.pageClientrenew.email,accBinding[self.args.account][2])
		self.__class__.pageClientrenew.myClick('下一步，工作财务',self.__class__.pageClientrenew.next2)
		self.__class__.pageClientrenew.myClick('下一步，税务财务',self.__class__.pageClientrenew.next3)
		self.__class__.pageClientrenew.myClick('确认及签署',self.__class__.pageClientrenew.next4)
		self.__class__.pageClientrenew.myClick('勾选1',self.__class__.pageClientrenew.checkBox_crs)
		self.__class__.pageClientrenew.myClick('勾选2',self.__class__.pageClientrenew.checkBox_fatca)
		self.__class__.pageClientrenew.myClick('勾选3',self.__class__.pageClientrenew.checkBox_agreement)
		self.__class__.pageClientrenew.clientRenew_sign()
		self.__class__.pageClientrenew.myClick('简易投资目标',self.__class__.pageClientrenew.next5)
		time.sleep(1)
		self.__class__.pageClientrenew.myClick('身份披露',self.__class__.pageClientrenew.next6)
		self.__class__.pageClientrenew.myClick('提交资料',self.__class__.pageClientrenew.next7)
		self.assertTrue(self.__class__.pageClientrenew.isEleExists(self.__class__.pageClientrenew.flag))
		self.__class__.pageClientrenew.myClick('撤回申请',self.__class__.pageClientrenew.withdraw)
		time.sleep(2)
		self.__class__.pageClientrenew.clickYes()
		swithToRightWeb(self.driver,0)
		self.__class__.pageClientrenew.myClick('关闭',self.__class__.pageClientrenew.close[self.__class__.pageClientrenew.PFN])
		# self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-143 资料年审 ========== ')

	# @unittest.skip('跳过')
	@ddt.data(*['日','月'])
	def test_CMBI_144(self,types):
		'''结单查询'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-144 结单查询 ========== ')
		year,month,day=time.strftime('%Y-%m-%d').split('-')
		remotePath=f'/invoice/{year}'
		if types=='月':
			remotePath=f'{remotePath}/Monthly_{year}{month}{day}/{year}{month}{day}_{self.args.account}_CUST.pdf'
		elif types=='日':
			remotePath=f'{remotePath}/{year}{month}/{year}{month}{day}/{year}{month}{day}_{self.args.account}_CUST.pdf'
		ftp_store_file("testData/common.pdf",remotePath)

		self.__class__.pageBusineManage.cilckCommon_more(35)
		swithToRightWeb(self.driver,'index.html#/checkInquire')
		self.__class__.pageStatement.click_statement(types)
		n=0 if types=='日' else 1
		try:
			self.__class__.pageStatement.click_view(n)
		except Exception as err:
			myAddScreen(self,'截图')
			raise err
		swithToRightWeb(self.driver,0)
		self.assertTrue(self.__class__.pageStatement.flagRead_Exists())

		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-144 结单查询 ========== ')

	# @unittest.skip('跳过')
	@ddt.data(*['开启','关闭'])
	def test_CMBI_145(self,status):
		'''登录邮件通知'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-145 登录邮件通知--{status} ========== ')
		if self.args.ttl:self.skipTest('ttl账户暂时跳过')
		self.__class__.pageBusineManage.cilckCommon_more(60)
		swithToRightWeb(self.driver,'emailSetting')
		if status=='开启':
			self.__class__.pageEmailSetting.clickOpen()
		else:
			self.__class__.pageEmailSetting.clickClose()
		self.__class__.pageEmailSetting.clickSave()
		# self.__class__.pageBar.goBack()
		login(self.driver,self.__class__.acc_pwd,cusNickName=self.__class__.nickName,args=self.args,forceLogout=1)
		flag=0
		for i in range(5):
			logging.info(f'等待30秒后查询')
			time.sleep(30)
			records1=getMailRecord_appadmin(self.args.account,self.args.env)
			records2=getMailRecord(self.args.account,self.args.env)
			records=records1+records2
			logging.info(f'3分钟内的记录: {records}')
			if status=='开启':
				if len(records)>0:
					flag=1
					break
			else:
				if len(records)==0:
					flag=1
					break
		self.assertEqual(flag,1)

		logging.info(f' ========== 测试结束 CMBI-145 登录邮件通知--{status} ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_146(self):
		'''模拟炒股跳转'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-146 模拟炒股跳转 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(59)
		swithToRightWeb(self.driver,'appweb/simulate/?')
		self.__class__.pageFakeTrade.clickgetFakerMoney()
		amount=self.__class__.pageFakeTrade.textAmount()
		logging.info(f'模拟炒股总资产: {amount}')
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-146 模拟炒股跳转 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_147(self):
		'''存入股票'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-147 存入股票 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(63)
		swithToRightWeb(self.driver,'/index.html#/stockDeposit')
		self.__class__.pageImportStock.click_inHKstock()
		self.__class__.pageImportStock.click_brokerList()
		time.sleep(1)
		self.__class__.pageImportStock.click_broker()
		self.__class__.pageImportStock.input_account()
		self.__class__.pageImportStock.input_phone()
		self.__class__.pageImportStock.click_next()
		time.sleep(1)
		self.__class__.pageImportStock.click_addstock()
		self.__class__.pageImportStock.input_stockName()
		time.sleep(1)
		self.__class__.pageImportStock.click_resultOne()
		self.__class__.pageImportStock.input_stockNum()
		self.__class__.pageImportStock.click_addStock()
		self.__class__.pageImportStock.click_next()
		time.sleep(1)
		self.__class__.pageImportStock.click_confirm()
		swithToRightWeb(self.driver,'/index.html#/contactDeposit')
		self.__class__.pageImportStock.click_done()
		swithToRightWeb(self.driver,'/index.html#/depositDetail')
		self.assertTrue(self.__class__.pageImportStock.isSucess())
		swithToRightWeb(self.driver,'0')

		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-147 存入股票 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_203(self):
		'''交易历史查询'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-203 交易历史查询 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(2)
		swithToRightWeb(self.driver,'/trade/entrust')
		self.__class__.pageTradeHistory.clickRecord()
		self.assertGreater(self.__class__.pageTradeHistory.getTradeRecord(),0)
		#每月6号需要手动执行SQL插入交易数据
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-203 交易历史查询 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	@ddt.data(*['HKD','USD','CNY'])
	def test_CMBI_204(self,curr):
		'''资金存入'''
		if self.args.debug:self.skipTest('debug跳过')
		_infoDic={'HKD':'港币','USD':'美元','CNY':'人民币'}
		logging.info(f' ========== 测试开始 CMBI-204 存入{_infoDic[curr]} ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(22)
		# self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.driver,'/index.html#/deposit')
		self.__class__.pageImportMoney.clickCurr(curr)
		# swithToRightWeb(self.driver,'index.html#/deposit/step3')
		self.__class__.pageImportMoney.clickOtherBank()
		# swithToRightWeb(self.driver,'index.html#/deposit/otherBankGuidstep1')
		self.__class__.pageImportMoney.clickNext()
		self.__class__.pageImportMoney.clickYes()
		# swithToRightWeb(self.driver,'index.html#/deposit/otherBankGuidStep2')
		self.__class__.pageImportMoney.clickExportBank()
		self.__class__.pageImportMoney.clickWingLungBank()
		self.assertIn(self.__class__.pageImportMoney.getField(),['存入账户','Deposit in'])
		# self.assertIn(self.__class__.pageImportMoney.getField2(),['存款账号',])
		#输入银行卡号
		self.__class__.pageImportMoney.clickKeyboard(0)
		bankCode=str(randint(10**10,10**12))
		keyboardInput(self.driver,bankCode,2)
		time.sleep(3)
		#输入金额
		self.__class__.pageImportMoney.clickKeyboard(1)
		keyboardInput(self.driver,n=1)
		time.sleep(3)
		self.__class__.pageImportMoney.clickUploadPic()
		if curr=='HKD':
			flag=self.__class__.pageAlert.clickAllow()
			if flag:self.__class__.pageImportMoney.clickUploadPic()
		self.__class__.pageUploadPic.uploadPic()
		time.sleep(1)
		swithToRightWeb(self.driver,'index.html#/deposit/otherBankGuidStep2')

		self.__class__.pageImportMoney.clickSubmit()
		self.__class__.pageImportMoney.clickIknow()
		swithToRightWeb(self.driver,'deposit/otherBankGuidresult')
		self.assertTrue(self.__class__.pageImportMoney.textStatus())
		# self.__class__.pageImportMoney.clickDone()
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(xy=1,n=2)
		logging.info(f' ========== 测试结束 CMBI-204 存入{_infoDic[curr]} ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	@ddt.data(*['HKD','USD','CNY'])
	def test_CMBI_206(self,curr):
		'''资金提取'''
		if self.args.debug:self.skipTest('debug跳过')
		_infoDic={'HKD':'港币','USD':'美元','CNY':'人民币'}
		addBankcard(self.args.account,int(10e16*random()),env=self.args.env)# 添加银行卡
		# stopAllApprove(self.args.account,self.args.env)# 终止所有资金提取
		threading.Thread(target=inmoney_CMS,args=(self.args.account,'HKD','20000',self.args.env,1,)).start()#资金存入
		logging.info(f' ========== 测试开始 CMBI-206 提取{_infoDic[curr]} ========== ')
		
		self.__class__.pageBusineManage.cilckCommon_more(23)
		swithToRightWeb(self.driver,'#/withdraw')
		self.__class__.pageExportMoney.clickCurr(curr)

		keyboardInput(self.driver)
		self.__class__.pageExportMoney.clickSubmit()
		self.__class__.pageExportMoney.clickIknow()
		self.assertTrue(self.__class__.pageExportMoney.textStatus())
		self.__class__.pageExportMoney.clickDone()
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=1)
		logging.info(f' ========== 测试结束 CMBI-206 提取{_infoDic[curr]} ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_208(self):
		'''撤销存入'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-208 撤销存入 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(26)
		self.__class__.pageAlert.clickAlert()
		swithToRightWeb(self.driver,'/index.html#/fundsHistory')
		for i in range(5):
			if self.__class__.pageImExportHistory.imCancelsExists():break
			else:time.sleep(1)
		num1=self.__class__.pageImExportHistory.getNumTerminated()
		self.__class__.pageImExportHistory.clickCancel()
		self.__class__.pageImExportHistory.clickConfirm()
		time.sleep(5)
		num2=self.__class__.pageImExportHistory.getNumTerminated()
		# self.assertEqual(num1+1,num2)
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(xy=2)
		logging.info(f' ========== 测试结束 CMBI-208 撤销存入 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_209(self):
		'''撤销提取'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-209 撤销提取 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(26)
		self.__class__.pageAlert.clickAlert()
		time.sleep(3)
		swithToRightWeb(self.driver,'index.html#/fundsHistory')
		# for i in range(5):
		# 	self.__class__.pageImExportHistory.clickExportHistory()
		time.sleep(1)
		self.__class__.pageImExportHistory.clickExportHistory()
		num1=self.__class__.pageImExportHistory.getNumTerminated('out')
		self.__class__.pageImExportHistory.clickCancel('out')
		self.__class__.pageImExportHistory.clickConfirm()
		time.sleep(5)
		num2=self.__class__.pageImExportHistory.getNumTerminated('out')
		# self.assertEqual(num1+1,num2)
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(xy=2)
		logging.info(f' ========== 测试结束 CMBI-209 撤销提取 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210(self):
		'''新股认购 现金认购成功'''
		if self.args.debug:self.skipTest('debug跳过')
		if self.args.ttl:
			stopAllApprove(self.args.account,self.args.env)# 终止所有资金提取

			ableBalance=getAvailableBalance(self.args.account,env=self.args.env)
			currMoney=float(ableBalance['data']['HKD'].replace(',',''))
			money=100000000-currMoney
			if money>0:
				logging.info(f'账户HKD资金: {currMoney} 需要存入: {money}')
				inmoney_CMS(self.args.account,'HKD',money,env=self.args.env)#资金存入
			elif money==0:
				logging.info(f'账户HKD资金: {currMoney} 无需存入')
			elif money<0:
				logging.info(f'账户HKD资金: {currMoney} 需要提取: {abs(money)}')
				approveId=withdrawalSave(self.args.account,'HKD',abs(money),self.args.env)#提取资金
				logging.info(f'提取结果: {approveId}')
				result=money_check(approveId['data']['id'],bigMoney=1)#审核提取
				logging.info(f'审核提取结果: {result}')
		else:
			# 加资金 
			sql=insertMoney(self.args.account,types='HKD',delOld=1)
			excuteSQL(sql,dbType='sqlserver',env=self.args.env)
		
		oldOrderNo=queryIPOorder(self.args.account,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		m_acc=accBinding[self.args.account][0]
		oldOrderNo=queryIPOorder(m_acc,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		logging.info(f' ========== 测试开始 CMBI-210 新股认购 现金认购成功 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.__class__.pageIPO.clickIknow_web()
		# self.__class__.pageIPO.clickbuyIPO()
		self.__class__.pageIPO.clickIPOfirst()

		try:
			self.__class__.pageIPO.clickCancel()
			self.__class__.pageIPO.clickCancelYes()
			self.__class__.pageBar.goBack()
		except:
			pass
		
		swithToRightWeb(self.driver,'/eipo')
		time.sleep(5)
		# text=self.__class__.pageIPO.checkNumbers()
		# text0=[
		# 	'40 倍杠杆 利率 2.50% 认购股数 12,863,500  认购金额257,263,884.70 融资金额250,832,287.58 预计利息85,901.47 手续费100.00',
		# 	'40 倍杠杆 利率 2.50% 认购股数 2,000,000  认购金额39,999,049.20 融资金额38,999,072.97 预计利息13,355.85 手续费100.00',
		# 	'40 倍杠杆 利率 2.50% 认购股数 500  认购金额9,999.77 融资金额9,749.78 预计利息3.34 手续费100.00',

		# 	'30 倍杠杆 利率 2.00% 认购股数 12,863,500  认购金额257,263,884.70 融资金额248,696,997.34 预计利息68,136.16 手续费100.00',
		# 	'30 倍杠杆 利率 2.00% 认购股数 2,000,000  认购金额39,999,049.20 融资金额38,667,080.86 预计利息10,593.72 手续费100.00',
		# 	'30 倍杠杆 利率 2.00% 认购股数 500  认购金额9,999.77 融资金额9,666.78 预计利息2.65 手续费100.00',

		# 	'20 倍杠杆 利率 1.50% 认购股数 12,863,500  认购金额257,263,884.70 融资金额244,400,690.47 预计利息50,219.32 手续费100.00',
		# 	'20 倍杠杆 利率 1.50% 认购股数 2,000,000  认购金额39,999,049.20 融资金额37,999,096.74 预计利息7,808.03 手续费100.00',
		# 	'20 倍杠杆 利率 1.50% 认购股数 500  认购金额9,999.77 融资金额9,499.78 预计利息1.95 手续费100.00',

		# 	'12.5 倍杠杆 利率 1.00% 认购股数 12,863,500  认购金额257,263,884.70 融资金额236,682,773.92 预计利息32,422.30 手续费100.00',
		# 	'12.5 倍杠杆 利率 1.00% 认购股数 2,000,000  认购金额39,999,049.20 融资金额36,799,125.26 预计利息5,040.98 手续费100.00',
		# 	'12.5 倍杠杆 利率 1.00% 认购股数 500  认购金额9,999.77 融资金额9,199.79 预计利息1.26 手续费100.00',

		# 	'10 倍杠杆 利率 0.50% 认购股数 12,863,500  认购金额257,263,884.70 融资金额231,537,496.23 预计利息15,858.73 手续费100.00',
		# 	'10 倍杠杆 利率 0.50% 认购股数 2,000,000  认购金额39,999,049.20 融资金额35,999,144.28 预计利息2,465.69 手续费100.00',
		# 	'10 倍杠杆 利率 0.50% 认购股数 500  认购金额9,999.77 融资金额8,999.79 预计利息0.62 手续费100.00',

		# 	'普通认购认购股数 9,000,000  认购金额179,995,721.40 融资金额0.00 预计利息0.00 手续费30.00',
		# 	'普通认购认购股数 2,000,000  认购金额39,999,049.20 融资金额0.00 预计利息0.00 手续费30.00',
		# 	'普通认购认购股数 500  认购金额9,999.77 融资金额0.00 预计利息0.00 手续费30.00',

		# 	'自定义认购股数 12,863,500  融资比例  (利率2.50%)  97.50%  认购金额257,263,884.70 融资金额250,832,287.58 预计利息85,901.47 手续费100.00',
		# 	'自定义认购股数 2,000,000  融资比例  (利率2.50%)  97.50%  认购金额39,999,049.20 融资金额38,999,072.97 预计利息13,355.85 手续费100.00',
		# 	'自定义认购股数 500  融资比例  (利率2.50%)  97.50%  认购金额9,999.77 融资金额9,749.78 预计利息3.34 手续费100.00',
		# ]
		# flag=1
		# for i in range(len(text)):
		# 	if text[i].replace(' ','')!=text0[i].replace(' ',''):
		# 		logging.info(f'断言失败: 实际: {text[i]} 预期: {text0[i]}')
		# 		flag=0
		# 	else:
		# 		logging.info(f"断言成功: {text[i]}")
		# self.assertTrue(flag)

		self.__class__.pageIPO.clickIPOdetail()
		self.assertTrue(self.__class__.pageIPO.ipoDetailFlag())

		self.__class__.pageIPO.pageBack()
		self.__class__.pageIPO.clickAgree()
		self.__class__.pageIPO.clickBut_normal()
		# self.__class__.pageIPO.clickIknow()
		myAddScreen(self,'截图')
		self.__class__.pageIPO.clickViewOrder()
		self.__class__.pageIPO.clickOrderOne()
		self.assertTrue(self.__class__.pageIPO.successFlag())
		self.__class__.pageIPO.clickCancel()
		self.__class__.pageIPO.clickCancelYes()
		self.assertTrue(self.__class__.pageIPO.cancelFlag())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=3)

		logging.info(f' ========== 测试结束 CMBI-210 新股认购 现金认购成功 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210_1(self):
		'''新股认购 融资认购成功'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-210_1 新股认购 融资认购成功 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.__class__.pageIPO.clickIknow_web()
		# self.__class__.pageIPO.clickbuyIPO()
		self.__class__.pageIPO.clickIPOfirst()

		try:
			self.__class__.pageIPO.clickCancel()
			self.__class__.pageIPO.clickCancelYes()
			self.__class__.pageBar.goBack()
		except:
			pass
		
		swithToRightWeb(self.driver,'/eipo')

		time.sleep(2)

		self.__class__.pageIPO.clickAgree()
		self.__class__.pageIPO.clickButton_buy()
		# self.__class__.pageIPO.clickIknow()
		myAddScreen(self,'截图')
		self.__class__.pageIPO.clickViewOrder()
		self.__class__.pageIPO.clickOrderOne()
		self.assertTrue(self.__class__.pageIPO.successFlag())
		self.__class__.pageIPO.clickCancel()
		self.__class__.pageIPO.clickCancelYes()
		self.assertTrue(self.__class__.pageIPO.cancelFlag())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=3)

		logging.info(f' ========== 测试结束 CMBI-210_1 新股认购 融资认购成功 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210_2(self):
		'''新股认购 重复认购失败'''
		if self.args.debug:self.skipTest('debug跳过')
		m_acc=accBinding[self.args.account][0]
		threading.Thread(target=inmoney_CMS,args=(m_acc,'HKD','20000',self.args.env,1,)).start()
		
		oldOrderNo=queryIPOorder(self.args.account,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		oldOrderNo=queryIPOorder(m_acc,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		orderNo=eipoOrder_save(m_acc,self.args.env)#接口实现孖展账户认购

		logging.info(f' ========== 测试开始 CMBI-210_2 新股认购 重复认购失败 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.__class__.pageIPO.clickIknow_web()
		# self.__class__.pageIPO.clickbuyIPO()
		self.__class__.pageIPO.clickIPOfirst()
		
		swithToRightWeb(self.driver,'/eipo')
		time.sleep(2)

		self.__class__.pageIPO.clickAgree()
		self.__class__.pageIPO.clickButton_buy()
		# # self.__class__.pageIPO.clickIknow()
		myAddScreen(self,'截图')
		self.assertTrue(self.__class__.pageIPO.cantBuy2())
		self.__class__.pageIPO.clickIknow_web()

		# self.__class__.pageIPO.clickViewOrder()
		# self.assertEqual('重复认购',self.__class__.pageIPO.clickOrderOne_result())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=3)

		if orderNo:eipoOrder_cancel(orderNo,self.args.env)# 接口实现孖展账户撤销认购

		logging.info(f' ========== 测试结束 CMBI-210_2 新股认购 重复认购失败 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210_3(self):
		'''新股认购 现金认购失败'''
		if self.args.debug:self.skipTest('debug跳过')
		threading.Thread(target=stopAllApprove,args=(self.args.account,self.args.env,)).start()# 终止所有资金提取
		approveId=withdrawalSave(self.args.account,'HKD',None,self.args.env)#提取资金
		logging.info(f'提取结果: {approveId}')
		result=money_check(approveId['data']['id'],bigMoney=1)#审核提取
		logging.info(f'审核提取结果: {result}')

		logging.info(f' ========== 测试开始 CMBI-210_3 新股认购 现金认购失败 ========== ')
		try:
			self.__class__.pageBusineManage.cilckCommon_more(8)
			self.__class__.pageIPO.clickIknow()
			swithToRightWeb(self.driver,'/appweb/eipo')
			self.__class__.pageIPO.clickIknow_web()
			# self.__class__.pageIPO.clickbuyIPO()
			self.__class__.pageIPO.clickIPOfirst()

			try:
				self.__class__.pageIPO.clickCancel()
				self.__class__.pageIPO.clickCancelYes()
				self.__class__.pageBar.goBack()
			except:
				pass
			
			swithToRightWeb(self.driver,'/eipo')
			time.sleep(2)
			self.assertEqual(7,self.__class__.pageIPO.unableBuyFlag())
			swithToRightWeb(self.driver,0)
			self.__class__.pageBar.goBack(n=3)
		except Exception as err:
			raise err
		finally:
			inmoney_CMS(self.args.account,'HKD','100000000',env=self.args.env)#资金存入

		logging.info(f' ========== 测试结束 CMBI-210_3 新股认购 现金认购失败 ========== ')

	# @no_retry
	# @unittest.skip('跳过')
	@ddt.data(*['顶头槌','乙组头','甲组一手'])
	def test_CMBI_210_4(self,t):
		'''通过聆讯预约额度'''
		if self.args.debug:self.skipTest('debug跳过')
		# _infoDic={'a':'顶头槌','b':'乙组头','c':'甲组一手'}
		logging.info(f' ========== 测试开始 CMBI-210_4 通过聆讯预约额度 {t} ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		# self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		# self.__class__.pageIPO.clickIknow_web()
		self.__class__.pageIPO.clickpreIPO()
		self.__class__.pageIPO.clickpreIPO_buy()
		if t=='顶头槌':
			self.__class__.pageIPO.clickpreIPO_buy_a()
		elif t=='乙组头':
			self.__class__.pageIPO.clickpreIPO_buy_b()
		elif t=='甲组一手':
			self.__class__.pageIPO.clickpreIPO_buy_c()

		self.__class__.pageIPO.clickpreIPO_buy_apply()
		self.__class__.pageIPO.clickpreIPO_buy_apply_yes()
		self.assertTrue(self.__class__.pageIPO.preipoBuyFlag())
		self.__class__.pageIPO.clickpreIPO_buy_cancel()
		self.__class__.pageIPO.clickpreIPO_buy_cancel_confirm()

		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-210_4 通过聆讯预约额度 {t} ========== ')

	# @no_retry
	# @unittest.skip('跳过')
	def test_CMBI_210_5(self):
		'''打新计算器默认1手'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-210_5_45314 打新计算器默认1手 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		# self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		# self.__class__.pageIPO.clickIknow_web()
		self.__class__.pageIPO.clickpreIPO()
		# self.__class__.pageIPO.clickpreIPO_buy()
		self.__class__.pageIPO.clickIpoCaculator()
		self.assertTrue(self.__class__.pageIPO.caculatorFlagExists())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-210_5_45314 打新计算器默认1手 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210_6(self):
		'''债券认购 现金充足时普通认购成功'''
		if self.args.debug:self.skipTest('debug跳过')
		stopAllApprove(self.args.account,self.args.env)# 终止所有资金提取
		ableBalance=getAvailableBalance(self.args.account,env=self.args.env)
		currMoney=float(ableBalance['data']['HKD'].replace(',',''))
		money=100000000-currMoney
		if money>0:
			logging.info(f'账户HKD资金: {currMoney} 需要存入: {money}')
			inmoney_CMS(self.args.account,'HKD',money,env=self.args.env)#资金存入
		
		oldOrderNo=queryIPOorder(self.args.account,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		m_acc=accBinding[self.args.account][0]
		oldOrderNo=queryIPOorder(m_acc,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		logging.info(f' ========== 测试开始 CMBI-210 债券认购 现金充足时普通认购成功 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.__class__.pageIPO.clickIknow_web()
		# self.__class__.pageIPO.clickbuyIPO()
		self.__class__.pageIPO.clickIPOfirst(2)

		try:
			self.__class__.pageIPO.clickCancel()
			self.__class__.pageIPO.clickCancelYes()
			self.__class__.pageBar.goBack()
		except:
			pass
		
		swithToRightWeb(self.driver,'/eipo')
		time.sleep(3)

		self.__class__.pageIPO.clickAgree()
		self.__class__.pageIPO.clickBut_normal(3)
		# self.__class__.pageIPO.clickIknow()
		myAddScreen(self,'截图')
		self.__class__.pageIPO.clickViewOrder()
		self.__class__.pageIPO.clickOrderOne()
		self.assertTrue(self.__class__.pageIPO.successFlag())
		self.__class__.pageIPO.clickCancel()
		self.__class__.pageIPO.clickCancelYes()
		self.assertTrue(self.__class__.pageIPO.cancelFlag())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=3)

		logging.info(f' ========== 测试结束 CMBI-210 债券认购 现金充足时普通认购成功 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210_7(self):
		'''债券认购 现金充足时融资认购成功'''
		if self.args.debug:self.skipTest('debug跳过')
		stopAllApprove(self.args.account,self.args.env)# 终止所有资金提取
		ableBalance=getAvailableBalance(self.args.account,env=self.args.env)
		currMoney=float(ableBalance['data']['HKD'].replace(',',''))
		money=100000000-currMoney
		if money>0:
			logging.info(f'账户HKD资金: {currMoney} 需要存入: {money}')
			inmoney_CMS(self.args.account,'HKD',money,env=self.args.env)#资金存入
		
		oldOrderNo=queryIPOorder(self.args.account,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		m_acc=accBinding[self.args.account][0]
		oldOrderNo=queryIPOorder(m_acc,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		logging.info(f' ========== 测试开始 CMBI-210 债券认购 现金充足时融资认购成功 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.__class__.pageIPO.clickIknow_web()
		# self.__class__.pageIPO.clickbuyIPO()
		self.__class__.pageIPO.clickIPOfirst(2)

		try:
			self.__class__.pageIPO.clickCancel()
			self.__class__.pageIPO.clickCancelYes()
			self.__class__.pageBar.goBack()
		except:
			pass
		
		swithToRightWeb(self.driver,'/eipo')
		time.sleep(3)

		self.__class__.pageIPO.clickAgree()
		self.__class__.pageIPO.clickButton_buy()
		# self.__class__.pageIPO.clickIknow()
		myAddScreen(self,'截图')
		self.__class__.pageIPO.clickViewOrder()
		self.__class__.pageIPO.clickOrderOne()
		self.assertTrue(self.__class__.pageIPO.successFlag())
		self.__class__.pageIPO.clickCancel()
		self.__class__.pageIPO.clickCancelYes()
		self.assertTrue(self.__class__.pageIPO.cancelFlag())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=3)

		logging.info(f' ========== 测试结束 CMBI-210 债券认购 现金充足时融资认购成功 ========== ')

	# @no_retry
	@unittest.skip('跳过')
	def test_CMBI_210_8(self):
		'''债券认购 现金不足时融资认购成功'''
		if self.args.debug:self.skipTest('debug跳过')
		stopAllApprove(self.args.account,self.args.env)# 终止所有资金提取
		approveId=withdrawalSave(self.args.account,'HKD',None,self.args.env)#提取资金
		logging.info(f'提取结果: {approveId}')
		result=money_check(approveId['data']['id'],bigMoney=1)#审核提取
		logging.info(f'审核提取结果: {result}')
		
		oldOrderNo=queryIPOorder(self.args.account,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		m_acc=accBinding[self.args.account][0]
		oldOrderNo=queryIPOorder(m_acc,self.args.env)
		if oldOrderNo:eipoOrder_cancel(oldOrderNo,self.args.env)

		logging.info(f' ========== 测试开始 CMBI-210 债券认购 现金不足时融资认购成功 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(8)
		self.__class__.pageIPO.clickIknow()
		swithToRightWeb(self.driver,'/appweb/eipo')
		self.__class__.pageIPO.clickIknow_web()
		# self.__class__.pageIPO.clickbuyIPO()
		self.__class__.pageIPO.clickIPOfirst(2)

		try:
			self.__class__.pageIPO.clickCancel()
			self.__class__.pageIPO.clickCancelYes()
			self.__class__.pageBar.goBack()
		except:
			pass
		
		swithToRightWeb(self.driver,'/eipo')
		time.sleep(3)

		self.__class__.pageIPO.clickAgree()
		self.__class__.pageIPO.clickButton_buy()
		# self.__class__.pageIPO.clickIknow()
		myAddScreen(self,'截图')
		self.__class__.pageIPO.clickViewOrder()
		self.__class__.pageIPO.clickOrderOne()
		self.assertTrue(self.__class__.pageIPO.successFlag())
		self.__class__.pageIPO.clickCancel()
		self.__class__.pageIPO.clickCancelYes()
		self.assertTrue(self.__class__.pageIPO.cancelFlag())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(n=3)

		logging.info(f' ========== 测试结束 CMBI-210 债券认购 现金不足时融资认购成功 ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*[0,1,2])
	def test_CMBI_215(self):
		'''新增银行卡'''
		if self.args.debug:self.skipTest('debug跳过')
		_infoDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f' ========== 测试开始 CMBI-215 新增银行卡 ========== ')
		
		self.__class__.pageBusineManage.cilckCommon_more(37)
		swithToRightWeb(self.driver,'/index.html#/bankcard')
		self.__class__.pageBankCard.clickBankAdd()
		# swithToRightWeb(self.driver,'/bankcard/settlementEdit')
		self.__class__.pageBankCard.clickChooseBank()
		self.__class__.pageBankCard.clickBankName()
		self.__class__.pageBankCard.clickKeyboard2()
		bankCode=str(randint(10**10,10**12))
		keyboardInput(self.driver,bankCode,2)
		self.__class__.pageBankCard.clickaccType()
		self.__class__.pageBankCard.chooseAcc()
		self.__class__.pageBankCard.clickSubmit()
		swithToRightWeb(self.driver,'/index.html#/bankcard')
		self.assertTrue(self.__class__.pageBankCard.successFlag(bankCode))
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-215 新增银行卡 ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*[0,1,2])
	def test_CMBI_216(self):
		'''修改银行卡'''
		if self.args.debug:self.skipTest('debug跳过')
		# _infoDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f' ========== 测试开始 CMBI-216 修改银行卡 ========== ')
		
		self.__class__.pageBusineManage.cilckCommon_more(37)
		swithToRightWeb(self.driver,'/index.html#/bankcard')
		self.__class__.pageBankCard.clickBankEdit()
		# swithToRightWeb(self.driver,'/bankcard/settlementEdit')
		self.__class__.pageBankCard.clickChooseBank()
		bankName=self.__class__.pageBankCard.clickBankName()
		self.__class__.pageBankCard.clickSubmit()
		swithToRightWeb(self.driver,'/index.html#/bankcard')
		self.assertTrue(self.__class__.pageBankCard.successFlag(bankName))
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-216 修改银行卡 ========== ')

	# @unittest.skip('跳过')
	# @ddt.data(*[0,1,2])
	def test_CMBI_217(self):
		'''删除银行卡'''
		if self.args.debug:self.skipTest('debug跳过')
		_infoDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f' ========== 测试开始 CMBI-217 删除银行卡 ========== ')
		
		self.__class__.pageBusineManage.cilckCommon_more(37)
		swithToRightWeb(self.driver,'/index.html#/bankcard')
		cardNum=self.__class__.pageBankCard.getCardNum()
		self.__class__.pageBankCard.clickBankDelete()
		self.__class__.pageBankCard.clickComfirm()
		time.sleep(5)
		self.assertEqual(cardNum-1,self.__class__.pageBankCard.getCardNum())
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-217 删除银行卡 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_218(self):
		'''CRS个人账户登记'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-218 CRS个人账户登记 ========== ')
		
		self.__class__.pageBusineManage.cilckCommon_more(43) 
		swithToRightWeb(self.driver,'settle/crsRegister')
		self.__class__.pageCRS.clickperson()
		# self.__class__.pageCRS.clickName()
		# self.__class__.pageCRS.clickComfirm()
		# self.__class__.pageCRS.inputAddr()
		# self.__class__.pageCRS.inputCity()
		# self.__class__.pageCRS.inputState()
		# self.__class__.pageCRS.inputCountry()
		# self.__class__.pageCRS.inputTaxNumber()#输入税务编号
		# self.__class__.pageCRS.inputIDcrad()
		self.__class__.pageCRS.clickSubmit()
		# myAddScreen(self,'截图')
		self.assertIn('处理中',self.__class__.pageCRS.msgExists())
		self.__class__.pageBar.goBack()
		logging.info(f' ========== 测试结束 CMBI-218 CRS个人账户登记 ========== ')

	# @unittest.skip('跳过')
	def test_CMBI_219(self):
		'''CRS公司实体登记'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-219 CRS公司实体登记 ========== ')
		
		self.__class__.pageBusineManage.cilckCommon_more(43)
		swithToRightWeb(self.driver,'settle/crsRegister')
		self.__class__.pageCRS.clickCompany()
		# self.__class__.pageCRS.inputEmail()
		self.__class__.pageCRS.clickSubmitCompany()
		self.assertIn('请留意查收邮件',self.__class__.pageCRS.msgExists())
		swithToRightWeb(self.driver,0)
		self.__class__.pageBar.goBack(xy=1)
		logging.info(f' ========== 测试结束 CMBI-219 CRS公司实体登记 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_224(self):
		'''修改手机号'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-224 修改手机号 ========== ')
		realTel=accBinding[self.args.account][1]
		fakeTel=str(int(realTel)+2)
		self.__class__.pageBusineManage.cilckCommon_more(38)
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.clickphon_address()
		# self.__class__.pageEditInfo.clickEdit('联系号码')

		while 1:
			if self.__class__.pageEditInfo.isDelExists('联系号码'):
				self.__class__.pageEditInfo.clickDel('联系号码')
				self.__class__.pageEditInfo.clickYesDel()
			else:
				break

		self.__class__.pageEditInfo.clickEdit('联系号码')
		corrTel=self.__class__.pageEditInfo.textOldTel()
		editPhone(self.args.account,corrTel,env=self.args.env)
		newTel=realTel if corrTel==fakeTel else fakeTel

		self.__class__.pageEditInfo.clickReload()
		self.__class__.pageEditInfo.inputNewTel(newTel)
		self.__class__.pageEditInfo.clickNextTel()
		time.sleep(3)
		smsCode=getSMScode(corrTel,env=self.args.env,n=4)

		swithToRightWeb(self.driver,0)
		self.__class__.pageEditInfo.clickInput()
		self.__class__.pageEditInfo.inputSMScode(smsCode)

		swithToRightWeb(self.driver,'/mobile/code')
		self.__class__.pageEditInfo.clickCheckTel()
		time.sleep(5)
		self.assertTrue(self.__class__.pageEditInfo.msgExists())

		self.__class__.pageEditInfo.clickBack()
		swithToRightWeb(self.driver,'/profile/contact')
		try:
			self.__class__.pageEditInfo.clickDel('联系号码')
			self.__class__.pageEditInfo.clickYesDel()
		except:
			pass
		self.__class__.pageBar.goBack(3)
		logging.info(f' ========== 测试结束 CMBI-224 修改手机号 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_225(self):
		'''修改邮箱'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-225 修改邮箱 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(38)
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.clickphon_address()
		# self.__class__.pageEditInfo.clickEmail()
		while 1:
			if self.__class__.pageEditInfo.isDelExists('电子邮箱'):
				self.__class__.pageEditInfo.clickDel('电子邮箱')
				self.__class__.pageEditInfo.clickYesDel()
			else:
				break

		self.__class__.pageEditInfo.clickEdit('电子邮箱')
		oldEmail=self.__class__.pageEditInfo.textOldEmail()
		email=accBinding[self.args.account][2]
		newEmail=''.join(sample('abcdefghijklmnopqrstuvwxyz',6))+'@'+''.join(sample('abcdefghijklmnopqrstuvwxyz',4))+'.'+''.join(sample('abcdefghijklmnopqrstuvwxyz',3))
		self.__class__.pageEditInfo.clickReload()
		self.__class__.pageEditInfo.inputNewEmail(newEmail)
		self.__class__.pageEditInfo.clickNextTel()
		time.sleep(3)
		smsCode=getEmailCode(email,env=self.args.env,n=4)

		swithToRightWeb(self.driver,0)
		self.__class__.pageEditInfo.clickInput()
		self.__class__.pageEditInfo.inputSMScode(smsCode)

		swithToRightWeb(self.driver,'/mobile/email/code')
		self.__class__.pageEditInfo.clickCheckEmail()
		self.assertTrue(self.__class__.pageEditInfo.msgExists())
		self.__class__.pageEditInfo.clickBack()
		swithToRightWeb(self.driver,'/profile/contact')
		try:
			self.__class__.pageEditInfo.clickDel('电子邮箱')
			self.__class__.pageEditInfo.clickYesDel()
		except:
			pass
		self.__class__.pageBar.goBack(3)
		logging.info(f' ========== 测试结束 CMBI-225 修改邮箱 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_225_1(self):
		'''证件信息维护'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-225_1 证件信息维护 ========== ')
		switch_ocr('off',self.args.env)
		self.__class__.pageBusineManage.cilckCommon_more(38)
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.clickCardInfo()
		if self.pageBar.PFN=='Android':self.__class__.pageEditInfo.clickReload()
		if self.__class__.pageEditInfo.withdrawExists():
			self.__class__.pageEditInfo.clickWithdraw()
			self.__class__.pageEditInfo.clickYesDel()
			time.sleep(10)

		self.__class__.pageEditInfo.clickEdit()
		#上传照片
		self.__class__.pageEditInfo.clickUploadfront()
		self.__class__.pageUploadPic.uploadPic()

		self.__class__.pageEditInfo.clickNextTel()
		time.sleep(3)
		# self.__class__.pageEditInfo.clickNextTel()
		myAddScreen(self,'截图')
		self.assertTrue(self.__class__.pageEditInfo.msgExists())
		self.__class__.pageEditInfo.clickBack()
		self.__class__.pageEditInfo.clickWithdraw()
		self.__class__.pageEditInfo.clickYesDel()
		time.sleep(10)
		self.__class__.pageBar.goBack(2)
		# switch_ocr('on',self.args.env)
		logging.info(f' ========== 测试结束 CMBI-225_1 证件信息维护 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_225_2(self):
		'''地址信息维护'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-225_2 地址信息维护 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(38)
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.clickphon_address()
		if self.pageBar.PFN=='Android':self.__class__.pageEditInfo.clickReload()
		self.__class__.pageEditInfo.clickEdit('地址信息')
		time.sleep(10)
		#上传照片
		self.__class__.pageEditInfo.clickUploadAddressImg()
		self.__class__.pageUploadPic.uploadPic()

		self.__class__.pageEditInfo.clickNextTel()
		time.sleep(10)
		self.assertTrue(self.__class__.pageEditInfo.msgExists())
		self.__class__.pageEditInfo.clickBack()
		self.__class__.pageEditInfo.clickWithdraw()
		self.__class__.pageEditInfo.clickYesDel()
		time.sleep(10)
		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-225_2 地址信息维护 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_225_3(self):
		'''财务状况信息维护'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-225_3 财务状况信息维护 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(38)
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.click_workMoney()
		if self.pageBar.PFN=='Android':self.__class__.pageEditInfo.clickReload()
		self.__class__.pageEditInfo.click_moneyInfo()
		time.sleep(5)
		self.__class__.pageEditInfo.inputsource_note()
		self.__class__.pageEditInfo.clickSave()
		time.sleep(5)
		myAddScreen(self,'截图')
		self.assertTrue(self.__class__.pageEditInfo.msgExists())
		self.__class__.pageEditInfo.clickBack()
		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-225_3 财务状况信息维护 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_225_4(self):
		'''雇佣信息维护'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-225_4 雇佣信息维护 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(38)
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.click_workMoney()
		if self.pageBar.PFN=='Android':self.__class__.pageEditInfo.clickReload()
		self.__class__.pageEditInfo.click_workInfo()
		self.__class__.pageEditInfo.inputCompanyname()
		self.__class__.pageEditInfo.clickSave()
		time.sleep(5)
		myAddScreen(self,'截图')
		self.assertTrue(self.__class__.pageEditInfo.msgExists())
		self.__class__.pageEditInfo.clickBack()
		self.__class__.pageBar.goBack(2)
		logging.info(f' ========== 测试结束 CMBI-225_4 雇佣信息维护 ========== ')

	# @unittest.skip('跳过')
	# @no_retry
	def test_CMBI_225_5(self):
		'''相关声明维护'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-225_5 相关声明维护 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(38)
		if self.pageBar.PFN=='Android':self.__class__.pageEditInfo.clickReload()
		swithToRightWeb(self.driver,'app/settle/')
		self.__class__.pageEditInfo.click_statement()
		self.__class__.pageEditInfo.clickbtn_statement()
		self.__class__.pageEditInfo.clickSave()
		time.sleep(5)
		myAddScreen(self,'截图')
		self.assertTrue(self.__class__.pageEditInfo.msgExists())
		self.__class__.pageEditInfo.clickBack()
		self.__class__.pageBar.goBack(1)
		logging.info(f' ========== 测试结束 CMBI-225_5 相关声明维护 ========== ')


	# @unittest.skip('跳过')
	def test_CMBI_226(self):
		'''风险测评'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-226 风险测评 ========== ')
		self.__class__.pageBusineManage.cilckCommon_more(39)
		swithToRightWeb(self.driver,'/settle/rpq')
		
		if self.__class__.pageRiskAss.btnReStartExists():
			self.__class__.pageRiskAss.clickReStart()
			# self.__class__.pageRiskAss.clickIknow()
			# self.__class__.pageRiskAss.inputResaon()
			# self.__class__.pageRiskAss.clickReStart2()
		else:
			self.__class__.pageRiskAss.clickStart()
		# time.sleep(3)
		self.__class__.pageRiskAss.clickIknow()
		self.__class__.pageRiskAss.clickOption()
		# self.__class__.pageRiskAss.clickSelect()
		self.__class__.pageRiskAss.clickComfirm()
		self.__class__.pageRiskAss.clickSubmit()
		self.__class__.pageRiskAss.clickDone()
		time.sleep(1)
		swithToRightWeb(self.driver,0)
		logging.info(f' ========== 测试结束 CMBI-226 风险测评 ========== ')


	# @unittest.skip('跳过')
	@ddt.data(*['HKD','USD'])
	def test_CMBI_227(self,curr):
		'''融资额度申请'''
		if self.args.debug:self.skipTest('debug跳过')
		logging.info(f' ========== 测试开始 CMBI-227 融资额度申请 {curr} ========== ')
		if self.args.ttl and curr=='USD':self.skipTest('ttl账户只有港元融资额度')
		m_acc=accBinding[self.args.account][0]
		pwd=accountPool[m_acc][0]
		nickname=accountPool[m_acc][1]
		resetpwd_ttl(m_acc,pwd,self.args.env)
		cancelFinance(m_acc,pwd,self.args.env,self.args.ttl)
		try:
			login(self.driver,acc_pwd=(m_acc,pwd),forceLogout=1,cusNickName=nickname,args=self.args)

			self.__class__.pageBar.clickMy()
			# self.__class__.pageAlert.clickAlert()
			self.__class__.pageMy.clickYWBL()
			# self.__class__.pageBusineManage.inputPwordIFneeded()
			swithToRightWeb(self.driver,'/appMap')
			self.__class__.pageBusineManage.cilckCommon_more(64)
			swithToRightWeb(self.driver,'settle/margin')
			if not self.args.ttl:
				if curr=='HKD':
					self.__class__.pageFinancingQuota.clickmarketHKD()
				elif curr=='USD':
					self.__class__.pageFinancingQuota.clickmarketUSD()
			self.__class__.pageFinancingQuota.inputAmount()
			self.__class__.pageFinancingQuota.clickSubmit()
			time.sleep(3)
			self.__class__.pageFinancingQuota.clickCancel()
			time.sleep(3)
			self.__class__.pageFinancingQuota.cancelMsgExists()
			self.__class__.pageBar.goBack()
		except Exception as e:
			raise e
		finally:
			logout(self.driver)
		logging.info(f' ========== 测试结束 CMBI-227 融资额度申请 {curr} ========== ')

	def tearDown(self):
		if self.args.debug:return
		self.__class__.pageBar.goBack()

	@classmethod
	def tearDownClass(cls):
		logging.info(' ########## 业务办理模块测试结束 ########## ')

if __name__=='__main__':
	# unittest.main()
	pass