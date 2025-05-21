//__fix__
module cnt8(
clk,
xrst,
en,
ld,
val,
cnt,
int
);
input	clk;
input	xrst;
input	en;
input	ld;
input	[7:0]	val;
output	[7:0]	cnt;
output	int;

reg	[7:0]	cnt_val;
reg	[7:0]	cnt;
always@(posedge clk or negedge xrst)begin
	if(!xrst)
		cnt_val <= 0;
	else if(ld)
		cnt_val <= val;
end
always@(posedge clk or negedge xrst)begin
	if(!xrst)
		cnt <= 0;
	else if(en)
		if(cnt>=cnt_val)
			cnt <= 0;
		else
			cnt <= cnt+1;
	else
		cnt <= 0;
end

assign	int = en&(cnt==cnt_val);

endmodule
