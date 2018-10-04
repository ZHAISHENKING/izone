# Flask+VUE练手项目


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
