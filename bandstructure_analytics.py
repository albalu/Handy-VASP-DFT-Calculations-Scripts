#!/usr/bin/env python

def read_eigenval(filename = 'EIGENVAL', nvbm = 0, fermi = 0, spinorbit = False):
    kpoints = []    # list of kpoints coordinates
    energies = []   # list of [list of spin up energies] at each k-point
    energies2 = []  # list of [list of spin down energies] at each k-point
    try:
        with open('EIGENVAL', 'r') as atest:
            pass
            counter = 0
            for line in atest:
                counter += 1
                if counter == 9:
                    if len(line.split()) == 2:
                        ispin = 1
                    elif len(line.split()) == 3:
                        ispin = 2
                    else:
                        raise ValueError('Unexpected EIGENVAL format!')
                    break
    except IOError:
        raise IOError('EIGENVAL file must be present')

    with open('EIGENVAL', 'r') as eigenval:
        counter = 0
        for line in eigenval:
            counter += 1
            if counter == 6:
                (nelec, nkpts, nbands) = map(int, line.split())
                if nvbm == 0:
                    if spinorbit:
                        nvbm = nelec
                    else:
                        nvbm = nelec / 2
            if counter == 7:
                break
        for i in range(nkpts):
            kpoints.append(next(eigenval).split()[0:3])
            energy = [next(eigenval).split()[1:ispin+1] for i in range(nbands)]
            energy = [item for sublist in energy for item in sublist]
            if ispin == 2:
                energy2 = energy[1::2]
                energy2 = [float(en) -  fermi for en in energy2]
                energy = energy[::2]
                energies2.append(energy2)
            energy = [float(en) - fermi for en in energy]
            energies.append(energy)
            try:
                next(eigenval)
            except:
                pass

        # Not sure if the following is right. Should we ever try to average spin up and spin down energies?
        # if ispin == 2:
        #     for i in range(len(energies)):
        #         for j in range(len(energies[0])):
        #             energies[i][j] = (float(energies[i][j]) + float(energies2[i][j]))/2

    return kpoints, energies, nvbm, nkpts
def get_band_as_list(energies, nband):
    band = []
    for energy_at_k in energies:
        band.append(energy_at_k[nband-1])
    return map(float, band)
def get_contour(kpoints, energies, energy_of_contour, tolerance = 0.002):
    contour = []    # The coordinates of k-points that have the energy_of_contour in their energy states
    for k in range(len(kpoints)):
        en = 0
        for energy in energies[k]:
            if abs(float(energy) - energy_of_contour) < tolerance:
                dumlist = map(float, kpoints[k])
                dumlist.append(en)
                contour.append(dumlist)
            en += 1
    return contour

def finger_print(kpoints, energies, nvbm):
    vb1 = get_band_as_list(energies, nvbm)
    cb1 = get_band_as_list(energies, nvbm + 1)
    vbm_kindex, vbm = max(enumerate(vb1), key=lambda x: x[1])
    cbm_kindex, cbm = min(enumerate(cb1), key=lambda x: x[1])
    kvbm = kpoints[vbm_kindex]
    kcbm = kpoints[cbm_kindex]

    return vbm, kvbm, cbm, kcbm

kpoints, energies, nvbm, nkpts = read_eigenval()
print(kpoints)
print(energies)
print(nvbm)
# kk = get_contour(kpoints, energies, 1.4, tolerance = 0.002)
# print(kk)

vbm, kvbm, cbm, kcbm = finger_print(kpoints, energies, nvbm)
print(vbm)
print(kvbm)
print(cbm)
print(kcbm)