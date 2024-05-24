import time

import pyautogui
from selenium import webdriver
import tkinter as tk

root=tk.Tk()
root.title('监狱-兴义')
root.geometry('1000x800')
root.resizable(False,False)


#提示语
tk.Label(root,text='使用分辨率:1920*1080').place(x=10,y=10)

#登录
def login():
    coption = webdriver.ChromeOptions()
    coption.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://192.168.1.253/SmartSecurity/login')
    time.sleep(5)
    pyautogui.moveTo(951,487)
    pyautogui.click()
    pyautogui.typewrite('5229455',interval=0.25)
    pyautogui.moveTo(967,950)
    pyautogui.click()
    pyautogui.typewrite('Admin@123',interval=0.25)
    pyautogui.click(969,698)
    time.sleep(5)
    driver.quit()


# 按钮-登录
btn_login=tk.Button(root,text='登录',height=1, width=8,command=lambda :login())
btn_login.place(x=10,y=40)

# 提示语 - 综合安防平台
tk.Label(root,text='综合安防平台').place(x=10,y=70)

# 功能-综合安防平台-各菜单点击
def allclick():
    coption= webdriver.ChromeOptions()
    coption.add_experimental_option('excludeSwitches',['enable-automation'])
    driver=webdriver.Chrome(options=coption)
    driver.maximize_window()
    driver.get('http://192.168.1.253/SmartSecurity/login')
    time.sleep(5)
    pyautogui.moveTo(951,487)
    pyautogui.click()
    pyautogui.typewrite('5229455', interval=0.25)
    pyautogui.moveTo(970, 590)
    pyautogui.click()
    pyautogui.typewrite('Admin@123', interval=0.25)
    pyautogui.click(969,698)
    time.sleep(5)
    pyautogui.moveTo(532,144)
    pyautogui.click()
    time.sleep(3)
    pyautogui.moveTo(684,149)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(851,147)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(1020,152)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(1182,149)
    pyautogui.click()
    time.sleep(5)
    driver.quit()

#按钮-综合安防平台-各菜单点击
btn_allclick=tk.Button(root,text='菜单按钮点击',height=1, width=10,command=lambda :allclick())
btn_allclick.place(x=10,y=100)

#功能 -警情中心
def plcenter():
    coption = webdriver.ChromeOptions()
    coption.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=coption)
    driver.maximize_window()
    driver.get('http://192.168.1.253/SmartSecurity/login')
    time.sleep(5)
    pyautogui.moveTo(951, 487)
    pyautogui.click()
    pyautogui.typewrite('5229455', interval=0.25)
    pyautogui.moveTo(970, 590)
    pyautogui.click()
    pyautogui.typewrite('Admin@123', interval=0.25)
    pyautogui.click(969, 698)
    time.sleep(8)
    pyautogui.moveTo(700,150)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(1761,377)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(534,963)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(518,963)
    pyautogui.click()
    pyautogui.moveTo(500,749)
    pyautogui.click()
    time.sleep(3)
    pyautogui.moveTo(434,825)
    pyautogui.click()
    pyautogui.typewrite('已处置',interval=0.25)
    time.sleep(5)
    driver.quit()



#按钮 -警情中心
btn_plcenter=tk.Button(root,text='警情中心',height=1, width=10,command=lambda :plcenter())
btn_plcenter.place(x=100,y=100)




root.mainloop()