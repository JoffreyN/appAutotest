import logging,re
from selenium.webdriver.common.by import By

from page.base import PageBase

class PageLingpai(PageBase):
	def __init__(self,driver):
		# 令牌APP页面 解锁密码 1111
		super().__init__(driver)

		self.getLP={
			'Android':(By.XPATH,"//*[@text='{}']/../..//*[@text='获取令牌']"),
			'iOS':(By.IOS_PREDICATE,"name contains '获取令牌'")
		}
		self.unlock={
			'Android':(By.XPATH,"//*[@resource-id='com.cmbi.zylp:id/ppe_pwd']/android.widget.EditText[1]"),
			'iOS':(By.IOS_PREDICATE,"name contains ''")
		}
		self.token={
			'Android':(By.ID,"com.cmbi.zylp:id/token_code_view"),
			'iOS':(By.IOS_PREDICATE,"")
		}

	def getToken(self):
		logging.info('获取动态令牌')
		token=self.findElement(self.token[self.PFN]).text.strip()
		return token

	def clickGetLP(self,account):
		logging.info(f'{account} 点击 获取令牌')
		xpath=(self.getLP[self.PFN][0],self.getLP[self.PFN][1].format(account))
		self.findElement(xpath,until='located').click()

	def inputUnlockpwd(self):
		logging.info('输入令牌APP解锁密码')
		try:
			self.findElement(self.unlock[self.PFN],timeout=10).send_keys('1111')
		except:
			logging.info('无需输入令牌APP解锁密码')
			