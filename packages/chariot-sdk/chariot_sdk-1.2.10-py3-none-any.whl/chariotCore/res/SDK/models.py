from typing import List
from pydantic import BaseModel


#   插件定义文件结构，用于自动生成插件
class PLUGIN_CONSTRUCTION(BaseModel):
    plugin_spec_version: str = "v2"
    name: str
    version: str
    hot_update: bool = True
    auto_generate: bool = True
    title: dict
    description: dict = None
    vendor: str = "chariot"
    tags: List[str] = None
    connection: dict = None
    actions: dict


#   执行数据验证类，用于传入插件数据的验证
class PLUGIN_TEST_MODEL(BaseModel):
    version: str
    type: str
    body: dict
