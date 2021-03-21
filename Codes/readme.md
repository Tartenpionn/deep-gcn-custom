# General information

- This code needs the files from https://github.com/lightaime/deep_gcns.git in order to be operational

- Further information of the code are available on this github repository in the readme files. Especially in the one in the sem_seg folder.

- A demonstration of this code is available at https://colab.research.google.com/drive/13wr-dwsHwLy6bhhnrBxeHGhPc5zCOc_H?usp=sharing



# Run the code

To run the code (once the python enironnement is set up) you need to launch the TestTournesol file with these arguments :
- --model_path : the path to the .ckpt file (tensoflow checkpoint) containing the pretrained model weigths.
- --dump_dir : the path to  the folder where the prediction files will be written
- --output_filelist : the path to txt file where the name of created files will be written
- --room_data_filelist : the path to a exiting txt file with a list of the paths of the file that need a prediction.
- --visu : whether or not output files need to be generated to display the prediction
- --block_size : the size of the block used to make entries
- --stride : the distance the block is moved between entries

The data is moved and resized to be in the unity cube.
Then entries for the network are made using block_size and stride.
For example setting block_size and stride to 0.5 will make 8 entries,
each entries will be a part of unity cube sliced in 8.
And each entries will fed to the network to construct the prediction.

# Visualize predictions

To visualize prediction you need to edit the loaddatatourn.py file 
to set up the file_data_path variable to the path to the file you want 
to display.

If you only want tou display a file with a point cloud you would rather
call the showdata function from loaddatatourn.py.

