import logging,time,traceback
from selenium.webdriver.common.by import By
from page.base import PageBase
from random import randint
from common.seleniumError import SCEENVE

class PageRiskAss(PageBase):
	def __init__(self,driver):
		# 风险评估 页面
		super().__init__(driver)
		#第一步
		self.btnStart=(By.XPATH,"//*[text()='开始测评']")
		# self.btnReStart=(By.ID,"rewriterpq")
		self.btnReStart2=(By.XPATH,"//*[contains(text(),'重新')]")
		self.btnNext0=(By.XPATH,"//*[text()='下一题']")

		#第二步
		self.reFillResaon=(By.XPATH,"//*[@class='inputGroup rewrite_list']/p[1]/input[1]")
		self.answer={
			'1':(By.XPATH,"//*[@id='dialogTest']//p[4]/input[1]"),
			'2':(By.XPATH,"//*[@id='page2']//p[4]/input[1]"),
			'3':(By.XPATH,"//*[@id='page3']//p[3]/input[1]"),
			'4':(By.XPATH,"//*[@id='page4']//p[5]/input[1]"),
			'5':(By.XPATH,"//*[@id='page5']//p[3]/input[1]"),
			'6':(By.XPATH,"//*[@id='page6']//p[5]/input[1]"),
			'7':(By.XPATH,"//*[@id='page7']//p[4]/input[1]"),
			'8':(By.XPATH,"//*[@id='page8']//p[5]/input[1]"),
			'9':(By.XPATH,"//*[@id='page9']//p[4]/input[1]"),
		}

		# self.btnSelect=(By.XPATH,"//*[@text='请选择']")#有两个,年限和次数
		# self.btnSelectAns=(By.XPATH,'//*[@resource-id="android:id/text1"]')#第2个

		#第三步
		self.btnSubmit=(By.XPATH,"//*[text()='提交']")
		self.btnDone=(By.XPATH,"//*[text()='完成']")

		# self.btnNext=(By.XPATH,"//*[@text='下一步，测评结果']")
		# self.btnNext2=(By.XPATH,"//*[@text='下一步，风险披露']")
		self.iKnow=(By.XPATH,'//*[contains(text(),"我知道了")]')

	def clickIknow(self):
		logging.info('点击 我知道了')
		for i in range(5):
			try:
				self.findElements(self.iKnow,until='located')[1].click()
				return
			except SCEENVE:
				if i==4:raise SCEENVE(f'{traceback.format_exc()}')
				else:time.sleep(3)


	def btnReStartExists(self):
		return self.isEleExists(self.btnReStart2) 

	#第一步
	def clickStart(self):
		logging.info('点击 开始测评')
		self.findElement(self.btnStart).click()

	def clickReStart(self):
		logging.info('点击 重新填写')
		self.findElement(self.btnReStart2).click()

	def inputResaon(self):
		logging.info('点击重置原因')
		try:
			self.findElement(self.reFillResaon,screen=0).click()
		except:
			pass

	def clickReStart2(self):
		logging.info('点击 重新测评')
		try:
			self.findElement(self.btnReStart2,screen=0).click()
		except:
			pass

	#第二步
	def clickOption(self,swipe=0):
		from common.seleniumError import SCESERE
		for i in range(1,10):
			logging.info(f'第 {i} 题')
			if i in [1]:
				logging.info('点击下一题')
				self.findElement(self.btnNext0).click()
			else:
				for j in range(5):
					try:
						self.findElement(self.answer[str(i)],until='located',screen=0).click()
						time.sleep(1)
						break
					except SCESERE:
						if j==4:raise SCESERE(f'第{i}题选项定位失败')
						time.sleep(1)
					except TypeError:
						logging.info('点击下一题')
						self.findElement(self.btnNext0).click()
						break
			if i==3:
				self.driver.execute_script("jumpPage(4,false)")
			elif i==9:
				from selenium.webdriver.support.select import Select
				Select(self.findElement((By.NAME,'q9_2_1'))).select_by_value("2")
				Select(self.findElement((By.NAME,'q9_2_2'))).select_by_value("2")
			time.sleep(0.5)
	
	# def clickNext(self):
	# 	logging.info('点击 下一步，测评结果')
	# 	self.findElement(self.btnNext).click()

	# def clickNext2(self):
	# 	logging.info('点击 下一步，风险披露')
	# 	self.findElement(self.btnNext2).click()

	# def clickSelect(self):
	# 	for ele in self.findElements(self.btnSelect):
	# 		ele.click()
	# 		self.findElements(self.btnSelectAns)[2].click()
	# 		time.sleep(1)

	def clickComfirm(self):
		logging.info('点击 下一步，客户确认')
		self.driver.execute_script("jumpPage('statement')")

	def clickSubmit(self):
		logging.info('点击 提交')
		self.findElement(self.btnSubmit).click()

	def clickDone(self):
		logging.info('点击 完成')
		self.findElement(self.btnDone).click()