import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import swipeUp

try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By

class PageMy(PageBase):
	def __init__(self,driver):
		# '我的' 页面
		super().__init__(driver)
		self.btnLogin={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_login'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='点击登录' or name=='Click to login'")
		}#注册/登录按钮
		self.eleNick={
			'Android':(By.ID,'com.cmbi.zytx:id/text_user_nick'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='nickName'")
		}#登录成功后用户nickname元素
		self.btnYWBL={
			'Android':(By.XPATH,"//*[@text='更多服务' or @text='More']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='更多服务' or name=='More'")
		}
		# self.btnCommonProb={
		# 	'Android':(By.XPATH,"//*[@text='常见问题']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='常见问题'")
		# }
		# self.btnContact={
		# 	'Android':(By.XPATH,"//*[@text='联系客服']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='联系客服'")
		# }
		# self.btnFakeTrade={
		# 	'Android':(By.XPATH,"//*[@text='模拟炒股']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='模拟炒股'")
		# }
		# self.btnCusManage={
		# 	'Android':(By.XPATH,"//*[@text='微客服']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='微客服'")
		# }

		self.btnSet={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_setting'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='mine setting'")
		}
		# self.btnFeedback={
		# 	'Android':(By.XPATH,"//*[@text='意见反馈']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='意见反馈'")
		# }

		self.eleAcc={
			'Android':(By.ID,'com.cmbi.zytx:id/account'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='accountM'")
		}#账户户口号 第 1 个

	def clickLogin(self):
		time.sleep(1)
		logging.info('点击 注册/登录 按钮')
		self.findElement(self.btnLogin[self.PFN]).click()

	def clickSet(self):
		logging.info('点击 设置 按钮')
		self.findElement(self.btnSet[self.PFN]).click()

	def clickYWBL(self):
		logging.info('点击 业务办理/更多服务 按钮')
		self.findElement(self.btnYWBL[self.PFN]).click()
		time.sleep(3)

	# def clickCusManage(self):
	# 	logging.info('点击 微客服 按钮')
	# 	self.findElement(self.btnCusManage[self.PFN]).click()

	# def clickFakeTrade(self):
	# 	logging.info('点击 模拟炒股 按钮')
	# 	self.findElement(self.btnFakeTrade[self.PFN]).click()

	# def clickCommonProb(self):
	# 	time.sleep(1)
	# 	swipeUp(self.driver)
	# 	logging.info('点击 常见问题 按钮')
	# 	self.findElement(self.btnCommonProb[self.PFN]).click()

	# def clickContact(self):
	# 	logging.info('点击 联系客服 按钮')
	# 	self.findElement(self.btnContact[self.PFN]).click()

	# def clickFeedback(self):
	# 	logging.info('点击 意见反馈 按钮')
	# 	self.findElement(self.btnFeedback[self.PFN]).click()

	def textNick(self,logit=1,timeout=10):
		if logit:logging.info('获取用户昵称')#已登录状态才能用此方法
		return self.findElement(self.eleNick[self.PFN],screen=False,timeout=timeout).text

	def textAcc(self):
		return self.findElements(self.eleAcc[self.PFN])[1].text.strip()

