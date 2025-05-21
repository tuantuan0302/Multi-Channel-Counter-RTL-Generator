import re
import shutil

# 读取配置文件，获取8bit和32bit计数器的通道数量
def read_config():
    try:
        with open("./template/def.txt", "r") as f_r1:
            lines = f_r1.readlines()

        ch_num_cnt8 = 0
        ch_num_cnt32 = 0

        for line in lines:
            line2 = re.sub(r'\s+', '', line)
            m = re.search(r'(\w+)=(\d+)', line2)
            if m:
                if m.group(1) == "ch_num_cnt8":
                    ch_num_cnt8 = int(m.group(2))
                elif m.group(1) == "ch_num_cnt32":
                    ch_num_cnt32 = int(m.group(2))

        # 验证配置有效性
        if ch_num_cnt8 == 0 and ch_num_cnt32 == 0:
            raise ValueError("8bit和32bit计数器的通道数不能同时为0")
        if ch_num_cnt8 > 8 or ch_num_cnt32 > 8:
            raise ValueError("计数器通道数不能超过8")

        return ch_num_cnt8, ch_num_cnt32
    except FileNotFoundError:
        raise FileNotFoundError("配置文件 def.txt 未找到，请检查路径是否正确")
    except Exception as e:
        raise e

# 生成 reg_rw.v 文件
def generate_reg_rw(ch_num_cnt8, ch_num_cnt32):
    try:
        with open("reg_rw_out.v", "w") as f_w2:
            # Write module declaration
            f_w2.write("module reg_rw(\n")
            ports = [
                "clk", "xrst", "cs", "rw", "addr", "wdata", "rdata"
            ]

            # Add cnt8 ports
            for i in range(ch_num_cnt8):
                ports.append(f"en8_{i}")
                ports.append(f"ld8_{i}")
                ports.append(f"val8_{i}")
                ports.append(f"cnt8_{i}")

            # Add cnt32 ports
            for i in range(ch_num_cnt32):
                ports.append(f"en32_{i}")
                ports.append(f"cnt32_{i}")

            f_w2.write(",\n".join(ports) + "\n);\n\n")

            # Write input declarations
            inputs = [
                "input\tclk;",
                "input\txrst;",
                "input\tcs;",
                "input\trw;",
                "input\t[7:0]\taddr;",
                "input\t[31:0]\twdata;"
            ]

            # Add cnt8 inputs
            for i in range(ch_num_cnt8):
                inputs.append(f"input\t[7:0]\tcnt8_{i};")

            # Add cnt32 inputs
            for i in range(ch_num_cnt32):
                inputs.append(f"input\t[31:0]\tcnt32_{i};")

            f_w2.write("\n".join(inputs) + "\n\n")

            # Write output declarations
            outputs = [
                "output\t[31:0]\trdata;"
            ]

            # Add cnt8 outputs
            for i in range(ch_num_cnt8):
                outputs.append(f"output\ten8_{i};")
                outputs.append(f"output\tld8_{i};")
                outputs.append(f"output\t[7:0]\tval8_{i};")

            # Add cnt32 outputs
            for i in range(ch_num_cnt32):
                outputs.append(f"output\ten32_{i};")

            f_w2.write("\n".join(outputs) + "\n\n")

            # Write register declarations
            regs = []
            for i in range(5):  # reg00 to reg04
                regs.append(f"reg\t[31:0]\treg0{i};")
            f_w2.write("\n".join(regs) + "\n")

            # Write wire declarations
            wires = []
            for i in range(2):  # reg10 to reg11
                wires.append(f"wire\t[31:0]\treg1{i};")
            for i in range(4):  # reg20 to reg23
                wires.append(f"wire\t[31:0]\treg2{i};")
            f_w2.write("\n".join(wires) + "\n\n")

            # Write write enable wires
            write_wires = []
            for i in range(5):  # w00 to w04
                write_wires.append(f"wire\tw0{i};")
            f_w2.write("\n".join(write_wires) + "\n\n")

            # Write read enable wires
            read_wires = []
            for i in range(5):  # r00 to r04
                read_wires.append(f"wire\tr0{i};")
            for i in range(2):  # r10 to r11
                read_wires.append(f"wire\tr1{i};")
            for i in range(4):  # r20 to r23
                read_wires.append(f"wire\tr2{i};")
            f_w2.write("\n".join(read_wires) + "\n\n")

            # Write write enable assignments
            write_assigns = []
            for i in range(5):  # w00 to w04
                write_assigns.append(f"assign\tw0{i} = cs&rw&(addr==8'h{i:02x});")
            f_w2.write("\n".join(write_assigns) + "\n\n")

            # Write read enable assignments
            read_assigns = []
            for i in range(5):  # r00 to r04
                read_assigns.append(f"assign\tr0{i} = cs&~rw&(addr==8'h{i:02x});")
            for i in range(2):  # r10 to r11
                read_assigns.append(f"assign\tr1{i} = cs&~rw&(addr==8'h1{i:01x});")
            for i in range(4):  # r20 to r23
                read_assigns.append(f"assign\tr2{i} = cs&~rw&(addr==8'h2{i:01x});")
            f_w2.write("\n".join(read_assigns) + "\n\n")

            # Write always block
            f_w2.write("always @(posedge clk or negedge xrst)begin\n")
            f_w2.write("\tif(!xrst)begin\n")
            for i in range(5):  # reg00 to reg04
                f_w2.write(f"\t\treg0{i} <= 0;\n")
            f_w2.write("\tend\n")
            f_w2.write("\telse if(w00) reg00 <= {0,wdata[6-1:0]};\n")
            f_w2.write("\telse if(w01) reg01 <= {0,wdata[6-1:0]};\n")
            f_w2.write("\telse if(w02) reg02 <= {0,wdata[4-1:0]};\n")
            f_w2.write("\telse if(w03) reg03 <= {0,wdata[4*8-1:0]};\n")
            f_w2.write("\telse if(w04) reg04 <= {0,wdata[2*8-1:0]};\n")
            f_w2.write("end\n\n")

            # Write output assignments
            output_assigns = []
            for i in range(ch_num_cnt8):
                output_assigns.append(f"assign\ten8_{i} = reg00[{i}];")
                output_assigns.append(f"assign\tld8_{i} = reg01[{i}];")

            for i in range(ch_num_cnt32):
                output_assigns.append(f"assign\ten32_{i} = reg02[{i}];")

            # Handle val8 assignments based on channel count
            if ch_num_cnt8 >= 4:
                output_assigns.append("assign\t{val8_3,val8_2,val8_1,val8_0}\t= reg03[4*8-1:0];")
            if ch_num_cnt8 >= 6:
                output_assigns.append("assign\t{val8_5,val8_4}\t= reg04[2*8-1:0];")

            # Handle reg10/reg11 assignments based on channel count
            if ch_num_cnt8 >= 4:
                output_assigns.append("assign\treg10\t= {0,cnt8_3,cnt8_2,cnt8_1,cnt8_0};")
            if ch_num_cnt8 >= 6:
                output_assigns.append("assign\treg11\t= {0,cnt8_5,cnt8_4};")

            # Handle cnt32 reg assignments
            for i in range(ch_num_cnt32):
                output_assigns.append(f"assign\treg2{i}\t= cnt32_{i};")

            f_w2.write("\n".join(output_assigns) + "\n\n")

            # Write rdata assignment
            f_w2.write("assign\trdata\t= \n")
            rdata_assigns = []
            for i in range(5):  # r00 to r04
                rdata_assigns.append(f"\t\t  r0{i} ? reg0{i} :")
            for i in range(2):  # r10 to r11
                rdata_assigns.append(f"\t\t  r1{i} ? reg1{i} :")
            for i in range(4):  # r20 to r23
                rdata_assigns.append(f"\t\t  r2{i} ? reg2{i} :")
            rdata_assigns.append("\t\t\t  0;")
            f_w2.write("\n".join(rdata_assigns) + "\n\n")

            f_w2.write("endmodule\n")

    except Exception as e:
        print(f"Error generating reg_rw_out.v: {str(e)}")
        raise


# 生成 cnt_top.v 文件
def generate_cnt_top(ch_num_cnt8, ch_num_cnt32):
    try:
        with open("./template/cnt_top.v", "r") as f_r3, open("cnt_top_out.v", "w") as f_w3:
            lines = f_r3.readlines()

            f_w3.write("module cnt_top(\n")
            f_w3.write("    clk,\n")
            f_w3.write("    xrst,\n")
            f_w3.write("    cs,\n")
            f_w3.write("    rw,\n")
            f_w3.write("    addr,\n")
            f_w3.write("    wdata,\n")
            f_w3.write("    rdata\n")

            # Add counter ports
            for i in range(ch_num_cnt8):
                f_w3.write(f"    , int8_{i}\n")
            for i in range(ch_num_cnt32):
                f_w3.write(f"    , int32_{i}\n")

            f_w3.write(");\n\n")

            f_w3.write("input clk;\n")
            f_w3.write("input xrst;\n")
            f_w3.write("input cs;\n")
            f_w3.write("input rw;\n")
            f_w3.write("input [7:0] addr;\n")
            f_w3.write("input [31:0] wdata;\n")
            f_w3.write("output [31:0] rdata;\n")

            # Output port declarations for 8-bit counters
            for i in range(ch_num_cnt8):
                f_w3.write(f"output int8_{i};\n")
            # Output port declarations for 32-bit counters
            for i in range(ch_num_cnt32):
                f_w3.write(f"output int32_{i};\n")

            f_w3.write("\n")

            # Internal wire declarations for 8-bit counters
            for i in range(ch_num_cnt8):
                f_w3.write(f"wire en8_{i};\n")
                f_w3.write(f"wire ld8_{i};\n")
                f_w3.write(f"wire [7:0] val8_{i};\n")
                f_w3.write(f"wire [7:0] cnt8_{i};\n")

            # Internal wire declarations for 32-bit counters
            for i in range(ch_num_cnt32):
                f_w3.write(f"wire en32_{i};\n")
                f_w3.write(f"wire [31:0] cnt32_{i};\n")

            f_w3.write("\n")

            # reg_rw instance
            f_w3.write("reg_rw REG_RW(\n")
            for i in range(ch_num_cnt8):
                f_w3.write(f"    .en8_{i}(en8_{i}),\n")
                f_w3.write(f"    .ld8_{i}(ld8_{i}),\n")
                f_w3.write(f"    .val8_{i}(val8_{i}),\n")
                f_w3.write(f"    .cnt8_{i}(cnt8_{i}),\n")
            for i in range(ch_num_cnt32):
                f_w3.write(f"    .en32_{i}(en32_{i}),\n")
                f_w3.write(f"    .cnt32_{i}(cnt32_{i}),\n")
            f_w3.write("    .clk(clk),\n")
            f_w3.write("    .xrst(xrst),\n")
            f_w3.write("    .cs(cs),\n")
            f_w3.write("    .rw(rw),\n")
            f_w3.write("    .addr(addr),\n")
            f_w3.write("    .wdata(wdata),\n")
            f_w3.write("    .rdata(rdata)\n")
            f_w3.write(");\n\n")

            # Generate instances of 8-bit counters
            for i in range(ch_num_cnt8):
                f_w3.write(f"cnt8 CNT8_{i}(\n")
                f_w3.write(f"    .clk(clk),\n")
                f_w3.write(f"    .xrst(xrst),\n")
                f_w3.write(f"    .en(en8_{i}),\n")
                f_w3.write(f"    .ld(ld8_{i}),\n")
                f_w3.write(f"    .val(val8_{i}),\n")
                f_w3.write(f"    .cnt(cnt8_{i}),\n")
                f_w3.write(f"    .int(int8_{i})\n")
                f_w3.write(");\n")

            # Generate instances of 32-bit counters
            for i in range(ch_num_cnt32):
                f_w3.write(f"cnt32 CNT32_{i}(\n")
                f_w3.write(f"    .clk(clk),\n")
                f_w3.write(f"    .xrst(xrst),\n")
                f_w3.write(f"    .en(en32_{i}),\n")
                f_w3.write(f"    .cnt(cnt32_{i}),\n")
                f_w3.write(f"    .int(int32_{i})\n")
                f_w3.write(");\n")

            f_w3.write("endmodule\n")

    except FileNotFoundError:
        raise FileNotFoundError("模板文件 cnt_top.v 未找到，请检查路径是否正确")
    except Exception as e:
        raise e

# 复制其他文件
def copy_other_files():
    try:
        shutil.copyfile("./template/cnt8.v", "./cnt8_out.v")
        shutil.copyfile("./template/cnt32.v", "./cnt32_out.v")
    except FileNotFoundError:
        raise FileNotFoundError("模板文件 cnt8.v 或 cnt32.v 未找到，请检查路径是否正确")
    except Exception as e:
        raise e

# 主函数
def main():
    try:
        # 步骤1：读取配置文件
        ch_num_cnt8, ch_num_cnt32 = read_config()
        print(f"配置读取成功: 8bit计数器通道数={ch_num_cnt8}, 32bit计数器通道数={ch_num_cnt32}")

        # 步骤2：生成 reg_rw.v 文件
        generate_reg_rw(ch_num_cnt8, ch_num_cnt32)
        print("reg_rw_out.v 生成成功")

        # 步骤3：生成 cnt_top.v 文件
        generate_cnt_top(ch_num_cnt8, ch_num_cnt32)
        print("cnt_top_out.v 生成成功")

        # 步骤4：复制其他文件
        copy_other_files()
        print("其他文件复制完成")

        print("多通道计数器RTL生成完成！")
    except Exception as e:
        print(f"错误发生: {str(e)}")

if __name__ == "__main__":
    main()