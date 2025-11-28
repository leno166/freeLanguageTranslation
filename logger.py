"""
@文件: logging.py
@作者: 雷小鸥
@日期: 2025/11/28 12:35
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import sys
import logging

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)