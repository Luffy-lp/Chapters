须知：
1.支持的设备三星平板S5E，和MUMU模拟器（1080*1920以及16：9分辨率）
2.绑定用户尽量设置仅一个Google用户，图库中最少有需要一个图片。确认开启图库权限。
3.如果要绑定用户需要填写uuid，并安装Google和翻墙网络
4.要连接adb会弹出允许调试点允许否则无法连接设备

使用步骤：
1.配置用例:
charpters\yamlfiles\yamlCase\casedatas.yml
根据需求定制用例
2.配置大厅弹框:
 charpters\yamlfiles\yamlCase\popup.yml
检查大厅弹框需要时间，根据实际弹框情况配置，但不配置遇到对应的弹框将无法处理只能手动点
3.配置运行环境:
charpters\yamlfiles\conf.yml
ADBdevice uuid必配

文件放在英文路径下，运行双击中文路径下charpters\run.exe

报告：
1.报告目录：charpters\result\report中的html
2.录制文件目录：charpters\result\res
3.报告中log操作系统日志 mylog步骤日志


动态查看步骤日志:
1.charpters目录下的tail.exe放在C:\Windows\System32下
2.开启自动化后运行charpters\logView.bat