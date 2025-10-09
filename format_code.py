import re

def format_code_block(text_block):
    # 定义正则表达式，匹配以 `code` 开头的标识符
    pattern = r'(\s*)(code\w*)'  # 捕获前缀空格或制表符和 code 开头的单词

    def replace_code(match):
        prefix = match.group(1)  # 获取前缀空格或制表符
        code_word = match.group(2)  # 获取以 code 开头的单词

        # 将 code_word 转为首字母大写
        formatted_code = '_'.join([word.capitalize() for word in code_word.split('_')])

        return f"{prefix}{formatted_code}"  # 拼接前缀和格式化后的单词

    # 使用 re.sub() 对文本块进行替换
    formatted_text_block = re.sub(pattern, replace_code, text_block, flags=re.IGNORECASE)

    return formatted_text_block

# 示例文本块
text_block = """
    CODE_SUCCESS = 0

    CODE_SYSTEM_ERROR = 10000             # 后台系统错误

    # 以1开头，系统级别错误，客户端程序员关注
    CODE_INVALID_TOKEN = 10001
    CODE_PARAMETER_CHOICES_ERROR = 10002  # 参数选择错误
    CODE_PARAMETER_REQUIRED = 10003       # 必要参数缺失
    CODE_PARAMETER_FORMAT_ERROR = 10004   # 参数格式不正确
    CODE_INVALID_DIGEST = 10005
    CODE_PARAMETER_LIMIT_ERROR = 10006    # 参数不在限制的范围内
    CODE_USER_ACCOUNT_INCORRECT = 10007   # 帐号验证不正确
    CODE_USER_NOT_ADMIN_ROLE = 10008  # 非管理员用户


    # 以30开头，例如：APPLICATION 错误，需要 end_user 程序员关注
    CODE_CLIENT_TOKEN_MISSING = 30001
    CODE_CLIENT_TOKEN_INVALID = 30002
    CODE_CLIENT_TOKEN_EXPIRED = 30003

    # 以31开头，需要客户端程序要制定友好的信息反馈给用户
    CODE_USER_NOT_EXIST = 31001
    CODE_ROLE_NOT_EXIST = 33001
    CODE_ROLE_EXIST = 33002
    CODE_ROLE_ALREADY_DELETED = 33003
    CODE_DOC_NOT_EXIST = 33001
    CODE_DOC_EXIST = 33002
    CODE_DOC_ALREADY_DELETED = 33003
    CODE_ROLE_DISABLED_USER_CANNOT_ENABLED = 33004
    CODE_ROLE_ALREADY_ENABLED_CANNOT_DELETE = 33005
    CODE_MENU_PARENT_DISABLED = 33006
    CODE_USER_ALREADY_ENABLED_CANNOT_DELETE = 33007
    CODE_AGENT_USER_CANNOT_DELETED = 33008

    CODE_PASSWD_ERROR = 31002
    CODE_AUTH_ERROR = 35001
    CODE_GET_VCODE_FREQUENTLY = 31003
    CODE_BINDING_PHONE_EXCCEED = 31004
    CODE_VCODE_ERROR = 31005
    CODE_SMS_FAIL = 31007
    CODE_FILE_NOT_FOUND = 31009
    CODE_PAY_EXPIRED = 31010
    CODE_VCODE_INVALID = 31011
    CODE_USER_EXIST = 31012
    CODE_ACTIVE_USER_NOT_EXIST = 31014
    CODE_FREEZE_USER_NOT_EXIST = 31015
    CODE_SMS_SEND_FAILED = 31017
    CODE_PHONE_NUMBER_INVALID = 31018
    CODE_CRM_ORDER_ID_INVALID = 32001

    CODE_NOT_REGISTED = 41000

    CODE_OBJ_NOT_EXIST = 50001
    CODE_OBJ_EXIST = 50002

    CODE_OTHER = 90000

    CODE_MSG_MAP = {
        CODE_SYSTEM_ERROR: 'Backend System error',
        CODE_INVALID_TOKEN: 'Invalid token',
        CODE_INVALID_DIGEST: 'Illegal request. Digest error',
        CODE_USER_ACCOUNT_INCORRECT: u'Invalid user account',
        CODE_USER_NOT_ADMIN_ROLE: u'The user not admin',

        CODE_CLIENT_TOKEN_MISSING: 'Miss token in request header',
        CODE_CLIENT_TOKEN_INVALID: 'The application token is invalid',
        CODE_CLIENT_TOKEN_EXPIRED: 'The application token was expired',

        CODE_USER_NOT_EXIST: 'User not exist',
        CODE_ROLE_NOT_EXIST: 'Role not exist',
        CODE_ROLE_DISABLED_USER_CANNOT_ENABLED: 'Cannot be activated. Cause the role has been disabled.',
        CODE_ROLE_ALREADY_ENABLED_CANNOT_DELETE: 'Role already enabled cannot be deleted.',
        CODE_USER_ALREADY_ENABLED_CANNOT_DELETE: 'User already enabled cannot be deleted.',
        CODE_AGENT_USER_CANNOT_DELETED: 'The Agent-User cannot be deleted.',
        CODE_MENU_PARENT_DISABLED: 'The parent_id menu [{0[parent_menu]}] has been disabled, Setting failed.',
        CODE_ROLE_EXIST: 'Role already exist',
        CODE_ROLE_ALREADY_DELETED: 'Role already deleted',
        CODE_DOC_NOT_EXIST: 'Record not exist',
        CODE_DOC_EXIST: 'Record already exist',
        CODE_DOC_ALREADY_DELETED: 'Record already deleted',
        CODE_PASSWD_ERROR: 'Password error',
        CODE_AUTH_ERROR: u'authenticate failed, recognize user',
        CODE_GET_VCODE_FREQUENTLY: 'Sending sms frequently',
        CODE_BINDING_PHONE_EXCCEED: 'The same phone exceeded',
        CODE_VCODE_ERROR: 'Validate code is error',
        CODE_SMS_FAIL: 'Sms sending failed. Try to check third party service',
        CODE_FILE_NOT_FOUND: 'File not found',
        CODE_PAY_EXPIRED: 'Pay time expired',
        CODE_VCODE_INVALID: 'Validate code is invalid',
        CODE_USER_EXIST: 'User is existed',
        CODE_ACTIVE_USER_NOT_EXIST: 'Active user not existed',
        CODE_FREEZE_USER_NOT_EXIST: 'Freeze user not existed',
        CODE_SMS_SEND_FAILED: 'SMS send failed',
        CODE_PHONE_NUMBER_INVALID: 'Phone number invalid',
        CODE_CRM_ORDER_ID_INVALID: 'CRM order id invalid',

        CODE_NOT_REGISTED: 'Not regist in the app',

        CODE_PARAMETER_REQUIRED: 'Parameter {0[param_name]} is required',
        CODE_PARAMETER_CHOICES_ERROR: 'Parameter {0[param_name]} {0[value]} is not a valid choice.'
        'Should be choosen from {0[choices]}',
        CODE_PARAMETER_FORMAT_ERROR: 'Bad parameter value "{0[value]}" for {0[param_name]}:'
        '{0[msg_err]}',
        CODE_PARAMETER_LIMIT_ERROR: 'Parameter {0[param_name]} must be within the range {0[limit_start]} to {0[limit_end]}',
    }

    # CODE_CLIENT_TOKEN_MISSING: u'请求 header 中不存在 token' (默认用英文显示，因为中文传到客户端容易产生unicode乱码)
    CODE_MSG_MAP_CN = {
        CODE_SYSTEM_ERROR: u'后台系统错误',
        CODE_INVALID_TOKEN: u'Token 失效',
        CODE_INVALID_DIGEST: u'非法请求，签名错误',

        CODE_CLIENT_TOKEN_MISSING: 'Miss token in request header',
        CODE_CLIENT_TOKEN_INVALID: u'Application Token 无效',
        CODE_CLIENT_TOKEN_EXPIRED: 'Application Token 已过期失效',

        CODE_USER_NOT_EXIST: u'用户不存在',
        CODE_ROLE_DISABLED_USER_CANNOT_ENABLED: u'该用户对应的角色已“禁用“，无法解冻成功！',
        CODE_ROLE_ALREADY_ENABLED_CANNOT_DELETE: u'该角色启用状态，无法删除！',
        CODE_USER_ALREADY_ENABLED_CANNOT_DELETE: u'该用户启用状态，无法删除！',
        CODE_AGENT_USER_CANNOT_DELETED: u'代理商用户，无法删除！',
        CODE_MENU_PARENT_DISABLED: u'设置有效状态失败，上级菜单【{0[parent_menu]}】已失效！',
        CODE_ROLE_NOT_EXIST: u'角色不存在',
        CODE_ROLE_EXIST: u'角色已经存在',
        CODE_ROLE_ALREADY_DELETED: u'角色已经被删除',
        CODE_DOC_NOT_EXIST: u'记录不存在',
        CODE_DOC_EXIST: u'记录已经存在',
        CODE_DOC_ALREADY_DELETED: u'记录已经被删除',
        CODE_PASSWD_ERROR: u'密码错误',
        CODE_AUTH_ERROR: u'签名验证失败，非法请求',
        CODE_GET_VCODE_FREQUENTLY: u'短信发送太频繁',
        CODE_BINDING_PHONE_EXCCEED: u'绑定手机数量超出限制',
        CODE_VCODE_ERROR: u'手机验证码错误',
        CODE_SMS_FAIL: u'短信发送失败',
        CODE_FILE_NOT_FOUND: u'文件未找到',
        CODE_PAY_EXPIRED: u'已过期，请付费后使用',
        CODE_VCODE_INVALID: u'验证码已过期',
        CODE_USER_EXIST: u'用户已存在',
        CODE_ACTIVE_USER_NOT_EXIST: u'不存在非冻结用户',
        CODE_FREEZE_USER_NOT_EXIST: u'不存在冻结用户',
        CODE_SMS_SEND_FAILED: u'短信发送失败',
        CODE_PHONE_NUMBER_INVALID: u'手机号码无效',
        CODE_CRM_ORDER_ID_INVALID: u'CRM订单无效',

        CODE_NOT_REGISTED: u'用户未注册',

        CODE_PARAMETER_REQUIRED: u'缺少参数 {0[param_name]}',
        CODE_PARAMETER_CHOICES_ERROR: u'参数 {0[param_name]} 的值 {0[value]} 非法，'
        u'需要在下列值中选择: {0[choices]}',
        CODE_PARAMETER_FORMAT_ERROR: u'参数 {0[param_name]} 的值 "{0[value]}" 格式错误: '
        '{0[msg_err]}',
        CODE_PARAMETER_LIMIT_ERROR: u'参数 {0[param_name]} 的值必须在以下范围内: {0[limit_start]} - {0[limit_end]}',
    }

"""

formatted_text_block = format_code_block(text_block)
print("Formatted Text Block:\n", formatted_text_block)
