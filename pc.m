
%% Loading

clear all;
%Read from File
xyloObj = VideoReader('People_5.mp4');
tic % start time
nFrames =xyloObj.NumberOfFrames;

speed=2; %Define Frame rate.
limit=nFrames/speed;


%Load Video to variables as Red Green Blue
for k = 1:speed:nFrames
    ex = read(xyloObj,k);
    tempRgbObj(:,:,:,int16(k/speed)+1) = ex(:,:,:);
%     if k > limit
%         break;
%     end
end;

%% Calculating.
tic
background = tempRgbObj(:,:,:, int16(k/speed)+1);
disk1 = strel('disk',3); % Create Disks    strel - Create morphological structuring element
disk3 = strel('disk',8); % Create Disks    SE = strel('diamond', R) 
disk2 = strel('square',12); % Create Disks
sum_Up=0;
sum_Down=0;
List=[];

for u =1:2:nFrames
    %%Filtering
    curBW=0; % current black white frame
    for j=1:2 % do 'or' between two frames which is next to other one
        k=int16(u/2)+j-1;
        bw3=0;
        subs3=0;
        curRGB = tempRgbObj(:,:,:, k);% current red green blue frame
        
       for i=1:3 % for each color (red green blue) do substraction
            C=curRGB(:,:,i);
            subs=imabsdiff(background(:,:,i),C);
            subs3=subs3+subs;
            bw=subs>30; % thresholding
            bw=imclose(bw,disk1);
            bw3=bw3+bw; % and sum up of them
        end
        bw3=(bw3~=0);
        bw3=imclose(bw3,disk3);
        bw3=imopen(bw3,disk2);
        curBW=curBW+bw3; % do 'or' between two frames
        curBW=(curBW~=0); % convert to binary
    end
    curBW(:,(1:75))=0; % erase noise which is at left of frame
    
    %% Find and Destroy
    
    [r,c] = size(List);
    [L,n] = bwlabel(curBW);    
    
    for i=1:n
        [row,col]=find(L==i);
        if size(row)<1000
            curBW=curBW-(L==i);
        end
    end
    [L,n] = bwlabel(curBW);
    
    i=1;
    while i<=c
        o=List(i);
        x=o.posX+o.hizX;
        y=o.posY+o.hizY;
        [buldumu,yeniX,yeniY] = search(curBW,floor(x),floor(y));
        if buldumu==1
            [rows,cols] = find (L==L(yeniX,yeniY));
            merX=ceil(mean(rows));
            merY=ceil(mean(cols));
            
            if o.giris==1 && merX>144
                sum_Down=sum_Down+1;
                o.giris=2;
            else if o.giris==2 && merX<144
                    sum_Up=sum_Up+1;
                    o.giris=1;
                end
            end
            
            object = struct('posX',merX,'posY',merY,'hizX',merX-o.posX,'hizY',merY-o.posY,'giris',o.giris,'matris',(L==L(yeniX,yeniY)));
            List(i)=object;
            o=object;
            curBW=curBW-object.matris;
            
            
        else
            if o.giris==1 && o.posX>144
                sum_Down=sum_Down+1;
            else if o.giris==2 && o.posX<144
                    sum_Up=sum_Up+1;
                end
            end
            
            List(i)=[];
            c=c-1;
        end
        i=i+1;
    end
    
    %% Adding List
    [L,n] = bwlabel(curBW); % find area which are white group, give a number and assign L
    
    for i=1:n
        [r,c]=find(L==i);
      if length(r) > 1500
        x=ceil(mean(r));%find x koordinate of object
        y=ceil(mean(c));%find y koordinate of object
        objmatrix=(L==i);
        
            if x<144 % object is going from up to down
                giris=1;
            else      % object is going from down to up
                giris=2;
            end
            object = struct('posX',x,'posY',y,'hizX',0,'hizY',0,'giris',giris,'matris',objmatrix);
            List = [List object]; % store object in list
        end
    end
    
    
    %%silinecek
    [row,col] = size(List);
    
    %for red dots
    for i=1:col
        o=List(i);
        curBW(o.posX,o.posY)=1;
        curRGB((o.posX-3:o.posX+3),(o.posY-3:o.posY+3),1)=255;
        curRGB((o.posX-3:o.posX+3),(o.posY-3:o.posY+3),2)=0;
        curRGB((o.posX-3:o.posX+3),(o.posY-3:o.posY+3),3)=0;
    end
    
    curRGB(144,:,3)=255;
    curRGB(144,:,2)=0;
    curRGB(144,:,1)=0;
    
    %figure(3),%title(strcat(int2str(k),' Up:',int2str(sum_Up),' Down:',int2str(sum_Down)));
    figure(1),text(5,134,strcat('Up:',int2str(sum_Up)),'color','green','fontsize',11,'fontweight','bold');
    figure(1),text(5,155,strcat('Down:',int2str(sum_Down)),'color','green','fontsize',11,'fontweight','bold');
    figure(1),imshow(curRGB);
    %     title(k),imtool(curRGB);
    %     title(k),imtool(yedek);
    
end


toc








