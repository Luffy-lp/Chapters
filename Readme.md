version1.6
须知：
1.检查yamlfiles\conf.yml的**号项目必须配置正确
2.保证google框架正常，支付等需要配置正常支付账号否则导致异常.
3.使用模拟器拷贝根目录下airtest\core\android\static\adb\windows中的全部内容覆盖到模拟器adb目录下
4.开启USB调试并勾选一直允许连接设备
5.resource目录下更换包,并在在yamlfiles\conf.yml\APKpackage 修改成对应的包名
6.部分手机的兼容性如果有问题请提单
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
1.一直提示still waiting for uiautomation ready;插件异常，卸载移动设备上的pocoservice和Yosemite。
2.error: cannot connect to daemon;无法连接到adb第一种情况，adb设备ID填写错误，填写正确即可。
3.error: cannot connect to daemon;无法连接到adb第二种情况，USB调试认证未开启，开启即可。
4.error: cannot connect to daemon;无法连接到adb第三种情况，频繁连接导致拒绝，尝试重启模拟器。
3.conf中用户ID未填写正确会导致无法阅读