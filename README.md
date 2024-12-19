<p align="center">
  <img src="https://socialify.git.ci/136478738/Nugget/image?description=1&descriptionEditable=ALLG%E6%B1%89%E5%8C%96&font=Bitter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Floating%20Cogs&pulls=1&stargazers=1&theme=Auto" alt="SparseBox"/> 
</p>

<br>汉化版本Nugget下载地址：<a href="https://nightly.link/136478738/Nugget/workflows/Build/main/artifact.zip"><img src="https://nightly.link/logo.svg" alt style="width: 20px;" /></a> [nightly.link](https://nightly.link/136478738/Nugget/workflows/Build/main/artifact.zip)

# Nugget 金块
Unlock your device's full potential!
<br>释放您设备的全部潜力！
<br>Sparserestore works on all versions iOS 17.0-18.2 developer beta 2. There is partial support for iOS 18.2 developer beta 3 and newer.
<br>Sparserestore 适用于所有版本的 iOS 17.0-18.2 开发者测试版 2。部分支持 iOS 18.2 开发者测试版 3 及更新版本。
<br>**Mobilegestalt and AI Enabler tweaks are not supported on iOS 18.2+.** It will never be supported, do not make issues asking for when it is supported.
<br>**iOS 18.2+ 不支持 Mobilegestalt 和 AI Enabler 调整。** 它永远不会被支持，不要再问了。
<br>Make sure you have installed the [requirements](#requirements) if you are on Windows or Linux.
<br>如果您使用的是 Windows 或 Linux，请确保已经安装了 [requirements](#requirements)。
<br>This uses the sparserestore exploit to write to files outside of the intended restore location, like mobilegestalt. Read the [Getting the File](#getting-the-file) section to learn how to get your mobilegestalt file.
<br>这利用了 sparserestore 漏洞来写入预期恢复位置之外的文件，例如 mobilegestalt。阅读 [Getting the File](#getting-the-file) 部分以了解如何获取 mobilegestalt 文件。
<br>Note: I am not responsible if your device bootloops. Please back up your data before using!
<br>注意：如果您的设备出现循环启动，我概不负责。请在使用前备份您的数据！
## Features 特征
### iOS 17.0+
- Enable Dynamic Island on any device 在任何设备上启用动态岛
- Enable iPhone X gestures on iPhone SEs 在 iPhone SE 上启用 iPhone X 手势
- Change Device Model Name (ie what shows in the Settings app) 更改设备型号名称（即“设置”应用中显示的名称）
- Enable Boot Chime 启用开机铃声
- Enable Charge Limit 启用充电限制
- Enable Tap to Wake on unsupported devices (ie iPhone SEs) 在不支持的设备（例如 iPhone SE）上启用“点击唤醒”
- Enable Collision SOS 启用碰撞 SOS
- Enable Stage Manager 启用阶段管理器 
- Disable the Wallpaper Parallax 禁用壁纸视差
- Disable Region Restrictions (ie. Shutter Sound) 禁用区域限制（例如快门声音）
  - Note: This does not include enabling EU sideloading outside the EU. That will come later. 注意：这不包括在欧盟以外启用欧盟侧载。这将在以后实现。
- Show the Apple Pencil options in Settings app 在“设置”应用中显示 Apple Pencil 选项
- Show the Action Button options in Settings app 在“设置”应用中显示“操作按钮”选项
- Show Internal Storage info (Might cause problems on some devices, use at your own risk) 显示内部存储信息（可能会导致某些设备出现问题，请自行承担风险）
- EU Enabler (iOS 17.6-) 欧盟侧载启动（iOS 17.6-）
- Springboard Options (from [Cowabunga Lite](https://github.com/leminlimez/CowabungaLite)) Springboard 选项（来自 [Cowabunga Lite](https://github.com/leminlimez/CowabungaLite)）
  - Set Lock Screen Footnote 设置锁定屏幕脚注
  - Disable Lock After Respring 重启后禁用锁定
  - Disable Screen Dimming While Charging 充电时禁用屏幕变暗
  - Disable Low Battery Alerts 禁用低电量警报
- Internal Options (from [Cowabunga Lite](https://github.com/leminlimez/CowabungaLite))内部选项（来自 [Cowabunga Lite](https://github.com/leminlimez/CowabungaLite)）
  - Build Version in Status Bar 状态栏中的版本
  - Force Right to Left 强制从右到左
  - Force Metal HUD Debug 强开Metal HUD调试
  - iMessage Diagnostics iMessage诊断
  - IDS Diagnostics IDS诊断
  - VC Diagnostics VC诊断
  - App Store Debug Gesture 应用商店调试手势
  - Notes App Debug Mode Notes应用调试模式
- Disable Daemons: 禁用守护进程：
  - OTAd 系统更新
  - UsageTrackingAgent 使用跟踪代理
  - Game Center 游戏中心
  - Screen Time Agent 屏幕时间代理
  - Logs, Dumps, and Crash Reports 日志、转储和崩溃报告
  - ATWAKEUP 醒来
  - Tipsd 尖端
  - VPN
  - Chinese WLAN service 中国 WLAN 服务
  - HealthKit 健康套件
- Risky (Hidden) Options: 风险（隐藏）选项：
  - Disable thermalmonitord 禁用温控
  - OTA Killer 杀死系统更新检测
  - Custom Resolution 自定义分辨率
### iOS 18.0+
- Enable iPhone 16 camera button page in the Settings app 在“设置”应用中启用 iPhone 16 相机按钮页面
- Enable AOD & AOD Vibrancy on any device 在任何设备上启用息屏显示和息屏显示动画
- Feature Flags (iOS 18.1b4-): 功能标志（iOS 18.1b4-）：
  - Enabling lock screen clock animation, lock screen page duplication button, and more! 启用锁屏时钟动画、锁屏页面复制按钮等！
  - Disabling the new iOS 18 Photos UI (iOS 18.0 betas only, unknown which patched it) 禁用新的 iOS 18 照片 UI（仅限 iOS 18.0 测试版，未知哪个修补了它）
### iOS 18.1+ 
- AI Enabler + Device Spoofing (fixed in iOS 18.2db3) AI启动+设备欺骗（已在 iOS 18.2db3 中修复）

## Requirements: 要求：
- **Windows:**
  - Either任何一个 [Apple Devices (from Microsoft Store)](https://apps.microsoft.com/detail/9np83lwlpz9k%3Fhl%3Den-US%26gl%3DUS&ved=2ahUKEwjE-svo7qyJAxWTlYkEHQpbH3oQFnoECBoQAQ&usg=AOvVaw0rZTXCFmRaHAifkEEu9tMI) app or应用程序或 [iTunes (from Apple website)](https://support.apple.com/en-us/106372)
- **Linux:**
  - [usbmuxd](https://github.com/libimobiledevice/usbmuxd) and和 [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice)

- **For Running Python: 对于运行 Python：**
  - pymobiledevice3
  - PySide6
  - Python 3.8 or newer

## Running the Python Program 运行 Python 程序
Note: It is highly recommended to use a virtual environment: 注意：强烈建议使用虚拟环境：
```
python3 -m venv .env # only needed once
# macOS/Linux:  source .env/bin/activate
# Windows:      .env/Scripts/activate.bat
pip3 install -r requirements.txt # only needed once
python3 main_app.py
```
Note: It may be either `python`/`pip` or `python3`/`pip3` depending on your path. 注意：根据您的路径，它可能是`python`/`pip`或`python3`/`pip3`。

The CLI version can be ran with `python3 cli_app.py`. CLI 版本可以使用`python3 cli_app.py`运行。

## Getting the File 获取文件
You need to get the mobilegestalt file that is specific to your device. To do that, follow these steps: 您需要获取特定于您设备的 mobilegestalt 文件。为此，请按照以下步骤操作：
1. Install the `Shortcuts` app from the iOS app store. 从 iOS 应用商店安装`快捷指令`应用程序。
2. Download this shortcut: https://www.icloud.com/shortcuts/d6f0a136ddda4714a80750512911c53b 下载此快捷指令：https://www.icloud.com/shortcuts/d6f0a136ddda4714a80750512911c53b
3. Save the file and share it to your computer. 保存文件并将其共享到您的计算机。
4. Place it in the same folder as the python file (or specify the path in the program) 放在和python文件同一文件夹下（或者在程序中指定路径）

## Building
To compile `mainwindow.ui` for Python, run the following command: 要为 Python 编译`mainwindow.ui`，请运行以下命令：
`pyside6-uic qt/mainwindow.ui -o qt/ui_mainwindow.py`

To compile the resources file for Python, run the following command: 要编译 Python 的资源文件，请运行以下命令：
`pyside6-rcc qt/resources.qrc -o resources_rc.py`

The application itself can be compiled by running `compile.py`. 应用程序本身可以通过运行`compile.py`来编译。

## Read More 阅读更多
If you would like to read more about the inner workings of the exploit and iOS restore system, I made a write up which you can read [here](https://gist.github.com/leminlimez/c602c067349140fe979410ef69d39c28). 如果你想了解更多有关漏洞利用和 iOS 恢复系统的内部工作原理，我写了一篇文章，你可以在[这里](https://gist.github.com/leminlimez/c602c067349140fe979410ef69d39c28)阅读。

## Credits 致谢
- [JJTech](https://github.com/JJTech0130) for Sparserestore/[TrollRestore](https://github.com/JJTech0130/TrollRestore)
- [disfordottie](https://x.com/disfordottie) for some global flag features
- [Mikasa-san](https://github.com/Mikasa-san) for [Quiet Daemon](https://github.com/Mikasa-san/QuietDaemon)
- [sneakyf1shy](https://github.com/f1shy-dev) for [AI Eligibility](https://gist.github.com/f1shy-dev/23b4a78dc283edd30ae2b2e6429129b5) (iOS 18.1 beta 4 and below)
- [lrdsnow](https://github.com/Lrdsnow) for [EU Enabler](https://github.com/Lrdsnow/EUEnabler)
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3) for restoring and device algorithms.
- [PySide6](https://doc.qt.io/qtforpython-6/) for the GUI library.
