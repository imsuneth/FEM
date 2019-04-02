close all
clear all 
clc
format long

%=================PROBLEM DEFINITION===========================

L=[2 1 2]; %length of each element in m
BC=[1 2 3 10 11 12];%Boundary conditions (type the nodes in ascending order)
Load_applied_dof=4;

Load_vector=[0; 0; 0 ; 1; 0; 0; 0; 0; 0; 0; 0; 0]; %input the external load vector
noe=3;%number of elements
ndofpn=3; %number of degrees of freedoms per node
nonpe=2; %number of nodes per element
tdof=12;
ECM=[1 2 3; 2 3 4]; % element connectivity (Columns represent element number)
angle=[pi/2 0 -pi/2]; %In radians
nIP=6; % number of integration points
if nIP==3
    wh=[1/3 4/3 1/3];
    x=[-1 0 1];
elseif nIP==4
    wh=[5/6 1/6 1/6 5/6];
    x=[-1 -0.447214 0.447214 1];
elseif nIP==5
    wh=[1/10 49/90 32/45 49/90 1/10];
    x=[-1 -0.654654 0 0.654654 1];
elseif nIP==6
    wh=[0.066667 0.378475 0.554858 0.554858 0.378475 0.066667];%weights for each integral point
    x=[-1 -0.765055 -0.285232 0.285232 0.765055 1]; %integral points locations
end
%............Fiber section...................................

width=0.4; %width of beam in m
d=0.4; %depth of beam in m
I=(d^3)*width/12;%Second moment of area about centeroidal axis
A=d*width; %cross sectional area

nof=20; %number of fibers in y direction
nofx=20; %number of fibers in x direction

Afib=(width/nofx)*(d/nof); %Area of a fiber




%=================DATA FOR ITERATIONS===============================

displacement_step=0.00001;%Displacement increment in m (Put with the sign)
displacement_steps=50000;
max_i=100;
max_z=1000;

....Newton raphson convergence criteria....
tol_force_i=10^(-5);
tol_Energy_i=10^(-3);

%....Section level convergence criteria.....
tol_force_z=10^(-10);





%===============MATERIAL MODELS=======================

%...........unconfined concrete properties.......... 
cover=0.025;%in m
fc_dash= -42800; %in Kpa
ec_dash= -0.002;
npop=0.8+(-fc_dash*0.001/17);
E=fc_dash*((npop-1+(0/ec_dash)^(npop*1))*(npop/ec_dash)-npop*(0/ec_dash)*(npop*1*(0/ec_dash)^(npop*1-1)*(1/ec_dash)))/(npop-1+(0/ec_dash)^(npop*1))^2;

axial_load=[0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0; 0]; %axial load applied

%.........Calculation of fcc'..........

%input parameters
d_hoopbars=4.76; %in mm
bc=6*25.4+9.5+4.76; % hoop bar centre to centre distance along x-long side in mm
dc=2.5*25.4+9.5+4.76; % hoop bar centre to centre distance along y-short side in mm
sigmaw=((2*25.4)^2)*6+((2.5*25.4)^2)*2;
s=2*25.4;
s_dash=s-4.76;
Ro_cc=8*71/(bc*dc);
Ke=(1-sigmaw/(6*bc*dc))*(1-s_dash/(2*bc))*(1-s_dash/(2*dc));
Asx=35.59;
Asy=35.59;
fyh=434;%yield strength of hoop bars in MPa

%calculation
Ro_y=Asy/(s*dc);
Ro_x=Asx/(s*bc);
f_dashlx=Ke*Ro_x*fyh;
f_dashly=Ke*Ro_y*fyh;
confining_stress_ratio_1=f_dashlx/(-fc_dash*0.001);
confining_stress_ratio_2=f_dashly/(-fc_dash*0.001);
fcc_dash=1*fc_dash; %kPa

%parameters for confined curve
E_cc=ec_dash*(1+5*((fcc_dash/fc_dash)-1));
Ec=(5000*(-fc_dash*0.001)^0.5)*1000;
Esec=fcc_dash/E_cc;
r=Ec/(Ec-Esec);
E_initial_confined=((r-1+(0/E_cc)^r)*(fcc_dash*r/E_cc)-(fcc_dash*(0/E_cc)*r*r*(0/E_cc^2)))/(r-1+(0/E_cc)^r)^2;
% fc_crack=(0.33*(-fc_dash*10^-3)^0.5)*1000;
fc_crack=0.5*1000;
Ecr=Ec;
ec_crack=fc_crack/Ecr; 
%----------Reinforcement details-----------
Esteel=[200000000 200000000]; %Esteelof each steel layer
Strain_hardening=0.03;
yield_strain=[0.0023 0.0023];%yield strain of each steel layer
% %top
% ntop=4;
% dtop=0.020;
% ytop=d/2-0.025-(dtop/2);
% Atop=(pi*ntop*dtop^2)/4;
% %bottom
% nbottom=2;
% dbottom=0.016;
% ybottom=-((d/2)-0.025-(dbottom/2));
% Abottom=(pi*nbottom*dbottom^2)/4;

%.......steel layer details..........

% Areaoflayers=2*0.001*[0.071 0.071 0.071 0.071 0.032 0.032 0.032 0.032 0.071 0.071 0.071 0.071];
% nobars=[4 2];
% dofbars=[0.020 0.016];
ysteel=[0.175 -0.175]; %distance to steel layers from middle(top to bottom)
Areaoflayers=2*0.001*[0.3141592654 0.3141592654];
% for ii=1:length(ysteel)
%     Areaoflayers(1,ii)=(pi*nobars(1,ii)*(dofbars(1,ii))^2)/4;
% end

%.......defining the nof and nofx of confined regions.......
xx1=(width/2)-(dc*0.001)/2;
yy1=d/2-cover-d_hoopbars*0.001/2;
xx2=-((width/2)-(dc*0.001)/2);
yy2=d/2-cover-d_hoopbars*0.001/2-bc*0.001;

fibxx1=round(0.5+nofx/2-(xx1*nofx/width));
fibyy1=round(0.5+nof/2-(yy1*nof/d));

fibxx2=round(0.5+nofx/2-(xx2*nofx/width));
fibyy2=round(0.5+nof/2-(yy2*nof/d));

%..............................
xx3=-xx2;
yy3=-yy2;
xx4=-xx1;
yy4=-yy1;

fibxx3=round(0.5+nofx/2-(xx3*nofx/width));
fibyy3=round(0.5+nof/2-(yy3*nof/d));

fibxx4=round(0.5+nofx/2-(xx4*nofx/width));
fibyy4=round(0.5+nof/2-(yy4*nof/d));
%===================SOURCE CODE==================================

SC=[BC Load_applied_dof];

LCM=zeros(nonpe*ndofpn,noe);

B_C=zeros(tdof,1);
for yy=1:tdof
    B_C(yy,1)=yy;
end
B_C(SC,:)=[];

for eee=1:noe
    for ppp=1:nonpe
        for qqq=1:ndofpn
            LCM(3*ppp-3+qqq,eee)=3*ECM(ppp,eee)-2+qqq-1;
        end
    end
end






Kfull=zeros(tdof,tdof); %Kfull is the complete structural stiffness matrix
hipo_element_stiffness=cell(1,noe);
hipo_element_Ke=cell(1,noe);

%..........initial section flexibility matrix.............
Kseci=zeros(2,2);
 for fib=1:nof

    yoffib=(d/2)*(1-(1/nof)-2*(fib-1)/nof); %y of each fiber
    for fibx=1:nofx
        xoffib=(width/2)*(1-(1/nofx)-2*(fibx-1)/nofx); %x of each fiber
        Kseci=Kseci+[1 -yoffib]'*E*Afib*[1 -yoffib];
    end
                        
end
for steelfib=1:length(ysteel)
    Kseci=Kseci+[1 -ysteel(1,steelfib)]'*Esteel(1,steelfib)*Areaoflayers(1,steelfib)*[1 -ysteel(1,steelfib)];
end


fseci=inv(Kseci);

section_strain=zeros(nof,1);
section_strain_steel=zeros(length(ysteel),1);

%--------------Deriving initial element and structure stiffnesses----------
for eeee=1:noe
    fb=zeros(3,3); %fb is the element flexibility matrix for basic system 
    for t=1:nIP
        Np=[0 0 1;((x(1,t)+1)/2)-1 (x(1,t)+1)/2 0];%Force interpolation matrix
        fb=fb+Np'*fseci*Np*wh(1,t)*(L(1,eeee)/2);
    end
    RBM=[0 1/L(1,eeee) 1 0 -1/L(1,eeee) 0; 0 1/L(1,eeee) 0 0 -1/L(1,eeee) 1; -1 0 0 1 0 0];     %Rigid body matrix
    ROT=[cos(angle(1,eeee)) sin(angle(1,eeee)) 0 0 0 0; 
        -sin(angle(1,eeee)) cos(angle(1,eeee)) 0 0 0 0; 
        0 0 1 0 0 0; 0 0 0 cos(angle(1,eeee)) sin(angle(1,eeee)) 0; 
        0 0 0 -sin(angle(1,eeee)) cos(angle(1,eeee)) 0;
        0 0 0 0 0 1];
    Kb=inv(fb);
    Ke_local=RBM'*Kb*RBM; %element stiffness matrix referring local coordiCAte system
    Ke=ROT'*Ke_local*ROT; %element stiffness matrix referring global coordiCAte system
    hipo_element_stiffness{1,eeee}=Kb;
    hipo_element_Ke{1,eeee}=Ke;
    
end
    


%------Assembling--------

for q=1:noe
    for loop1=1:ndofpn*nonpe
        i1=LCM(loop1,q);
        for loop2=1:ndofpn*nonpe
            i2=LCM(loop2,q);
            Kfull(i1,i2)=Kfull(i1,i2)+hipo_element_Ke{1,q}(loop1,loop2);
        end
    end
end
Ks=Kfull;

%Finding reduced structural stiffness matrix

for a=1:length(BC)
    for b=1:tdof 
       Ks(BC(a),b)=0;
       Ks(b,BC(a))=0;
    end
    Ks(BC(a),BC(a))=1;
end 

%..............Calculation of reference load vector............

ref_disp_vector=Ks\Load_vector;
ref_force_vector=Kfull*ref_disp_vector;
reference_load=ref_force_vector/abs(ref_force_vector(Load_applied_dof,1));


hipo_element_force=cell(1,noe);
hipo_element_deformation=cell(1,noe);
for dd=1:noe
    hipo_element_force{1,dd}=[0;0;0];
    hipo_element_deformation{1,dd}=[0;0;0];
end
Tangent_stiffnesses=zeros(nof,1);
hipo_section_flexibility=cell(noe,nIP);
curvature=zeros(noe,nIP);
hipo_section_force=cell(noe,nIP);
hipo_section_deformation=cell(noe,nIP);
hipo_deltaehs=cell(noe,nIP);
hipo_resisting_force=cell(noe,nIP);
section_steel_strain=zeros(2,1);
for dd=1:noe
    for ww=1:nIP
       hipo_section_force{dd,ww}=[0;0];
       hipo_section_deformation{dd,ww}=[0;0];
       hipo_deltaehs{dd,ww}=[0;0];
       hipo_resisting_force{dd,ww}=[0;0];
       hipo_section_flexibility{dd,ww}=fseci;
    end
end


Un=zeros(tdof,1);
Pn1=zeros(tdof,1);
section_sigma=zeros(nof,1);
hipo_section_sigma=cell(noe,nIP);
hipo_section_strain=cell(noe,nIP);

figure  
% subplot(2,2,1); 
grid on
Gstru=animatedline('Marker','.');
addpoints(Gstru,0,0)
% axis([0 0.005 0 460]);
title('Structure')


X=zeros(displacement_steps,1);
Y=zeros(displacement_steps,1);
XC=zeros(displacement_steps,1);
YC=zeros(displacement_steps,1);
XT=zeros(displacement_steps,1);
YT=zeros(displacement_steps,1);
SXT=zeros(displacement_steps,1);
SYT=zeros(displacement_steps,1);
SXB=zeros(displacement_steps,1);
SYB=zeros(displacement_steps,1);

%..............Calculation of section forces and deformations for axial
%force
axial_deformation=Ks\axial_load;
axial_load_actual=Kfull*axial_deformation;
Pn1=Pn1+axial_load_actual;
Un=Un+axial_deformation;
for eeee=1:noe
    RBM=[0 1/L(1,eeee) 1 0 -1/L(1,eeee) 0; 0 1/L(1,eeee) 0 0 -1/L(1,eeee) 1; -1 0 0 1 0 0];     %Rigid body matrix
            
    ROT=[cos(angle(1,eeee)) sin(angle(1,eeee)) 0 0 0 0; 
        -sin(angle(1,eeee)) cos(angle(1,eeee)) 0 0 0 0; 
        0 0 1 0 0 0; 
        0 0 0 cos(angle(1,eeee)) sin(angle(1,eeee)) 0; 
        0 0 0 -sin(angle(1,eeee)) cos(angle(1,eeee)) 0;
        0 0 0 0 0 1];      % Rotational matrix

    deltaqerbm_global=axial_deformation(LCM(:,eeee),1);
    deltaqerbm=ROT*deltaqerbm_global;
    deltaqe=RBM*deltaqerbm;
    deltaQe=hipo_element_stiffness{1,eeee}*deltaqe; 
    hipo_element_force{1,eeee}=deltaQe;
    hipo_element_deformation{1,eeee}=deltaqe;
    for hhhh=1:nIP
        Np=[0 0 1;((x(1,hhhh)+1)/2)-1 (x(1,hhhh)+1)/2 0];
        deltaShs=Np*deltaQe;
        hipo_section_force{eeee,hhhh}= hipo_section_force{eeee,hhhh}+deltaShs;    
        hipo_section_deformation{eeee,hhhh}=hipo_section_flexibility{eeee,hhhh}*deltaShs;
    end
end
for n=1:displacement_steps%Displacement step

    number_of_displacement_steps = sprintf(' number_of_displacement_steps = %g', n);
    disp(number_of_displacement_steps)
    K11=Ks;
    K11(:,SC)=[];
    K11(SC,:)=[];
    
    K12=Ks;
    K12=K12(:,Load_applied_dof);
    K12(SC,:)=[];
    
    K21=Ks;
    K21=K21(Load_applied_dof,:);
    K21(:,SC)=[];
    
   
    K22=Ks(Load_applied_dof,Load_applied_dof);
    
    P1=reference_load;
    P1(SC,:)=[];
    
    P2=reference_load(Load_applied_dof,1);
    
    deltaUI=K11\P1;
    deltaUII=K11\(-K12*displacement_step);
    deltalamda=(K21*deltaUII+K22*displacement_step)/(P2-K21*deltaUI);
    lamda=deltalamda;
    deltaUi11=deltalamda*deltaUI+deltaUII;
    deltaUi=zeros(tdof,1);
    for qqq=1:length(B_C)
        deltaUi(B_C(qqq,1),1)=deltaUi11(qqq,1);
    end
    deltaUi(Load_applied_dof,1)=displacement_step;
    
    Ui=deltaUi;
    deltaUi_stiffness_cal=deltaUi;
    for i=1:max_i % Structure state determination
        
        Kfull=zeros(tdof,tdof);
        
        
        for e=1:noe %choosing the element
            RBM=[0 1/L(1,e) 1 0 -1/L(1,e) 0; 0 1/L(1,e) 0 0 -1/L(1,e) 1; -1 0 0 1 0 0];     %Rigid body matrix
            
            ROT=[cos(angle(1,e)) sin(angle(1,e)) 0 0 0 0; 
                -sin(angle(1,e)) cos(angle(1,e)) 0 0 0 0; 
                0 0 1 0 0 0; 
                0 0 0 cos(angle(1,e)) sin(angle(1,e)) 0; 
                0 0 0 -sin(angle(1,e)) cos(angle(1,e)) 0;
                0 0 0 0 0 1];      % Rotational matrix
            
            deltaqerbm_global=deltaUi_stiffness_cal(LCM(:,e),1);
            deltaqerbm=ROT*deltaqerbm_global;
            deltaqe=RBM*deltaqerbm;
            fb=zeros(3,3);
            deltaQe=hipo_element_stiffness{1,e}*deltaqe; 

            for h=1:nIP %section level
                Np=[0 0 1;((x(1,h)+1)/2)-1 (x(1,h)+1)/2 0];
                deltaShs=Np*deltaQe;               
                hipo_section_force{e,h}= hipo_section_force{e,h}+deltaShs;
                
                for z=1:max_z
                    
                    Shsres=zeros(2,1);
                    Ksec=zeros(2,2);
                    deltaehs=hipo_section_flexibility{e,h}*deltaShs;
                   
                    hipo_section_deformation{e,h}=hipo_section_deformation{e,h}+deltaehs;
               
                    for fib=1:nof

                        yoffib=(d/2)*(1-(1/nof)-2*(fib-1)/nof); %y of each fiber
                        strainfib=[1 -yoffib]*hipo_section_deformation{e,h};
                        section_strain(fib,1)=strainfib;
                        for fibx=1:nofx
                            if strainfib<0
                                 if fib>=fibyy1 && fib<=fibyy2 && fibx>=fibxx1 && fibx<=fibxx2
                                    sigmafib=(fcc_dash*(strainfib/E_cc)*r)/(r-1+(strainfib/E_cc)^r);
                                    Etangent=((r-1+(strainfib/E_cc)^r)*(fcc_dash*r/E_cc)-(fcc_dash*(strainfib/E_cc)*r*r*(strainfib/E_cc^2)))/(r-1+(strainfib/E_cc)^r)^2;
                                 elseif fib>=fibyy3 && fib<=fibyy4 && fibx>=fibxx3 && fibx<=fibxx4
                                    sigmafib=(fcc_dash*(strainfib/E_cc)*r)/(r-1+(strainfib/E_cc)^r);
                                    Etangent=((r-1+(strainfib/E_cc)^r)*(fcc_dash*r/E_cc)-(fcc_dash*(strainfib/E_cc)*r*r*(strainfib/E_cc^2)))/(r-1+(strainfib/E_cc)^r)^2; 
                                 else
                                     
                                     npop=0.8+(-fc_dash*0.001/17);
                                     if (strainfib/ec_dash)<1
                                        kpop=1;
                                      elseif (strainfib/ec_dash)>1  
                                         kpop=0.67+(-fc_dash*0.001/62);
                                     end
                                     sigmafib=fc_dash*((npop*(strainfib/ec_dash))/(npop-1+(strainfib/ec_dash)^(npop*kpop)));
                                     Etangent=fc_dash*((npop-1+(strainfib/ec_dash)^(npop*kpop))*(npop/ec_dash)-npop*(strainfib/ec_dash)*(npop*kpop*(strainfib/ec_dash)^(npop*kpop-1)*(1/ec_dash)))/(npop-1+(strainfib/ec_dash)^(npop*kpop))^2;
                                 end

                            else

                                if strainfib<=ec_crack
                                   Etangent=Ecr;
                                   sigmafib=Etangent*strainfib;

                                else

                                  sigmafib=fc_crack/(1+(200*strainfib)^0.5);   
                                  Etangent=-(fc_crack*(200)^0.5)/(2*((strainfib)^0.5)*(1+(200*strainfib)^0.5)^2);

                                end
                            
                            end
                        
                        
                        %Obtaining fibre stresses for a section 
                        section_sigma(fib,1)=sigmafib;
                        
                        Shsres= Shsres+[sigmafib*Afib; -sigmafib*Afib*(yoffib)];
                        Ksec=Ksec+[1 -(yoffib)]'*Etangent*Afib*[1 -(yoffib)];
                 
                        Tangent_stiffnesses(fib,1)=Etangent;
                        if h==1 && fib==nof
                            comfib_strain(n,1)=strainfib;
                            comfib_stress(n,1)=sigmafib;
                        end
                        if h==2 && fib==1
                            tenfib_strain(n,1)=strainfib;
                            tenfib_stress(n,1)=sigmafib;
                        end
                        
                        end
                    end
                    if h==1
                       strain_sec1=section_strain;
                       stress_sec1=section_sigma;
                    elseif h==2
                        strain_sec2=section_strain;
                       stress_sec2=section_sigma;
                    elseif h==3
                        strain_sec3=section_strain;
                       stress_sec3=section_sigma;    
                    elseif h==4
                        strain_sec4=section_strain;
                       stress_sec4=section_sigma;
                    elseif h==5
                        strain_sec5=section_strain;
                       stress_sec5=section_sigma;
                    elseif h==6
                        strain_sec6=section_strain;
                       stress_sec6=section_sigma;
                    end
                            
                    
                    
                        for steelfib=1:length(ysteel)
                        strainfib_steel=[1 -(ysteel(1,steelfib))]*hipo_section_deformation{e,h};
                        section_strain_steel(steelfib,1)=strainfib_steel;

                            if abs(strainfib_steel)<=yield_strain(1,steelfib)
                                Esteelcode=Esteel(1,steelfib);
                                sigmafib_steel=Esteelcode*strainfib_steel;
                            elseif strainfib_steel>0

                                   Esteelcode=Esteel(1,steelfib)*Strain_hardening;

                                   sigmafib_steel=Esteelcode*(abs(strainfib_steel)-yield_strain(1,steelfib))+Esteel(1,steelfib)*yield_strain(1,steelfib);
                            else
                                    Esteelcode=Esteel(1,steelfib)*Strain_hardening;
                                    sigmafib_steel=-Esteelcode*(abs(strainfib_steel)-yield_strain(1,steelfib))-Esteel(1,steelfib)*yield_strain(1,steelfib);


                            end

                            Shsres= Shsres+[sigmafib_steel*Areaoflayers(1,steelfib); -sigmafib_steel*Areaoflayers(1,steelfib)*(ysteel(1,steelfib))];
                            Ksec=Ksec+[1 -(ysteel(1,steelfib))]'*Esteelcode*Areaoflayers(1,steelfib)*[1 -(ysteel(1,steelfib))];
                            if h==1 && steelfib==length(ysteel)
                                comfibsteel_strain(n,1)=strainfib_steel;
                                comfibsteel_stress(n,1)=sigmafib_steel;
                            end
                            if h==1 && steelfib==1
                                tenfibsteel_strain(n,1)=strainfib_steel;
                                tenfibsteel_stress(n,1)=sigmafib_steel;
                            end


                        end
%                     if e==1 && h==6 &&  z==1
%                         Shsres
%                        end

                    hipo_resisting_force{e,h}=Shsres;
%                     if z==1 && abs(hipo_section_force{e,h}(2,1))<abs(hipo_resisting_force{e,h}(2,1))
%                         uiuhfv=0;
%                     end
               
                    hipo_section_sigma{e,h}=section_sigma;
                    hipo_section_strain{e,h}=section_strain;
                    
                    hipo_section_flexibility{e,h}=inv(Ksec); 
                   
                    dbstop if warning
                    Shsunb=hipo_section_force{e,h}-Shsres;
%                     if e==1 && h==4
%                     
%                         Section_force_11 = hipo_section_force{e,h}
%                         Shsres
%                         Shsunb
%                       
%                         inv(hipo_section_flexibility{e,h})
%                         section_deformation_11=hipo_section_deformation{e,h}
%                       
%                     end
                    
                    if max(abs(Shsunb))<tol_force_z
                        break
                    end
                    
                    deltaShs=Shsunb;
                end
                number_of_section_level_iterations = sprintf(' number_of_section_level_iterations = %g', z);
                disp(number_of_section_level_iterations)
                if z==max_z
                     disp('section level convergence cannot be achieved')
                     return 
                end
                
%                 if e==1 && h==6
% %                     deltaQe
% %                     Section_force_11 = hipo_section_force{1,h+(e-1)*6}
% %                     Shsres
% %                     Shsunb
%                       n
%                       inv(hipo_section_flexibility{1,h+(e-1)*6})
%                       hipo_section_deformation{1,h+(e-1)*6}
%                       hipo_resisting_force{1,h+(e-1)*6}
%                 end
                fb=fb+Np'*hipo_section_flexibility{e,h}*Np*wh(1,h)*(L(1,e)/2); 
                
            end
            hipo_element_stiffness{1,e}=inv(fb);
            
            Ke_local=RBM'* hipo_element_stiffness{1,e}*RBM;
            Ke=ROT'*Ke_local*ROT;
            for loop1=1:ndofpn*nonpe
                i1=LCM(loop1,e);
                for loop2=1:ndofpn*nonpe
                    i2=LCM(loop2,e);
                    Kfull(i1,i2)=Kfull(i1,i2)+Ke(loop1,loop2);
                end
            end 
        end
             
        Ks=Kfull;
        %Finding reduced structural stiffness matrix
         for a=1:length(BC)
             for b=1:tdof
                 Ks(BC(a),b)=0;
                 Ks(b,BC(a))=0; 
             end
                Ks(BC(a),BC(a))=1;
         end 
         
        Pres=Kfull*deltaUi;
        Rstr1=Pres;
        Rstr1(SC,:)=[];
         
        Rstr2=Pres(Load_applied_dof,1);
        if i==1
            Out_of_balance_force=lamda-Rstr2;
        else
            Out_of_balance_force=Out_of_balance_force+deltalamda-Rstr2;
        end
        
 
         
         R1=P1;
         R2=Out_of_balance_force;
         
         K11=Ks;
         K11(:,SC)=[];
         K11(SC,:)=[];

         K12=Ks;
         K12=K12(:,Load_applied_dof);
         K12(SC,:)=[];

         K21=Ks;
         K21=K21(Load_applied_dof,:);
         K21(:,SC)=[];


         K22=Ks(Load_applied_dof,Load_applied_dof);

         P1=reference_load;
         P1(SC,:)=[];

         P2=reference_load(Load_applied_dof,1);

         deltaUI=K11\P1;
         deltaUII=K11\(R1);
         deltalamda=(-R2+K21*deltaUII)/(P2-K21*deltaUI);
%          deltaF=deltalamda*reference_load;
         lamda=lamda+deltalamda;
         deltaUi11=deltalamda*deltaUI+deltaUII;
         deltaUi=zeros(tdof,1);
         for qqq=1:length(B_C)
             deltaUi(B_C(qqq,1),1)=deltaUi11(qqq,1);
         end
         deltaUi(Load_applied_dof,1)=0;
         Ui=Ui+deltaUi;
         Pcorrective=deltalamda*reference_load;
         
        for aa=1:length(BC)
            Pcorrective(BC(aa),1)=0;
        end
        Energy_tol_force=Out_of_balance_force;
        for bb=1:length(BC)
            Energy_tol_force(BC(bb),1)=0;
        end
        deltaU_corrective=Ks\Pcorrective;
        deltaUi_stiffness_cal=deltaU_corrective;
         if max(abs(Out_of_balance_force))<tol_force_i
             break
         end
%          if 0.5*(Ks\ Energy_tol_force)'*Out_of_balance_force<tol_Energy_i
%              break
%          end
        
       
    end
 %...........Updating reference load vector................
    ref_disp_vector=Ks\Load_vector;
    ref_force_vector=Kfull*ref_disp_vector;
    reference_load=ref_force_vector/abs(ref_force_vector(Load_applied_dof,1));
    Pn1=Pn1+lamda*reference_load;
    Un=Un+Ui;
    number_of_NR = sprintf(' number_of_NR = %g', i);
    disp(number_of_NR)
    if i==max_i
        disp('structure level convergence cannot be achieved')
        return
    end
    
   %---------------plotting fibre stresses of sections for each load step--------
   y21=zeros(nof,1);
   for u=1:nof
       y21(u,1)=(d/2)*(1-(1/nof)-2*(u-1)/nof);
   end
%......section fiber stress strain variation.......


% for ee=1:noe
%     for hh=1:nIP
%         figure(4+n)
%         
%         subplot(noe,2,2*ee-1)
%         plot(hipo_section_strain{ee,hh},y21)
%         hold on 
%         title('Axial Strain')
%         grid on
%         xlabel('ex') % x-axis label
%         ylabel('Depth (m)') % y-axis label
%         
%         subplot(noe,2,2*ee)
%         plot(hipo_section_sigma{ee,hh},y21)
%         hold on 
%         title('Axial Stress')
%         grid on
%         xlabel('fcx') % x-axis label
%         ylabel('Depth (m)') % y-axis label     
%         
%         
%            
%     end
% end
% 
% 
% fpath = 'D:\images\Journal';
% fCAme = sprintf('FIG%d.png',n);
% saveas(gca, fullfile(fpath, fCAme), 'png');
% close(figure(2+n))

   
  % ------------plotting section curvature variation along the member------
% for ee=1:noe
%    figure(10000)
%    
%    subplot(noe,1,ee)
%    plot(([0; 0.234945; 0.714768; 1.285232; 1.765055; 2]*L(1,ee)/2),curvature(ee,:))
%    grid on
%    hold on
%    title(['Curvature Variation along element' num2str(ee)])
%     
% end


%.............Pushover curve......................
    X(n,1)=abs(Un(Load_applied_dof,1));
    Y(n,1)=abs(Pn1(Load_applied_dof,1));
    addpoints(Gstru,abs(Un(Load_applied_dof,1)),abs(Pn1(Load_applied_dof,1)));
    drawnow limitrate

if n==754
    jjjjj=0;
end
% Pn1
% Un
% hipo_resisting_force{1,1}
% hipo_section_deformation{1,1}
% inv(hipo_section_flexibility{1,1})

% AAA(n,1)=(-(Pn1(8,1)*2))+hipo_section_force{1,1}(2,1);

end

    
            
                
                       
                        
                
                
            
            
                    
            
            
        
        
   