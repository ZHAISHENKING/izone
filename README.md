# Flask+VUE练手项目

### 前端页面

> v1 https://github.com/ZHAISHENKING/izone-frontend     
> 功能：图片视频展示，俄罗斯方块小游戏  
> 主要练习vue-cli搭建基础项目，elementUI组件库常用组件使用（表单，模态框，表格，列表等） 

> v2 https://github.com/ZHAISHENKING/izone-vue    
> 功能：图片上传组件，头像裁剪组件，登录注册功能     
> 主要练习vue计算属性，vuex的使用及各种组件传值方法，如：v-on事件+$emit，:props传值，$panrents访问父实例

### 后端接口

> https://github.com/ZHAISHENKING/izone


### 说明
项目功能是 上传图片视频并分类展示		
图床使用的是七牛云，可自行注册并开通内容存储		
项目未上传本地配置常量文件
`local_settings.py`
内容如下
```python
QINIU_AK = 'ak'
QINIU_SK = 'sk'
QINIU_BUCKET = '七牛云存储镜像'
QINIU_DOMAIN = '七牛云存储域名'
TMP_FILE_NAME = 'clipboard.png'
SQLPWD = "mysql的密码"

```

### 项目使用
首先创建一个数据库名为 `izone`
```bash
git pull ...
pip install -r req.txt
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
# 如果以上都没有问题
python manage.py runserver
```


