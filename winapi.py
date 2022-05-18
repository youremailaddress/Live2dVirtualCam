'''
 @Date: 2022-05-18 14:59:36
 @LastEditors: Wu Han
 @LastEditTime: 2022-05-19 03:05:44
 @FilePath: \test\winapi.py
'''
import win32gui
import win32con
import sys,os,subprocess
import time
import winreg,ctypes
from PIL import Image
import pyvirtualcam
import numpy as np
import d3dshot

def check_if_install_obs():
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "CLSID\{27B05C2D-93DC-474A-A5DA-9BBA34CB2A9C}\InprocServer32")
        return 1
    except FileNotFoundError:
        return 0

def install_obs():
    os.system("OBS-VirtualCam2.0.4-Installer.exe")

def run_app():
    subprocess.Popen(["python","app.py"])

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
# 电脑上只有前两个 后面的没测试过

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

if __name__ == "__main__":
    print("[Info] 检查是否安装 Obs-Virtual-Cam...")
    if not check_if_install_obs():
        print("[Warning] 找不到 Obs 设备.请先安装驱动")
        install_obs()
        print("[Info] Obs 安装成功")
    print("[Info] 是")
    print("[Info] 开始检查浏览器...")
    for browser in ["chrome","edge"]:
        path = get_browser_path(browser)
        if path != None:
            break
    if path == None:
        print("[Fatal] 找不到支持的浏览器！")
        exit(-1)
    print("[Info] 浏览器路径 {}".format(path))
    print("[Info] 开始 web 服务器...")
    run_app()
    time.sleep(1)
    print("[Info] 开始打开浏览器...")
    cmd = '"{}" --app="{}"'.format(path,"data:text/html,<html><body><script>window.moveTo(1980,700);window.resizeTo(500,500);window.location='http://127.0.0.1:8086';</script></body></html>")
    os.popen(cmd)
    print("[Info] 等待浏览器加载完成...")
    time.sleep(5)
    print("[Info] 浏览器加载完成...")
    hwnd_map = {}
    win32gui.EnumWindows(get_all_hwnd, 0)
    d = d3dshot.create()
    with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
        while True:
            try:
                for h, t in hwnd_map.items():
                    if t :
                        if 'ababa' in t:
                            win32gui.ShowWindow(h, win32con.SW_RESTORE)
                            win32gui.SetWindowPos(h, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                            win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                            (x1, y1, x2, y2) = get_window_rect(h)
                            img_ready = d.screenshot((x1+5, y1+50, x2-20, y2-20))
                            img_ready = resize(img_ready, cam.width, cam.height)
                            img_4 = img_ready.convert("RGBA")
                            img_4 = np.array(img_4,dtype=np.uint8)
                            cam.send(img_4)
                            cam.sleep_until_next_frame()
            except Exception as e:
                if isinstance(e,BaseException):
                    print("[Info] 窗口已关闭")
                    exit(0)
                pass
