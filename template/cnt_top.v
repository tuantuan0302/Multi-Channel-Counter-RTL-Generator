//__fix__
module cnt_top(
clk
,xrst
,cs
,rw
,addr
,wdata
,rdata
//__cnt8__
,int8_0
//__cnt32__
,int32_0
//__fix__
);
input	clk;
input	xrst;
input	cs;
input	rw;
input	[7:0]	addr;
input	[31:0]	wdata;
output	[31:0]	rdata;
//__cnt8__
output	int8_0;
//__cnt32__
output	int32_0;

//__cnt8__
wire	en8_0;
wire	ld8_0;
wire	[7:0]	val8_0;
wire	[7:0]	cnt8_0;
//__cnt32__
wire	en32_0;
wire	[31:0]	cnt32_0;

//__fix__
reg_rw REG_RW(
//__cnt8__
	.en8_0	(en8_0	),
	.ld8_0	(ld8_0	),
	.val8_0	(val8_0	),
	.cnt8_0	(cnt8_0	),
//__cnt32__
	.en32_0	(en32_0	),
	.cnt32_0(cnt32_0),
//__fix__
	.clk	(clk	),
	.xrst	(xrst	),
	.cs	(cs	),
	.rw	(rw	),
	.addr	(addr	),
	.wdata	(wdata	),
	.rdata	(rdata	)
);

//__cnt8__
cnt8 CNT8_0(
	.clk	(clk	),
	.xrst	(xrst	),
	.en	(en8_0	),
	.ld	(ld8_0	),
	.val	(val8_0	),
	.cnt	(cnt8_0	),
	.int	(int8_0	)
);

//__cnt32__
cnt32 CNT32_0(
	.clk	(clk	),
	.xrst	(xrst	),
	.en	(en32_0	),
	.cnt	(cnt32_0),
	.int	(int32_0)
);

//__fix__
endmodule
