import logging,time
from selenium.webdriver.common.by import By

from .base import PageBase

class PageCamera(PageBase):
	def __init__(self,driver):
		# 相机拍照页面 页面
		super().__init__(driver)
		self.btnShutter=(By.ID,'com.android.camera2:id/shutter_button')#快门
		self.btnDone=(By.ID,'com.android.camera2:id/done_button')#选择

		self.btnShutter1=(By.ID,'com.huawei.camera:id/shutter_button')#快门
		self.btnDone1=(By.ID,'com.huawei.camera:id/done_button')#选择

	def clickShutter(self):
		logging.info('点击 拍照')
		try:
			self.findElement(self.btnShutter,screen=False).click()
		except AttributeError:
			self.findElement(self.btnShutter1,screen=False).click()

	def clickDone(self):
		logging.info('点击 选择')
		try:
			self.findElement(self.btnDone,screen=False).click()
		except AttributeError:		
			self.findElement(self.btnDone1,screen=False).click()

