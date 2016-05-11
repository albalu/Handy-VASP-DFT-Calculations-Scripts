%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is a code to generate an adaptive but dense enough k-point mesh
% around CBM/VBM of a semiconductor. Generally this k-point is Gamma-point.
% 
% The non-self consistent calculation with this kpoint should be sufficient
% for the code, aMoBT and to obtain convergance and smoothness to some
% extent. Using a dense kpoint mesh is recommended.
%
% by: Alireza Faghaninia 
% Washington University in St. Louis
% alireza@wustl.edu
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% You can change center_kpoint in case CBM/VBM is not at Gamma-point
% Specifying the cented k-point is not available in version 1.0 of aMoBT
center_kpoint = [0 0 0 1];
k = [];
k = [k; center_kpoint ];

% You can change the follwoing step however you want
step=[0.001 0.002 0.003 0.004 0.008 0.012 0.016 0.024 0.032 0.048 0.064 0.096 0.128 0.192 0.256];
for i = 1:length(step)
for kx=center_kpoint(1)-step(i):step(i):center_kpoint(1)+step(i)
	for ky=center_kpoint(2)-step(i):step(i):center_kpoint(2)+step(i)
		for kz=center_kpoint(3)-step(i):step(i):center_kpoint(3)+step(i)
			if (kx-center_kpoint(1))^2+(ky-center_kpoint(2))^2+(kz-center_kpoint(3))^2>0.0000000000001
				k=[k; [kx ky kz 1] ];
			end
		end
	end
end
end

l=size(k);
kp=fopen('KPOINTS_for_aMoBT','w');
fprintf(kp,'%s','Explicitly entered kpoints');
fprintf(kp,'\n');
fprintf(kp,'%6d',l(1));
fprintf(kp,'\n');
fprintf(kp,'%s','Reciprocal lattice');
fprintf(kp,'\n');
for i=1:l(1)
	fprintf(kp,'%10.6f',k(i,:));
	fprintf(kp,'\n');
end
fclose(kp);
k
l(1)
