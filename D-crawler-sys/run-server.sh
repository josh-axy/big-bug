source `dirname $0`/env.sh

# 开始启动
echo "server 运行目录： ${server_root_path}"
(cd ${server_root_path};python ./main.py)&
wait
