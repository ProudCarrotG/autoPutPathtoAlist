# 需要上传的文件目录
FILES_PATH = ''

# 服务器是否支持https
ALIST_HTTPS = 0
# alist服务器地址
ALIST_SERVER = 'localhost'
# alist服务器端口
ALIST_PORT = '5244'

# 是否使用域名
USE_DOMAIN = 0
# alist服务器域名（应该可以写‘地址:端口'的形势（没测试过））
ALIST_DOMAIN = ''

# alist服务器的目标路径
ALIST_PATH = '\\'

# TOKEN的优先级更高
# 如果token为空,则尝试使用账号密码获取token
# 如果账号为空,则尝试使用空的token登录guest账号
ALIST_USERNAME = ''
ALIST_PASSWORD = ''
ALIST_TOKEN = ''

# 用户设置的超时时间，默认为None
# 如果不设置超时时间，当与服务器传输文件时服务器未响应，程序会一直等待服务器响应，可能会产生卡死
# USER_TIMEOUT = 10