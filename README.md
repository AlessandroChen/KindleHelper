# 使用说明

本程序使用 `python3` 爬取小说的每个章节，在本地生成 `Markdown` 文件，最终通过 `pandoc` 和 `kindlegen` 生成 `.mobi` 格式书籍

由于开发时间紧张，有些小地方还待改进，欢迎提出 `issue`

本程序暂时没有考虑GUI界面，适用于大部分Linux系统



# 特性

* 自动转换（可选 `mobi` `epub` 格式）
* 可选章节（选择章节下载）
* 自动推送（在 `Config/config.py` 中配置）



# 预览

(随机下载的小说，侵删)



<img src="https://github.com/AlessandroChen/KindleHelper/blob/master/preview1.jpg" height = "250" div align=center/>

<img src="https://github.com/AlessandroChen/KindleHelper/blob/master/preview2.jpg" height = "250" div align=center/>

# 安装

**Arch(Manjaro)** :

  ```bash
$ pacman -S pandoc kindlegen
$ git clone https://github.com/AlessandroChen/KindleHelper.git
  ```

**Debian(Ubuntu)** :

```bash
$ apt-get install pandoc kindlegen
$ git clone https://github.com/AlessandroChen/KindleHelper.git
```



# Plan

* 加速下载
* 美化界面
* 详细Guide
* 多源下载
* 添加GUI界面
* 优化爬取
* 一键搜索
* 写Wiki

