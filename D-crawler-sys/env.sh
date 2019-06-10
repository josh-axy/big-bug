# host IP 应该设置成公网IP
export host="localhost"

# 本地IP
export localhost="localhost"

# 项目根目录
export project_root_path=`(cd $(dirname $0);pwd)`

# server 根目录
export server_root_path="${project_root_path}/server"

# crawler 根目录
export crawler_root_path="${project_root_path}/crawler"
# webdriver 路径
export webdriver_path="${crawler_root_path}/geckodriver"

# config 根目录
export config_root_path="${project_root_path}/config"
