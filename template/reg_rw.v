//__fix__
module reg_rw(
clk
,xrst
,cs
,rw
,addr
,wdata
,rdata
//__cnt8__1//repeat 0 ~ M times
,en8_0
,ld8_0
,val8_0
,cnt8_0
//__cnt32__1//repeat 0 ~ M times
,en32_0
,cnt32_0
//__fix__
);
input	clk;
input	xrst;
input	cs;
input	rw;
input	[7:0]	addr;
input	[31:0]	wdata;
output	[31:0]	rdata;
//__cnt8__1//repeat 0 ~ M times
output	en8_0;
output	ld8_0;
output	[7:0]	val8_0;
input	[7:0]	cnt8_0;
//__cnt32__1//repeat 0 ~ M times
output	en32_0;
input	[31:0]	cnt32_0;

//__cnt8__2//have or no
reg	[31:0]	reg00;
reg	[31:0]	reg01;
//__cnt32__2//have or no
reg	[31:0]	reg02;
//__cnt8__3//have or no or need add a line
reg	[31:0]	reg03;
wire	[31:0]	reg10;
//__cnt32__1//repeat 0 ~ M times
wire	[31:0]	reg20;

//__cnt8__2//have or no
wire	w00;
wire	w01;
//__cnt32__2//have or no
wire	w02;
//__cnt8__3//hove or no or need add a line
wire	w03;

//__cnt8__2//have or no
wire	r00;
wire	r01;
//__cnt32__2//have or no
wire	r02;
//__cnt8__3//have or no or need add a line
wire	r03;
wire	r10;
//__cnt32__1//repeat 0 ~ M times
wire	r20;

//__cnt8__2//have or no
assign	w00 = cs&rw&(addr==8'h00);
assign	w01 = cs&rw&(addr==8'h01);
//__cnt32__2//have or no
assign	w02 = cs&rw&(addr==8'h02);
//__cnt8__3//hove or no or need add a line
assign	w03 = cs&rw&(addr==8'h03);

//__cnt8__2//have or no
assign	r00 = cs&~rw&(addr==8'h00);
assign	r01 = cs&~rw&(addr==8'h01);
//__cnt32__2//have or no
assign	r02 = cs&~rw&(addr==8'h02);
//__cnt8__3//hove or no or need add a line
assign	r03 = cs&~rw&(addr==8'h03);
assign	r10 = cs&~rw&(addr==8'h10);
//__cnt32__1//repeat 0 ~ M times
assign	r20 = cs&~rw&(addr==8'h20);
	
//__fix__
always @(posedge clk or negedge xrst)begin
	if(!xrst)begin
//__cnt8__2//have or no
		reg00 <= 0;
		reg01 <= 0;
//__cnt32__2//have or no
		reg02 <= 0;
//__cnt8__3//hove or no or need add a line
		reg03 <= 0;
//__fix__
	end
//__cnt8__4//have or no or need modify{}content
	else if(w00) reg00 <= {0,wdata[1-1:0]};
	else if(w01) reg01 <= {0,wdata[1-1:0]};
//__cnt32__4//have or no or need modify{}content
	else if(w02) reg02 <= {0,wdata[1-1:0]};
//__cnt8__5//have or no or need modify{}content or add a line
	else if(w03) reg03 <= {0,wdata[1*8-1:0]};
//__fix__
end

//__cnt8__1//repeat 0 ~ M times
assign	en8_0 = reg00[0];
assign	ld8_0 = reg01[0];
//__cnt32__1//repeat 0 ~ M times
assign	en32_0	= reg02[0];
//__cnt8__5//have or no or need modify{}content or add a line
assign	{val8_0}	= reg03[1*8-1:0];
assign	reg10	= {0,cnt8_0};
//__cnt32__1//repeat 0 ~ M times
assign	reg20	= cnt32_0;

//__fix__
assign	rdata	= 
//__cnt8__2//have or no
		  r00 ? reg00 :
		  r01 ? reg01 :
//__cnt32__2//have or no
		  r02 ? reg02 :
//__cnt8__3//hove or no or need add a line
		  r03 ? reg03 :
		  r10 ? reg10 :
//__cnt32__1//repeat 0 ~ M times
		  r20 ? reg20 :
//__fix__
			  0;
endmodule
