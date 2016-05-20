#!/usr/bin/env python

import pymatgen
import pymatgen.structure_prediction as sp
import pymatgen.core.structure as stt
from pymatgen.structure_prediction import substitutor
from pymatgen.core.periodic_table import Specie
from pymatgen.transformations.standard_transformations import AutoOxiStateDecorationTransformation


mp_api_key = 'fDJKEZpxSyvsXdCt'
api = pymatgen.MPRester(mp_api_key)

id = 'mp-2068'
st = api.get_structure_by_material_id(id)

# print(st.composition)
# #print(structure.atomic_numbers)
# # print(structure)
# print(dir(st))
# j = st.SiteCollection.get_distance(0,4)
# j = st.lattice_vectors
# print(j)
# list = pymatgen.structure_prediction.pred_from_structures(st)
# print(dir(sp))
# print(sp.__path__)
# print(sp.__doc__)
# print(dir(pymatgen.core.structure))
# print(dir(stt.SiteCollection))

# print(sp.__builtins__)
# print(dir(test))
# i = test.SubstitutionPredictor(st.composition)
Subs = substitutor.Substitutor()
# Subs._threshold = 0.001 # Any threshold beyond 0.001 brings it out of the default hence it doesn't work: has to figure out how to explicitly set the threshold probability
struc = AutoOxiStateDecorationTransformation().apply_transformation(st)
spgr = struc.get_spacegroup_info()
print(struc.get_spacegroup_info())

# print(struc)
cations = ['Co', 'Rh', 'Ir']
#cations = ['Li', 'Na', 'K', 'Rb', 'Cs']
# cations2 = ['C','Si','Ge','Sn', 'Pb']
anions = ['F', 'Cl', 'Br', 'I']
counter = 0
for cation in cations:
    # for cation2 in cations2:
    for anion in anions:
        try:
            # list = Subs.pred_from_structures(target_species=[Specie(cation, +1), Specie(cation2, +2), Specie(anion, -1)], structures_list=[{'structure': struc, 'id': 'TEST'}])
            list = Subs.pred_from_structures(target_species=[Specie(cation, +3), Specie(anion, -1)], structures_list=[{'structure': struc, 'id': 'TEST'}])
        except:
            pass
        for c in list:
            counter += 1
            # c.final_structure.to(filename=cation + cation2 + anion +'3' + '_' + spgr[0] + ".cif")
            c.final_structure.to(filename=cation + anion + '3' + '_' + spgr[0] + ".cif")

# list_of_all_combos = Subs.pred_from_list([Specie('Be', +2), Specie('O', -2)])
# print(list_of_all_combos)
print(counter)