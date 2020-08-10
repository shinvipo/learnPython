import pyautogui
import time

n = int(input())
time.sleep(10)
pyautogui.typewrite("Shin")
pyautogui.typewrite("\n")
pyautogui.typewrite("AutoType From 0 to ")
pyautogui.typewrite(str(n))
pyautogui.typewrite("\n")
for i in range(n):
	pyautogui.typewrite(str(i))
	pyautogui.typewrite("\n")
	time.sleep(1)
