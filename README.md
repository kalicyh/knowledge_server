# knowledge_backend
 知识库后端-基于fastapi+vue

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

### 生产环境下编译和压缩
```
yarn build
```

### 代码检查并自动修复
```
yarn lint
```

### 自定义配置
请参见 [配置参考](https://cli.vuejs.org/config/)。