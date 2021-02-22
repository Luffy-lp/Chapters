version1.6
须知：
1.检查yamlfiles\conf.yml的**号项目必须配置正确
2.保证google框架正常，支付等需要配置正常支付账号否则导致异常.
3.使用模拟器拷贝根目录下airtest\core\android\static\adb\windows中的全部内容覆盖到模拟器adb目录下
4.开启USB调试并勾选一直允许连接设备
5.尽量使用手机mobileconf.yml中
包放在英文路径下双击根目录下的run.exe

目录说明：
1.用例配置:\yamlfiles\yamlCase\casedatas.yml
2.弹框配置:\yamlfiles\yamlCase\popup.yml
3.小说配置:\yamlfiles\yamlstory\yamlchat_typeconf.yml
4.报告目录：result\repor
5.录制文件目录：result\res

注意项：
1.阅读仅支持新存档不兼容老存档
2.模拟器不会有录制文件

常见问题：
1.一直提示still waiting for uiautomation ready;频繁操作导致插件异常，卸载移动设备上的pocoservice和Yosemite
2.sockect或者adb连接中断;检查adb是否连接正常或者游戏未启动。
3.conf中用户ID未填写正确会导致无法阅读