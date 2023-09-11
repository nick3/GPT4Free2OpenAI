# 使用官方的Python 3基础镜像
FROM python:3

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖项
RUN pip install -r requirements.txt

# 设置环境变量来指定Flask运行的端口（将端口号设为变量）
ENV FLASK_RUN_PORT=8080

# 暴露容器的端口，可以与环境变量匹配
EXPOSE 8080

# 启动Flask应用
CMD ["flask", "run", "--host=0.0.0.0"]