`timescale 1ns/1ns

module tb_top;

parameter CYCLE = 100;
reg	clk;
reg	xrst;
reg	cs;
reg	rw;
reg	[7:0]	addr;
reg	[31:0]	wdata;
wire	[31:0]	rdata;

//RTL instance
cnt_top cnt_top(
	.clk	(clk  ),
	.xrst	(xrst ),
	.cs	(cs   ),
	.rw	(rw   ),
	.addr	(addr ),
	.wdata	(wdata),
	.rdata	(rdata)
);

//generate clk
initial begin
	clk = 0;
	forever begin
		#(CYCLE/2);
		clk = 1;
		#(CYCLE/2);
		clk = 0;
	end
end

//generate reset
initial begin
	xrst = 1;
	#(3*CYCLE);
	xrst = 0;
	#(5*CYCLE);
	xrst = 1;
end

integer i;
//generate input
initial	begin
	cs = 0;
	rw = 0;
	addr = 0;
	wdata = 0;
	wait(!xrst);
	wait(xrst);
	#CYCLE;
	reg_wr('h03,'h02);
	reg_wr('h03,'h0302);
	reg_wr('h03,'h040302);
	reg_wr('h03,'h040302);
	reg_wr('h03,'h05040302);
	reg_wr('h04,'h06);
	reg_wr('h04,'h0706);
	reg_wr('h04,'h080706);
	reg_wr('h04,'h09080706);
	reg_wr('h01,'h1);
	reg_wr('h01,'h2);
	reg_wr('h01,'h4);
	reg_wr('h01,'h8);
	reg_wr('h01,'h10);
	reg_wr('h01,'h20);
	reg_wr('h01,'h40);
	reg_wr('h01,'h80);
	reg_wr('h01,'h00);
	reg_wr('h00,'h1);
	reg_wr('h00,'h3);
	reg_wr('h00,'h7);
	reg_wr('h00,'hF);
	reg_wr('h00,'h1F);
	reg_wr('h00,'h3F);
	reg_wr('h00,'h7F);
	reg_wr('h00,'hFF);
	reg_wr('h02,'h1);
	reg_wr('h02,'h3);
	reg_wr('h02,'h7);
	reg_wr('h02,'hF);
	reg_wr('h02,'h1F);
	reg_wr('h02,'h3F);
	reg_wr('h02,'h7F);
	reg_wr('h02,'hFF);
	#(1000*CYCLE);
	$display($time,"sim end!!!");
	$finish;
end

task reg_wr;
input	[7:0]	in_addr;
input	[31:0]	in_data;
begin
	@(posedge clk);
	#1;
	cs = 1;
	rw = 1;
	addr = in_addr;
	wdata = in_data;
	@(posedge clk);
	#1;
	cs = 0;
	rw = 0;
	addr = 0;
	wdata = 0;
end
endtask

task reg_rd;
input	[7:0]	in_addr;
input	[31:0]	out_data;
begin
	@(posedge clk);
	#1;
	cs = 1;
	rw = 0;
	addr = in_addr;
	out_data = rdata;
	@(posedge clk);
	#1;
	cs = 0;
	rw = 0;
	addr = 0;
	out_data = 0;
end
endtask
endmodule
