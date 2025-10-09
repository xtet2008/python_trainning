from pydantic import BaseModel
from typing import Optional
import geoip2.database
import geoip2.errors
from pathlib import Path
import logging
from fastapi import HTTPException

# logger = logging.getLogger(__name__)


class GeolocationService:
    def __init__(self, db_path: str = "data/GeoLite2-City.mmdb"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"GeoIP 数据库文件不存在: {self.db_path}")

        # 初始化数据库读取器
        self.reader = geoip2.database.Reader(str(self.db_path))
        print(f"GeoIP 数据库已加载: {self.db_path}")
        # logger.info(f"GeoIP 数据库已加载: {self.db_path}")

    def get_location(self, ip_address: str) -> dict:
        """
        根据 IP 地址获取地理位置信息
        """
        try:
            # 查询 IP 地址
            response = self.reader.city(ip_address)

            # 提取位置信息
            location_data = {
                "ip_address": ip_address,
                "country": response.country.name,
                "country_code": response.country.iso_code,
                "city": response.city.name,
                "subdivision": None,
                "subdivision_code": None,
                "postal_code": response.postal.code,
                "latitude": float(response.location.latitude) if response.location.latitude else None,
                "longitude": float(response.location.longitude) if response.location.longitude else None,
                "timezone": response.location.time_zone,
                "success": True,
                "message": "查询成功"
            }

            # 获取省份/州信息（取第一个subdivision）
            if response.subdivisions:
                subdivision = response.subdivisions[0]
                location_data["subdivision"] = subdivision.name
                location_data["subdivision_code"] = subdivision.iso_code

            return location_data

        except geoip2.errors.AddressNotFoundError:
            return {
                "ip_address": ip_address,
                "success": False,
                "message": "IP 地址未找到对应的地理位置信息"
            }
        except geoip2.errors.GeoIP2Error as e:
            return {
                "ip_address": ip_address,
                "success": False,
                "message": f"GeoIP 查询错误: {str(e)}"
            }
        except Exception as e:
            # logger.error(f"查询 IP {ip_address} 时发生错误: {str(e)}")
            print(f"查询 IP {ip_address} 时发生错误: {str(e)}")
            return {
                "ip_address": ip_address,
                "success": False,
                "message": f"查询失败: {str(e)}"
            }

    def get_locations_batch(self, ip_addresses: list[str]) -> list[dict]:
        """
        批量查询多个 IP 地址的地理位置信息
        """
        results = []
        for ip in ip_addresses:
            result = self.get_location(ip)
            results.append(result)
        return results

    def close(self):
        """
        关闭数据库连接
        """
        if hasattr(self, 'reader'):
            self.reader.close()

    def __del__(self):
        self.close()


class LocationResponse(BaseModel):
    ip_address: str
    country: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    subdivision: Optional[str] = None  # 省/州
    subdivision_code: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    isp: Optional[str] = None
    success: bool
    message: Optional[str] = None



"""根据 IP 地址查询地理位置"""
geo_service = GeolocationService()

try:
    # 验证 IP 地址格式
    ips = ['115.171.79.197', '174.138.224.239', '122.177.103.173', '151.82.133.200', '70.27.140.156', '103.224.173.28', '192.168.0.230']
    for ip in ips:
        geo_result = geo_service.get_location(ip)
        # result = LocationResponse(**geo_result)
        print(f'\ndebug info: geo_service.get_location("{ip}")\n', geo_result)
except ValueError:
    raise HTTPException(status_code=400, detail="无效的 IP 地址格式")

geo_service.close()
# logger.info("地理位置服务已关闭")
print("地理位置服务已关闭")

