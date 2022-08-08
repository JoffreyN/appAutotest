from selenium.webdriver.common.touch_actions import TouchActions
# from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from HTMLReport import addImage
import traceback,time,logging
import socket,urllib3
from common.seleniumError import *
from common.tools import switch_execute,myAddScreen

from business.others import reOpenApp

class PageBase(object):
	def __init__(self,driver):
		self.driver=driver
		try:
			self.PFN=self.driver.capabilities['platformName']
		except KeyError:
			self.PFN='Android'

	def findElement(self,loc,screen=True,timeout=15,until='click'):
		try:
			if until=='click':
				WebDriverWait(self.driver,timeout,0.5).until(EC.element_to_be_clickable(loc))
			elif until=='located':
				WebDriverWait(self.driver,timeout,0.5).until(EC.presence_of_element_located(loc))
			return self.driver.find_element(*loc)
		except (SCETE,SCENSEE):
			msg=f'{self} 页面未找到 {loc} 元素'
			logging.error(msg)
			if screen:
				myAddScreen(self,msg)
				# try:self.driver.switch_to.context(self.driver.contexts[0])
				# except AttributeError:pass
				# logging.info(f'已切换为原生context')
				# addImage(self.driver.get_screenshot_as_base64(),msg,traceback.format_exc())
			return
		except (socket.timeout,urllib3.exceptions.ReadTimeoutError):
			reOpenApp(self.driver)
			raise Exception(f'{self} 页面发生timeout异常 元素 {loc} \n{traceback.format_exc()}')
		except:
			msg=f'{self} 页面发生其它异常 元素 {loc} \n{traceback.format_exc()}'
			logging.error(msg)
			if screen:
				myAddScreen(self,msg)
				# try:self.driver.switch_to.context(self.driver.contexts[0])
				# except AttributeError:pass
				# logging.info(f'已切换为原生context')
				# addImage(self.driver.get_screenshot_as_base64(),*msg.split('\n',1))
			return
 
	def findElements(self,loc,screen=True,timeout=15,until='click'):
		try:
			if until=='click':
				WebDriverWait(self.driver,timeout,0.5).until(EC.element_to_be_clickable(loc))
			elif until=='located':
				WebDriverWait(self.driver,timeout,0.5).until(EC.presence_of_element_located(loc))
			return self.driver.find_elements(*loc)
		except (SCETE,SCENSEE):
			msg=f'{self} 页面未找到 {loc} 元素'
			logging.error(msg)
			if screen:
				myAddScreen(self,msg)
				# try:self.driver.switch_to.context(self.driver.contexts[0])
				# except AttributeError:pass
				# logging.info(f'已切换为原生context')
				# addImage(self.driver.get_screenshot_as_base64(),msg,traceback.format_exc())
			return
		except (socket.timeout,urllib3.exceptions.ReadTimeoutError):
			reOpenApp(self.driver)
			raise Exception(f'{self} 页面发生timeout异常 元素 {loc} \n{traceback.format_exc()}')
		except:
			msg=f'{self} 页面发生其它异常 元素 {loc} \n{traceback.format_exc()}'
			logging.error(msg)
			if screen:
				myAddScreen(self,msg)
				# try:self.driver.switch_to.context(self.driver.contexts[0])
				# except AttributeError:pass
				# logging.info(f'已切换为原生context')
				# addImage(self.driver.get_screenshot_as_base64(),*msg.split('\n',1))
			return

	def myClick(self,msg,loc,until='click',scroll=0):
		logging.info(f'点击 {msg}')
		ele=self.findElement(loc,until=until)
		if scroll:
			self.driver.execute_script("arguments[0].scrollIntoView();",ele)
		ele.click()

	def myInput(self,msg,loc,value):
		logging.info(f'{msg}输入 {value}')
		self.findElement(loc).send_keys(value)

	# def myAddScreen
	def myTap(self,ele):
		TouchActions(self.driver).tap(ele).perform()

	def myDriverTap(self,xy,xy_size):
		# xy: 要点击的坐标, xy=[x,y]
		# xy_size: 获取该坐标时的设备分辨率大小 xy_size=(x_size,y_size)
		self.size=self.driver.get_window_size()
		self.width=self.size['width']
		self.height=self.size['height']
		self.driver.tap([((xy[0]/xy_size[0])*self.width,(xy[1]/xy_size[1])*self.height)])

	def clickByScript(self,ele):
		self.driver.execute_script("arguments[0].click();",ele)

	def scrollClick(self,ele):
		self.driver.execute_script("arguments[0].scrollIntoView();",ele)
		ele.click()

	def clickByEleXY(self,ele):
		x,y=ele.location.values()
		h,w=ele.size.values()
		# logging.info( x,y,h,w)
		self.driver.tap([(int(x+w/2),int(y+h/2))])

	@switch_execute
	def clickByRightXY(self,xy):
		oldSize=(414,896)
		newSize=tuple(self.driver.get_window_size().values())
		newX=int(round(newSize[0]/oldSize[0]*xy[0],0))
		newY=int(round(newSize[1]/oldSize[1]*xy[1],0))
		self.driver.tap([(newX,newY)])

	def setValue(self,loc,vaule,clearFirst=False,clickFirst=True):
		try:
			loc=getattr(self,f"_{loc}")
			if clickFirst:self.find_element(*loc).click()
			if clearFirst:self.find_element(*loc).clear()
			self.find_element(*loc).set_value(vaule)
		except AttributeError:
			logging.error(f'{self} 页面未找到 {loc} 元素\n{traceback.format_exc()}')

	def getToast(self,text=None,timeout=5):
		xpath=f"//*[contains(@text,'{text}')]" if text else '/hierarchy/android.widget.Toast'
		try:
			toast_loc=(By.XPATH,xpath)
			WebDriverWait(self.driver,timeout,0.1).until(EC.presence_of_element_located(toast_loc))
			toast=self.driver.find_element(*toast_loc).text
			logging.info(f'toast debug: {toast}')
			return toast
		except (SCETE,SCENSEE):
			logging.error(f'{self} 页面未找到toast {xpath} 元素')
			return
		except:
			logging.error(f'{self} 页面查找toast {xpath} 时发生其它异常\n{traceback.format_exc()}')
			return

	def isEleExists(self,loc,timeout=10,screen=0):
		try:
			WebDriverWait(self.driver,timeout,0.5).until(EC.presence_of_element_located(loc))
			if self.driver.find_element(*loc):return 1
			else:return 0
		except (SCETE,SCENSEE):
			msg=f'{self} 找不到元素 {loc}'
			logging.error(msg)
			if screen:myAddScreen(self,msg)
			# if screen:addImage(self.driver.get_screenshot_as_base64(),msg,traceback.format_exc())
			return 0
		except (socket.timeout,urllib3.exceptions.ReadTimeoutError):
			reOpenApp(self.driver)
			raise Exception(f'{self} 页面发生timeout异常 元素 {loc} \n{traceback.format_exc()}')
		except:
			logging.error(f'{self} 页面发生其它异常 元素 {loc} \n{traceback.format_exc()}')
			return 0

	def waitTo(self,ignoreError=(SCENSEE,SCEWDE),loc=None,operate='click',value='',timeout=10,account=None,reopen=False,screen=True):
		#ignoreError:要忽略的错误； account:超时后重置后重新登录
		if operate=='click':
			while timeout:
				try:
					self.driver.find_element(*loc).click()
					return
				except ignoreError:
					time.sleep(0.5)
					timeout-=0.5
					continue
				except:
					logging.error(traceback.format_exc())
		elif operate=='send_keys':
			while timeout:
				try:
					self.driver.find_element(*loc).send_keys(value)
					return
				except ignoreError:
					time.sleep(0.5)
					timeout-=0.5
					continue
				except:
					logging.error(traceback.format_exc())
		elif operate=='set_value':
			while timeout:
				try:
					self.driver.find_element(*loc).set_value(value)
					return
				except ignoreError:
					time.sleep(0.5)
					timeout-=0.5
					continue
				except:
					logging.error(traceback.format_exc())
		elif operate=='getText':
			while timeout:
				try:
					text=self.driver.find_element(*loc).text
					return text
				except ignoreError:
					time.sleep(0.5)
					timeout-=0.5
					continue
				except:
					logging.error(traceback.format_exc())
		elif operate=='getAttribute':
			while timeout:
				try:
					text=self.driver.find_element(*loc).get_attribute(value)
					return text
				except ignoreError:
					time.sleep(0.5)
					timeout-=0.5
					continue
				except:
					logging.error(traceback.format_exc())
		msg=f'{self} 无法找到元素 {loc}'
		logging.error(msg)
		if screen:
			try:
				self.driver.switch_to.context(self.driver.contexts[0])
				logging.info(f'已切换为原生context')
			except AttributeError:
				pass
			addImage(self.driver.get_screenshot_as_base64(),*msg.split('\n',1))
		if reopen:reOpenApp(self.driver)
		raise TimeoutError

	def driver_back(self):
		for i in range(5):
			try:
				self.driver.back()
				return
			except Exception as err:
				if i==4:raise err
				if hasattr(err, 'message'):
					errText=str(err.message)
				else:
					errText=str(err)
				if 'An unknown server-side error occurred while processing the command. Original error: Could not proxy. Proxy error: Could not proxy command to the remote server. Original error: timeout of 240000ms exceeded' in errText:
					reOpenApp(self.driver)

	def goBack(self,n=1,xy=0):
		if n==0:return
		# self.driver.switch_to.context(self.driver.contexts[0])
		# logging.info(f'已切换为原生context')
		if self.PFN!='iOS':
			for i in range(n):
				if xy:
					self.driver.tap([(80,150)])
				else:
					self.driver_back()
				time.sleep(0.5)
		else:
			for i in range(n):
				self.driver.tap([(30,66)])
				time.sleep(0.5)


