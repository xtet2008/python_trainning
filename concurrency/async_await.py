# coding:utf-8
# @Time : 2023/11/13 00:02 
# @Author : Andy.Zhang
# @Desc :


'''
async 和 await 是原生协程，是Python3.5以后引入的两个关键词，不需要额外安装依赖包即可使用
asyncio 是 Python3.7 以上的模块，所以最好能使用 python3.7 以上版本

async 是“异步”的简写， 所以应该很好理解 async 用于申明一个 function 是异步的
await 可以认为是 async wait 的简写，而 await 用于等待一个异步方法执行完成。

使用 async def function_name(args) 定义的函数名（即：协和函数），后期要调用的时候，必须前端加关键字 await 调用，不能直接调用，否则报错
await function_name(args)  使用 await 调用是 OK 正确的
function_name(args)  直接调用会报错
'''


import time
import asyncio
from _functions import cost_time

async def print_num(num):
    print("Maoli is printing " + str(num) + " nows")
    await asyncio.sleep(1)
    print("Maoli prints " +str(num) + " OK")

@cost_time
async def main(nums):
    print('\t\n同步调用：普通的 await 调用 async 协和属于')
    for num in nums:
        _ = print_num(num)  # 此时 _ 代表一个 future 对象，中文翻译成“未来”，代表是一个【可等待对象】即协和，但要正式调用后才会执行
        await _  # 使用

@cost_time
async def main_create_task(nums):
    print('\t\ncreate_task 异步调用')
    tasks = [asyncio.create_task(print_num(num)) for num in nums]
    for task in tasks:
        await task

@cost_time
async def main_gather_call_create_task(nums):
    print('\t\ncreate_task asyncio.gather 异步调用')
    tasks = [asyncio.create_task(print_num(num)) for num in nums]
    await asyncio.gather(*tasks)  # *tasks 解包列表，将列表变成了函数的参数

# main([i for i in range(1,6)])  # 当 main 被 async 关键字定义为协程之后，无法直接调用，这样会出错
# asyncio.run(main([1,2,3,4,5]))  # asyncio.run() 函数用来运行最高层级的入口点

asyncio.run(main([i for i in range(1,6)]))  # asyncio.run() 函数用来运行最高层级的入口点
asyncio.run(main_create_task([i for i in range(1,6)]))
asyncio.run(main_gather_call_create_task([i for i in range(1,6)]))




