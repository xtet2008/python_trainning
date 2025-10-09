#!/usr/bin/env python3
"""
GeoIP 数据库下载脚本
支持下载 MaxMind GeoLite2 免费数据库
"""

import os
import requests
import tarfile
import shutil
from pathlib import Path
import logging
import sys

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GeoIPDownloader:
    def __init__(self, license_key: str = None):
        """
        初始化下载器

        Args:
            license_key: MaxMind 许可证密钥（免费注册获得）
        """
        self.license_key = license_key
        self.data_dir = Path("./data")
        self.data_dir.mkdir(exist_ok=True)

        # MaxMind GeoLite2 数据库下载链接
        self.databases = {
            'GeoLite2-City': 'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={}&suffix=tar.gz',
            'GeoLite2-Country': 'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={}&suffix=tar.gz',
            'GeoLite2-ASN': 'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-ASN&license_key={}&suffix=tar.gz'
        }

        # 备用免费数据库链接（可能不是最新的）
        self.free_databases = {
            'GeoLite2-City': 'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb',
            'GeoLite2-Country': 'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb',
            'GeoLite2-ASN': 'https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb'
        }

    def _format_size(self, size_bytes: int) -> str:
        """
        格式化文件大小显示

        Args:
            size_bytes: 字节大小

        Returns:
            str: 格式化的大小字符串
        """
        return f"{size_bytes / (1024 * 1024):.2f} MB"

    def _download_with_progress(self, url: str, file_path: Path, description: str) -> bool:
        """
        带进度显示的下载函数

        Args:
            url: 下载链接
            file_path: 保存路径
            description: 下载描述

        Returns:
            bool: 下载是否成功
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # 获取文件总大小
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            print(f"正在下载 {description}...")
            if total_size > 0:
                print(f"文件大小: {self._format_size(total_size)}")
            else:
                print("文件大小: 未知")

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # 显示进度
                        if total_size > 0:
                            percentage = (downloaded_size / total_size) * 100
                            downloaded_mb = self._format_size(downloaded_size)
                            total_mb = self._format_size(total_size)

                            # 创建进度条
                            progress_bar_length = 30
                            filled_length = int(progress_bar_length * downloaded_size // total_size)
                            bar = '█' * filled_length + '-' * (progress_bar_length - filled_length)

                            # 使用 \r 回到行首覆盖之前的输出
                            print(f"\r进度: [{bar}] {downloaded_mb}/{total_mb} ({percentage:.1f}%)", end='', flush=True)
                        else:
                            # 如果无法获取总大小，只显示已下载量
                            downloaded_mb = self._format_size(downloaded_size)
                            print(f"\r已下载: {downloaded_mb}", end='', flush=True)

            print()  # 换行
            logger.info(f"{description} 下载完成: {file_path}")
            return True

        except Exception as e:
            print()  # 确保错误信息在新行显示
            logger.error(f"下载 {description} 失败: {e}")
            if file_path.exists():
                file_path.unlink()
            return False

    def download_official(self, db_name: str) -> bool:
        """
        从 MaxMind 官方下载数据库（需要许可证密钥）

        Args:
            db_name: 数据库名称

        Returns:
            bool: 下载是否成功
        """
        if not self.license_key:
            logger.error("需要 MaxMind 许可证密钥才能下载官方数据库")
            return False

        url = self.databases[db_name].format(self.license_key)
        tar_file = self.data_dir / f"{db_name}.tar.gz"

        try:
            # 使用带进度的下载函数
            if not self._download_with_progress(url, tar_file, f"{db_name} (官方源)"):
                return False

            # 解压文件
            logger.info(f"正在解压 {db_name}...")
            with tarfile.open(tar_file, 'r:gz') as tar:
                # 找到 .mmdb 文件
                for member in tar.getmembers():
                    if member.name.endswith('.mmdb'):
                        # 提取到数据目录
                        tar.extract(member, self.data_dir)
                        # 重命名为标准名称
                        extracted_path = self.data_dir / member.name
                        final_path = self.data_dir / f"{db_name}.mmdb"
                        shutil.move(str(extracted_path), str(final_path))
                        logger.info(f"{db_name} 解压完成: {final_path}")
                        break

            # 清理临时文件
            tar_file.unlink()

            # 清理解压的目录
            for item in self.data_dir.iterdir():
                if item.is_dir() and db_name in item.name:
                    shutil.rmtree(item)

            return True

        except Exception as e:
            logger.error(f"处理 {db_name} 失败: {e}")
            if tar_file.exists():
                tar_file.unlink()
            return False

    def download_free(self, db_name: str) -> bool:
        """
        从免费源下载数据库

        Args:
            db_name: 数据库名称

        Returns:
            bool: 下载是否成功
        """
        url = self.free_databases[db_name]
        file_path = self.data_dir / f"{db_name}.mmdb"

        # 使用带进度的下载函数
        return self._download_with_progress(url, file_path, f"{db_name} (免费源)")

    def download_all(self, use_official: bool = False) -> dict:
        """
        下载所有数据库

        Args:
            use_official: 是否使用官方源（需要许可证密钥）

        Returns:
            dict: 下载结果
        """
        results = {}

        for db_name in self.databases.keys():
            print(f"\n{'=' * 60}")
            if use_official:
                success = self.download_official(db_name)
            else:
                success = self.download_free(db_name)

            results[db_name] = success

        return results

    def check_databases(self) -> dict:
        """
        检查数据库文件是否存在

        Returns:
            dict: 数据库状态
        """
        status = {}

        for db_name in self.databases.keys():
            file_path = self.data_dir / f"{db_name}.mmdb"
            status[db_name] = {
                'exists': file_path.exists(),
                'path': str(file_path),
                'size': file_path.stat().st_size if file_path.exists() else 0
            }

        return status


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='下载 GeoIP 数据库')
    parser.add_argument('--license-key', help='MaxMind 许可证密钥')
    parser.add_argument('--official', action='store_true', help='使用官方源（需要许可证密钥）')
    parser.add_argument('--check', action='store_true', help='检查数据库状态')

    args = parser.parse_args()
    args.license_key = args.license_key or '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'
    print(f'\nMaxMind license_key:{args.license_key}\n')

    downloader = GeoIPDownloader(license_key=args.license_key)

    if args.check:
        # 检查数据库状态
        status = downloader.check_databases()
        print("\n数据库状态:")
        print("-" * 50)
        for db_name, info in status.items():
            status_text = "✓ 存在" if info['exists'] else "✗ 不存在"
            size_mb = info['size'] / 1024 / 1024 if info['size'] > 0 else 0
            print(f"{db_name:20} {status_text:10} {size_mb:8.1f} MB")
        return

    # 下载数据库
    print("开始下载 GeoIP 数据库...")
    print("=" * 60)

    if args.official:
        if not args.license_key:
            print("错误: 使用官方源需要提供 --license-key 参数")
            print("请访问 https://www.maxmind.com/en/geolite2/signup 注册免费账号获取密钥")
            return

        print("使用官方源下载...")
        results = downloader.download_all(use_official=True)
    else:
        print("使用免费源下载...")
        print("注意: 免费源的数据可能不是最新的")
        results = downloader.download_all(use_official=False)

    # 显示结果
    print("\n" + "=" * 60)
    print("下载结果:")
    print("-" * 50)
    for db_name, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"{db_name:20} {status}")

    # 最终状态检查
    print("\n最终状态:")
    print("-" * 50)
    status = downloader.check_databases()
    all_ready = True

    for db_name, info in status.items():
        status_text = "✓ 就绪" if info['exists'] else "✗ 缺失"
        size_mb = info['size'] / 1024 / 1024 if info['size'] > 0 else 0
        print(f"{db_name:20} {status_text:10} {size_mb:8.1f} MB")
        if not info['exists']:
            all_ready = False

    if all_ready:
        print(f"\n🎉 所有数据库已就绪！可以启动 API 服务了。")
        print("运行命令: python main.py")
    else:
        print(f"\n⚠️  部分数据库缺失，请检查下载过程。")


if __name__ == "__main__":
    main()
