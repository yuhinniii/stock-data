# 自动数据生成工作流
# 每天在指定时间运行，自动生成最新市场数据

name: Update Market Data

on:
  schedule:
    # 每天北京时间 8:00、12:00、18:00、22:00 运行
    - cron: '0 0,4,10,14 * * *'
  workflow_dispatch:  # 允许手动触发

jobs:
  update-data:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: 设置 Python 环境
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: 生成市场数据
        run: python scripts/fetch_data.py
          
      - name: 提交更新
        uses: EndBug/add-and-commit@v9
        with:
          message: '自动更新市场数据'
          add: 'data/market-data.json'
