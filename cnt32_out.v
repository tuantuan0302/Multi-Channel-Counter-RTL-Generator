//__fix__
module cnt32(
clk,
xrst,
en,
cnt,
int
);
input	clk;
input	xrst;
input	en;
output	[31:0]	cnt;
output	int;

reg	[31:0]	cnt;
always@(posedge clk or negedge xrst)begin
	if(!xrst)
		cnt <= 0;
	else if(en)
		cnt <= cnt+1;
	else
		cnt <= 0;
end

assign	int = en&(cnt==32'hFFFF_FFFF);

endmodule
