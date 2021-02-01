须知：
1.yamlfiles\conf.yml中将ADB设备ID配置到ADBdevice，可以用adb devices查找
2.如果需要绑定用户yamlfiles\conf.yml需要正确添加用户UUID,已经选择登陆的方式和登陆的用户(可以仅选择登陆方式，其他默认)。
3.google配置可以支付的账号否则无法支付导致异常
4.文件放在英文路径下，运行双击中文路径下charpters\run.exe

使用说明：
1.用例配置:
\yamlfiles\yamlCase\casedatas.yml
根据自己的需要配置用例,配置规则参考casedatas.yml中的说明
2.弹框配置:
\yamlfiles\yamlCase\popup.yml
新弹框需要添加到此配置项中
3.小说配置:
\yamlfiles\yamlstory\yamlchat_typeconf.yml

报告：
1.报告目录：charpters\result\report中的html
2.录制文件目录：charpters\result\res
3.报告中log操作系统日志 mylog步骤日志


动态查看步骤日志:
1.charpters目录下的tail.exe放在C:\Windows\System32下
2.开启自动化后运行charpters\logView.bat

注意项：
1.要连接adb会弹出允许调试点允许否则无法连接设备
2.设备频繁连接adb可能回导致设备出现adb devcies offline状态需要重启USB调试并允许调试
3.阅读仅支持新存档不兼容老存档
4.模拟器概率无法使用录制功能
5.尽量保证模拟器的adb版本一致，拷贝airtestadb版本覆盖模拟器adb版本
