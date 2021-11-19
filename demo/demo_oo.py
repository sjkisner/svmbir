import os
import numpy as np
import matplotlib.pyplot as plt
import svmbir

"""
Demonstration of class 'svmbir.Recon' which produces a callable wrapper to
the svmbir.recon() function.

rec_op = svmbir.Recon( **kwargs)
recon_img = rec_op( sino, angles, **kwargs)

Methods:
    rec_op.print_params()
    rec_op.save_params( filename.npy, binaries=True)
    rec_op.load_params( filename.npy)
    rec_op.set_param( 'keyword', val)
    rec_op.set_params( keyword1=val1, keyword2=val2, etc.)
    rec_op.set_defaults()
    bproj_img = rec_op.backproject( sino, angles)
"""

# Generate sinogram
phantom = svmbir.phantom.gen_shepp_logan(256,256)
phantom = np.expand_dims(phantom, axis=0)
angles = np.linspace(-np.pi/2, np.pi, 144, endpoint=False)
sino = svmbir.project(phantom, angles, 256)

# MBIR using functional
img1 = svmbir.recon(sino, angles, sharpness=-1, max_iterations=100, stop_threshold=0)

# MBIR using class 'Recon'

# Create instance of callable Recon class
#   -any recon() keyword argument after 'sino' and 'angles' can input to the constructor
rec_op = svmbir.Recon( sharpness=-1, max_iterations=100, stop_threshold=0)
# The callable instance is a wrapper for svmbir.recon()
#   -arguments can also be added here
img2 = rec_op(sino, angles)
img3 = rec_op(sino, angles, max_iterations=100, sharpness=1)
# alternately we could access svmbir.recon() as a standard class method:
img4 = rec_op.recon(sino, angles, max_iterations=100, sharpness=1)

# Arguments are held in the 'params' attribute (type=dict)
print(rec_op.params)

# Any kwarg inputs to the constructor or the __call__() method will update 'params' dict
print("sharpness",rec_op.params['sharpness'])

# You could update a parameter directly like this:
rec_op.params['positivity'] = False
# ..but it won't catch a misspelled key, so better to do this:
rec_op.set_param('positivity',False)
# otherwise you might add a nonsense parameter
#rec_op.set_param('your a douche',True)  # (this will raise an exception)

# Some 'Recon' class methods
rec_op.set_param('positivity',True)     # set single parameter
rec_op.set_params(positivity=True, stop_threshold=0)     # set multiple params from keyworded list
rec_op.save_params( 'param_dict.npy', binaries=False)   # saves to numpy pickle file
                                                        #   -sets binaries (init_img,weights) to None
rec_op.load_params( 'param_dict.npy')   # loads from file
rec_op.print_params()                   # prints dict elements 1 line at time
# TBD:
#rec_op.recon(sino,angles,kwargs)       # can do this if preferred over __call__() method

img5 = rec_op.backproject(sino, angles)

plt.figure(); plt.imshow(img1[0,:,:],cmap='gray',vmin=1,vmax=1.2); plt.colorbar(); plt.title('using functional')
plt.figure(); plt.imshow(img2[0,:,:],cmap='gray',vmin=1,vmax=1.2); plt.colorbar(); plt.title('using class, 1st result')
plt.figure(); plt.imshow(img3[0,:,:],cmap='gray',vmin=1,vmax=1.2); plt.colorbar(); plt.title('using class, 2nd result')
plt.figure(); plt.imshow(img4[0,:,:],cmap='gray',vmin=1,vmax=1.2); plt.colorbar(); plt.title('using class, 3nd result')
plt.figure(); plt.imshow(img5[0,:,:],cmap='gray'); plt.colorbar(); plt.title('using class, backprojection')
plt.show()

input("press Enter")
