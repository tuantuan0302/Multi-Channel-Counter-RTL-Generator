# Multi-Channel Counter RTL Generator (MCC-RTLGen)

## Introduction

**MCC-RTLGen** is a Python-based tool designed to automatically generate Verilog RTL code for multi-channel counters. This tool dynamically generates the register read/write module (`reg_rw.v`) and the top-level module (`cnt_top.v`) based on user-defined configurations. With a simple configuration file, users can easily specify the number of 8-bit and 32-bit counter channels without manually modifying the code.

## Project Structure
MCC-RTLGen/
├── generate_rtl.py       # 主脚本
├── template/
│   ├── def.txt               # 配置文件
│   ├── cnt_top.v             # 顶层模块模板
│   ├── cnt8.v                # 8位计数器模板
│   ├── cnt32.v               # 32位计数器模板
│   ├── reg_rw_out.v          # 寄存器读写模块模板
├── reg_rw_out.v              # 生成的寄存器读写模块
├── cnt_top_out.v             # 生成的顶层模块
├── cnt8_out.v                # 生成的8位计数器模块
├── cnt32_out.v               # 生成的32位计数器模块

## Usage

### Prerequisites
Ensure you have Python 3 installed. This project does not require any external Python libraries.

### Configuration File
Create or edit the `def.txt` file in the `template/` directory to define the number of 8-bit and 32-bit counter channels. Example:
ch_num_cnt8=6
ch_num_cnt32=4



#PS
The generated files will be saved in the current directory:

    reg_rw_out.v: Register read/write module
    cnt_top_out.v: Top-level module
    cnt8_out.v and cnt32_out.v: 8-bit and 32-bit counter modules (copied from template files)

# For more detailed information and project notes, please visit the MCC-RTLGen project page on Yuque.

## https://www.yuque.com/yuqueyonghup60ypd/tuan_ic/qkv9dfpa28gxc3x4#
