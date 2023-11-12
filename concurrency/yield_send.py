# coding:utf-8
# @Time : 2023/11/12 23:43 
# @Author : Andy.Zhang
# @Desc :

print('new line \t\n\t\n')
def customer():
    while True:
        _ = yield
        print('开始消费：', _)


custom = customer()
next(custom)  # 在后续调用 .send()发送数据之前，需要先调用一次 next 函数以启动生成器，让 customer 生成 器内部处于 yield 语句暂停
for i in range(5):
    print('开始生产：', i)
    custom.send(i)  # 调用 send(i)之后，会把 i的值传递给 custom 中 yield 对应的变量，并继续往后执行代码，停到下一个 yield 表达式或终止
