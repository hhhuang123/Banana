# Banana

## 背景：
banana旨在创建一个类似于github contribution的win桌面端程序。目的在于记录使用电脑的时间，用于统计和对比近期的学习时间。
## 用法：
下载该文件，将exe文件创建桌面快捷方式，点击运行即可。
程序逻辑：
- 学习时间以每10分钟计数，按日计时，每日可累加。
- 学习时间越长，颜色越深。
- 鼠标移动到对应日期可显示当前日期及学习时间。
程序界面：
![image](https://github.com/hhhuang123/Banana/assets/48477626/5ff95101-e948-402a-9c90-03c6c2066365)

## 代码相关：
编译
```
pyinstaller --path pyQT6_package_path\site-packages\PyQt6\Qt6\bin -F -w --icon=xxx\Banana\images\banana.ico xxx\Banana\banana.py
```
