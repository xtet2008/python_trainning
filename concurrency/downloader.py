# coding:utf-8
# @Time : 2023/6/27 07:44 
# @Author : Andy.Zhang
# @Desc :

'''
python concurrency/downloader.py \
                     -f https://hnd-jp-ping.vultr.com/vultr.com.1000MB.bin \
                     -f https://sel-kor-ping.vultr.com/vultr.com.1000MB.bin \
                     -c 5


# python downloader.py -f https://example.com/file1.ext /path/to/save/file1.ext <file1_sha256> \
#                      -f https://example.com/file2.ext /path/to/save/file2.ext <file2_sha256> \
#                      -c 5 -p http://proxy.example.com:8080

pip install aiohttp
pip install tqdm

syncio.gather() 异步并发下载文件
--concurrency   限制同时下载的文件数量
tqdm    下载过程中显示进度条
argparse    命令行参数
logging.basicConfig 日志记录
--proxy 代理支持
SHA-256 验证文件的完整性


'''

import aiohttp
import asyncio
import os
import argparse
import logging
import hashlib
from tqdm.asyncio import tqdm


def setup_logging():
    logging.basicConfig(filename="downloader.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def parse_args():
    parser = argparse.ArgumentParser(description="Async file downloader")
    # parser.add_argument("-f", "--file", nargs=3, action="append", metavar=("URL", "SAVE_PATH", "SHA256"),
    #                     help="The URL of the file to download, the path where it should be saved, and the SHA-256 hash")
    parser.add_argument("-f", "--file",  action="append", metavar=("URL"), help="The URL of the file to download")
    parser.add_argument("-d", "--dir_to_save", type=str, default="/tmp", metavar=("save dir"), help="the path where it should be saved")
    parser.add_argument("-c", "--concurrency", type=int, default=3, help="Maximum number of concurrent downloads (default: 3)")
    parser.add_argument("-p", "--proxy", type=str, help="Proxy URL to use for downloads")

    args = parser.parse_args()

    if args.file is None:
        parser.error("At least one file is required for downloading")

    return args


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


async def download_file(url, save_path=None, sha256_hash=None, proxy=None):
    try:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download file: {url}, status: {response.status}")
                    total_size = int(response.headers.get('Content-Length', 0))
                    save_path = os.path.join(save_path, os.path.basename(url))
                    with open(save_path, 'wb') as f:
                        with tqdm(total=total_size, desc=save_path, unit='B', unit_scale=True) as pbar:
                            while True:
                                chunk = await response.content.read(1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                                pbar.update(len(chunk))
            # downloaded_sha256 = calculate_sha256(save_path)
            # if downloaded_sha256 == sha256_hash:
            #     logging.info(f"File downloaded and verified: {save_path}")
            #     return save_path
            # else:
            #     logging.error(f"File verification failed: {save_path}")
            #     os.remove(save_path)
            #     return None
    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return None

async def main(args):
    global semaphore
    semaphore = asyncio.Semaphore(args.concurrency)

    tasks = [
        # download_file(file[0], file[1], file[2], proxy=args.proxy) for file in args.file
        download_file(file, args.dir_to_save, proxy=args.proxy) for file in args.file
    ]

    downloaded_files = await asyncio.gather(*tasks, return_exceptions=True)
    for downloaded_file in downloaded_files:
        if downloaded_file is None:
            logging.error(f"File failed to download.")

if __name__ == '__main__':
    setup_logging()
    args = parse_args()
    asyncio.run(main(args))

