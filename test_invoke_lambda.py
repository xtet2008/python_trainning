import boto3
import json


def invoke_addition_lambda(a, b):
    """
    调用AWS Lambda加法函数并获取结果

    参数:
        a (int/float): 第一个数
        b (int/float): 第二个数

    返回:
        dict: Lambda函数的响应
    """
    # 创建Lambda客户端
    lambda_client = boto3.client('lambda', region_name='us-east-1')


    # 准备输入数据
    payload = {
        'a': a,
        'b': b
    }

    # 转换为JSON
    payload_json = json.dumps(payload)

    # 调用Lambda函数
    response = lambda_client.invoke(
        FunctionName='sd-datahub-crawler-testcrawler',  # 替换为你的Lambda函数名
        InvocationType='RequestResponse',  # 同步调用
        Payload=json.dumps("")  # 传递空字符串作为 Payload
    )

    # 读取和解析响应
    response_payload = response['Payload'].read().decode('utf-8')
    result = json.loads(response_payload)
    print(result)
    return result


# 示例使用
if __name__ == "__main__":
    result = invoke_addition_lambda(10, 20)
    print("Lambda计算结果:", result)
    print(f"10 + 20 = {result['result']}")
