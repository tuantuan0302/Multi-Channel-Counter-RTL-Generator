module cnt_top(
    clk,
    xrst,
    cs,
    rw,
    addr,
    wdata,
    rdata
    , int8_0
    , int8_1
    , int8_2
    , int8_3
    , int8_4
    , int8_5
    , int32_0
    , int32_1
    , int32_2
    , int32_3
);

input clk;
input xrst;
input cs;
input rw;
input [7:0] addr;
input [31:0] wdata;
output [31:0] rdata;
output int8_0;
output int8_1;
output int8_2;
output int8_3;
output int8_4;
output int8_5;
output int32_0;
output int32_1;
output int32_2;
output int32_3;

wire en8_0;
wire ld8_0;
wire [7:0] val8_0;
wire [7:0] cnt8_0;
wire en8_1;
wire ld8_1;
wire [7:0] val8_1;
wire [7:0] cnt8_1;
wire en8_2;
wire ld8_2;
wire [7:0] val8_2;
wire [7:0] cnt8_2;
wire en8_3;
wire ld8_3;
wire [7:0] val8_3;
wire [7:0] cnt8_3;
wire en8_4;
wire ld8_4;
wire [7:0] val8_4;
wire [7:0] cnt8_4;
wire en8_5;
wire ld8_5;
wire [7:0] val8_5;
wire [7:0] cnt8_5;
wire en32_0;
wire [31:0] cnt32_0;
wire en32_1;
wire [31:0] cnt32_1;
wire en32_2;
wire [31:0] cnt32_2;
wire en32_3;
wire [31:0] cnt32_3;

reg_rw REG_RW(
    .en8_0(en8_0),
    .ld8_0(ld8_0),
    .val8_0(val8_0),
    .cnt8_0(cnt8_0),
    .en8_1(en8_1),
    .ld8_1(ld8_1),
    .val8_1(val8_1),
    .cnt8_1(cnt8_1),
    .en8_2(en8_2),
    .ld8_2(ld8_2),
    .val8_2(val8_2),
    .cnt8_2(cnt8_2),
    .en8_3(en8_3),
    .ld8_3(ld8_3),
    .val8_3(val8_3),
    .cnt8_3(cnt8_3),
    .en8_4(en8_4),
    .ld8_4(ld8_4),
    .val8_4(val8_4),
    .cnt8_4(cnt8_4),
    .en8_5(en8_5),
    .ld8_5(ld8_5),
    .val8_5(val8_5),
    .cnt8_5(cnt8_5),
    .en32_0(en32_0),
    .cnt32_0(cnt32_0),
    .en32_1(en32_1),
    .cnt32_1(cnt32_1),
    .en32_2(en32_2),
    .cnt32_2(cnt32_2),
    .en32_3(en32_3),
    .cnt32_3(cnt32_3),
    .clk(clk),
    .xrst(xrst),
    .cs(cs),
    .rw(rw),
    .addr(addr),
    .wdata(wdata),
    .rdata(rdata)
);

cnt8 CNT8_0(
    .clk(clk),
    .xrst(xrst),
    .en(en8_0),
    .ld(ld8_0),
    .val(val8_0),
    .cnt(cnt8_0),
    .int(int8_0)
);
cnt8 CNT8_1(
    .clk(clk),
    .xrst(xrst),
    .en(en8_1),
    .ld(ld8_1),
    .val(val8_1),
    .cnt(cnt8_1),
    .int(int8_1)
);
cnt8 CNT8_2(
    .clk(clk),
    .xrst(xrst),
    .en(en8_2),
    .ld(ld8_2),
    .val(val8_2),
    .cnt(cnt8_2),
    .int(int8_2)
);
cnt8 CNT8_3(
    .clk(clk),
    .xrst(xrst),
    .en(en8_3),
    .ld(ld8_3),
    .val(val8_3),
    .cnt(cnt8_3),
    .int(int8_3)
);
cnt8 CNT8_4(
    .clk(clk),
    .xrst(xrst),
    .en(en8_4),
    .ld(ld8_4),
    .val(val8_4),
    .cnt(cnt8_4),
    .int(int8_4)
);
cnt8 CNT8_5(
    .clk(clk),
    .xrst(xrst),
    .en(en8_5),
    .ld(ld8_5),
    .val(val8_5),
    .cnt(cnt8_5),
    .int(int8_5)
);
cnt32 CNT32_0(
    .clk(clk),
    .xrst(xrst),
    .en(en32_0),
    .cnt(cnt32_0),
    .int(int32_0)
);
cnt32 CNT32_1(
    .clk(clk),
    .xrst(xrst),
    .en(en32_1),
    .cnt(cnt32_1),
    .int(int32_1)
);
cnt32 CNT32_2(
    .clk(clk),
    .xrst(xrst),
    .en(en32_2),
    .cnt(cnt32_2),
    .int(int32_2)
);
cnt32 CNT32_3(
    .clk(clk),
    .xrst(xrst),
    .en(en32_3),
    .cnt(cnt32_3),
    .int(int32_3)
);
endmodule
