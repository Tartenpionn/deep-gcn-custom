import open3d as op3d
import indoor3d_util
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import obj_util


def loadData(file_path, num_point, block_size=1.0, stride=1.0,
            random_sample=False, sample_num=None, sample_aug=1):
    """ This function load and slice the point cloud from the file pointed by file_path.
    
    This function shape the data in order to feed the network.
    The data is moved and resized to be in the unity cube.
    Then entries for the network are made using block_size and stride.
    For example setting block_size and stride to 0.5 will make 8 entries,
    each entries will be a part of unity cube sliced in 8.
    And each entries will fed to the network to construct the prediction.
    ARGS:
        file_path: absolute or relative path of the file containing the point cloud.
        num_point: the number of point for each batch, it is the size of the first layer of the network.
        block_size: the size of the block used to construct entries.
        stride: the distance the block will be moved to construct the next entry.
                this value must be between 0 and block_size
        random_sample: wether or not points have to be taken randomly in case the entry has mor points than num_point
        sample_num:
        sample_aug: wther or not the value must be augmented to create more entries for a better prediction
    RETURN:
        a matrix to feed in the network.
    """
    cloud = op3d.io.read_point_cloud(file_path)
    pts = np.array(cloud.points)
    min_x = np.min(pts[:,0])
    min_y = np.min(pts[:,1])
    min_z = np.min(pts[:,2])
    pts[:,0]-=min_x
    pts[:,1]-=min_y
    pts[:,2]-=min_z
    max = np.amax(pts)
    pts*=1/max
    max = np.max(pts)
    nb_points = np.shape(pts)[0]
    print('nb points : ',nb_points)
    labels = np.array(cloud.colors)
    data_label = np.concatenate((pts,labels,np.zeros((nb_points,1))),axis=1)
    return indoor3d_util.room2blocks_plus_normalized(data_label, num_point, block_size, stride,
             random_sample, sample_num, sample_aug)

def loadDataRaw(file_path):
    """ This function load the point cloud from the file pointed by file_path.
    
    ARGS:
        file_path: absolute or relative path of the file containing the point cloud.
    RETURN:
        a matrix of shape (nb_point, 7). 
            Each row are xyzrgb data of the point and a 0 is added to simulate a class for the groun truth. 
    """
    cloud = op3d.io.read_point_cloud(file_path)
    pts = np.array(cloud.points)
    nb_points = np.shape(pts)[0]
    labels = np.array(cloud.colors)
    return np.concatenate((pts,labels,np.zeros((nb_points,1))),axis=1)

def showdata(file_path):
    """ This function display the point cloud from the file pointed by file_path.
    
    ARGS:
        file_path: absolute or relative path of the file containing the point cloud.
    """
    cloud = op3d.io.read_point_cloud(file_path)
    draw_geometries([cloud])


def main():
    """ This fonction load and show the file wich path is file_data_path. 
    
    This function is called when the file is launched (and not when it's imported).
    Assumption are made that the file had been created by a network prediction.
    It display predictions with a color for each class.
    Colors and labels of the class are taken from indoor3d_util.
    Any faces in the file won't be displayed.
    """
    file_data_path="/media/pierre/Elements/n7/ProjetLong/deep_gcns/sem_seg/pretrained/ResGCN-56/log5/dump/A29[17-09-25]_pred.obj"
    # Load the file in xyz and rgb variablesp 
    if file_data_path[-3:]=='obj':
        xyz,rgb = obj_util.read_obj(file_data_path)
        xyz=np.array(xyz).astype('float64')
        rgb=np.array(rgb).astype('uint8')
    elif file_data_path[-3:]=='ply':
        pc = open3d.io.read_point_cloud(file_data_path)
        xyz = np.array(pc.points)
        rgb = np.array(pc.colors)*255
    else:
        points,colors=0,0
        point_cloud= np.loadtxt(file_data_path,skiprows=1)
        mean_Z=0
        spatial_query=point_cloud[abs( point_cloud[:,2]-mean_Z)<1]
        xyz=spatial_query[:,:3]
        rgb=spatial_query[:,3:6]
    
    # Display the xyz and rgb variables by class
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X = xyz[:,0]
    Y = xyz[:,1]
    Z = xyz[:,2]
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0

    mid_x = (X.max()+X.min()) * 0.5
    mid_y = (Y.max()+Y.min()) * 0.5
    mid_z = (Z.max()+Z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    # Tri des donn??es par classes

    classes = [i for i in indoor3d_util.g_class2color.keys()]
    classes_colors = [i for i in indoor3d_util.g_class2color.values()]
    
    classes_idx = []
    for c_id in range(np.shape(classes_colors)[0]):
        classes_idx.append(np.where(rgb==classes_colors[c_id]))
        Xc = X[classes_idx[-1][0]]
        Yc = Y[classes_idx[-1][0]]
        Zc = Z[classes_idx[-1][0]]
        rgbc = rgb[classes_idx[-1][0]]
        scat = ax.scatter(Xc, Yc, Zc,c = rgbc/255,s=2)
    ax.legend(classes,loc=(1,0))


    plt.show()

if __name__ == "__main__":
    main()
