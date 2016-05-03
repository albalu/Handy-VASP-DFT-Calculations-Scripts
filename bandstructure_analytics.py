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
            energy = [next(eigenval).split()[1:ispin] for i in range(nbands)]
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
    return band
def get_contour(kpoints, energies, energy_of_contour, tolerance = 0.002):
    for i in range(len(energies)):
        for energy in energies[i]:
            if ene

kpoints, energies, nvbm, nkpts = read_eigenval()
print(kpoints)
print(energies)
print(nvbm)
