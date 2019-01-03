#!/bin/sh
# author:师
# date: 2019.1.3

# 代码提交
izoneCommit(){
  echo "--------函数开始执行----------"
  cd /Users/mac/WebstormProjects/frontend/izone
  git pull origin master && echo "拉取成功"
  npm run build
  sleep 5
  cd /Users/mac/PycharmProjects/flask/izone
  rm -rf dist/
  cp -R /Users/mac/WebstormProjects/frontend/izone/dist ./
  echo "拷贝成功"
  echo "-----准备提交-----"
  echo "请输入注释："
  read a
  git add .
  git commit -m $a
  echo "git 提交注释：$1"
  git push origin master
  echo "-----提交结束-----"
  echo "--------函数执行结束----------"

}

izoneCommit
