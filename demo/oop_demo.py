import os
import numpy as np
from demo_utils import plot_image
import svmbir

"""
This file demonstrates the generation of a Shepp-Logan phantom followed by sinogram projection and reconstruction using MBIR. 
The phantom, sinogram, and reconstruction are then displayed. 
"""

# Simulated image parameters
num_rows_cols = 256 # assumes a square image

# Simulated sinogram parameters
num_views = 144
tilt_angle = np.pi/2 # Tilt range of +-90deg

# Reconstruction parameters
T = 0.1
p = 1.1
sharpness = 0.0
snr_db = 40.0

# Generate phantom with a single slice
phantom = svmbir.phantom.gen_shepp_logan(num_rows_cols, num_rows_cols)
phantom = np.expand_dims(phantom, axis=0)

# Generate sinogram by projecting phantom
angles = np.linspace(-tilt_angle, tilt_angle, num_views, endpoint=False)
sino = svmbir.project(phantom, angles, num_rows_cols )
(num_views, num_slices, num_channels) = sino.shape

# Perform MBIR reconstruction with functional
recon = svmbir.recon(sino, angles, T=T, p=p, sharpness=sharpness,snr_db=snr_db)


# create instance of callable Recon class
rec_op = svmbir.Recon(max_iterations=10,positivity=True)

rec_op.print_params()
rec_op.save_params('param_dict.npy')
rec_op.load_params('param_dict.npy')
rec_op.set_param('max_iterations',20)
rec_op.set_defaults()
# bproj = recon_op.backproject(sino,angles) #TBD
# mask = recon_op.return_mask() #TBD

# Setting, printing, saving, loading parameters
rec_op.print_params()
rec_op.save_params('param_dict.npy')

print("A: max_iterations",rec_op.params['max_iterations'])

#rec_op.params['max_resolutions'] = 20  # can do it this way, but don't
rec_op.set_param('max_iterations',20)
print("B: max_iterations",rec_op.params['max_iterations'])

rec_op.load_params('param_dict.npy')
print("C: max_iterations",rec_op.params['max_iterations'])

rec_op.set_defaults()
print("D: max_iterations",rec_op.params['max_iterations'])

recon2 = rec_op(sino,angles,max_iterations=5)    # call svmbir.recon through instance
print("E: max_iterations",rec_op.params['max_iterations'])

rec_op.set_param('your a douche',True)

# Compute Normalized Root Mean Squared Error
nrmse = svmbir.phantom.nrmse(recon[0], phantom[0])
nrmse2 = svmbir.phantom.nrmse(recon2[0], phantom[0])

print(nrmse,nrmse2)

exit()

# create output folder
os.makedirs('output', exist_ok=True)

# Display parameters
vmin = 1.0
vmax = 1.2

# display phantom
plot_image(phantom[0], title='Shepp Logan Phantom', filename='output/shepp_logan_phantom.png', vmin=vmin, vmax=vmax)

# display sinogram
plot_image(np.squeeze(sino), title='Sinogram', filename='output/shepp_logan_sinogram.png')

# display reconstruction
title = f'Reconstruction with NRMSE={nrmse:.3f}.'
plot_image(recon[0], title=title, filename='output/shepp_logan_recon.png', vmin=vmin, vmax=vmax)

input("press Enter")
