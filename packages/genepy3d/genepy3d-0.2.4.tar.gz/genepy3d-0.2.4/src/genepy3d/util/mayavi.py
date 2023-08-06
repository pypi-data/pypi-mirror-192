# -*- coding: utf-8 -*-
"""Plot objects using Mayavi.

This module plot the basic objects in GeNePy3D using Mayavi--VTK based library
for 3D visualization.


.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import numpy as np

def plot_curve(mlab,crv,r=1.,clc=(1.,0.,0.),opacity=1.,ntheta=18,npnt=200):
    """Plot a curve in 3D.
    
    Args:
        mlab (Mayavi object): Mayavi plot object.
        crv (Curve): 3D curve.
        r (float or array of float): radius.
        clc (tuple of float): color.
        opacity (float): transparency.
        ntheta (int): number of angles for sampling the points from the given radii. 
        npnt (int): number of points that used to be displayed (see mask_points in mlab.mesh())
        
    Returns:
        mlab mesh object
    
    """
    
    x, y, z = crv.coors[:,0], crv.coors[:,1], crv.coors[:,2]
    
    # Sampling of a unit curve tube
    step = 2*np.pi/ntheta
    T, Theta = np.mgrid[0:len(x), 0:2*np.pi+step:step]
    T = T.astype(int)
    
    Xc = np.take(x,T)
    Yc = np.take(y,T)
    Zc = np.take(z,T)
    
    # Check input radius
    if isinstance(r,np.ndarray):
        if len(r) == len(x):
            R = np.take(r,T)
        else:
            raise Exception("r must be the same length with curve")
    else:
        R = r
    
    # Curve surf in YZ plane
    Xx = Xc 
    Yx = Yc + (np.sin(Theta)*R)
    Zx = Zc + (np.cos(Theta)*R)

    # Curve surf in XZ plane
    Xy = Xc + (np.cos(Theta)*R)
    Yy = Yc 
    Zy = Zc + (np.sin(Theta)*R)

    # Curve surf in XY plane
    Xz = Xc + (np.cos(Theta)*R)
    Yz = Yc + (np.sin(Theta)*R)
    Zz = Zc
    
    # Plot meshes
    meshx = mlab.mesh(Xx, Yx, Zx,mask_points=npnt,mode="sphere",color=clc,representation='surface',opacity=opacity);
    meshy = mlab.mesh(Xy, Yy, Zy,mask_points=npnt,mode="sphere",color=clc,representation='surface',opacity=opacity);
    meshz = mlab.mesh(Xz, Yz, Zz,mask_points=npnt,mode="sphere",color=clc,representation='surface',opacity=opacity);

    return meshx, meshy, meshz


def plot_points(mlab,pnt,r=1.,clc=(1.,0.,0.),opacity=1.):
    """Plot points in 3D.
    
    Args:
        mlab (Mayavi object): Mayavi plot object.
        pnt (Point): 3D point cloud.
        r (float or array of float): radius.
        clc (tuple of float): color.
        opacity (float): transparency.
        
    Returns:
        mlab mesh object
    
    """
    
    x, y, z = pnt.coors[:,0], pnt.coors[:,1], pnt.coors[:,2]
    
    # Check input radius
    if isinstance(r,np.ndarray):
        if len(r) == len(x):
            s = r*2 # size of the point in mayavi plo() is the diameter
        else:
            raise Exception("r must be the same length with curve")
    else:
        s = np.array([r*2 for _ in x])
    
    obj = mlab.points3d(x,y,z,s,scale_factor=1,color=clc,opacity=opacity)
    
    return obj


def plot_tree(mlab,tr,r=None,clc=(0.5,0.5,0.5),opacity=1.,
              show_branchings=False,br_clc=(0.,0.,1.),br_r=None,
              show_leaves=False,lf_clc=(1.,1.,0.),lf_r=None,
              show_connectors=False,cn_clc=(0.,1.,0.),cn_r=None,
              show_root=False,ro_clc=(1.,0.,0.),ro_r=None):
    """Plot tree in 3D.
    
    Args:
        mlab (Mayavi object): Mayavi plot object.
        tr (Tree): 3D tree.
        r (None, float or int): if None then plot the radius stored in tree, otherwise plot a constant radius.
        clc (tuple or dict): if tuple then entire tree has one color, if dict then colors are assigned for each structure_id.
        opacity (float): transparence.
        show_branchings (bool): if True plot branching points. 
        br_clc (tuple): color of branching points.
        br_r (None, float or int): radius of branching points. if None then plot the real radius, otherwise plot a constant radius.
        show_leaves (bool): if True plot leaf points.
        lf_clc (tuple): color of leaf points.
        lf_r (None, float or int): radius of leaf points. if None then plot the real radius, otherwise plot a constant radius.
        show_connectors (bool): if True plot connectors.
        cn_clc (tuple): color of connectors.
        cn_r (None, float or int): radius of connector points. if None then plot the real radius, otherwise plot a constant radius.
        show_root (bool): if True plot the root points.
        ro_clc (tuple): color of root points.
        ro_r (None, float or int): radius of root points. if None then plot the real radius, otherwise plot a constant radius.
        
    
    """
    
    from genepy3d.obj.curves import Curve
    from genepy3d.obj.points import Points
    
    # Set up colors
    clcdic = {}
    if isinstance(clc,tuple):
        clcdic['default'] = clc
    elif isinstance(clc,dict):
        if 'default' not in clc.keys():
            clcdic['default'] = (0.,1.,0.) # default color
        for key,val in clc.items():
            clcdic[key] = val
    else:
        raise Exception('clc must be tuple or dict')
    
    # Decompose tree into segments
    components = tr.decompose_segments().values()
    for compo in components:
        
        data = tr.get_features(['x','y','z','r','structure_id'],nodeid=compo).values
        crv = Curve(data[:,:3])
        
        # Check input radius
        if isinstance(r,(float,int)):
            r_compo = r
        else:
            r_compo = data[:,3]
        
        # Set up color for the segment
        s = int(data[-1,4])
        if s in clcdic.keys():
            clc_compo = clcdic[s]
        else:
            clc_compo = clcdic['default']
        
        plot_curve(mlab,crv,r=r_compo,clc=clc_compo,opacity=opacity)
        
    if show_branchings==True:
        
        nodes = tr.get_branchingnodes()
        
        if len(nodes)>0:
        
            data = tr.get_features(['x','y','z','r'],nodeid=nodes).values
            
            pnts = Points(data[:,:3])
            
            # Check input radius
            if isinstance(br_r,(float,int)):
                r_compo = br_r
            else:
                r_compo = data[:,3]
            
            plot_points(mlab,pnts,r_compo,br_clc)
        
    if show_leaves==True:
        
        nodes = tr.get_leaves()
        
        data = tr.get_features(['x','y','z','r'],nodeid=nodes).values
        
        pnts = Points(data[:,:3])
        
        # Check input radius
        if isinstance(lf_r,(float,int)):
            r_compo = lf_r
        else:
            r_compo = data[:,3]
        
        plot_points(mlab,pnts,r_compo,lf_clc)
        
    if show_connectors==True:
        
        nodes = tr.get_connectors().index.values
        
        if len(nodes)>0:
        
            data = tr.get_features(['x','y','z','r'],nodeid=nodes).values
            
            pnts = Points(data[:,:3])
            
            # Check input radius
            if isinstance(cn_r,(float,int)):
                r_compo = cn_r
            else:
                r_compo = data[:,3]
            
            plot_points(mlab,pnts,r_compo,cn_clc)
    
    if show_root==True:
        
        nodes = tr.get_root()
        data = tr.get_features(['x','y','z','r'],nodeid=nodes).values
        
        pnts = Points(data[:,:3])
        
        # Check input radius
        if isinstance(ro_r,(float,int)):
            r_compo = ro_r
        else:
            r_compo = data[:,3]
        
        plot_points(mlab,pnts,r_compo,ro_clc)
    
def plot_surface(mlab,surf,clc=(0.5,0.5,0.5),opacity=0.5):
    """Plot surface in 3D.
    
    Args:
        mlab (Mayavi object): Mayavi plot object.
        surf (Surface): 3D surface.
        clc (tuple of float): color.
        opacity (float): transparency.
        
    Returns:
        mlab object.
    
    """
    
    x, y, z = surf.vertices[:,0], surf.vertices[:,1], surf.vertices[:,2]
    triangles = surf.faces
    
    obj = mlab.triangular_mesh(x,y,z,triangles,color=clc,opacity=opacity)
    
    return obj


























