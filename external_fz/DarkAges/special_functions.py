import numpy as np
import os
import dill
data_dir = os.path.join( os.path.dirname(os.path.realpath( __file__ )), 'data' )

def approx_dirac(point,array):
	ret =  np.zeros_like(array).astype(np.float64)
	interpol_idx = np.interp(point,array,np.arange(len(array)))
	i = int(interpol_idx)
	spacing = float(array[i+1] - array[i])
	print spacing
	for j in xrange(array.shape[0]):
		print point, abs( (point - array[j]) / spacing )
		print max(0,1. - abs( (point - array[j]) / spacing ))
		ret[j] = max(0,1. - abs( (point - array[j]) / spacing ))
	return ret

def secondaries_from_muon(E_secondary, E_primary):
	if not hasattr(E_secondary,'__len__'):
		E_secondary = np.asarray([E_secondary])
	else:
		E_secondary = np.asarray(E_secondary)
	if not os.path.isfile( os.path.join(data_dir, 'muon_secondaries.obj')):
		data = np.genfromtxt( os.path.join(data_dir, 'muon_normed.dat'), unpack = True, usecols=(0,1,2,3))
		from .interpolator import NDlogInterpolator
		spec_interpolator = NDlogInterpolator(data[0,:], data[1:,:].T, exponent = 1, scale = 'lin-log')
		dump_dict = {'spec_interpolator':spec_interpolator}
		with open(os.path.join(data_dir, 'muon_secondaries.obj'),'wb') as dump_file:
			dill.dump(dump_dict, dump_file)
	else:
		with open(os.path.join(data_dir, 'muon_secondaries.obj'),'rb') as dump_file:
			dump_dict = dill.load(dump_file)
			spec_interpolator = dump_dict.get('spec_interpolator')
	x = E_secondary / E_primary
	out = spec_interpolator.__call__(x)
	out = out / E_secondary[:,None]
	return out

def secondaries_from_pi0(E_secondary, E_primary):
	if not hasattr(E_secondary,'__len__'):
		E_secondary = np.asarray([E_secondary])
	else:
		E_secondary = np.asarray(E_secondary)
	if not os.path.isfile( os.path.join(data_dir, 'pi0_secondaries.obj')):
		data = np.genfromtxt( os.path.join(data_dir, 'pi0_normed.dat'), unpack = True, usecols=(0,1,2,3))
		from .interpolator import NDlogInterpolator
		spec_interpolator = NDlogInterpolator(data[0,:], data[1:,:].T, exponent = 1, scale = 'lin-log')
		dump_dict = {'spec_interpolator':spec_interpolator}
		with open(os.path.join(data_dir, 'pi0_secondaries.obj'),'wb') as dump_file:
			dill.dump(dump_dict, dump_file)
	else:
		with open(os.path.join(data_dir, 'pi0_secondaries.obj'),'rb') as dump_file:
			dump_dict = dill.load(dump_file)
			spec_interpolator = dump_dict.get('spec_interpolator')
	x = E_secondary / E_primary
	out = spec_interpolator.__call__(x)
	out = out / E_secondary[:,None]
	return out

def secondaries_from_piCh(E_secondary, E_primary):
	if not hasattr(E_secondary,'__len__'):
		E_secondary = np.asarray([E_secondary])
	if not os.path.isfile( os.path.join(data_dir, 'piCh_secondaries.obj')):
		data = np.genfromtxt( os.path.join(data_dir, 'piCh_normed.dat'), unpack = True, usecols=(0,1,2,3))
		from .interpolator import NDlogInterpolator
		spec_interpolator = NDlogInterpolator(data[0,:], data[1:,:].T, exponent = 1, scale = 'lin-log')
		dump_dict = {'spec_interpolator':spec_interpolator}
		with open(os.path.join(data_dir, 'piCh_secondaries.obj'),'wb') as dump_file:
			dill.dump(dump_dict, dump_file)
	else:
		with open(os.path.join(data_dir, 'piCh_secondaries.obj'),'rb') as dump_file:
			dump_dict = dill.load(dump_file)
			spec_interpolator = dump_dict.get('spec_interpolator')
	x = E_secondary / E_primary
	out = spec_interpolator.__call__(x)
	out = out / E_secondary[:,None]
	return out

def luminosity_accreting_bh(Energy,recipe,PBH_mass):
	if not hasattr(Energy,'__len__'):
		Energy = np.asarray([Energy])
	if recipe=='spherical_accretion':
		a = 0.5
		Ts = 0.4*511e3
		Emin = 1
		Emax = Ts
		out = np.zeros_like(Energy)
		Emin_mask = Energy > Emin
		# Emax_mask = Ts > Energy
	 	out[Emin_mask] = Energy[Emin_mask]**(-a)*np.exp(-Energy[Emin_mask]/Ts)
		out[~Emin_mask] = 0.
		# out[~Emax_mask] = 0.

	elif recipe=='disk_accretion':
		a = -2.5+np.log10(PBH_mass)/3.
		Emin = (10/PBH_mass)**0.5
		# print a, Emin
		Ts = 0.4*511e3
		out = np.zeros_like(Energy)
		Emin_mask = Energy > Emin
		out[Emin_mask] = Energy[Emin_mask]**(-a)*np.exp(-Energy[Emin_mask]/Ts)
		out[~Emin_mask] = 0.
		Emax_mask = Ts > Energy
		out[~Emax_mask] = 0.
	else:
		from .__init__ import DarkAgesError as err
		raise err('I cannot understand the recipe "{0}"'.format(recipe))
	# print out, Emax_mask
	return out/Energy #We will remultiply by Energy later in the code
