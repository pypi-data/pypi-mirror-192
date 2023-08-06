import numpy as np

def MacKenzie(thetao,depth_value, so):
    a=1448.96
    b=4.591
    c=-5.304*10**-2
    d=2.374*10**-4
    e=1.340
    f=1.630*10**-2
    g=1.675*10**-7
    h=-1.025*10**-2
    j=-7.139*10**-13
    return a+b*thetao+c*thetao**2+d*thetao**3+e*(so-35)+f*depth_value+g*depth_value**2+h*thetao*(so-35)+j*thetao*depth_value**3


def MacKenzie_uncertainty(thetao,depth_value, so, std_thetao, std_so):
    a=1448.96
    b=4.591
    c=-5.304*10**-2
    d=2.374*10**-4
    e=1.340
    f=1.630*10**-2
    g=1.675*10**-7
    h=-1.025*10**-2
    j=-7.139*10**-13
    return (b+2*c*thetao+3*d*thetao**2+h*(so-35)+j*depth_value**3)*std_thetao+(e+h*thetao)*std_so

def get_std_arr(x, l1, l2):
    std=x['thetao'].copy()
    d=x.depth
    v=np.zeros(d.shape)
    for ii in range(d.shape[0]):
        v[ii]=l2[0]
        for i in range(len(l1)):
            v[ii]=l2[i]
            if d[ii]<l1[i]:
                break
        std[:,ii,:,:]=v[ii]
    return std

def depth_value(x):
    depth_value=x['thetao'].copy()
    d=x.depth
    for ii in range(d.shape[0]):
        depth_value[:,ii,:,:]=d[ii]
    return depth_value

def build_template_from_data_array(data_array,remove_attributes = True):
    res =data_array.copy()
    if remove_attributes:
        res.attrs=[]
    return res.attrs

def assign_value_by_dimention_range_with_template(template,rDimension,rRange,rValue ):
    res=template.copy()
    d=template[rDimension]
    v=np.zeros(d.shape)
    for ii in range(d.shape[0]):
        v[ii]=rValue[0]
        for i in range(len(rRange)):
            v[ii]=rValue[i]
            if d[ii]<rRange[i]:
                break
        res[{rDimension:ii}]=v[ii]
    return res
def bring_dimension_labels_to_value(template,rDimension):
    res=template.copy()
    d=template[rDimension]
    for ii in range(d.shape[0]):
        res[{rDimension:ii}]=d[ii]
    return res

