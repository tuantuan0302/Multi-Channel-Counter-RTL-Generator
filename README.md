# Multi-Channel Counter RTL Generator (MCC-RTLGen)

## Introduction

**MCC-RTLGen** is a Python-based tool designed to automatically generate Verilog RTL code for multi-channel counters. This tool dynamically generates the register read/write module (`reg_rw.v`) and the top-level module (`cnt_top.v`) based on user-defined configurations. With a simple configuration file, users can easily specify the number of 8-bit and 32-bit counter channels without manually modifying the code.

## Project Structure
MCC-RTLGen/
├── generate_verilog.py       # Main script
├── template/
│   ├── def.txt               # Configuration file
│   ├── cnt_top.v             # Top-level module template
│   ├── cnt8.v                # 8-bit counter template
│   ├── cnt32.v               # 32-bit counter template
│   ├── reg_rw.v              # Register read/write module template
│   ├── reg_rw_out.v              # Generated register read/write module
├── cnt_top_out.v             # Generated top-level module
├── cnt8_out.v                # Generated 8-bit counter module
├── cnt32_out.v               # Generated 32-bit counter module

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
