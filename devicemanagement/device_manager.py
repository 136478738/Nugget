import traceback
import plistlib
from pathlib import Path

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QSettings

from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.exceptions import MuxException, PasswordRequiredError

from devicemanagement.constants import Device, Version
from devicemanagement.data_singleton import DataSingleton

from tweaks.tweaks import tweaks, FeatureFlagTweak, EligibilityTweak, AITweak, BasicPlistTweak, AdvancedPlistTweak, RdarFixTweak, NullifyFileTweak
from tweaks.custom_gestalt_tweaks import CustomGestaltTweaks
from tweaks.basic_plist_locations import FileLocationsList, RiskyFileLocationsList
from Sparserestore.restore import restore_files, FileToRestore

def show_error_msg(txt: str, detailed_txt: str = None):
    detailsBox = QMessageBox()
    detailsBox.setIcon(QMessageBox.Critical)
    detailsBox.setWindowTitle("错误!")
    detailsBox.setText(txt)
    if detailed_txt != None:
        detailsBox.setDetailedText(detailed_txt)
    detailsBox.exec()

def show_apply_error(e: Exception, update_label=lambda x: None):
    if "Find My" in str(e):
        show_error_msg("为了使用此工具，必须禁用“查找”。",
                       detailed_txt="从设置中禁用“查找我的”（设置 -> [您的姓名] -> 查找我的），然后重试。")
    elif "Encrypted Backup MDM" in str(e):
        show_error_msg("Nugget 无法在此设备上使用。点击“显示详细信息”可了解更多信息。",
                       detailed_txt="您的设备已受管理，并且 MDM 备份加密已开启。必须关闭此功能才能使 Nugget 正常工作。请不要在您的学校/工作设备上使用 Nugget！")
    elif "SessionInactive" in str(e):
        show_error_msg("会话已终止。请刷新设备列表并重试。")
    elif isinstance(e, PasswordRequiredError):
        show_error_msg("设备受密码保护！您必须信任设备上的计算机。",
                       detailed_txt="解锁您的设备。在弹出的窗口中，点击“信任”，输入您的密码，然后重试。")
    else:
        show_error_msg(type(e).__name__ + ": " + repr(e), detailed_txt=str(traceback.format_exc()))
    print(traceback.format_exc())
    update_label("恢复失败")

class DeviceManager:
    ## Class Functions
    def __init__(self):
        self.devices: list[Device] = []
        self.data_singleton = DataSingleton()
        self.current_device_index = 0

        # preferences
        # TODO: Move to its own class
        self.apply_over_wifi = False
        self.auto_reboot = True
        self.allow_risky_tweaks = False
        self.show_all_spoofable_models = False
        self.skip_setup = True
        self.supervised = False
        self.organization_name = ""
    
    def get_devices(self, settings: QSettings):
        self.devices.clear()
        # handle errors when failing to get connected devices
        try:
            connected_devices = usbmux.list_devices()
        except:
            show_error_msg(
                """
                无法获取设备列表。单击“显示详细信息”查看回溯。

                如果您使用的是 Windows，请确保您拥有来自 Microsoft Store 的iTunes应用程序或来自 Apple 网站的 iTunes。
                如果您使用的是 Linux，请确保已安装 usbmuxd 和 libimobiledevice。
                """, detailed_txt=str(traceback.format_exc())
            )
            self.set_current_device(index=None)
            return
        # Connect via usbmuxd
        for device in connected_devices:
            if self.apply_over_wifi or device.is_usb:
                try:
                    ld = create_using_usbmux(serial=device.serial)
                    vals = ld.all_values
                    model = vals['ProductType']
                    hardware = vals['HardwareModel']
                    cpu = vals['HardwarePlatform']
                    try:
                        product_type = settings.value(device.serial + "_model", "", type=str)
                        hardware_type = settings.value(device.serial + "_hardware", "", type=str)
                        cpu_type = settings.value(device.serial + "_cpu", "", type=str)
                        if product_type == "":
                            # save the new product type
                            settings.setValue(device.serial + "_model", model)
                        else:
                            model = product_type
                        if hardware_type == "":
                            # save the new hardware model
                            settings.setValue(device.serial + "_hardware", hardware)
                        else:
                            hardware = hardware_type
                        if cpu_type == "":
                            # save the new cpu model
                            settings.setValue(device.serial + "_cpu", cpu)
                        else:
                            cpu = cpu_type
                    except:
                        pass
                    dev = Device(
                            uuid=device.serial,
                            name=vals['DeviceName'],
                            version=vals['ProductVersion'],
                            build=vals['BuildVersion'],
                            model=model,
                            hardware=hardware,
                            cpu=cpu,
                            locale=ld.locale,
                            ld=ld
                        )
                    tweaks["RdarFix"].get_rdar_mode(model)
                    self.devices.append(dev)
                except MuxException as e:
                    # there is probably a cable issue
                    print(f"MUX ERROR with lockdown device with UUID {device.serial}")
                    show_error_msg("MuxException: " + repr(e) + "\n\nIf you keep receiving this error, try using a different cable or port.",
                                   detailed_txt=str(traceback.format_exc()))
                except Exception as e:
                    print(f"ERROR with lockdown device with UUID {device.serial}")
                    show_error_msg(type(e).__name__ + ": " + repr(e), detailed_txt=str(traceback.format_exc()))
        
        if len(self.devices) > 0:
            self.set_current_device(index=0)
        else:
            self.set_current_device(index=None)

    ## CURRENT DEVICE
    def set_current_device(self, index: int = None):
        if index == None or len(self.devices) == 0:
            self.data_singleton.current_device = None
            self.data_singleton.device_available = False
            self.data_singleton.gestalt_path = None
            self.current_device_index = 0
            tweaks["SpoofModel"].value[0] = "Placeholder"
            tweaks["SpoofHardware"].value[0] = "Placeholder"
            tweaks["SpoofCPU"].value[0] = "Placeholder"
        else:
            self.data_singleton.current_device = self.devices[index]
            if Version(self.devices[index].version) < Version("17.0"):
                self.data_singleton.device_available = False
                self.data_singleton.gestalt_path = None
            else:
                self.data_singleton.device_available = True
                tweaks["SpoofModel"].value[0] = self.data_singleton.current_device.model
                tweaks["SpoofHardware"].value[0] = self.data_singleton.current_device.hardware
                tweaks["SpoofCPU"].value[0] = self.data_singleton.current_device.cpu
            self.current_device_index = index
        
    def get_current_device_name(self) -> str:
        if self.data_singleton.current_device == None:
            return "未连接设备"
        else:
            return self.data_singleton.current_device.name
        
    def get_current_device_version(self) -> str:
        if self.data_singleton.current_device == None:
            return ""
        else:
            return self.data_singleton.current_device.version
    
    def get_current_device_build(self) -> str:
        if self.data_singleton.current_device == None:
            return ""
        else:
            return self.data_singleton.current_device.build
    
    def get_current_device_uuid(self) -> str:
        if self.data_singleton.current_device == None:
            return ""
        else:
            return self.data_singleton.current_device.uuid
        
    def get_current_device_model(self) -> str:
        if self.data_singleton.current_device == None:
            return ""
        else:
            return self.data_singleton.current_device.model
        
    def get_current_device_supported(self) -> bool:
        if self.data_singleton.current_device == None:
            return False
        else:
            return self.data_singleton.current_device.supported()
    
    def get_current_device_patched(self) -> bool:
        if self.data_singleton.current_device == None:
            return True
        else:
            return self.data_singleton.current_device.is_exploit_fully_patched()
        

    def reset_device_pairing(self):
        # first, unpair it
        if self.data_singleton.current_device == None:
            return
        self.data_singleton.current_device.ld.unpair()
        # next, pair it again
        self.data_singleton.current_device.ld.pair()
        QMessageBox.information(None, "配对重置", "您的设备配对已成功重置。请刷新设备列表后再应用。")
        

    def add_skip_setup(self, files_to_restore: list[FileToRestore], restoring_domains: bool):
        if self.skip_setup and (not self.get_current_device_supported() or restoring_domains):
            # add the 2 skip setup files
            cloud_config_plist: dict = {
                "SkipSetup": ["WiFi", "Location", "Restore", "SIMSetup", "Android", "AppleID", "IntendedUser", "TOS", "Siri", "ScreenTime", "Diagnostics", "SoftwareUpdate", "Passcode", "Biometric", "Payment", "Zoom", "DisplayTone", "MessagingActivationUsingPhoneNumber", "HomeButtonSensitivity", "CloudStorage", "ScreenSaver", "TapToSetup", "Keyboard", "PreferredLanguage", "SpokenLanguage", "WatchMigration", "OnBoarding", "TVProviderSignIn", "TVHomeScreenSync", "Privacy", "TVRoom", "iMessageAndFaceTime", "AppStore", "Safety", "Multitasking", "ActionButton", "TermsOfAddress", "AccessibilityAppearance", "Welcome", "Appearance", "RestoreCompleted", "UpdateCompleted"],
                "AllowPairing": True,
                "ConfigurationWasApplied": True,
                "CloudConfigurationUIComplete": True,
                "ConfigurationSource": 0,
                "PostSetupProfileWasInstalled": True,
                "IsSupervised": False,
            }
            if self.supervised == True:
                cloud_config_plist["IsSupervised"] = True
                cloud_config_plist["OrganizationName"] = self.organization_name
            files_to_restore.append(FileToRestore(
                contents=plistlib.dumps(cloud_config_plist),
                restore_path="Library/ConfigurationProfiles/CloudConfigurationDetails.plist",
                domain="SysSharedContainerDomain-systemgroup.com.apple.configurationprofiles"
            ))
            purplebuddy_plist: dict = {
                "SetupDone": True,
                "SetupFinishedAllSteps": True,
                "UserChoseLanguage": True
            }
            files_to_restore.append(FileToRestore(
                contents=plistlib.dumps(purplebuddy_plist),
                restore_path="mobile/com.apple.purplebuddy.plist",
                domain="ManagedPreferencesDomain"
            ))

    def get_domain_for_path(self, path: str, owner: int = 501) -> str:
        # returns Domain: str?, Path: str
        if self.get_current_device_supported() and not path.startswith("/var/mobile/") and not owner == 0:
            # don't do anything on sparserestore versions
            return path, None
        fully_patched = self.get_current_device_patched()
        # just make the Sys Containers to use the regular way (won't work for mga)
        sysSharedContainer = "SysSharedContainerDomain-"
        sysContainer = "SysContainerDomain-"
        if not fully_patched:
            sysSharedContainer += "."
            sysContainer += "."
        mappings: dict = {
            "/var/Managed Preferences/": "ManagedPreferencesDomain",
            "/var/root/": "RootDomain",
            "/var/preferences/": "SystemPreferencesDomain",
            "/var/MobileDevice/": "MobileDeviceDomain",
            "/var/mobile/": "HomeDomain",
            "/var/db/": "DatabaseDomain",
            "/var/containers/Shared/SystemGroup/": sysSharedContainer,
            "/var/containers/Data/SystemGroup/": sysContainer
        }
        for mapping in mappings.keys():
            if path.startswith(mapping):
                new_path = path.replace(mapping, "")
                new_domain = mappings[mapping]
                # if patched, include the next part of the path in the domain
                if fully_patched and (new_domain == sysSharedContainer or new_domain == sysContainer):
                    parts = new_path.split("/")
                    new_domain += parts[0]
                    new_path = new_path.replace(parts[0] + "/", "")
                return new_path, new_domain
        return path, None
    
    def concat_file(self, contents: str, path: str, files_to_restore: list[FileToRestore], owner: int = 501, group: int = 501):
        # TODO: try using inodes here instead
        file_path, domain = self.get_domain_for_path(path, owner=owner)
        files_to_restore.append(FileToRestore(
            contents=contents,
            restore_path=file_path,
            domain=domain,
            owner=owner, group=group
        ))
    
    ## APPLYING OR REMOVING TWEAKS AND RESTORING
    def apply_changes(self, resetting: bool = False, update_label=lambda x: None):
        # set the tweaks and apply
        # first open the file in read mode
        update_label("正在将更改应用于文件...")
        gestalt_plist = None
        if self.data_singleton.gestalt_path != None:
            with open(self.data_singleton.gestalt_path, 'rb') as in_fp:
                gestalt_plist = plistlib.load(in_fp)
        # create the other plists
        flag_plist: dict = {}
        eligibility_files = None
        ai_file = None
        basic_plists: dict = {}
        basic_plists_ownership: dict = {}
        files_data: dict = {}
        uses_domains: bool = False

        # set the plist keys
        if not resetting:
            for tweak_name in tweaks:
                tweak = tweaks[tweak_name]
                if isinstance(tweak, FeatureFlagTweak):
                    flag_plist = tweak.apply_tweak(flag_plist)
                elif isinstance(tweak, EligibilityTweak):
                    eligibility_files = tweak.apply_tweak()
                elif isinstance(tweak, AITweak):
                    ai_file = tweak.apply_tweak()
                elif isinstance(tweak, BasicPlistTweak) or isinstance(tweak, RdarFixTweak) or isinstance(tweak, AdvancedPlistTweak):
                    basic_plists = tweak.apply_tweak(basic_plists, self.allow_risky_tweaks)
                    basic_plists_ownership[tweak.file_location] = tweak.owner
                    if tweak.enabled and tweak.owner == 0:
                        uses_domains = True
                elif isinstance(tweak, NullifyFileTweak):
                    tweak.apply_tweak(files_data)
                    if tweak.enabled and tweak.file_location.value.startswith("/var/mobile/"):
                        uses_domains = True
                else:
                    if gestalt_plist != None:
                        gestalt_plist = tweak.apply_tweak(gestalt_plist)
                    elif tweak.enabled:
                        # no mobilegestalt file provided but applying mga tweaks, give warning
                        show_error_msg("未提供 mobilegestalt 文件！请选择您的文件以应用 mobilegestalt 调整。")
                        update_label("失败")
                        return
            # set the custom gestalt keys
            if gestalt_plist != None:
                gestalt_plist = CustomGestaltTweaks.apply_tweaks(gestalt_plist)
        
        gestalt_data = None
        if resetting:
            gestalt_data = b""
        elif gestalt_plist != None:
            gestalt_data = plistlib.dumps(gestalt_plist)
        
        # Generate backup
        update_label("正在生成备份...")
        # create the restore file list
        files_to_restore: dict[FileToRestore] = [
        ]
        self.concat_file(
            contents=plistlib.dumps(flag_plist),
            path="/var/preferences/FeatureFlags/Global.plist",
            files_to_restore=files_to_restore
        )
        self.add_skip_setup(files_to_restore, uses_domains)
        if gestalt_data != None:
            self.concat_file(
                contents=gestalt_data,
                path="/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/com.apple.MobileGestalt.plist",
                files_to_restore=files_to_restore
            )
        if eligibility_files:
            new_eligibility_files: dict[FileToRestore] = []
            if not self.get_current_device_supported():
                # update the files
                for file in eligibility_files:
                    self.concat_file(
                        contents=file.contents,
                        path=file.restore_path,
                        files_to_restore=new_eligibility_files
                    )
            else:
                new_eligibility_files = eligibility_files
            files_to_restore += new_eligibility_files
        if ai_file != None:
            self.concat_file(
                contents=ai_file.contents,
                path=ai_file.restore_path,
                files_to_restore=files_to_restore
            )
        for location, plist in basic_plists.items():
            ownership = basic_plists_ownership[location]
            self.concat_file(
                contents=plistlib.dumps(plist),
                path=location.value,
                files_to_restore=files_to_restore,
                owner=ownership, group=ownership
            )
        for location, data in files_data.items():
            self.concat_file(
                contents=data,
                path=location.value,
                files_to_restore=files_to_restore,
                owner=ownership, group=ownership
            )
        # reset basic tweaks
        if resetting:
            empty_data = plistlib.dumps({})
            for location in FileLocationsList:
                self.concat_file(
                    contents=empty_data,
                    path=location.value,
                    files_to_restore=files_to_restore
                )
            if self.allow_risky_tweaks:
                for location in RiskyFileLocationsList:
                    self.concat_file(
                        contents=empty_data,
                        path=location.value,
                        files_to_restore=files_to_restore
                    )

        # restore to the device
        update_label("正在恢复至设备...")
        try:
            restore_files(files=files_to_restore, reboot=self.auto_reboot, lockdown_client=self.data_singleton.current_device.ld)
            msg = "Your device will now restart."
            if not self.auto_reboot:
                msg = "请重新启动您的设备才能查看更改。"
            QMessageBox.information(None, "成功！", "全部完成！" + msg)
            update_label("成功！")
        except Exception as e:
            show_apply_error(e, update_label)

    ## RESETTING MOBILE GESTALT
    def reset_mobilegestalt(self, settings: QSettings, update_label=lambda x: None):
        # restore to the device
        update_label("正在恢复至设备...")
        try:
            # remove the saved device model, hardware, and cpu
            settings.setValue(self.data_singleton.current_device.uuid + "_model", "")
            settings.setValue(self.data_singleton.current_device.uuid + "_hardware", "")
            settings.setValue(self.data_singleton.current_device.uuid + "_cpu", "")
            file_path, domain = self.get_domain_for_path(
                "/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/com.apple.MobileGestalt.plist"
            )
            restore_files(files=[FileToRestore(
                    contents=b"",
                    restore_path=file_path,
                    domain=domain
                )], reboot=self.auto_reboot, lockdown_client=self.data_singleton.current_device.ld)
            msg = "您的设备现在将重新启动。"
            if not self.auto_reboot:
                msg = "请重新启动您的设备才能查看更改。"
            QMessageBox.information(None, "成功！", "全部完成！" + msg)
            update_label("成功！")
        except Exception as e:
            show_apply_error(e)
