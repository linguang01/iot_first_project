# -
这是我迈出的一些步
```markdown
# 物联网环境数据采集与存储系统
基于 MQTT 协议的物联网数据采集闭环系统：模拟多设备传感器数据上报，实现"设备模拟 → 数据传输 → 实时接收 → 数据落盘（JSONL + SQLite）"全链路功能。
## 项目架构
```
sensor_simulator.py ──publish──> MQTT Broker (broker.emqx.io)
                                        │
                                        ▼
                              data_collector.py
                              ├── 保存 JSONL 文件 (data/目录)
                              └── 写入 SQLite 数据库 (sensor_data.db)
```
## 项目结构
```
iot_first_project/
├── publisher.py         # 第2天：MQTT 发布者（入门练习）
├── subscriber.py        # 第3天：MQTT 订阅者（入门练习）
├── sensor_simulator.py  # 传感器数据模拟器
├── data_collector.py    # 数据采集与落盘
├── data/                # JSONL 数据文件
└── sensor_data.db       # SQLite 数据库
```
## 运行方式
```bash
# 1. 安装依赖
pip install paho-mqtt
# 2. 终端1：启动传感器模拟器（每5秒上报一条数据）
python sensor_simulator.py
# 3. 终端2：启动数据采集器（接收并落盘）
python data_collector.py
# 4. 查看数据
# - JSONL：打开 data/日期.jsonl
# - SQLite：用 DB Browser for SQLite 打开 sensor_data.db
```
## 踩坑记录
| 错误 | 错误思路 | 正确思路 |
|------|---------|---------|
| import 模拟器拿数据 | 以为模块间能直接共享变量 | 独立进程只能通过 MQTT 通信，数据入口是 on_message 回调 |
| SQL 建表报语法错误 | 把 Python 习惯带进 SQL | SQL 最后一个字段后不加逗号 |
| INSERT 占位符不匹配 | 列名和参数分开写忘了对齐 | 列名、?、参数三者数量一一对应 |
| 数据库启动时插入后关闭 | 把入库当成一次性任务 | 入库放回调里，每收到一条消息执行一次 |
| paho-mqtt 2.x 报 API 版本错误 | 参考的是 1.x 旧教程 | 用 mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, ...) |
## 后续计划
- [ ] 数据可视化（Matplotlib 趋势图）
- [ ] Flask Web API 查询接口
- [ ] 多设备管理与状态监控
```
---
