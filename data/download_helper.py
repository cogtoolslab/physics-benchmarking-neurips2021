import requests
import tarfile
import os

def download_file(scenarios, types):
    # This function is used to download dataset into corresponding folders

    # define some data root directory
    url_base = "https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/"
    dir_base = "./physion_train/"
    for s in scenarios:
        for t in types:
            dataset = s + "_" + t  + "_HDF5s.tar.gz"
            url = url_base + dataset
            dir_file = dir_base + t + "/" + s + "/" 
            # dir_target = dir_file + dataset
            
            # Check whether the specified path exists or not
            isExist = os.path.exists(dir_file)

            if not isExist:
                # Create a new directory because it does not exist 
                os.makedirs(dir_file)
            
            print("Downloading from " + url)
            print("Moving file to and decompressing in " + dir_file)

            # download & decompress
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                file = tarfile.open(fileobj=response.raw, mode="r|gz")
                file.extractall(path=dir_file)

            print("Complete.")
        print("All downloads complete!")
