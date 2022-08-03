import numpy as np
import os,sys,glob

"""
########################################################
Read/readidb.py

    returns dictionary for idb
    keys:
    - interaction_range (0 = local)
    - monomer_types (what are the possible types used)
    - discretization
    - avg_inconsist (relevant for non-local couplings)
    - seq_params (dict with oligomer types (key) + 3 arguments: types, vec (groundstate), params (identifier model + list of model parameters))
########################################################
"""

def readidb(filename):

    def gen_seq_combinations(interaction_range,monomer_types):
        num = 2*(interaction_range+1)
        seqs = list()
        def iterate(seq,pos):
            for i in range(len(monomer_types)):
                added_seq = seq + monomer_types[i]
                nextpos = pos+1
                if nextpos < num:
                    iterate(added_seq,nextpos)
                else:
                    seqs.append(added_seq)

        iterate('',0)
        return seqs

    def get_paramset_line_ids(lines,seqs):
        seq_ids = list()
        missing = list()
        for seq in seqs:
            found = False
            for i in range(len(lines)):
                if seq == lines[i].strip():
                    seq_ids.append([seq,i])
                    found = True
                    break
            if not found:
                missing.append(seq)
        return seq_ids,missing

    def stripsplit(line,delimiter=' ',replaces=['\t','\n']):
        for repl in replaces:
            line = line.replace(repl,delimiter)
        line = line.strip()
        while delimiter+delimiter in line:
            line = line.replace(delimiter+delimiter,delimiter)
        return line.split(delimiter)


    with open(filename,'r') as f:
        lines = f.readlines()
        lines = [line for line in lines if len(line.strip()) > 0 and line.strip()[0] != '#']

        idb = dict()
        for line in lines:
            arg = line.split(' ')[0].split('=')[0]
            if arg.lower() == 'interaction_range':
                interaction_range = int(line.split('=')[-1].strip())
            if arg.lower() == 'monomer_types':
                monomer_types = line.split('=')[-1].strip()
            if arg.lower() in ['discretization','disc_len']:
                disc_len = float(line.split('=')[-1].strip())
            if arg.lower() == 'avg_inconsist':
                avg_inconsist = bool(line.split('=')[-1].strip())

        successful = True
        try:
            idb['interaction_range'] = interaction_range
        except NameError:
            print('argument "interaction_range" not found in idb file')
            successful = False
        try:
            idb['monomer_types'] = monomer_types
        except NameError:
            print('argument "monomer_types" not found in idb file')
            successful = False
        try:
            idb['disc_len'] = disc_len
        except NameError:
            print('argument "disc_len" (or "discretization") not found in idb file')
            successful = False
        try:
            idb['avg_inconsist'] = avg_inconsist
        except NameError:
            print('argument "avg_inconsist" not found in idb file')
            successful = False

        seqs = gen_seq_combinations(interaction_range,monomer_types)
        seq_ids,missing = get_paramset_line_ids(lines,seqs)
        if len(missing) > 0:
            print('The following sequence parameters have not been specified in the IDB files:')
            for seq in missing:
                print(' - %s'%seq)
            raise Exception('Inconsistent IDB file')

        num_interactions = 1+2*interaction_range

        seq_params = dict()
        ids  = [seq_id[1] for seq_id in seq_ids]
        seqs = [seq_id[0] for seq_id in seq_ids]
        for i in range(len(ids)):
            if i == len(ids)-1:
                till = len(lines)
            else:
                till = ids[i+1]
            paramlines = lines[ids[i]:till]

            seq = seqs[i]
            params = list()
            vec    = None
            for line in paramlines:
                if len(stripsplit(line)) > 1:
                    splitline = stripsplit(line)
                    if splitline[0].lower() == 'vec':
                        vec = [float(v) for v in splitline[1:]]
                    else:
                        param = [splitline[0]] + [float(v) for v in splitline[1:]]
                        params.append(param)

            if len(params) != num_interactions:
                print('Sequence "%s" requires %d interaction parameter sets, %d given'%(seq,num_interactions,len(params)))
                raise Exception('Inconsistent IDB file')

            seq_param = dict()
            seq_param['seq']    = seq
            seq_param['vec']    = vec
            seq_param['params'] = params
        seq_params[seq] = seq_param
        idb['seq_params'] = seq_params
        return idb




if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: python %s idbfn"%sys.argv[0])
        sys.exit(0)
    fn_idb  = sys.argv[1]

    idb = readidb(fn_idb)


    print(idb['seq_params'][[key for key in idb['seq_params'].keys()][0]])
