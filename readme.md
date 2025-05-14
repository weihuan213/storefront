# Django 电商平台

## 项目概述
这是一个基于Django框架构建的简易电商平台，包含商品展示、购物车管理、订单处理等核心功能。项目采用Django自带的用户认证系统，并包含完整的商品-订单业务逻辑。

## 主要功能

### 商品模块
- 商品详情展示（Product）
- SKU唯一标识管理
- 库存跟踪

### 购物车系统
- 登录用户专属购物车
- 商品添加/移除功能
- 价格快照（保留下单时价格）
- 订单总价自动计算

### 订单流程
- 购物车结算功能
- 简洁的结账页面
- 订单成功确认页

## 技术栈
- ​**核心框架**: Django 4.x+
- ​**数据库**: 默认SQLite（支持切换其他数据库）
- ​**用户认证**: Django内置认证系统
- ​**前端模板**: HTML模板驱动（模板路径：`shop/templates/shop/`）
- ​**交互特性**:
  - 外键关系（商品分类）
  - 模型属性计算（总价）
  - 查询优化（Q对象联合查询）

## 模型结构
```plaintext
User -> Order (1:N)
Order -> OrderItem (1:N)
Product <- OrderItem (1:N)
Category -> Product (1:N)

## 依赖环境

django
ppython

## 项目运行
运行命令 python manage.py runserver
