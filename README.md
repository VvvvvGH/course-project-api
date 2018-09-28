# 说明
这是为了课程项目写的一个简单API，代码非常糟糕。
# TODO
- [ ] **框架搭建**
    - [x] 管理Manager
    - [x] 配置Config
    - [x] 项目
        - [x] Swagger文档
        - [x] API示例
        - [x] 数据库连接 
        - [x] 错误处理
    - [x] 用户
        - [x] 视图函数
        - [x] 数据库模型
        - [x] 数据库迁移
        - [ ] 测试
    - [x] 邮件
        - [x] 邮件服务
        - [x] 用户激活
        - [x] 密码重置
    - [ ] 单元测试
    


# 部署
部署将用到
+ gunicorn
+ supervisor

启动选项参考
'''
gunicorn -w 4 -b IP:PORT -k gevent wsgi:api
'''
