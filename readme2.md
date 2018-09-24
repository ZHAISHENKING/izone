# Flask+Vue快速打造个人网站（二）

> 2018.9.17 23:09

### 后端

后端框架使用flask考虑的是前后端分离，可以快速开发API，还有就是以前写的一些代码直接复用

在接口这块其实都差不多，主要来讲项目的模块化划分		

`模块化项目`是为了使代码更加清晰、可复用、低耦合，与django不同的是，前期使用flask时在github撸了很多demo，发现大部分项目结构都不同，各有各的分法。

```bash
# 模块化想法
models数据模型、routes全局路由、config全局配置、 一个启动文件、一个app初始化文件、utils外部方法包
```

<img src="http://qiniu.s001.xin/zbpbb.jpg" width="250">

模块化划分好之后,就是一些`外部库的用法`

- Flask-admin
- flask-migrate
- Flask-BabelEx
- Flask-Cors
- Flask-login
- Flask-restful
- Flask-script
- Flask-sqlalchemy
- blueprint

