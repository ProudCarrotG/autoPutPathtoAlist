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

# 文件冲突处理方法（遇到重复文件时的处理方法）
# 0：每个文件单独询问（默认）
# 1：跳过该文件（速度最快）
# 2：删除alist同名文件，重新上传文件
# 3：对比alist文件与本地文件的大小，若大小相同则跳过，不相同则删除alist文件，重新上传
# 4：强行上传（新上传的文件会由alist自动命名，文件名可能会出现多个后缀或（2）的情况，不建议使用
CONFLICT_SOLUTION: 0
