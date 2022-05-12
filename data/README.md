## Download helper to get partial data

In order to download only part of PhysionTest-Complete (380 GB in total), you can use the `download_data.ipynb` and follow the instruction in the notebook.

The downloaded files will be store in `./data` following this structure:
- data
  - physion_train
      - dynamics_training
        - Dominoes
          - Individual hdf5s for each example
        - Drop
        - ...
    - readout_training
      - ...
    - readout_test
      - ...



(Reference to the complete `PhysionTrain-Dynamics` and `PhysionTrain-Readout`)
| Scenario | Dynamics Training Set         | Readout Training Set       | Test Set      |
| -------- | -------------------- | ----------------- | ---------------- |
| Dominoes | [Dominoes_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_dynamics_training_HDF5s.tar.gz) | [Dominoes_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_readout_training_HDF5s.tar.gz)         | [Dominoes_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_testing_HDF5s.tar.gz) |
| Support | [Support_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_dynamics_training_HDF5s.tar.gz) | [Support_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_readout_training_HDF5s.tar.gz)         | [Support_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_testing_HDF5s.tar.gz) |
| Collide | [Collide_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_dynamics_training_HDF5s.tar.gz) | [Collide_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_readout_training_HDF5s.tar.gz)         | [Collide_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_testing_HDF5s.tar.gz) |
| Contain | [Contain_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_dynamics_training_HDF5s.tar.gz) | [Contain_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_readout_training_HDF5s.tar.gz)         | [Contain_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_testing_HDF5s.tar.gz) |
| Drop | [Drop_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_dynamics_training_HDF5s.tar.gz) | [Drop_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_readout_training_HDF5s.tar.gz)         | [Drop_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_testing_HDF5s.tar.gz) |
| Roll | [Roll_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Roll_dynamics_training_HDF5s.tar.gz) | [Roll_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Rollreadout_HDF5s.tar.gz)         | [Roll_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Roll_testing_HDF5s.tar.gz) |
| Link | [Link_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_dynamics_training_HDF5s.tar.gz) | [Link_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_readout_training_HDF5s.tar.gz)         | [Link_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_testing_HDF5s.tar.gz) |
| Drape | [Drape_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_dynamics_training_HDF5s.tar.gz) | [Drape_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_readout_training_HDF5s.tar.gz)         | [Drape_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_testing_HDF5s.tar.gz) |
