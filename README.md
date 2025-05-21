# Multi-Channel Counter RTL Generator (MCC-RTLGen)
MCC-RTLGen 是一个基于Python的工具，用于自动生成多通道计数器的Verilog RTL代码。该工具可以根据用户配置文件动态生成包含8位和32位计数器的寄存器读写模块（reg_rw.v）和顶层模块（cnt_top.v）。通过简单的配置文件，用户可以轻松地定义计数器的通道数量，而无需手动修改代码。
MCC-RTLGen/
├── generate_verilog.py       # 主脚本
├── template/
│   ├── def.txt               # 配置文件
│   ├── cnt_top.v             # 顶层模块模板
│   ├── cnt8.v                # 8位计数器模板
│   ├── cnt32.v               # 32位计数器模板
│   ├── reg_rw.v              # 寄存器读写模块模板
├── reg_rw_out.v              # 生成的寄存器读写模块
├── cnt_top_out.v             # 生成的顶层模块
├── cnt8_out.v                # 生成的8位计数器模块
├── cnt32_out.v               # 生成的32位计数器模块
