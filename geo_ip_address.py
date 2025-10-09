from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import geoip2.database
import geoip2.errors
import ipaddress
import os
from typing import Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# 响应模型
class GeolocationResponse(BaseModel):
    ip: str
    country: Optional[str] = None
    country_code: Optional[str] = None
    province: Optional[str] = None  # 省/州
    city: Optional[str] = None
    postal_code: Optional[str] = None  # 邮政编码
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    isp: Optional[str] = None  # 如果使用 ISP 数据库
    accuracy_radius: Optional[int] = None


class IPRequest(BaseModel):
    ip: str

    @validator('ip')
    def validate_ip(cls, v):
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError:
            raise ValueError('无效的 IP 地址格式')


# 数据库路径配置
GEOIP_DB_PATH = {
    'city': './data/GeoLite2-City.mmdb',
    'country': './data/GeoLite2-Country.mmdb',
    'asn': './data/GeoLite2-ASN.mmdb'  # ISP 信息
}


class GeoIPService:
    def __init__(self):
        self.city_reader = None
        self.country_reader = None
        self.asn_reader = None
        self.load_databases()

    def load_databases(self):
        """加载 GeoIP 数据库"""
        try:
            if os.path.exists(GEOIP_DB_PATH['city']):
                self.city_reader = geoip2.database.Reader(GEOIP_DB_PATH['city'])
                logger.info("城市数据库加载成功")

            if os.path.exists(GEOIP_DB_PATH['country']):
                self.country_reader = geoip2.database.Reader(GEOIP_DB_PATH['country'])
                logger.info("国家数据库加载成功")

            if os.path.exists(GEOIP_DB_PATH['asn']):
                self.asn_reader = geoip2.database.Reader(GEOIP_DB_PATH['asn'])
                logger.info("ASN 数据库加载成功")

        except Exception as e:
            logger.error(f"数据库加载失败: {e}")

    def get_location(self, ip: str) -> GeolocationResponse:
        """获取 IP 地理位置信息"""
        result = GeolocationResponse(ip=ip)

        try:
            # 首先尝试使用城市数据库（包含最详细信息）
            if self.city_reader:
                try:
                    response = self.city_reader.city(ip)

                    # 国家信息
                    if response.country.name:
                        # result.country = response.country.names.get('zh-CN', response.country.name)
                        result.country = response.country.names.get('en', response.country.name)
                        result.country_code = response.country.iso_code

                    # 省/州信息
                    if response.subdivisions.most_specific.name:
                        # result.province = response.subdivisions.most_specific.names.get(
                        #     'zh-CN',
                        #     response.subdivisions.most_specific.name
                        # )
                        result.province = response.subdivisions.most_specific.names.get(
                            'en',
                            response.subdivisions.most_specific.name
                        )

                    # 城市信息
                    if response.city.name:
                        # result.city = response.city.names.get('zh-CN', response.city.name)
                        result.city = response.city.names.get('en', response.city.name)

                    # 邮政编码
                    result.postal_code = response.postal.code

                    # 经纬度
                    if response.location.latitude and response.location.longitude:
                        result.latitude = float(response.location.latitude)
                        result.longitude = float(response.location.longitude)
                        result.accuracy_radius = response.location.accuracy_radius

                    # 时区
                    result.timezone = response.location.time_zone

                except geoip2.errors.AddressNotFoundError:
                    logger.warning(f"城市数据库中未找到 IP: {ip}")

            # 如果城市数据库没有结果，尝试国家数据库
            if not result.country and self.country_reader:
                try:
                    response = self.country_reader.country(ip)
                    # result.country = response.country.names.get('zh-CN', response.country.name)
                    result.country = response.country.names.get('en', response.country.name)
                    result.country_code = response.country.iso_code
                except geoip2.errors.AddressNotFoundError:
                    logger.warning(f"国家数据库中未找到 IP: {ip}")

            # 获取 ISP 信息
            if self.asn_reader:
                try:
                    asn_response = self.asn_reader.asn(ip)
                    result.isp = asn_response.autonomous_system_organization
                except geoip2.errors.AddressNotFoundError:
                    logger.warning(f"ASN 数据库中未找到 IP: {ip}")

        except Exception as e:
            logger.error(f"查询 IP {ip} 时发生错误: {e}")
            raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

        return result

    def close(self):
        """关闭数据库连接"""
        if self.city_reader:
            self.city_reader.close()
        if self.country_reader:
            self.country_reader.close()
        if self.asn_reader:
            self.asn_reader.close()


# 创建服务实例
geo_service = GeoIPService()




"""根据 IP 地址查询地理位置"""
try:
    # 验证 IP 地址格式
    ips = ['46.232.48.60', '117.139.165.184', '74.119.41.6', '123.168.100.202']
    for ip in ips:
        ipaddress.ip_address(ip)

        # print(f'\ndebug info: geo_service.get_location("{ip}")\n', geo_service.get_location(ip))
        geo_result = geo_service.get_location(ip)

        data = geo_result.model_dump()
        print(f"\n🌍 ip: {ip}")
        print(f"🌍 国家: {data.get('country', 'N/A')} ({data.get('country_code', 'N/A')})")
        print(f"🏛️  省/州: {data.get('province', 'N/A')}")
        print(f"🏙️  城市: {data.get('city', 'N/A')}")
        print(f"📮 邮编: {data.get('postal_code', 'N/A')}")
        print(f"📍 坐标: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}")
        print(f"🕐 时区: {data.get('timezone', 'N/A')}")
        print(f"🌐 ISP: {data.get('isp', 'N/A')}")
        print(f"📏 精度半径: {data.get('accuracy_radius', 'N/A')} km")
except ValueError:
    raise HTTPException(status_code=400, detail="无效的 IP 地址格式")



"""应用关闭时释放资源"""
geo_service.close()
