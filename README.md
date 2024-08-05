# knowledge_server
 知识库后端-基于fastapi+vue

[前端地址](https://github.com/kalicyh/knowledge_client)

用于果之都项目的语料库，便于复制粘贴

## Docker 部署

### 配置

```sh
cp docker-compose.yml.example docker-compose.yml
```

修改`DATABASE_URL`

### 运行

```sh
docker-compose up -d
```

## 项目设置
```
yarn setup
```

### 开发环境下编译和热重载
```
yarn dev
```

### 开发环境下编译测试
```
yarn test
```

### 代码检查并自动修复
```
yarn lint
```

## 项目结构

```sh
.
├── Dockerfile                          # Docker 配置文件，用于创建 Docker 镜像
├── README.md                           # 项目说明文档
├── api                                 # 后端代码目录
│   ├── __init__.py                     # 初始化模块
│   ├── __pycache__                     # Python 字节码缓存目录
│   │   ├── __init__.cpython-312.pyc    # 编译后的 __init__.py 文件
│   │   ├── crud.cpython-312.pyc        # 编译后的 crud.py 文件
│   │   ├── database.cpython-312.pyc    # 编译后的 database.py 文件
│   │   └── main.cpython-312.pyc        # 编译后的 main.py 文件
│   ├── crud.py                         # 数据库操作相关代码
│   ├── database.py                     # 数据库模型和连接配置
│   ├── main.py                         # FastAPI 应用主文件
│   └── routes                          # 路由文件目录
│       ├── moments.py                  # 处理与 moments 相关的路由
│       └── talking_points.py           # 处理与 talking_points 相关的路由
├── babel.config.js                     # Babel 配置文件，用于 JavaScript 转译
├── dist                                # 编译后的前端资源目录
│   ├── css                             # CSS 文件目录
│   │   └── app.0ad5bad0.css            # 编译后的 CSS 文件
│   ├── favicon.ico                     # 网站图标
│   ├── index.html                      # 主页 HTML 文件
│   └── js                              # JavaScript 文件目录
│       ├── app.212486b0.js             # 编译后的 JavaScript 文件
│       ├── app.212486b0.js.map         # JavaScript 源映射文件
│       ├── chunk-vendors.d6172196.js   # 供应商代码的编译文件
│       └── chunk-vendors.d6172196.js.map # 供应商代码的源映射文件
├── docker-compose.yml                  # Docker Compose 配置文件
├── docker-compose.yml.example          # Docker Compose 配置文件示例
├── jsconfig.json                       # JavaScript 配置文件
├── package.json                        # Node.js 依赖管理文件
├── poetry.lock                         # Poetry 锁定的依赖文件
├── public                              # 静态文件目录
│   ├── favicon.ico                     # 网站图标
│   └── index.html                      # 主页 HTML 文件
├── pyproject.toml                      # Python 项目配置文件（Poetry）
├── src                                 # 前端源代码目录
│   ├── App.vue                         # 主 Vue 组件
│   ├── assets                          # 静态资源目录
│   │   └── logo.png                    # 项目 logo 图片
│   ├── components                      # Vue 组件目录
│   │   └── ExcelUploader.vue           # Excel 文件上传组件
│   └── main.js                         # Vue 应用入口文件
├── tests                               # 测试代码目录
│   └── __init__.py                     # 初始化测试模块
├── vue.config.js                       # Vue 配置文件
└── yarn.lock                           # Yarn 锁定的依赖文件

```


### 打印项目结构
```sh
tree -L 3 --prune -I 'node_modules'
```
