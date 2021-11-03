# GO博客系统

# 目录结构
```
├── go.mod           
├── go.sum
├── README.md
├── common 日志等通用方法
│    ├── logmanage.go  // 日志管理
│    └── log.log // 日志记录
├── cmd    // 启动入口
│    ├── bootstrap.go  // 相关初始化
│    └── main.go // 启动入
├── configs     // 配置文件
│   └── config.yaml
└── internal    // 内部封装逻辑
    ├── conf    // 内部配置
    │   └── config.go
    ├── data    // 业务数据访问，类型 model层
    │   ├── sqlent //数据结构
    │   │     ├── log.go   //日志
    │   │     ├── permission.go //权限
    │   │     ├── posts.go //帖子
    │   │     ├── user.go //用户
    │   │     └── tab.go //标签
    │   ├── log.go //数据操作结构
    │   ├── permission.go
    │   ├── posts.go 
    │   ├── user.go 
    │   └── tab.go
    ├── biz     // 业务逻辑的组装层
    │   ├── posts.go 
    │   ├── user.go 
    │   └── tab.go
    ├──api  // api逻辑层
    │   ├── posts.go 
    │   ├── user.go 
    │   └── tab.go
    └── router.go  // 路由管理
```