module reg_rw(
clk,
xrst,
cs,
rw,
addr,
wdata,
rdata,
en8_0,
ld8_0,
val8_0,
cnt8_0,
en8_1,
ld8_1,
val8_1,
cnt8_1,
en8_2,
ld8_2,
val8_2,
cnt8_2,
en8_3,
ld8_3,
val8_3,
cnt8_3,
en8_4,
ld8_4,
val8_4,
cnt8_4,
en8_5,
ld8_5,
val8_5,
cnt8_5,
en32_0,
cnt32_0,
en32_1,
cnt32_1,
en32_2,
cnt32_2,
en32_3,
cnt32_3
);

input	clk;
input	xrst;
input	cs;
input	rw;
input	[7:0]	addr;
input	[31:0]	wdata;
input	[7:0]	cnt8_0;
input	[7:0]	cnt8_1;
input	[7:0]	cnt8_2;
input	[7:0]	cnt8_3;
input	[7:0]	cnt8_4;
input	[7:0]	cnt8_5;
input	[31:0]	cnt32_0;
input	[31:0]	cnt32_1;
input	[31:0]	cnt32_2;
input	[31:0]	cnt32_3;

output	[31:0]	rdata;
output	en8_0;
output	ld8_0;
output	[7:0]	val8_0;
output	en8_1;
output	ld8_1;
output	[7:0]	val8_1;
output	en8_2;
output	ld8_2;
output	[7:0]	val8_2;
output	en8_3;
output	ld8_3;
output	[7:0]	val8_3;
output	en8_4;
output	ld8_4;
output	[7:0]	val8_4;
output	en8_5;
output	ld8_5;
output	[7:0]	val8_5;
output	en32_0;
output	en32_1;
output	en32_2;
output	en32_3;

reg	[31:0]	reg00;
reg	[31:0]	reg01;
reg	[31:0]	reg02;
reg	[31:0]	reg03;
reg	[31:0]	reg04;
wire	[31:0]	reg10;
wire	[31:0]	reg11;
wire	[31:0]	reg20;
wire	[31:0]	reg21;
wire	[31:0]	reg22;
wire	[31:0]	reg23;

wire	w00;
wire	w01;
wire	w02;
wire	w03;
wire	w04;

wire	r00;
wire	r01;
wire	r02;
wire	r03;
wire	r04;
wire	r10;
wire	r11;
wire	r20;
wire	r21;
wire	r22;
wire	r23;

assign	w00 = cs&rw&(addr==8'h00);
assign	w01 = cs&rw&(addr==8'h01);
assign	w02 = cs&rw&(addr==8'h02);
assign	w03 = cs&rw&(addr==8'h03);
assign	w04 = cs&rw&(addr==8'h04);

assign	r00 = cs&~rw&(addr==8'h00);
assign	r01 = cs&~rw&(addr==8'h01);
assign	r02 = cs&~rw&(addr==8'h02);
assign	r03 = cs&~rw&(addr==8'h03);
assign	r04 = cs&~rw&(addr==8'h04);
assign	r10 = cs&~rw&(addr==8'h10);
assign	r11 = cs&~rw&(addr==8'h11);
assign	r20 = cs&~rw&(addr==8'h20);
assign	r21 = cs&~rw&(addr==8'h21);
assign	r22 = cs&~rw&(addr==8'h22);
assign	r23 = cs&~rw&(addr==8'h23);

always @(posedge clk or negedge xrst)begin
	if(!xrst)begin
		reg00 <= 0;
		reg01 <= 0;
		reg02 <= 0;
		reg03 <= 0;
		reg04 <= 0;
	end
	else if(w00) reg00 <= {0,wdata[6-1:0]};
	else if(w01) reg01 <= {0,wdata[6-1:0]};
	else if(w02) reg02 <= {0,wdata[4-1:0]};
	else if(w03) reg03 <= {0,wdata[4*8-1:0]};
	else if(w04) reg04 <= {0,wdata[2*8-1:0]};
end

assign	en8_0 = reg00[0];
assign	ld8_0 = reg01[0];
assign	en8_1 = reg00[1];
assign	ld8_1 = reg01[1];
assign	en8_2 = reg00[2];
assign	ld8_2 = reg01[2];
assign	en8_3 = reg00[3];
assign	ld8_3 = reg01[3];
assign	en8_4 = reg00[4];
assign	ld8_4 = reg01[4];
assign	en8_5 = reg00[5];
assign	ld8_5 = reg01[5];
assign	en32_0 = reg02[0];
assign	en32_1 = reg02[1];
assign	en32_2 = reg02[2];
assign	en32_3 = reg02[3];
assign	{val8_3,val8_2,val8_1,val8_0}	= reg03[4*8-1:0];
assign	{val8_5,val8_4}	= reg04[2*8-1:0];
assign	reg10	= {0,cnt8_3,cnt8_2,cnt8_1,cnt8_0};
assign	reg11	= {0,cnt8_5,cnt8_4};
assign	reg20	= cnt32_0;
assign	reg21	= cnt32_1;
assign	reg22	= cnt32_2;
assign	reg23	= cnt32_3;

assign	rdata	= 
		  r00 ? reg00 :
		  r01 ? reg01 :
		  r02 ? reg02 :
		  r03 ? reg03 :
		  r04 ? reg04 :
		  r10 ? reg10 :
		  r11 ? reg11 :
		  r20 ? reg20 :
		  r21 ? reg21 :
		  r22 ? reg22 :
		  r23 ? reg23 :
			  0;

endmodule
