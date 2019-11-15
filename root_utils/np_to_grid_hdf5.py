import numpy as np
import os
import argparse
import h5py
import root_utils.pos_utils as pu

def get_args():
    parser = argparse.ArgumentParser(description='convert and merge .npz files to hdf5')
    parser.add_argument('input_files', type=str, nargs='+')
    parser.add_argument('-o', '--output_file', type=str)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    config = get_args()
    print("ouput file:", config.output_file)
    f = h5py.File(config.output_file, 'w')

    total_rows = 0
    files = []
    for input_file in config.input_files:
        if os.path.isdir(input_file):
            for infile in os.listdir(input_file):
                full_file = os.path.join(input_file, infile)
                if os.path.isfile(full_file):
                    print("Adding file to list:", full_file)
                    files.append(full_file)
        else:
            if not os.path.isfile(input_file):
                raise ValueError(input_file+" does not exist")
            print("Adding file to list:", input_file)
            files.append(input_file)

    for input_file in files:
        npz_file = np.load(input_file)
        print(npz_file['event_id'].shape[0],"events found in ", input_file)
        total_rows += npz_file['event_id'].shape[0]

    print("Total events:", total_rows)

    dset_labels=f.create_dataset("labels",
                                 shape=(total_rows,),
                                 dtype=np.int32)
    dset_PATHS=f.create_dataset("root_files",
                                shape=(total_rows,),
                                dtype=h5py.special_dtype(vlen=str))
    dset_IDX=f.create_dataset("event_ids",
                              shape=(total_rows,),
                              dtype=np.int32)
    dset_event_data=f.create_dataset("event_data",
                                     shape=(total_rows, 16, 40, 38),
                                     dtype=np.float32)
    dset_energies=f.create_dataset("energies",
                                   shape=(total_rows, 1),
                                   dtype=np.float32)
    dset_positions=f.create_dataset("positions",
                                    shape=(total_rows, 1, 3),
                                    dtype=np.float32)
    dset_angles=f.create_dataset("angles",
                                 shape=(total_rows, 2),
                                 dtype=np.float32)
    offset = 0
    offset_next = 0
    label_map = {22: 0, 11: 1, 13: 2}
    for input_file in files:
        print("processing file:", input_file)
        npz_file = np.load(input_file)
        event_id = npz_file['event_id']
        root_file = npz_file['root_file']
        pid = npz_file['pid']
        position = npz_file['position']
        direction = npz_file['direction']
        energy = npz_file['energy']
        hit_time = npz_file['digi_hit_time']
        hit_charge = npz_file['digi_hit_charge']
        hit_pmt = npz_file['digi_hit_pmt']
        hit_trigger = npz_file['digi_hit_trigger']
        trigger_time = npz_file['trigger_time']

        offset_next += event_id.shape[0]

        dset_IDX[offset:offset_next] = event_id
        dset_PATHS[offset:offset_next] = root_file
        dset_energies[offset:offset_next,:] = energy.reshape(-1,1)
        dset_positions[offset:offset_next,:,:] = position.reshape(-1,1,3)

        labels = np.full(pid.shape[0], -1)
        labels[pid==22] = 0
        labels[pid==11] = 1
        labels[pid==13] = 2
        dset_labels[offset:offset_next] = labels

        polar = np.arccos(direction[:,1])
        azimuth = np.arctan2(direction[:,2], direction[:,0])
        dset_angles[offset:offset_next,:] = np.hstack((polar.reshape(-1,1),azimuth.reshape(-1,1)))

        for i in range(hit_pmt.shape[0]):
            first_trigger = np.argmin(trigger_time[i])
            module_index = pu.module_index(hit_pmt[i])
            wall_indices = np.where((hit_trigger[i]==first_trigger) & pu.is_barrel(module_index))
            wall_indices = np.where(pu.is_barrel(module_index))
            pmt_in_module = pu.pmt_in_module_id(hit_pmt[i][wall_indices])
            wall_row, wall_col = pu.row_col(module_index[wall_indices])
            event_data = np.zeros((16, 40, 38))
            event_data[wall_row, wall_col, pmt_in_module] = hit_charge[i][wall_indices]
            event_data[wall_row, wall_col, pmt_in_module + 19] = hit_time[i][wall_indices]
            dset_event_data[offset+i,:] = event_data

        offset = offset_next
    f.close()
