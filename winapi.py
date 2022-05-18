'''
 @Date: 2022-05-18 14:59:36
 @LastEditors: Wu Han
 @LastEditTime: 2022-05-18 20:19:37
 @FilePath: \test\winapi.py
'''
import win32gui
import win32con
import win32com.client
import keyboard,sys,os,subprocess
import time
import winreg,ctypes
from PIL import Image, ImageGrab
import pyvirtualcam
import numpy as np

def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd) and
        win32gui.IsWindowEnabled(hwnd) and
        win32gui.IsWindowVisible(hwnd)):
        hwnd_map.update({hwnd: win32gui.GetWindowText(hwnd)})

_browser_regs = {
    'chrome': r"SOFTWARE\Clients\StartMenuInternet\Google Chrome\DefaultIcon",
    'edge': r"SOFTWARE\Clients\StartMenuInternet\Microsoft Edge\DefaultIcon",
    'firefox': r"SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon",
    '360': r"SOFTWARE\Clients\StartMenuInternet\360Chrome\DefaultIcon",
    'IE': r"SOFTWARE\Clients\StartMenuInternet\IEXPLORE.EXE\DefaultIcon",
}

def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom

def get_browser_path(browser):
    """
    获取浏览器的安装路径
    :param browser: 浏览器名称
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _browser_regs[browser])
    except FileNotFoundError:
        return None
    value, _type = winreg.QueryValueEx(key, "")
    return value.split(',')[0]

for browser in ["chrome","edge","firefox","360","IE"]:
    path = get_browser_path(browser)
    if path != None:
        break
if path == None:
    print("No browser found!")
    exit(-1)

cmd = '"{}" --app="{}"'.format(path,"data:text/html,<html><body><script>window.moveTo(1980,700);window.resizeTo(500,500);window.location='http://127.0.0.1:8086';</script></body></html>")
os.popen(cmd)

def resize(image_pil, width, height):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')

def m():
    os.popen('taskkill.exe /F /pid:'+str(os.getpid()))

keyboard.add_hotkey("ctrl + alt + space", m)
with pyvirtualcam.Camera(width=1280, height=720, fps=20) as cam:
    while True:
        try:
            hwnd_map = {}
            win32gui.EnumWindows(get_all_hwnd, 0)
            for h, t in hwnd_map.items():
                if t :
                    if 'ababa' in t:
                        # h 为想要放到最前面的窗口句柄
                        win32gui.BringWindowToTop(h)
                        shell = win32com.client.Dispatch("WScript.Shell")
                        shell.SendKeys('%')
                        # 被其他窗口遮挡，调用后放到最前面
                        win32gui.SetForegroundWindow(h)
                        # 解决被最小化的情况
                        win32gui.ShowWindow(h, win32con.SW_RESTORE)
                        (x1, y1, x2, y2) = get_window_rect(h)
                        img_ready = ImageGrab.grab((x1+5, y1+50, x2-20, y2-20))
                        # img_ready = img_ready.transpose(Image.FLIP_LEFT_RIGHT)
                        img_ready = resize(img_ready, cam.width, cam.height)
                        img_4 = img_ready.convert("RGBA")
                        img_4 = np.array(img_4,dtype=np.uint8)
                        cam.send(img_4)
                        cam.sleep_until_next_frame()
        except Exception as e:
            print(str(e))
            pass
        # time.sleep(1/60)
        