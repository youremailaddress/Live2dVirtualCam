'''
 @Date: 2022-05-18 14:59:36
 @LastEditors: Wu Han
 @LastEditTime: 2022-05-18 22:19:22
 @FilePath: \test\test.py
'''
import win32gui
import win32con
import win32com.client
def get_all_hwnd(hwnd, mouse):
        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            AC_cycle_uefi.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    
def set_KVM_window_top():
    try:
        win32gui.EnumWindows(AC_cycle_uefi.get_all_hwnd, 0)
        handle=""
        for h, t in AC_cycle_uefi.hwnd_title.items():
            if t:
                if "ababa" in t:
                    handle =  t
                    print("{} {}".format(h,t))
        # 置顶窗口
        logger.write("Set window on the top",handle)
        hwnd = win32gui.FindWindow(None, handle)
        # hwnd = win32gui.FindWindow('xx.exe', None)
        # 窗口需要正常大小且在后台，不能最小化
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        # 窗口需要最大化且在后台，不能最小化
        # ctypes.windll.user32.ShowWindow(hwnd, 3)
        # win32gui.SetForegroundWindow(hwnd)
        #
        # win32gui.SetActiveWindow(hwnd)
        # win32gui.SetForegroundWindow(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)


    except Exception as e:
        print(str(e))

set_KVM_window_top()