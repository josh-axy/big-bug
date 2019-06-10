source `dirname $0`/env.sh

# 开始启动
echo "crawler 运行目录： ${crawler_root_path}"
(cd ${crawler_root_path};python ./test.py)&
wait
