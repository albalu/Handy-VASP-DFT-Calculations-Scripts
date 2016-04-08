%%% This function reads EIGENVAL file (VASP file for energy) and returns
%%% the VBM and CBM and their corresponding KPOINTS.
%%% Currently works for ISPIN=1, ISPIN=2 and LSORBIT=TRUE
%%% By Alireza Faghaninia with the help of Mike Sullivan
%%% please contact alireza@wustl.edu for questions(bug reports appreciated)

function [evbm,kvbm,ecbm,kcbm] = find_vbm_cbm(filename,spinorbit)

if nargin < 2
    spinorbit = 0;
else
    if strcmp(spinorbit, 'false') || strcmp(spinorbit, 'False') || strcmp(spinorbit, 'FALSE')
        spinorbit = 0
    end
    if strcmp(spinorbit, 'true') || strcmp(spinorbit, 'True') || strcmp(spinorbit, 'TRUE')
        spinorbit = 1
    end
end

if nargin < 1
    filename = 'EIGENVAL'
end
    

eigenval = fopen(filename,'r');
buffer=fscanf(eigenval, '%d',4);  %reading the first line  
ispin=buffer(4); %4th number is ispin (ispin =1: non-magnetic calculation, ispin=2: magnetic)
for i = 1:5
    fgetl(eigenval);
end

temp = fscanf(eigenval,'%d');
NKPTS = temp(2);
NBVAL = ceil(temp(1)/2);
NBTOT = temp(3);
if spinorbit == 1
    NBVAL = temp(1)
end
energies = zeros(NKPTS, NBTOT);
kpoints = zeros(NKPTS,4);
kcbm = zeros(1,3);
kvbm = zeros(1,3);
for i = 1:NKPTS
    kpoints(i,:) = fscanf(eigenval, '%f',4);
    for j = 1:NBTOT
        if ispin == 1
            temp = fscanf(eigenval,'%d %f',2);
        else
            temp = fscanf(eigenval,'%d %f %f',3);
        end
        energies(i,j) = temp(2);
    end
end

evbm = -1000;
ecbm = 1000;
for i = 1:NKPTS
        if(energies(i,NBVAL)>evbm)
            evbm = energies(i,NBVAL);
            kvbm = kpoints(i,1:3);
        end
end
for i = 1:NKPTS
        if(energies(i,NBVAL+1)<ecbm)
            ecbm = energies(i,NBVAL+1);
            kcbm = kpoints(i,1:3);
        end
end
