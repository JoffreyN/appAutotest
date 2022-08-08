import logging
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By

from page.base import PageBase

class PageSet(PageBase):
	def __init__(self,driver):
		# '设置' 页面
		super().__init__(driver)
		self.btnLogout={
			'Android':(By.ID,'com.cmbi.zytx:id/safe_logout'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='安全退出' or name=='Log Out'")
		}#安全退出按钮
		self.btnLogout_comfirm={
			'Android':(By.ID,'com.cmbi.zytx:id/safe_logout'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确定' or name=='Confirm'")
		}#安全退出按钮
		self.btnSer={
			'Android':(By.ID,'com.cmbi.zytx:id/rlayout_server_address_setting'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='网络环境' or name=='Switch Server'")
		}#切换服务器按钮
		self.eleEnv={
			'Android':(By.ID,'com.cmbi.zytx:id/server_address_setting'),
			'iOS':(AppiumBy.XPATH,'//*[@name="网络环境" or @name="Switch Server"]/following-sibling::*[1]')
			# 'iOS':(AppiumBy.IOS_PREDICATE,"name=='env'")
		}#当前服务器环境
		self.btnAbout=(By.IOS_PREDICATE,'name=="关于我们" or name=="About"')
		self.eleVer={
			'Android':(By.ID,'com.cmbi.zytx:id/verson_code'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='version'")
		}#版本号
		self.btnChangePwd={
			'Android':(By.XPATH,"//*[@text='忘记/重置密码' or @text='Change Login Password']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='忘记/重置密码' or name=='Change Login Password'")
		}

		self.btnDEV={
			'Android':(By.XPATH,'//*[@class="android.widget.ListView"]/android.widget.LinearLayout[1]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='DEV'")
		}
		self.btnTEST={
			'Android':(By.XPATH,'//*[@class="android.widget.ListView"]/android.widget.LinearLayout[2]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='TEST'")
		}
		self.btnUAT={
			'Android':(By.XPATH,'//*[@class="android.widget.ListView"]/android.widget.LinearLayout[3]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='UAT'")
		}
		self.btnPRE={
			'Android':(By.XPATH,'//*[@class="android.widget.ListView"]/android.widget.LinearLayout[4]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='PRE'")
		}
		self.btnPROD={
			'Android':(By.XPATH,'//*[@class="android.widget.ListView"]/android.widget.LinearLayout[5]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='PROD'")
		}

		self.btnConfirm={
			'Android':(By.ID,'com.cmbi.zytx:id/buttonDefaultPositive'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='-1'")
		}#确定
		self.rebootConfirm={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_confirm'),
			'iOS':(AppiumBy.IOS_PREDICATE,"")
		}#确定
		


	def clickLogout(self):
		logging.info('点击 安全退出 按钮')
		self.findElement(self.btnLogout[self.PFN]).click()

	def clickLogout_confirm(self):
		logging.info('点击 确定 按钮')
		if self.PFN=='iOS':
			self.findElement(self.btnLogout_comfirm[self.PFN]).click()

	def clickSwiSer(self):
		logging.info('点击 切换服务器 按钮')
		self.findElement(self.btnSer[self.PFN]).click()

	def chooseSer(self,server):
		serverDic={
			'DEV':self.btnDEV[self.PFN],
			'TEST':self.btnTEST[self.PFN],
			'UAT':self.btnUAT[self.PFN],
			'PRE':self.btnPRE[self.PFN],
			'PROD':self.btnPROD[self.PFN],
		}
		logging.info(f'点击选择 服务器 {server}')
		self.findElement(serverDic[server]).click()

	def clickConfirm(self):
		if self.PFN!='iOS':
			logging.info('点击选择 确定')
			self.findElement(self.btnConfirm[self.PFN]).click()
		else:
			pass

	def clickRebootYes(self):
		if self.PFN!='iOS':
			logging.info('点击 确认')
			self.findElement(self.rebootConfirm[self.PFN]).click()
		else:
			pass

	def textVersion(self):
		logging.info('获取当前安装的app版本号……')
		if self.PFN=='iOS':self.findElement(self.btnAbout).click()
		version=self.findElement(self.eleVer[self.PFN],until='located').text.strip()
		if self.PFN=='iOS':self.driver.back()
		return version

	def textEnv(self):
		logging.info('获取当前服务器环境……')
		env=self.findElement(self.eleEnv[self.PFN]).text.strip()
		return env
		# return env.split('(')[-1][0:-1]

	def clickChangePwd(self):
		logging.info('点击 忘记/重置密码')
		self.findElement(self.btnChangePwd[self.PFN]).click()

