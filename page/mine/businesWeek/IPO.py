import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import switch_execute,getSoup

class PageIPO(PageBase):
	def __init__(self,driver):
		# 新股认购 页面
		super().__init__(driver)
		self.item=(By.XPATH,"//p[contains(text(),'AUTO(自动化)')]/../../..//div[contains(text(),'立即认购') or contains(text(),'IPO Subs')]")
		self.item2=(By.XPATH,"//p[contains(text(),'债券(自动化)')]/../../..//div[contains(text(),'立即认购') or contains(text(),'IPO Subs')]")
		self.ipoDetail=(By.CLASS_NAME,'ipoDetail')
		self.ipoDetail_flag=(By.XPATH,"//*[contains(text(),'招股书')]")
		self.btnAgree=(By.CLASS_NAME,"md-agree-icon")
		self.cancel=(By.XPATH,"//*[text()='撤销订单' or text()='Cancel']")
		self.cancelYes=(By.XPATH,"//*[contains(text(),'确认撤销') or contains(text(),'Confirm')]")
		self.viewOrder=(By.XPATH,"//*[contains(text(),'查看订单') or contains(text(),'Order Details')]")
		self.orderOne=(By.XPATH,"//*[@class='item' and @sensors-data-type='list']")
		self.orderOne_result=(By.XPATH,"//*[@class='item' and @sensors-data-type='list'][1]//span[6]")


		self.btnNums=(By.CLASS_NAME,'md-cell-item')
		self.btnNumOne=(By.XPATH,"//*[@class='popup']/ul[1]/li[1]")
		self.btnBuy=(By.CLASS_NAME,"detail-btn")
		self.confirm=(By.XPATH,"//a[contains(text(),'取消预约') or contains(text(),'Confirm')]")
		self.iKnow=(By.XPATH,"//*[contains(text(),'我知道了') or contains(text(),'I see')]")
		self.flag2=(By.XPATH,"//*[contains(text(),'已撤销') or contains(text(),'Cancelled')]")
		self.alert={
			'Android':(By.XPATH,'//*[contains(@text,"知道了") or contains(@text,"I see")]'),
			'iOS':(By.IOS_PREDICATE,"name contains '知道了' or name contains 'I see'")
		}
		
		#通过聆讯
		# self.buyIPO=(By.XPATH,"//span[contains(text(),'新股认购')]")
		self.preIPO=(By.XPATH,"//span[contains(text(),'已递表') or contains(text(),'Delivered')]")
		self.preIPO_buy=(By.XPATH,"//div[contains(text(),'自动化')]/..//div[contains(text(),'预约额度') or contains(text(),'Reservation')]")

		self.preIPO_buy_c=(By.XPATH,'//p[@sensors-data-title="甲组一手" or @sensors-data-title="One-lot"]')# 甲组一手
		self.preIPO_buy_b=(By.XPATH,'//p[@sensors-data-title="乙组头" or @sensors-data-title="Pool B"]')# 乙组头
		self.preIPO_buy_a=(By.XPATH,'//p[@sensors-data-title="顶头槌" or @sensors-data-title="Max Ticket"]')

		self.preIPO_buy_apply=(By.CLASS_NAME,'confirm-button')# 申请预约
		self.preIPO_buy_apply_yes=(By.CLASS_NAME,'md-dialog-btn')# 申请预约 

		self.preIPO_buy_flag=(By.XPATH,"//p[contains(text(),'预约已提交') or contains(text(),'request submitted')]")
		self.preIPO_buy_cancel=(By.CLASS_NAME,'cancel-button')# 取消预约

		self.noBuy=(By.XPATH,"//*[contains(text(),'购买力不足')]")
		self.noBuy2=(By.XPATH,"//*[contains(text(),'不可重复认购')]")
		
		self.ipoCaculator=(By.XPATH,"//p[contains(text(),'打新计算器') or contains(text(),'Calculator')]/..")
		self.caculatorFlag=(By.XPATH,"//p[contains(text(),'认购手数') or contains(text(),'Lots Subscribed')]")

	def caculatorFlagExists(self):
		return self.isEleExists(self.caculatorFlag,screen=1)

	def clickIpoCaculator(self):
		logging.info('点击 打新计算器')
		self.findElement(self.ipoCaculator).click()

	def clickpreIPO(self):
		logging.info('点击 已递表')
		self.findElement(self.preIPO).click()

	def clickpreIPO_buy(self):
		logging.info('点击 预约额度')
		self.findElement(self.preIPO_buy).click()


	def clickpreIPO_buy_c(self):
		logging.info('点击 甲组一手')
		self.findElement(self.preIPO_buy_c).click()

	def clickpreIPO_buy_b(self):
		logging.info('点击 乙组头')
		self.findElement(self.preIPO_buy_b).click()

	def clickpreIPO_buy_a(self):
		logging.info('点击 顶头槌')
		self.findElement(self.preIPO_buy_a).click()


	def clickpreIPO_buy_apply(self):
		logging.info('点击 申请预约')
		self.findElement(self.preIPO_buy_apply).click()

	def clickpreIPO_buy_apply_yes(self):
		logging.info('再次点击 申请预约')
		self.findElements(self.preIPO_buy_apply_yes,until='located')[2].click()

	def preipoBuyFlag(self):
		time.sleep(3)
		return self.isEleExists(self.preIPO_buy_flag,screen=1)

	def clickpreIPO_buy_cancel(self):
		logging.info('点击 取消预约')
		self.findElement(self.preIPO_buy_cancel).click()

	def clickpreIPO_buy_cancel_confirm(self):
		logging.info('点击 确认')
		self.findElement(self.confirm).click()


	@switch_execute
	def clickIknow(self):
		try:
			self.findElement(self.alert[self.PFN]).click()
			logging.info('点击 我知道了')
		except AttributeError:
			pass

	def clickIknow_web(self):
		logging.info('点击 我知道了')
		try:
			self.findElement(self.iKnow,screen=False).click()
		except AttributeError:
			pass

	def clickIPOfirst(self,n=1):
		logging.info('点击自动化专用新股立即认购')
		if n==1:
			self.scrollClick(self.findElement(self.item))
		else:
			self.scrollClick(self.findElement(self.item2))

	def checkNumbers(self):
		logging.info('获取不同的认购方案的资金数额')
		soup=getSoup(self.driver)
		textList=[]
		cards=soup.select_one('.swiper-wrapper').select('.swiper-slide')
		j=0
		for i in range(len(cards)):
			a=self.driver.find_elements_by_class_name('group-a')[i]
			b=self.driver.find_elements_by_class_name('group-b')[i]
			c=self.driver.find_elements_by_class_name('group-c')[i]
			for e in [a,b,c]:
				self.clickByScript(e)
				soup=getSoup(self.driver)
				text=soup.select_one('.swiper-wrapper').select('.swiper-slide')[i].text.strip()
				end=text.index('购买力')
				text=text[:end].replace('最大认购  乙组头  甲组1手 ','').replace('融资金额',' 融资金额').replace('预计利息',' 预计利息').replace('手续费',' 手续费')
				textList.append(text)
				j+=1
		return textList

	def clickIPOdetail(self):
		logging.info('点击 详情')
		self.findElement(self.ipoDetail).click()
	
	def ipoDetailFlag(self):
		time.sleep(3)
		return self.isEleExists(self.ipoDetail_flag,screen=1)

	def pageBack(self):
		self.driver.execute_script("window.history.back();")

	def clickAgree(self):
		logging.info('点击 勾选同意')
		eles=self.findElements(self.btnAgree)
		for ele in eles:
			self.myTap(ele)

	def clickBut_normal(self,n=5):
		logging.info('点击普通认购')
		self.driver.execute_script(f"document.getElementsByClassName('btn')[{n}].click();")

	def clickButton_buy(self):
		logging.info('点击融资认购')
		self.driver.execute_script("document.getElementsByClassName('btn')[0].click();")

	def successFlag(self):
		time.sleep(3)
		return self.isEleExists(self.cancel,screen=1)

	def clickCancel(self,timeout=15,screen=1):
		logging.info('点击 撤销订单')
		self.findElement(self.cancel,screen=screen,timeout=timeout).click()

	def clickCancelYes(self):
		logging.info('点击 确认撤销')
		self.findElement(self.cancelYes,until='located').click()

	def clickViewOrder(self):
		logging.info('点击 查看订单')
		eles=self.findElements(self.viewOrder,until='located')
		for e in eles:
			try:e.click()
			except:pass

	def clickOrderOne(self):
		logging.info('点击查看第一条订单记录')
		self.findElements(self.orderOne,until='located')[0].click()

	def clickOrderOne_result(self):
		return self.findElement(self.orderOne_result,until='located').text.strip()

	def unableBuyFlag(self):
		return len(self.findElements(self.noBuy,until='located'))

	def cancelFlag(self):
		return self.isEleExists(self.flag2)
		
	def cantBuy2(self):
		return self.isEleExists(self.noBuy2)		
