from open3d import *
import indoor3d_util
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import obj_util


def loadData(filename, num_point, block_size=1.0, stride=1.0,
            random_sample=False, sample_num=None, sample_aug=1):
    cloud = read_point_cloud(filename)
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

def loadDataRaw(filename):
    cloud = read_point_cloud(filename)
    pts = np.array(cloud.points)
    nb_points = np.shape(pts)[0]
    labels = np.array(cloud.colors)
    return np.concatenate((pts,labels,np.zeros((nb_points,1))),axis=1)

def showdata(filename):
    cloud = read_point_cloud(filename)
    draw_geometries([cloud])


def main():
    #actual code to load,slice and display the point cloud
    file_data_path="/media/pierre/Elements/n7/ProjetLong/deep_gcns/sem_seg/pretrained/ResGCN-56/log5/dump/A29[17-09-25]_pred.obj"
    if file_data_path[-3:]=='obj':
        xyz,rgb = obj_util.read_obj(file_data_path)
        xyz=np.array(xyz).astype('float64')
        rgb=np.array(rgb).astype('uint8')
    else:
        points,colors=0,0
        point_cloud= np.loadtxt(file_data_path,skiprows=1)
        mean_Z=0#np.mean(point_cloud,axis=0)[2]
        spatial_query=point_cloud[abs( point_cloud[:,2]-mean_Z)<1]
        xyz=spatial_query[:,:3]
        rgb=spatial_query[:,3:6]
    #ax = plt.axes(projection='3d')
    #ax.scatter(xyz[:,0], xyz[:,1], xyz[:,2], c = rgb/255, s=0.01)
    #plt.show()


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
    print('Shape prediction : ',np.shape(xyz))
    # Tri des données par classes

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
