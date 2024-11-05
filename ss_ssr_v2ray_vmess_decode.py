import base64
import json

'''
A method of decoding base64, ss url and ssr url. 
also decoding v2ray config
'''


def fill(b64):
    return b64 + "=" * (4 - len(b64) % 4)


def clear_ssr(deb64):
    pos = deb64.rfind('/')
    return deb64[:pos] if pos > 0 else deb64


def clear_ss(deb64):
    pos = deb64.rfind('#')
    return deb64[:pos] if pos > 0 else deb64


def ssr_parse(txt):
    # ssr://server:port:protocol:method:obfs:password_base64/?params_base64
    conf = clear_ssr(bytes.decode(base64.urlsafe_b64decode(fill(txt)))).split(':')
    conf_dict = dict()
    conf_dict["ip"] = conf[0]
    conf_dict["port"] = conf[1]
    conf_dict["protocol"] = conf[2]
    conf_dict["method"] = conf[3]
    conf_dict["obfs"] = conf[4]
    conf_dict["password"] = clear_ssr(bytes.decode(base64.urlsafe_b64decode(fill(conf[5]))))
    return conf_dict


def ss_parse(txt):
    # method:password@server:port
    conf = clear_ss(bytes.decode(base64.urlsafe_b64decode(fill(txt))))
    conf_list = []
    for part in conf.split('@'):
        conf_list += part.split(':')
    conf_dict = dict()
    conf_dict["method"] = conf_list[0]
    conf_dict["password"] = conf_list[1]
    conf_dict["ip"] = conf_list[2]
    conf_dict["port"] = conf_list[3]
    return conf_dict


def parse(txt):
    if 'ssr://' in txt:
        return ssr_parse(txt.replace('ssr://', ''))
    if 'ss://' in txt:
        return ss_parse(txt.replace('ss://', ''))
    raise Exception('ss url or ssr url format error.')




def base64_decode(encoded_string):
    # 将 Base64 编码的字符串解码为字节
    decoded_bytes = base64.b64decode(encoded_string)

    # 如果你希望得到一个字符串，可以将字节转换为字符串
    decoded_string = decoded_bytes.decode('utf-8')

    return decoded_string


def decode_v2ray_vmess(vmess_url):
    # 解析 vmess URL 格式：vmess://<base64 编码的字符串>
    if vmess_url.startswith("vmess://"):
        vmess_base64 = vmess_url[8:]  # 去掉 "vmess://"
    else:
        raise ValueError("Invalid Vmess URL format")

    # Base64 解码
    decoded_bytes = base64.b64decode(vmess_base64 + '==' if len(vmess_base64) % 4 else vmess_base64)

    # 解码后的字节转换为字符串（假设是 UTF-8 编码的 JSON 格式）
    decoded_string = decoded_bytes.decode('utf-8')

    # 解析 JSON 配置
    try:
        decoded_json = json.loads(decoded_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode Vmess JSON data: {e}")

    return decoded_json


def decode_v2ray_config(encoded_data):
    # 解码 Base64 编码的数据
    decoded_bytes = base64.b64decode(encoded_data)

    # 将解码后的字节转换为字符串，假设它是 JSON 格式
    decoded_string = decoded_bytes.decode('utf-8')

    # 如果解码后的数据是 JSON 格式，可以进一步解析为 Python 对象
    try:
        decoded_json = json.loads(decoded_string)
    except json.JSONDecodeError:
        decoded_json = decoded_string  # 如果不是 JSON 格式则直接返回原始字符串

    return decoded_json




if __name__ == '__main__':
    # decoding base64
    encoded_string = 'SGVsbG8gd29ybGQh'  # 'Hello world!' 的 Base64 编码
    decoded_string = base64_decode(encoded_string)
    print(decoded_string)
    ssr_list_base64 = '''
    c3NyOi8vWVdKNmFqRXViVzF2WkhNdWMybDBaVG95TXpVME9EcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZSWGcxY0dGM05WbHhaelZhTW1oSlJXeFJWRVZOWnpWd1UzWTFiM2xDVkd0WloxWnJiRkZOYVVSdWRscEliRzVaUVRaaWJUVnBZVmMwZFZreU9YUW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL1lXRm9hek11YlcxdlpITXVjMmwwWlRveU16VTFNRHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWUlhvMWNHRjNOVmx4WnpWYU1taEpSV3hSVkVWTlp6VndVM1kxYjNsQ1ZHdFpaMVpyYkZGTmFVUnVkbHBJYkc1WlFUWmliVFZwWVZjMGRWa3lPWFFtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9ZV0ZvYXpRdWJXMXZaSE11YzJsMFpUb3lNelUxTVRwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGVlJUQTFjR0YzTlZseFp6VmFNbWhUVmtKTlVYbEViV3hMWDIxcVNVWlBVbWxDVjFOV1FYbEpUMlU1YTJWWFpHZEVjSFZpYlVwd1ltazFhbUl5TUNabmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9hSFYxY3k1dGJXOWtjeTV6YVhSbE9qSXpOVFV5T21GMWRHaGZZV1Z6TVRJNFgzTm9ZVEU2WVdWekxUSTFOaTFqWm1JNmFIUjBjRjl6YVcxd2JHVTZVMnBPU2xaR1FuZ3ZQMjlpWm5Od1lYSmhiVDFhVkVGM1dXMVJNRTE2WnpCT1ZHZDFZbGRzYW1OdE9YcGlNbG93VEcxT2RtSlJKbkJ5YjNSdmNHRnlZVzA5VGtSTk5FNUVWVFJQYm10NVlWVjNNVTFSSm5KbGJXRnlhM005VVZWRk1UVTNOazgxV25VNVRWTkNTbFZGZUVSSlJscEtWVVJKWnpVM01sSTFXakpCVDIwMWRWbHRiSFZNYlU1MllsRW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL1lXRTFkWE15TG0xdGIyUnpMbk5wZEdVNk1qTTBPbUYxZEdoZllXVnpNVEk0WDNOb1lURTZZV1Z6TFRJMU5pMWpabUk2YUhSMGNGOXphVzF3YkdVNlUycE9TbFpHUW5ndlAyOWlabk53WVhKaGJUMWFWRUYzV1cxUk1FMTZaekJPVkdkMVlsZHNhbU50T1hwaU1sb3dURzFPZG1KUkpuQnliM1J2Y0dGeVlXMDlUa1JOTkU1RVZUUlBibXQ1WVZWM01VMVJKbkpsYldGeWEzTTlVVlZGTVRVM05rODFXblU1VFdsQ1NsVkZlRVJKUTBKWFUxWkJlVWxQWlRsclpWZGtaMFJ3ZFdKdFNuQmlhVFZxWWpJd0ptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL1FVRTNkWE16TG0xdGIyUnpMbk5wZEdVNk1qRTFOREk2WVhWMGFGOWhaWE14TWpoZmMyaGhNVHBoWlhNdE1qVTJMV05tWWpwb2RIUndYM05wYlhCc1pUcFRhazVLVmtaQ2VDOF9iMkptYzNCaGNtRnRQVnBVUVhkWmJWRXdUWHBuTUU1VVozVmlWMnhxWTIwNWVtSXlXakJNYlU1MllsRW1jSEp2ZEc5d1lYSmhiVDFPUkUwMFRrUlZORTl1YTNsaFZYY3hUVkVtY21WdFlYSnJjejFSVlVVeE5UYzJUelZhZFRsTmVVSktWVVY0UkVsR1drcFZSRWxuTlRjeVVqVmFNa0ZQYlRWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vUVVFMWRYTTBMbTF0YjJSekxuTnBkR1U2TWpNMU9ERTZZWFYwYUY5aFpYTXhNamhmYzJoaE1UcGhaWE10TWpVMkxXTm1ZanBvZEhSd1gzTnBiWEJzWlRwVGFrNUtWa1pDZUM4X2IySm1jM0JoY21GdFBWcFVRWGRaYlZFd1RYcG5NRTVVWjNWaVYyeHFZMjA1ZW1JeVdqQk1iVTUyWWxFbWNISnZkRzl3WVhKaGJUMU9SRTAwVGtSVk5FOXVhM2xoVlhjeFRWRW1jbVZ0WVhKcmN6MVJWVVV4TlRjMlR6VmFkVGxPUTBKS1ZVVjRSRWxEUWxkVFZrRjVTVTlsT1d0bFYyUm5SSEIxWW0xS2NHSnBOV3BpTWpBbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vWVdFMWRYTTFMbTF0YjJSekxuTnBkR1U2TWpNMU9ESTZZWFYwYUY5aFpYTXhNamhmYzJoaE1UcGhaWE10TWpVMkxXTm1ZanBvZEhSd1gzTnBiWEJzWlRwVGFrNUtWa1pDZUM4X2IySm1jM0JoY21GdFBWcFVRWGRaYlZFd1RYcG5NRTVVWjNWaVYyeHFZMjA1ZW1JeVdqQk1iVTUyWWxFbWNISnZkRzl3WVhKaGJUMU9SRTAwVGtSVk5FOXVhM2xoVlhjeFRWRW1jbVZ0WVhKcmN6MVJWVVV4TlRjMlR6VmFkVGxPVTBKS1ZVVjRSRWxEUWxkVFZrRjVTVTlsT1d0bFYyUm5SSEIxWW0xS2NHSnBOV3BpTWpBbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vYUhWcWNDNXRiVzlrY3k1emFYUmxPakl6TlRZMk9tRjFkR2hmWVdWek1USTRYM05vWVRFNllXVnpMVEkxTmkxalptSTZhSFIwY0Y5emFXMXdiR1U2VTJwT1NsWkdRbmd2UDI5aVpuTndZWEpoYlQxYVZFRjNXVzFSTUUxNlp6Qk9WR2QxWWxkc2FtTnRPWHBpTWxvd1RHMU9kbUpSSm5CeWIzUnZjR0Z5WVcwOVRrUk5ORTVFVlRSUGJtdDVZVlYzTVUxUkpuSmxiV0Z5YTNNOVVWVkZNalZ3Wld3MWNIbHpUVk5DU2xWRmVFUkpSbHBLVlVSSlp6VTNNbEkxV2pKQlQyMDFkVmx0YkhWTWJVNTJZbEVtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9ZV0ZxY0RjdWJXMXZaSE11YzJsMFpUb3lNelUyTnpwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGVlJUSTFjR1ZzTlhCNWMwMXBRa3BWUlhoRVNVWmFTbFZFU1djMU56SlNOVm95UVU5dE5YVlpiV3gxVEcxT2RtSlJKbWR5YjNWd1BUWmFkVEkxTkVzMU5VeHhValUzTWxJMVdqSkJUMjFPYWxsdFNucGplVFZxWWpJdwpzc3I6Ly9kbWx3TW5SM0xtMXRiMlJ6TG5OcGRHVTZNak0xT0RRNllYVjBhRjloWlhNeE1qaGZjMmhoTVRwaFpYTXRNalUyTFdObVlqcG9kSFJ3WDNOcGJYQnNaVHBUYWs1S1ZrWkNlQzhfYjJKbWMzQmhjbUZ0UFZwVVFYZFpiVkV3VFhwbk1FNVVaM1ZpVjJ4cVkyMDVlbUl5V2pCTWJVNTJZbEVtY0hKdmRHOXdZWEpoYlQxT1JFMDBUa1JWTkU5dWEzbGhWWGN4VFZFbWNtVnRZWEpyY3oxUlZVVTBOVmt5ZHpWaVF6aEpSbHBLVlVSSlp6VTNNbEkxV2pKQlQyMDFkVmx0YkhWTWJVNTJZbEVtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9kbWx3TW5SM0xtMXRiMlJ6TG5OcGRHVTZNak0xTkRrNllYVjBhRjloWlhNeE1qaGZjMmhoTVRwaFpYTXRNalUyTFdObVlqcG9kSFJ3WDNOcGJYQnNaVHBUYWs1S1ZrWkNlQzhfYjJKbWMzQmhjbUZ0UFZwVVFYZFpiVkV3VFhwbk1FNVVaM1ZpVjJ4cVkyMDVlbUl5V2pCTWJVNTJZbEVtY0hKdmRHOXdZWEpoYlQxT1JFMDBUa1JWTkU5dWEzbGhWWGN4VFZFbWNtVnRZWEpyY3oxUlZVVTBOVmt0ZHpWeWJTMU5VMFJ0YkV0ZmJXcEpSazlTYVVKWFUxWkJlVWxQWlRsclpWZGtaMFJ3ZFdKdFNuQmlhVFZxWWpJd0ptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL2RtbHdNblIzTG0xdGIyUnpMbk5wZEdVNk1qTTFOVE02WVhWMGFGOWhaWE14TWpoZmMyaGhNVHBoWlhNdE1qVTJMV05tWWpwb2RIUndYM05wYlhCc1pUcFRhazVLVmtaQ2VDOF9iMkptYzNCaGNtRnRQVnBVUVhkWmJWRXdUWHBuTUU1VVozVmlWMnhxWTIwNWVtSXlXakJNYlU1MllsRW1jSEp2ZEc5d1lYSmhiVDFPUkUwMFRrUlZORTl1YTNsaFZYY3hUVkVtY21WdFlYSnJjejFSVlVVME5Wa3RkelZ5YlMxTmFVUnRiRXRmYldwSlJrOVNhVUpYVTFaQmVVbFBaVGxyWlZka1owUndkV0p0U25CaWFUVnFZakl3U2labmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9ZV0Y1YVc1a2RURXViVzF2WkhNdWMybDBaVG95TXpVM05qcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZSVFExWWpZek5WcDFPVWxHV2twVlJFbG5OVGN5VWpWYU1rRlBiVFYxV1cxc2RVeHRUblppVVdzbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vWVdGNWFXNWtkVEV1YlcxdlpITXVjMmwwWlRveU16VTFORHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWUlRRMWNrOTNOVnAxT1VsR1drcFZSRWxuTlRjeVVqVmFNa0ZQYlRWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVdGNWFXNWtkVEV1YlcxdlpITXVjMmwwWlRveU16VTRNRHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWUlRRMWNrOTNOVnAxT1UxcFFsZFRWa0Y1U1U5bE9XdGxWMlJuUkhCMVltMUtjR0pwTldwaU1qQW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL2RtbHdNblIzTG0xdGIyUnpMbk5wZEdVNk1qTTFPRE02WVhWMGFGOWhaWE14TWpoZmMyaGhNVHBoWlhNdE1qVTJMV05tWWpwb2RIUndYM05wYlhCc1pUcFRhazVLVmtaQ2VDOF9iMkptYzNCaGNtRnRQVnBVUVhkWmJWRXdUWHBuTUU1VVozVmlWMnhxWTIwNWVtSXlXakJNYlU1MllsRW1jSEp2ZEc5d1lYSmhiVDFPUkUwMFRrUlZORTl1YTNsaFZYY3hUVkVtY21WdFlYSnJjejFSVlVVME5ra3RlVFZpTmt3MVlUWXRTVVphU2xWRVNXYzFOekpTTlZveVFVOXROWFZaYld4MVRHMU9kbUpSSm1keWIzVndQVFphZFRJMU5FczFOVXh4VWpVM01sSTFXakpCVDIxT2FsbHRTbnBqZVRWcVlqSXcKc3NyOi8vWVdGNWFXNWtkVEV1YlcxdlpITXVjMmwwWlRveU16VTJNanBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWUlRRMlMxZGZOVFF0ZERVMGJWcEpSbHBLVlVSSlp6VTNNbEkxV2pKQlQyMDFkVmx0YkhWTWJVNTJZbEVtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9ZV0Y1YVc1a2RURXViVzF2WkhNdWMybDBaVG95TXpVMU5UcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZSVFEyVEdGTE5Wa3lXRWxHV2twVlJFbG5OVGN5VWpWYU1rRlBiVFYxV1cxc2RVeHRUblppVVNabmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9ZV0U0YldGc1lXbDRhWGxoTG0xdGIyUnpMbk5wZEdVNk1qTTFOelU2WVhWMGFGOWhaWE14TWpoZmMyaGhNVHBoWlhNdE1qVTJMV05tWWpwb2RIUndYM05wYlhCc1pUcFRhazVLVmtaQ2VDOF9iMkptYzNCaGNtRnRQVnBVUVhkWmJWRXdUWHBuTUU1VVozVmlWMnhxWTIwNWVtSXlXakJNYlU1MllsRW1jSEp2ZEc5d1lYSmhiVDFPUkUwMFRrUlZORTl1YTNsaFZYY3hUVkVtY21WdFlYSnJjejFSVlVVME5tRnRjelZ3TW13MlMxZGZOVXh4WVVsR1drcFZSRWxuTlRjeVVqVmFNa0ZQYlRWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVdGNWFXNWtkVEV1YlcxdlpITXVjMmwwWlRveU16VTNORHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWU0d0Mk5GUnVkbHBtYld4eE9IaEpSbHBLVlVSSlp6VTNNbEkxV2pKQlQyMDFkVmx0YkhWTWJVNTJZbEVtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9ZV0ZxYVdGdVlXUmhNUzV0Ylc5a2N5NXphWFJsT2pJek5UY3lPbUYxZEdoZllXVnpNVEk0WDNOb1lURTZZV1Z6TFRJMU5pMWpabUk2YUhSMGNGOXphVzF3YkdVNlUycE9TbFpHUW5ndlAyOWlabk53WVhKaGJUMWFWRUYzV1cxUk1FMTZaekJPVkdkMVlsZHNhbU50T1hwaU1sb3dURzFPZG1KUkpuQnliM1J2Y0dGeVlXMDlUa1JOTkU1RVZUUlBibXQ1WVZWM01VMVJKbkpsYldGeWEzTTlVVlZJYkdseFJHMXBOMTlzY0V0amVFbEdXa3BWUkVsbk5UY3lValZhTWtGUGJUVjFXVzFzZFV4dFRuWmlVU1puY205MWNEMDJXblV5TlRSTE5UVk1jVkkxTnpKU05Wb3lRVTl0VG1wWmJVcDZZM2sxYW1JeU1BCnNzcjovL1lXRnFhV0Z1WVdSaE1pNXRiVzlrY3k1emFYUmxPakl6TlRjek9tRjFkR2hmWVdWek1USTRYM05vWVRFNllXVnpMVEkxTmkxalptSTZhSFIwY0Y5emFXMXdiR1U2VTJwT1NsWkdRbmd2UDI5aVpuTndZWEpoYlQxYVZFRjNXVzFSTUUxNlp6Qk9WR2QxWWxkc2FtTnRPWHBpTWxvd1RHMU9kbUpSSm5CeWIzUnZjR0Z5WVcwOVRrUk5ORTVFVlRSUGJtdDVZVlYzTVUxUkpuSmxiV0Z5YTNNOVVWVkliR2x4UkcxcE4xOXNjRXRqZVVsR1drcFZSRWxuTlRjeVVqVmFNa0ZQYlRWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVdGNWFXNWtkVEV1YlcxdlpITXVjMmwwWlRveU16VTNNRHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWU0d4cVlrUnNkWEZaZUVsR1drcFZSRWxuTlRjeVVqVmFNa0ZQYlRWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVhObk1TNXRiVzlrY3k1emFYUmxPakl6TlRjNU9tRjFkR2hmWVdWek1USTRYM05vWVRFNllXVnpMVEkxTmkxalptSTZhSFIwY0Y5emFXMXdiR1U2VTJwT1NsWkdRbmd2UDI5aVpuTndZWEpoYlQxYVZFRjNXVzFSTUUxNlp6Qk9WR2QxWWxkc2FtTnRPWHBpTWxvd1RHMU9kbUpSSm5CeWIzUnZjR0Z5WVcwOVRrUk5ORTVFVlRSUGJtdDVZVlYzTVUxUkpuSmxiV0Z5YTNNOVVWVkliV3h5Ukd4cGNVUnNibUZGZUVsRmJGRlVSVTFuU1U5aFZYSXRZVTFuVlRWSFNVWmFTbFZFU1djMU56SlNOVm95UVU5dE5YVlpiV3gxVEcxT2RtSlJKbWR5YjNWd1BUWmFkVEkxTkVzMU5VeHhValUzTWxJMVdqSkJUMjFPYWxsdFNucGplVFZxWWpJdwpzc3I6Ly9ZWE5uTWk1dGJXOWtjeTV6YVhSbE9qRXhNVGsyT21GMWRHaGZZV1Z6TVRJNFgzTm9ZVEU2WVdWekxUSTFOaTFqWm1JNmFIUjBjRjl6YVcxd2JHVTZVMnBPU2xaR1FuZ3ZQMjlpWm5Od1lYSmhiVDFhVkVGM1dXMVJNRTE2WnpCT1ZHZDFZbGRzYW1OdE9YcGlNbG93VEcxT2RtSlJKbkJ5YjNSdmNHRnlZVzA5VGtSTk5FNUVWVFJQYm10NVlWVjNNVTFSSm5KbGJXRnlhM005VVZWSWJXeHlSR3hwY1VSc2JtRkZlVWxGYkZGVVJVMW5TVTloVlhJdFlVMW5WVFZIU1VaYVNsVkVTV2MxTnpKU05Wb3lRVTl0TlhWWmJXeDFURzFPZG1KUkptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL1lXRnpaek11YlcxdlpITXVjMmwwWlRveE1URXlNRHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWU0cxc2NrUnNhWEZFYkc1aFJYcEpSV3hSVkVWTlp6VndVM1kxYjNsQ1ZHdFpaMVpyYkZGTmFVUnVkbHBJYkc1WlFUWmliVFZwWVZjMGRWa3lPWFFtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9ZV0Z6WnpNdWJXMXZaSE11YzJsMFpUb3hNVEU1TnpwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGVlNHMXNja1JzYVhGRWJHNWhSVEJKUld4UlZFVk5aMGxQWVZWeUxXRk5aMVUxUjBsR1drcFZSRWxuTlRjeVVqVmFNa0ZQYlRWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVdGelp6TXViVzF2WkhNdWMybDBaVG94TVRFNU9EcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZTRzFzY2tSc2FYRkViRzVoUlRGSlJXeFJWRVZOWnpWd1UzWTFiM2xDVkd0WloxWnJiRkZOYVVSdWRscEliRzVaUVRaaWJUVnBZVmMwZFZreU9YUW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL1lXRjRhVzVxYVdGd2J6WXViVzF2WkhNdWMybDBaVG94TVRFNU9UcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZTRzFzY2tSc2FYRkViRzVoUlRKSlJXeFJWRVZOWjBsUFlWVnlMV0ZOWjFVMVIwbEdXa3BWUkVsbk5UY3lValZhTWtGUGJUVjFXVzFzZFV4dFRuWmlVU1puY205MWNEMDJXblV5TlRSTE5UVk1jVkkxTnpKU05Wb3lRVTl0VG1wWmJVcDZZM2sxYW1JeU1BCnNzcjovL1lXRjVhVzVuWjNWdk1TNXRiVzlrY3k1emFYUmxPakl6TlRVMk9tRjFkR2hmWVdWek1USTRYM05vWVRFNllXVnpMVEkxTmkxalptSTZhSFIwY0Y5emFXMXdiR1U2VTJwT1NsWkdRbmd2UDI5aVpuTndZWEpoYlQxYVZFRjNXVzFSTUUxNlp6Qk9WR2QxWWxkc2FtTnRPWHBpTWxvd1RHMU9kbUpSSm5CeWIzUnZjR0Z5WVcwOVRrUk5ORTVFVlRSUGJtdDVZVlYzTVUxUkpuSmxiV0Z5YTNNOVVWVkliMmszU0d4dE56QjRTVVZzUmxWRmQyZFdhMnhSVFdsRWJuWmFTR3h1V1VFMlltMDFhV0ZYTkhWWk1qbDBKbWR5YjNWd1BUWmFkVEkxTkVzMU5VeHhValUzTWxJMVdqSkJUMjFPYWxsdFNucGplVFZxWWpJdwpzc3I6Ly9ZV0Y1YVc1blozVnZNaTV0Ylc5a2N5NXphWFJsT2pJek5UVTNPbUYxZEdoZllXVnpNVEk0WDNOb1lURTZZV1Z6TFRJMU5pMWpabUk2YUhSMGNGOXphVzF3YkdVNlUycE9TbFpHUW5ndlAyOWlabk53WVhKaGJUMWFWRUYzV1cxUk1FMTZaekJPVkdkMVlsZHNhbU50T1hwaU1sb3dURzFPZG1KUkpuQnliM1J2Y0dGeVlXMDlUa1JOTkU1RVZUUlBibXQ1WVZWM01VMVJKbkpsYldGeWEzTTlVVlZJYjJrM1NHeHROekI1U1VWc1JsVkZkMmRXYTJ4UlRXbEViblphU0d4dVdVRTJZbTAxYVdGWE5IVlpNamwwSm1keWIzVndQVFphZFRJMU5FczFOVXh4VWpVM01sSTFXakpCVDIxT2FsbHRTbnBqZVRWcVlqSXcKc3NyOi8vWVdGNWFXNW5aM1Z2TXk1dGJXOWtjeTV6YVhSbE9qSXpOVFU0T21GMWRHaGZZV1Z6TVRJNFgzTm9ZVEU2WVdWekxUSTFOaTFqWm1JNmFIUjBjRjl6YVcxd2JHVTZVMnBPU2xaR1FuZ3ZQMjlpWm5Od1lYSmhiVDFhVkVGM1dXMVJNRTE2WnpCT1ZHZDFZbGRzYW1OdE9YcGlNbG93VEcxT2RtSlJKbkJ5YjNSdmNHRnlZVzA5VGtSTk5FNUVWVFJQYm10NVlWVjNNVTFSSm5KbGJXRnlhM005VVZWSWIyazNTR3h0TnpCNlNVVnNSbFZGZDJkV2EyeFJUV2xFYm5aYVNHeHVXVUUyWW0wMWFXRlhOSFZaTWpsMEptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL1lXRnJjakV1YlcxdlpITXVjMmwwWlRvME5qVTBPbUYxZEdoZllXVnpNVEk0WDNOb1lURTZZV1Z6TFRJMU5pMWpabUk2YUhSMGNGOXphVzF3YkdVNlUycE9TbFpHUW5ndlAyOWlabk53WVhKaGJUMWFWRUYzV1cxUk1FMTZaekJPVkdkMVlsZHNhbU50T1hwaU1sb3dURzFPZG1KUkpuQnliM1J2Y0dGeVlXMDlUa1JOTkU1RVZUUlBibXQ1WVZWM01VMVJKbkpsYldGeWEzTTlVVlZJY0c0MmJteHROekI0U1VWc1VWUkZUV2RKUmxwS1ZVUkpaelUzTWxJMVdqSkJUMjAxZFZsdGJIVk1iVTUyWWxFbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vWVdGcmNqSXViVzF2WkhNdWMybDBaVG8wTmpVMU9tRjFkR2hmWVdWek1USTRYM05vWVRFNllXVnpMVEkxTmkxalptSTZhSFIwY0Y5emFXMXdiR1U2VTJwT1NsWkdRbmd2UDI5aVpuTndZWEpoYlQxYVZFRjNXVzFSTUUxNlp6Qk9WR2QxWWxkc2FtTnRPWHBpTWxvd1RHMU9kbUpSSm5CeWIzUnZjR0Z5WVcwOVRrUk5ORTVFVlRSUGJtdDVZVlYzTVUxUkpuSmxiV0Z5YTNNOVVWVkljRzQyYm14dE56QjVTVVZzVVZSRlRXZEpSbHBLVlVSSlp6VTNNbEkxV2pKQlQyMDFkVmx0YkhWTWJVNTJZbEVtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9ZV0ZvYXpFdWJXMXZaSE11YzJsMFpUb3lOREl3TnpwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGVlNIQndjRzV0ZFVzNGVFbEZiRkZVUlUxbk5YQlRkalZ2ZVVKVWExbG5WbXRzVVUxcFJHNTJXa2hzYmxsQk5tSnROV2xoVnpSMVdUSTVkQ1puY205MWNEMDJXblV5TlRSTE5UVk1jVkkxTnpKU05Wb3lRVTl0VG1wWmJVcDZZM2sxYW1JeU1BCnNzcjovL1lXRm9hekl1YlcxdlpITXVjMmwwWlRveU5ESXdOanBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWU0hCd2NHNXRkVXM0ZVVsRmJGRlVSVTFuTlhCVGRqVnZlVUpVYTFsblZtdHNVVTFwUkc1MldraHNibGxCTm1KdE5XbGhWelIxV1RJNWRDWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVdGb2F6TXdMbTF0YjJSekxuTnBkR1U2TWpReU1EVTZZWFYwYUY5aFpYTXhNamhmYzJoaE1UcGhaWE10TWpVMkxXTm1ZanBvZEhSd1gzTnBiWEJzWlRwVGFrNUtWa1pDZUM4X2IySm1jM0JoY21GdFBWcFVRWGRaYlZFd1RYcG5NRTVVWjNWaVYyeHFZMjA1ZW1JeVdqQk1iVTUyWWxFbWNISnZkRzl3WVhKaGJUMU9SRTAwVGtSVk5FOXVhM2xoVlhjeFRWRW1jbVZ0WVhKcmN6MVJWVWh3Y0hCdWJYVkxPSHBKUld4UlZFVk5aelZ3VTNZMWIzbENWR3RaWjFacmJGRk5hVVJ1ZGxwSWJHNVpRVFppYlRWcFlWYzBkVmt5T1hRbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vWVdGb2F6VXViVzF2WkhNdWMybDBaVG95TkRJd05EcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZTSEJ3Y0c1dGRVczRNVWxGYkZGVVJVMW5OWEJUZGpWdmVVSlVhMWxuVm10c1VVMXBSRzUyV2toc2JsbEJObUp0TldsaFZ6UjFXVEk1ZENabmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9ZV0ZvYXpZdWJXMXZaSE11YzJsMFpUb3lOREl3TXpwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGVlNIQndjRzV0ZFVzNE1rbEZiRkZVUlUxbk5YQlRkalZ2ZVVKVWExbG5WbXRzVVUxcFJHNTJXa2hzYmxsQk5tSnROV2xoVnpSMVdUSTVkQ1puY205MWNEMDJXblV5TlRSTE5UVk1jVkkxTnpKU05Wb3lRVTl0VG1wWmJVcDZZM2sxYW1JeU1BCnNzcjovL1lXRm9hemN1YlcxdlpITXVjMmwwWlRveU5ESXdNanBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZWU0hCd2NHNXRkVXM0TTBsRmJGRlVSVTFuTlhCVGRqVnZlVUpVYTFsblZtdHNVVTFwUkc1MldraHNibGxCTm1KdE5XbGhWelIxV1RJNWRDWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vWVdGb2F6Z3ViVzF2WkhNdWMybDBaVG95TkRJd01UcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRlZTSEJ3Y0c1dGRVczRORWxGYkZGVVJVMW5OWEJUZGpWdmVVSlVhMWxuVm10c1VVMXBSRzUyV2toc2JsbEJObUp0TldsaFZ6UjFXVEk1ZENabmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9ZV0ZvYXprdWJXMXZaSE11YzJsMFpUb3lOREl3TURwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGVlNIQndjRzV0ZFVzNE5VbEZiRkZVUlUxbk5YQlRkalZ2ZVVKVWExbG5WbXRzVVUxcFJHNTJXa2hzYmxsQk5tSnROV2xoVnpSMVdUSTVkQ1puY205MWNEMDJXblV5TlRSTE5UVk1jVkkxTnpKU05Wb3lRVTl0VG1wWmJVcDZZM2sxYW1JeU1BCnNzcjovL05HaHJMbTF0YjJSekxuTnBkR1U2TWpNMU5qZzZZWFYwYUY5aFpYTXhNamhmYzJoaE1UcGhaWE10TWpVMkxXTm1ZanBvZEhSd1gzTnBiWEJzWlRwVGFrNUtWa1pDZUM4X2IySm1jM0JoY21GdFBWcFVRWGRaYlZFd1RYcG5NRTVVWjNWaVYyeHFZMjA1ZW1JeVdqQk1iVTUyWWxFbWNISnZkRzl3WVhKaGJUMU9SRTAwVGtSVk5FOXVhM2xoVlhjeFRWRW1jbVZ0WVhKcmN6MVJaV0ZYYzA5WFMyOVBWMlJ2VkVWblZtdHNVVTFUUkc1MldraHNibGxCTm1KdE5XbGhWelIxV1RJNWRDWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vTldockxtMXRiMlJ6TG5OcGRHVTZNak0xTkRJNllYVjBhRjloWlhNeE1qaGZjMmhoTVRwaFpYTXRNalUyTFdObVlqcG9kSFJ3WDNOcGJYQnNaVHBUYWs1S1ZrWkNlQzhfYjJKbWMzQmhjbUZ0UFZwVVFYZFpiVkV3VFhwbk1FNVVaM1ZpVjJ4cVkyMDVlbUl5V2pCTWJVNTJZbEVtY0hKdmRHOXdZWEpoYlQxT1JFMDBUa1JWTkU5dWEzbGhWWGN4VFZFbWNtVnRZWEpyY3oxUlpXRlhjMDlYUzI5UFYyUnZWRWxuVm10c1VVMVRSRzUyV2toc2JsbEJObUp0TldsaFZ6UjFXVEk1ZENabmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9NMmhyTG0xdGIyUnpMbk5wZEdVNk1qTTFORE02WVhWMGFGOWhaWE14TWpoZmMyaGhNVHBoWlhNdE1qVTJMV05tWWpwb2RIUndYM05wYlhCc1pUcFRhazVLVmtaQ2VDOF9iMkptYzNCaGNtRnRQVnBVUVhkWmJWRXdUWHBuTUU1VVozVmlWMnhxWTIwNWVtSXlXakJNYlU1MllsRW1jSEp2ZEc5d1lYSmhiVDFPUkUwMFRrUlZORTl1YTNsaFZYY3hUVkVtY21WdFlYSnJjejFSWldGWGMwOVhTMjlQVjJSdlZFMW5WbXRzVVUxVFJHMXNja1J1ZGxwSWJHNVpRVFppYlRWcFlWYzBkVmt5T1hRbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vZGpKb2F6VXViVzF2WkhNdWMybDBaVG95TXpVME5EcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWRmxZVmR6VDFkTGIwOVhaRzlVVVdkV2EyeFJUVk5FYm5aYVNHeHVXVUUyWW0wMWFXRlhOSFZaTWpsMEptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL2RqSm9hell1YlcxdlpITXVjMmwwWlRveU16VTBOVHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkZsWVZkelQxZExiMDlYWkc5VVdXZFdhMnhSVFZORWJuWmFTR3h1V1VFMlltMDFhV0ZYTkhWWk1qbDBKbWR5YjNWd1BUWmFkVEkxTkVzMU5VeHhValUzTWxJMVdqSkJUMjFPYWxsdFNucGplVFZxWWpJdwpzc3I6Ly9kakpvYXpZdWJXMXZaSE11YzJsMFpUb3lNelUwTnpwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGbFlWZHpUMWRMYjA5WFpHOVVZMmRXYTJ4UlRWTkViblphU0d4dVdVRTJZbTAxYVdGWE5IVlpNamwwSm1keWIzVndQVFphZFRJMU5FczFOVXh4VWpVM01sSTFXakpCVDIxT2FsbHRTbnBqZVRWcVlqSXcKc3NyOi8vU0VzeUxtMXRiMlJ6TG5OcGRHVTZNVEV6T1RBNllYVjBhRjloWlhNeE1qaGZjMmhoTVRwaFpYTXRNalUyTFdObVlqcG9kSFJ3WDNOcGJYQnNaVHBUYWs1S1ZrWkNlQzhfYjJKbWMzQmhjbUZ0UFZwVVFYZFpiVkV3VFhwbk1FNVVaM1ZpVjJ4cVkyMDVlbUl5V2pCTWJVNTJZbEVtY0hKdmRHOXdZWEpoYlQxT1JFMDBUa1JWTkU5dWEzbGhWWGN4VFZFbWNtVnRZWEpyY3oxUlpXMXRiV1ZoTkhKNlVXZFdhMnhSVFZORWJuWmFTR3h1V1VFMlltMDFhV0ZYTkhWWk1qbDBKbWR5YjNWd1BUWmFkVEkxTkVzMU5VeHhValUzTWxJMVdqSkJUMjFPYWxsdFNucGplVFZxWWpJdwpzc3I6Ly9hR3N4TG0xdGIyUnpMbk5wZEdVNk1URXpPVEU2WVhWMGFGOWhaWE14TWpoZmMyaGhNVHBoWlhNdE1qVTJMV05tWWpwb2RIUndYM05wYlhCc1pUcFRhazVLVmtaQ2VDOF9iMkptYzNCaGNtRnRQVnBVUVhkWmJWRXdUWHBuTUU1VVozVmlWMnhxWTIwNWVtSXlXakJNYlU1MllsRW1jSEp2ZEc5d1lYSmhiVDFPUkUwMFRrUlZORTl1YTNsaFZYY3hUVkVtY21WdFlYSnJjejFSWlcxdGJXVmhOSEo2VldkV2EyeFJUVk5FYm5aYVNHeHVXVUUyWW0wMWFXRlhOSFZaTWpsMEptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL2FHdDBNaTV0Ylc5a2N5NXphWFJsT2pFeE16a3pPbUYxZEdoZllXVnpNVEk0WDNOb1lURTZZV1Z6TFRJMU5pMWpabUk2YUhSMGNGOXphVzF3YkdVNlUycE9TbFpHUW5ndlAyOWlabk53WVhKaGJUMWFWRUYzV1cxUk1FMTZaekJPVkdkMVlsZHNhbU50T1hwaU1sb3dURzFPZG1KUkpuQnliM1J2Y0dGeVlXMDlUa1JOTkU1RVZUUlBibXQ1WVZWM01VMVJKbkpsYldGeWEzTTlVV1Z0YlcxbFlUUnllbGxuVm10c1VVMVRSRzUyV2toc2JsbEJObUp0TldsaFZ6UjFXVEk1ZENabmNtOTFjRDAyV25VeU5UUkxOVFZNY1ZJMU56SlNOVm95UVU5dFRtcFpiVXA2WTNrMWFtSXlNQQpzc3I6Ly9hR3RpYmpFdWJXMXZaSE11YzJsMFpUb3hNVFkzTVRwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZGbGJXMXRaV0UwY25wbloxWnJiRkZOVTBSdWRscEliRzVaUVRaaWJUVnBZVmMwZFZreU9YUW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL01UQXViVzF2WkhNdWMybDBaVG95TXpVMU9UcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBWa3RaUzFxZFZkaWRsUkZaMVpyYkZGTlUwUnVkbHBJYkc1WlFUWmliVFZwWVZjMGRWa3lPWFFtWjNKdmRYQTlObHAxTWpVMFN6VTFUSEZTTlRjeVVqVmFNa0ZQYlU1cVdXMUtlbU41TldwaU1qQQpzc3I6Ly9NVEV1YlcxdlpITXVjMmwwWlRveU16VTJNRHBoZFhSb1gyRmxjekV5T0Y5emFHRXhPbUZsY3kweU5UWXRZMlppT21oMGRIQmZjMmx0Y0d4bE9sTnFUa3BXUmtKNEx6OXZZbVp6Y0dGeVlXMDlXbFJCZDFsdFVUQk5lbWN3VGxSbmRXSlhiR3BqYlRsNllqSmFNRXh0VG5aaVVTWndjbTkwYjNCaGNtRnRQVTVFVFRST1JGVTBUMjVyZVdGVmR6Rk5VU1p5WlcxaGNtdHpQVkV0WlMxcWRWZGlkbFJKWjFacmJGRk5VMFJ1ZGxwSWJHNVpRVFppYlRWcFlWYzBkVmt5T1hRbVozSnZkWEE5TmxwMU1qVTBTelUxVEhGU05UY3lValZhTWtGUGJVNXFXVzFLZW1ONU5XcGlNakEKc3NyOi8vTVRJdWJXMXZaSE11YzJsMFpUb3lNelUyTVRwaGRYUm9YMkZsY3pFeU9GOXphR0V4T21GbGN5MHlOVFl0WTJaaU9taDBkSEJmYzJsdGNHeGxPbE5xVGtwV1JrSjRMejl2WW1aemNHRnlZVzA5V2xSQmQxbHRVVEJOZW1jd1RsUm5kV0pYYkdwamJUbDZZakphTUV4dFRuWmlVU1p3Y205MGIzQmhjbUZ0UFU1RVRUUk9SRlUwVDI1cmVXRlZkekZOVVNaeVpXMWhjbXR6UFZrdFpTMXFkVmRpZGxSTloxWnJiRkZOVTBSdWRscEliRzVaUVRaaWJUVnBZVmMwZFZreU9YUW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL01UUXViVzF2WkhNdWMybDBaVG95TXpVM01UcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBUVndaV3cxY0hselRWTkNWMU5XUVhnMU56SlNOVm95UVU5dE5YVlpiV3gxVEcxT2RtSlJKbWR5YjNWd1BUWmFkVEkxTkVzMU5VeHhValUzTWxJMVdqSkJUMjFPYWxsdFNucGplVFZxWWpJdwpzc3I6Ly9kakpxY0M1dGJXOWtjeTV6YVhSbE9qSXpOVFl6T21GMWRHaGZZV1Z6TVRJNFgzTm9ZVEU2WVdWekxUSTFOaTFqWm1JNmFIUjBjRjl6YVcxd2JHVTZVMnBPU2xaR1FuZ3ZQMjlpWm5Od1lYSmhiVDFhVkVGM1dXMVJNRTE2WnpCT1ZHZDFZbGRzYW1OdE9YcGlNbG93VEcxT2RtSlJKbkJ5YjNSdmNHRnlZVzA5VGtSTk5FNUVWVFJQYm10NVlWVjNNVTFSSm5KbGJXRnlhM005TlhCbGJEVndlWE5OYVVSdWRscEliRzVaUVRaaWJUVnBZVmMwZFZreU9YUW1aM0p2ZFhBOU5scDFNalUwU3pVMVRIRlNOVGN5VWpWYU1rRlBiVTVxV1cxS2VtTjVOV3BpTWpBCnNzcjovL01UTXViVzF2WkhNdWMybDBaVG95TXpVMk9UcGhkWFJvWDJGbGN6RXlPRjl6YUdFeE9tRmxjeTB5TlRZdFkyWmlPbWgwZEhCZmMybHRjR3hsT2xOcVRrcFdSa0o0THo5dlltWnpjR0Z5WVcwOVdsUkJkMWx0VVRCTmVtY3dUbFJuZFdKWGJHcGpiVGw2WWpKYU1FeHRUblppVVNad2NtOTBiM0JoY21GdFBVNUVUVFJPUkZVMFQyNXJlV0ZWZHpGTlVTWnlaVzFoY210elBUWmFMWEExV25VNVRWTkNWMU5XUVhoSlQyVTVhMlZsY20xVWNIVmliVXB3WW1rMWFtSXlNQ1puY205MWNEMDJXblV5TlRSTE5UVk1jVkkxTnpKU05Wb3lRVTl0VG1wWmJVcDZZM2sxYW1JeU1BCnNzcjovL01UVXViVzF2WkhNdWMybDBaVG94TURVNllYVjBhRjloWlhNeE1qaGZjMmhoTVRwaFpYTXRNalUyTFdObVlqcG9kSFJ3WDNOcGJYQnNaVHBUYWs1S1ZrWkNlQzhfYjJKbWMzQmhjbUZ0UFZwVVFYZFpiVkV3VFhwbk1FNVVaM1ZpVjJ4cVkyMDVlbUl5V2pCTWJVNTJZbEVtY0hKdmRHOXdZWEpoYlQxT1JFMDBUa1JWTkU5dWEzbGhWWGN4VFZFbWNtVnRZWEpyY3owMldpMXdOVnAxT1UxcFFsZFRWa0Y0U1U5bE9XdGxWMlJuUnpWMVdXMXNkVXh0VG5aaVVTWm5jbTkxY0QwMlduVXlOVFJMTlRWTWNWSTFOekpTTlZveVFVOXRUbXBaYlVwNlkzazFhbUl5TUEKc3NyOi8vZW1oaGJpNHdaSGwyY3k1MGIzQTZNVEF3T0RZNmIzSnBaMmx1T21Ob1lXTm9ZVEl3TFdsbGRHWTZjR3hoYVc0NlpWUktjRlJFVlhndlAyOWlabk53WVhKaGJUMG1jSEp2ZEc5d1lYSmhiVDBtY21WdFlYSnJjejAxV1cxd05Vd3lXalZ5VjBJMldXVlFOemQ1WVU5VVl6Sk1hazAxVmtWSkptZHliM1Z3UFRaYWRUSTFORXMxTlV4eFVqVTNNbEkxV2pKQlQyMU9hbGx0U25wamVUVnFZakl3CnNzcjovL2VtaGhiaTR3WkhsMmN5NTBiM0E2TVRBd09EWTZiM0pwWjJsdU9tTm9ZV05vWVRJd0xXbGxkR1k2Y0d4aGFXNDZaVlJLY0ZSRVZYZ3ZQMjlpWm5Od1lYSmhiVDBtY0hKdmRHOXdZWEpoYlQwbWNtVnRZWEpyY3owMlRDMUlOWEI1WmpWd1pUSTJXbVV3TnpkNVlVMXFRWGxPVXpCM1QwTXdlVTFSSm1keWIzVndQVFphZFRJMU5FczFOVXh4VWpVM01sSTFXakpCVDIxT2FsbHRTbnBqZVRWcVlqSXcK
    '''
    ssr_list = base64_decode(ssr_list_base64)
    print(ssr_list)


    print('\n')

    # decoding ss or ssr
    # print(parse('ss://YWVzLTEyOC1jdHI6dmllbmNvZGluZy5jb21AMTUyLjg5LjIwOC4xNDY6MjMzMw'))
    # print(parse('ssr://MTUyLjg5LjIwOC4xNDY6MjMzMzphdXRoX3NoYTFfdjQ6YWVzLTEyOC1jdHI6cGxhaW46ZG1sbGJtTnZaR2x1Wnk1amIyMA'))
    # print(parse('ssr://YWJ6ajEubW1vZHMuc2l0ZToyMzU0ODphdXRoX2FlczEyOF9zaGExOmFlcy0yNTYtY2ZiOmh0dHBfc2ltcGxlOlNqTkpWRkJ4Lz9vYmZzcGFyYW09WlRBd1ltUTBNemcwTlRndWJXbGpjbTl6YjJaMExtTnZiUSZwcm90b3BhcmFtPU5ETTRORFU0T25reWFVdzFNUSZyZW1hcmtzPVFVRXg1cGF3NVlxZzVaMmhJRWxRVEVNZzVwU3Y1b3lCVGtZZ1ZrbFFNaURudlpIbG5ZQTZibTVpYVc0dVkyOXQmZ3JvdXA9Nlp1MjU0SzU1THFSNTcyUjVaMkFPbU5qWW1KemN5NWpiMjA'))
    for ssr in ssr_list.splitlines():
        print(parse(ssr))

    print('\n')

    # decoding v2ray config
    encoded_data = 'eyJ1dWlkIjoiZmYyM2FjZGI5YzMwNTMyZGFmMjJkZDg0YjcxYjYyYjQifQ=='  # 这是一个示例的 Base64 编码 UUID
    decoded_data = decode_v2ray_config(encoded_data)
    print(decoded_data)

    # decoding vmess
    v2ray_list_base64 = '''dm1lc3M6Ly9leUoySWpvaU1pSXNJbkJ6SWpvaVFVRTE1NzZPNVp1OU5pQldNbkpoZVNEbnZaSGxuWUE2Ym01aWFXNHVZMjl0SWl3aVlXUmtJam9pWVdFMWJXVnBaM1Z2Tmk1dGJXOWtjeTV6YVhSbElpd2ljRzl5ZENJNklqTXpORE0zSWl3aWFXUWlPaUpqTTJJM01EbGxPQzB5WTJVeExUTTBORFl0WVdVNE15MW1OVGxoTkdFeU5UUmxZamdpTENKaGFXUWlPaUl3SWl3aWJtVjBJam9pZEdOd0lpd2lkSGx3WlNJNkltNXZibVVpTENKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlKOQp2bWVzczovL2V5SjJJam9pTWlJc0luQnpJam9pUVVFMjVwZWw1cHlzTXlCMk1uSmhlU0RudlpIbG5ZQTZibTVpYVc0dVkyOXRJaXdpWVdSa0lqb2lZV0UyY21saVpXNHpMbTF0YjJSekxuTnBkR1VpTENKd2IzSjBJam9pTXpNME16VWlMQ0pwWkNJNkltTXpZamN3T1dVNExUSmpaVEV0TXpRME5pMWhaVGd6TFdZMU9XRTBZVEkxTkdWaU9DSXNJbUZwWkNJNklqQWlMQ0p1WlhRaU9pSjBZM0FpTENKMGVYQmxJam9pYm05dVpTSXNJbWh2YzNRaU9pSWlMQ0p3WVhSb0lqb2lJaXdpZEd4eklqb2lJbjA9CnZtZXNzOi8vZXlKMklqb2lNaUlzSW5Ceklqb2lRVUU0NXJPVjVadTlJRll5Y21GNUlPZTlrZVdkZ0RwdWJtSnBiaTVqYjIwaUxDSmhaR1FpT2lKaFlUaG1ZV2QxYnk1dGJXOWtjeTV6YVhSbElpd2ljRzl5ZENJNklqTXpORE01SWl3aWFXUWlPaUpqTTJJM01EbGxPQzB5WTJVeExUTTBORFl0WVdVNE15MW1OVGxoTkdFeU5UUmxZamdpTENKaGFXUWlPaUl3SWl3aWJtVjBJam9pZEdOd0lpd2lkSGx3WlNJNkltNXZibVVpTENKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlKOQp2bWVzczovL2V5SjJJam9pTWlJc0luQnpJam9pUVVFNDVyNno1clN5SUZZeWNtRjVJT2U5a2VXZGdEcHVibUpwYmk1amIyMGlMQ0poWkdRaU9pSmhZVGhoYjJSaGJHbDVZUzV0Ylc5a2N5NXphWFJsSWl3aWNHOXlkQ0k2SWpNek5ETTRJaXdpYVdRaU9pSmpNMkkzTURsbE9DMHlZMlV4TFRNME5EWXRZV1U0TXkxbU5UbGhOR0V5TlRSbFlqZ2lMQ0poYVdRaU9pSXdJaXdpYm1WMElqb2lkR053SWl3aWRIbHdaU0k2SW01dmJtVWlMQ0pvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUo5CnZtZXNzOi8vZXlKMklqb2lNaUlzSW5Ceklqb2lRZWFXc09XS29PV2RvVFVnZGpKeVlYa2c1NzJSNVoyQU9tNXVZbWx1TG1OdmJTSXNJbUZrWkNJNkltRjRhVzVxYVdGd2J6VXViVzF2WkhNdWMybDBaU0lzSW5CdmNuUWlPaUl6TXpRek5DSXNJbWxrSWpvaVl6TmlOekE1WlRndE1tTmxNUzB6TkRRMkxXRmxPRE10WmpVNVlUUmhNalUwWldJNElpd2lZV2xrSWpvaU1DSXNJbTVsZENJNkluUmpjQ0lzSW5SNWNHVWlPaUp1YjI1bElpd2lhRzl6ZENJNklpSXNJbkJoZEdnaU9pSWlMQ0owYkhNaU9pSWlmUT09CnZtZXNzOi8vZXlKMklqb2lNaUlzSW5Ceklqb2lZK2UranVXYnZUUWdkakp5WVhrZzU3MlI1WjJBT201dVltbHVMbU52YlNJc0ltRmtaQ0k2SW1OdFpXbG5kVzgwTG0xdGIyUnpMbk5wZEdVaUxDSndiM0owSWpvaU16TTBNellpTENKcFpDSTZJbU16WWpjd09XVTRMVEpqWlRFdE16UTBOaTFoWlRnekxXWTFPV0UwWVRJMU5HVmlPQ0lzSW1GcFpDSTZJakFpTENKdVpYUWlPaUowWTNBaUxDSjBlWEJsSWpvaWJtOXVaU0lzSW1odmMzUWlPaUlpTENKd1lYUm9Jam9pSWl3aWRHeHpJam9pSW4wPQp2bWVzczovL2V5SjJJam9pTWlJc0luQnpJam9pNVltcDVMMlo1cldCNlllUDc3eWFPVGMyTGpNNVZFSWlMQ0poWkdRaU9pSjZhR0Z1TGpCa2VYWnpMblJ2Y0NJc0luQnZjblFpT2lJeE1EQTROaUlzSW1sa0lqb2lZek5pTnpBNVpUZ3RNbU5sTVMwek5EUTJMV0ZsT0RNdFpqVTVZVFJoTWpVMFpXSTRJaXdpWVdsa0lqb2lNQ0lzSW01bGRDSTZJblJqY0NJc0luUjVjR1VpT2lKdWIyNWxJaXdpYUc5emRDSTZJaUlzSW5CaGRHZ2lPaUl2SWl3aWRHeHpJam9pSW4wPQp2bWVzczovL2V5SjJJam9pTWlJc0luQnpJam9pNkwrSDVweWY1cGUyNlplMDc3eWFNakF5TlMwd09DMHlNU0lzSW1Ga1pDSTZJbnBvWVc0dU1HUjVkbk11ZEc5d0lpd2ljRzl5ZENJNklqRXdNRGcySWl3aWFXUWlPaUpqTTJJM01EbGxPQzB5WTJVeExUTTBORFl0WVdVNE15MW1OVGxoTkdFeU5UUmxZamdpTENKaGFXUWlPaUl3SWl3aWJtVjBJam9pZEdOd0lpd2lkSGx3WlNJNkltNXZibVVpTENKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWk4aUxDSjBiSE1pT2lJaWZRPT0K'''
    v2ray_list = base64_decode(v2ray_list_base64)
    print(v2ray_list)
    for v2ray in v2ray_list.splitlines():
        print(decode_v2ray_vmess(v2ray))

