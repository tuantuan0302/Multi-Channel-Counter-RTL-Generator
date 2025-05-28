import re
import shutil


def read_config():
    """读取并验证配置文件"""
    try:
        with open("./template/def.txt", "r") as f:
            config = {}
            for line in f:
                line = re.sub(r'\s+', '', line)
                if match := re.match(r'(\w+)=(\d+)', line):
                    config[match[1]] = int(match[2])

            ch8 = config.get("ch_num_cnt8", 0)
            ch32 = config.get("ch_num_cnt32", 0)

            if not (0 <= ch8 <= 8 and 0 <= ch32 <= 8):
                raise ValueError("通道数范围错误(0-8)")
            if ch8 == 0 and ch32 == 0:
                raise ValueError("8bit和32bit通道不能同时为0")

            return ch8, ch32

    except FileNotFoundError:
        raise FileNotFoundError("配置文件def.txt未找到")
    except Exception as e:
        raise RuntimeError(f"配置错误: {str(e)}")


def generate_reg_rw(ch8, ch32):
    """生成寄存器模块"""
    try:
        with open("./template/reg_rw.v", "r") as src, open("reg_rw_out.v", "w") as dest:
            flags = {'mode': 'fix', 'cnt8_case': 0, 'cnt32_case': 0}

            for line in src:
                if re.search(r"//__fix__", line):
                    flags = {'mode': 'fix', 'cnt8_case': 0, 'cnt32_case': 0}
                    dest.write(line)
                    continue

                if match := re.search(r"//__cnt8__(\d+)", line):
                    flags = {'mode': 'cnt8', 'cnt8_case': int(match.group(1)), 'cnt32_case': 0}
                    continue

                if match := re.search(r"//__cnt32__(\d+)", line):
                    flags = {'mode': 'cnt32', 'cnt8_case': 0, 'cnt32_case': int(match.group(1))}
                    continue

                if flags['mode'] == 'fix':
                    dest.write(line)
                elif flags['mode'] == 'cnt8':
                    if flags['cnt8_case'] == 1 and ch8 > 0:
                        for i in range(ch8):
                            new_line = re.sub(r'_0(\b|\[)', f'_{i}\\1', line)
                            new_line = re.sub(r'\[0\]', f'[{i}]', new_line)
                            dest.write(new_line)
                    elif flags['cnt8_case'] == 2:
                        new_line = re.sub(r'\d+\'d\d+', f"{max(1, ch8)}'d{ch8}", line)
                        dest.write(new_line)
                elif flags['mode'] == 'cnt32':
                    if flags['cnt32_case'] == 1 and ch32 > 0:
                        for i in range(ch32):
                            new_line = re.sub(r'_0(\b|\[)', f'_{i}\\1', line)
                            new_line = re.sub(r'8\'h20', f'8\'h{0x20 + i:02x}', new_line)
                            dest.write(new_line)
                    elif flags['cnt32_case'] == 2:
                        new_line = re.sub(r'\d+\'d\d+', f"{max(1, ch32)}'d{ch32}", line)
                        dest.write(new_line)
                else:
                    dest.write(line)
    except Exception as e:
        raise RuntimeError(f"reg_rw生成失败: {str(e)}")


def generate_cnt_top(ch8, ch32):
    """生成顶层模块"""
    try:
        with open("./template/cnt_top.v", "r") as src, open("cnt_top_out.v", "w") as dest:
            module_line = None
            output_line = None
            wire_line = None
            reg_rw_line = None
            cnt8_instance_line = None
            cnt32_instance_line = None

            for line in src:
                # 处理模块端口行
                if line.strip().startswith("module cnt_top"):
                    module_line = line
                    # 动态插入8bit和32bit端口
                    if ch8 > 1 or ch32 > 1:
                        port_line = "    , int8_0\n"
                        for i in range(1, ch8):
                            port_line += f"    , int8_{i}\n"
                        for i in range(1, ch32):
                            port_line += f"    , int32_{i}\n"
                        module_line = module_line.replace("//__cnt8__", port_line)
                        module_line = module_line.replace("//__cnt32__", "")
                        module_line = module_line.replace("//__fix__", "")
                    dest.write(module_line)
                    continue

                # 处理输出声明行
                if "output" in line and ("int8_0" in line or "int32_0" in line):
                    output_line = line
                    # 动态插入8bit和32bit输出声明
                    if ch8 > 1 or ch32 > 1:
                        output_decl = "output\tint8_0;\n"
                        for i in range(1, ch8):
                            output_decl += f"output\tint8_{i};\n"
                        for i in range(1, ch32):
                            output_decl += f"output\tint32_{i};\n"
                        output_line = output_decl
                    dest.write(output_line)
                    continue

                # 处理wire信号行
                if "wire" in line and ("en8_0" in line or "en32_0" in line):
                    wire_line = line
                    # 动态插入8bit和32bit wire信号
                    if ch8 > 1 or ch32 > 1:
                        wire_decl = "wire\ten8_0;\n"
                        wire_decl += "wire\tld8_0;\n"
                        wire_decl += "wire\t[7:0]\tval8_0;\n"
                        wire_decl += "wire\t[7:0]\tcnt8_0;\n"
                        for i in range(1, ch8):
                            wire_decl += f"wire\ten8_{i};\n"
                            wire_decl += f"wire\tld8_{i};\n"
                            wire_decl += f"wire\t[7:0]\tval8_{i};\n"
                            wire_decl += f"wire\t[7:0]\tcnt8_{i};\n"
                        wire_decl += "wire\ten32_0;\n"
                        wire_decl += "wire\t[31:0]\tcnt32_0;\n"
                        for i in range(1, ch32):
                            wire_decl += f"wire\ten32_{i};\n"
                            wire_decl += f"wire\t[31:0]\tcnt32_{i};\n"
                        wire_line = wire_decl
                    dest.write(wire_line)
                    continue

                # 处理reg_rw模块连接行
                if "reg_rw REG_RW" in line:
                    reg_rw_line = line
                    # 动态插入8bit和32bit端口连接
                    if ch8 > 1 or ch32 > 1:
                        reg_rw_conn = "reg_rw REG_RW(\n"
                        reg_rw_conn += "\t.en8_0\t(en8_0\t),\n"
                        reg_rw_conn += "\t.ld8_0\t(ld8_0\t),\n"
                        reg_rw_conn += "\t.val8_0\t(val8_0\t),\n"
                        reg_rw_conn += "\t.cnt8_0\t(cnt8_0\t),\n"
                        for i in range(1, ch8):
                            reg_rw_conn += f"\t.en8_{i}\t(en8_{i}\t),\n"
                            reg_rw_conn += f"\t.ld8_{i}\t(ld8_{i}\t),\n"
                            reg_rw_conn += f"\t.val8_{i}\t(val8_{i}\t),\n"
                            reg_rw_conn += f"\t.cnt8_{i}\t(cnt8_{i}\t),\n"
                        reg_rw_conn += "\t.en32_0\t(en32_0\t),\n"
                        reg_rw_conn += "\t.cnt32_0\t(cnt32_0\t),\n"
                        for i in range(1, ch32):
                            reg_rw_conn += f"\t.en32_{i}\t(en32_{i}\t),\n"
                            reg_rw_conn += f"\t.cnt32_{i}\t(cnt32_{i}\t),\n"
                        reg_rw_conn += "\t.clk\t(clk\t),\n"
                        reg_rw_conn += "\t.xrst\t(xrst\t),\n"
                        reg_rw_conn += "\t.cs\t(cs\t),\n"
                        reg_rw_conn += "\t.rw\t(rw\t),\n"
                        reg_rw_conn += "\t.addr\t(addr\t),\n"
                        reg_rw_conn += "\t.wdata\t(wdata\t),\n"
                        reg_rw_conn += "\t.rdata\t(rdata\t)\n);\n"
                        reg_rw_line = reg_rw_conn
                    dest.write(reg_rw_line)
                    continue

                # 处理8bit计数器实例化行
                if "cnt8 CNT8_0" in line:
                    cnt8_instance_line = line
                    # 动态插入8bit计数器实例
                    if ch8 > 1:
                        cnt8_instances = ""
                        for i in range(ch8):
                            cnt8_instances += f"""
cnt8 CNT8_{i} (
    .clk(clk),
    .xrst(xrst),
    .en(en8_{i}),
    .ld(ld8_{i}),
    .val(val8_{i}),
    .cnt(cnt8_{i}),
    .int(int8_{i})
);\n\n"""
                        cnt8_instance_line = cnt8_instances
                    dest.write(cnt8_instance_line)
                    continue

                # 处理32bit计数器实例化行
                if "cnt32 CNT32_0" in   在 line:
                    cnt32_instance_line = line
                    # 动态插入32bit计数器实例
                    if ch32 > 1:
                        cnt32_instances = ""
                        for i in   在 range(ch32):
                            cnt32_instances += f"""
cnt32 CNT32_{i} (
    .clk(clk),
    .xrst(xrst),
    .en(en32_{i}),
    .cnt(cnt32_{i}),
    .int(int32_{i})
);\n\n"""
                        cnt32_instance_line = cnt32_instances
                    dest.write(cnt32_instance_line)
                    continue

                dest.write(line)
    except Exception as e:
        raise RuntimeError(f"cnt_top生成失败: {str(e)}")


def copy_templates():
    """复制基础模块"""
    try:
        shutil.copy("./template/cnt8.v", "cnt8_out.v")
        shutil.copy("./template/cnt32.v", "cnt32_out.v")
    except Exception as e:   除了例外e：
        raise RuntimeError(f"模板复制失败: {str(e)}")


def main():
    try:   试一试:
        ch8, ch32 = read_config()
        generate_reg_rw(ch8, ch32)
        generate_cnt_top(ch8, ch32)
        copy_templates()
        print("生成成功！输出文件：")
        print("- reg_rw_out.v\n- cnt_top_out.v\n- cnt8_out.v\n- cnt32_out.v")
    except Exception as e:
        print(f"错误: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
