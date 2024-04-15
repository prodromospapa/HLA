import numpy as np

f = open(f'ouput_HvG.npy', 'rb')
data = np.load(f)
arr = np.ones((len(data), len(data), len(loci_index_list)), dtype=np.int8)
loci_index = {"A":0,"B":1,"C":2,"DRB1":3,"DQB1":4}
for sample in data:
    print(sample[i,:,loci])