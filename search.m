function [ buldumu,x,y ] = search( Matris,a,b )
%FÝND Summary of this function goes here
%   Detailed explanation goes here

[r,c]=size(Matris);
for t=1:20 % Search by spiral
    x=ceil(t*cos(t)/10+a);
    y=ceil(t*sin(t)/10+b);
    if x<=r && y<=c && x>0 && y>0
        if Matris(x,y)==1
            buldumu=1;
            return;
        end
    end
end
buldumu=0;
end

