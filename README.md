# 使用说明

本程序使用 `python3` 爬取小说的每个章节，在本地生成 `Markdown` 文件，最终通过 `pandoc` 和 `kindlegen` 生成 `.mobi` 格式书籍

通过 `smtp` 推送至kindle

由于开发时间紧张，有些小地方还待改进，欢迎提出 `issue`

本程序暂时没有考虑GUI界面，适用于大部分Linux系统

（下载速度参考：20MB带宽，700章，40s，老机型）



# 特性

* 自动转换（可选 `mobi` `epub` 格式）（推荐选择 `mobi` 格式）
* 直接搜索
* 多线程下载 （默认 进程数 600）
* 可选章节（选择章节下载）
* 自动推送（在 `Config/config.py` 中配置）

# 安装

**Arch(Manjaro)** :

```bash
$ sudo pacman -S pandoc kindlegen
$ git clone https://github.com/AlessandroChen/KindleHelper.git
```

**Debian(Ubuntu)** :

```bash
$ sudo apt-get install pandoc kindlegen
$ git clone https://github.com/AlessandroChen/KindleHelper.git
```



# 运行

**请在 Config 文件夹下更改用户信息**，SMTP设置可以参照（参照[百度经验-QQ邮箱](https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html)）

```bash
$ mkdir book
$ cd book
# 请确保你在一个空文件夹下进行下载
$ python3 kindlehelper.py
# 运行下载小说，并自动转化推送
$ python3 kdpush <Filename>.mobi
# 如果你有想要推送的文件，也可以自动推送
```



# 预览

(随机下载的小说，侵删)



<img src="https://github.com/AlessandroChen/KindleHelper/blob/master/Preview/preview1.jpg" height = "250" div align=center/>

<img src="https://github.com/AlessandroChen/KindleHelper/blob/master/Preview/preview2.jpg" height = "250" div align=center/>



# Plan

- [x] 加速下载 (19.2.16) [lxml解析、多线程]

- [ ] 美化界面

- [ ] 详细Guide

- [ ] 多源下载

- [ ] 添加GUI界面

- [ ] 优化爬取

- [x] 一键搜索 (19.3.17) [优质源搜索，几乎无遗漏]

- [ ] 写Wiki

- [ ] 一键安装

# 待解决算法

* 章节一一对应  (19.3.17) [完成算法构思]


