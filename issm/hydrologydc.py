import numpy as np
from issm.project3d import project3d
from issm.fielddisplay import fielddisplay
from issm.checkfield import checkfield
from issm.WriteData import WriteData

class hydrologydc(object):
	"""
	Hydrologydc class definition

	Usage:
		hydrologydc=hydrologydc();
	"""

	def __init__(self): # {{{
		self.water_compressibility    = 0
		self.isefficientlayer         = 0
		self.penalty_factor           = 0
		self.penalty_lock             = 0
		self.rel_tol                  = 0
		self.max_iter                 = 0
		self.sedimentlimit_flag       = 0
		self.sedimentlimit            = 0
		self.transfer_flag            = 0
		self.leakage_factor           = 0
		self.basal_moulin_input       = float('NaN')

		self.spcsediment_head         = float('NaN')
		self.sediment_transmitivity   = float('NaN')
		self.sediment_compressibility = 0
		self.sediment_porosity        = 0
		self.sediment_thickness       = 0


		self.spcepl_head              = float('NaN')
		self.mask_eplactive_node      = float('NaN')
		self.epl_compressibility      = 0
		self.epl_porosity             = 0
		self.epl_initial_thickness    = 0
		self.epl_colapse_thickness    = 0
		self.epl_thick_comp           = 0
		self.epl_max_thickness        = 0
		self.epl_conductivity         = 0
		self.eplflip_lock             = 0
				 
		#set defaults
		self.setdefaultparameters()
	#}}}
	def __repr__(self): # {{{
		string='   hydrology Dual Porous Continuum Equivalent parameters:'
		string='   - general parameters'
		string="%s\n%s"%(string,fielddisplay(self,'water_compressibility','compressibility of water [Pa^-1]'))
		string="%s\n%s"%(string,fielddisplay(self,'isefficientlayer','do we use an efficient drainage system [1: true 0: false]'))
		string="%s\n%s"%(string,fielddisplay(self,'penalty_factor','exponent of the value used in the penalisation method [dimensionless]'))
		string="%s\n%s"%(string,fielddisplay(self,'penalty_lock','stabilize unstable constraints that keep zigzagging after n iteration (default is 0, no stabilization)'))
		string="%s\n%s"%(string,fielddisplay(self,'rel_tol','tolerance of the nonlinear iteration for the transfer between layers [dimensionless]'))
		string="%s\n%s"%(string,fielddisplay(self,'max_iter','maximum number of nonlinear iteration'))
		string="%s\n%s"%(string,fielddisplay(self,'basal_moulin_input','water flux at a given point [m3 s-1]'))
		string="%s\n%s"%(string,fielddisplay(self,'sedimentlimit_flag','what kind of upper limit is applied for the inefficient layer'))
		string="%s\n\t\t%s"%(string,'0: no limit')
		string="%s\n\t\t%s"%(string,'1: user defined sedimentlimit')
		string="%s\n\t\t%s"%(string,'2: hydrostatic pressure')
		string="%s\n\t\t%s"%(string,'3: normal stress')
	
		if self.sedimentlimit_flag==1:
			string="%s\n%s"%(string,fielddisplay(self,'sedimentlimit','user defined upper limit for the inefficient layer [m]'))

		string="%s\n%s"%(string,fielddisplay(self,'transfer_flag','what kind of transfer method is applied between the layers'))
		string="%s\n\t\t%s"%(string,'0: no transfer')
		string="%s\n\t\t%s"%(string,'1: constant leakage factor: leakage_factor')
			 
		if self.transfer_flag is 1:
			string="%s\n%s"%(string,fielddisplay(self,'leakage_factor','user defined leakage factor [m]'))

		string="%s\n%s"%(string,'   - for the sediment layer')
		string="%s\n%s"%(string,fielddisplay(self,'spcsediment_head','sediment water head constraints (NaN means no constraint) [m above MSL]'))
		string="%s\n%s"%(string,fielddisplay(self,'sediment_compressibility','sediment compressibility [Pa^-1]'))
		string="%s\n%s"%(string,fielddisplay(self,'sediment_porosity','sediment [dimensionless]'))
		string="%s\n%s"%(string,fielddisplay(self,'sediment_thickness','sediment thickness [m]'))
		string="%s\n%s"%(string,fielddisplay(self,'sediment_transmitivity','sediment transmitivity [m^2/s]'))

		if self.isefficientlayer==1:
			string="%s\n%s"%(string,'   - for the epl layer')
			string="%s\n%s"%(string,fielddisplay(self,'spcepl_head','epl water head constraints (NaN means no constraint) [m above MSL]'))
			string="%s\n%s"%(string,fielddisplay(self,'mask_eplactive_node','active (1) or not (0) EPL'))
			string="%s\n%s"%(string,fielddisplay(self,'epl_compressibility','epl compressibility [Pa^-1]'))
			string="%s\n%s"%(string,fielddisplay(self,'epl_porosity','epl [dimensionless]'))
			string="%s\n%s"%(string,fielddisplay(self,'epl_max_thickness','epl initial thickness [m]'))
			string="%s\n%s"%(string,fielddisplay(self,'epl_initial_thickness','epl initial thickness [m]'))			
			string="%s\n%s"%(string,fielddisplay(self,'epl_colapse_thickness','epl colapsing thickness [m]'))
			string="%s\n%s"%(string,fielddisplay(self,'epl_thick_comp','epl thickness computation flag'))
			string="%s\n%s"%(string,fielddisplay(self,'epl_conductivity','epl conductivity [m^2/s]'))
			string="%s\n%s"%(string,fielddisplay(self,'eplflip_lock','lock epl activity to avoid flip-floping (default is 0, no stabilization)'))
		return string
#}}}
	def extrude(self,md): # {{{
		self.spcsediment_head=project3d(md,'vector',self.spcsediment_head,'type','node','layer',1)
		self.sediment_transmitivity=project3d(md,'vector',self.sediment_transmitivity,'type','node','layer',1)
		self.basal_moulin_input=project3d(md,'vector',self.basal_moulin_input,'type','node','layer',1)
		if self.isefficientlayer==1 :
			self.spcepl_head=project3d(md,'vector',self.spcepl_head,'type','node','layer',1)
			self.mask_eplactive_node=project3d(md,'vector',self.mask_eplactive_node,'type','node','layer',1)
		return self
	#}}}
	def setdefaultparameters(self): #{{{ 

		#Parameters from de Fleurian 2014
		self.water_compressibility    = 5.04e-10
		self.isefficientlayer         = 1
		self.penalty_factor           = 3
		self.penalty_lock             = 0
		self.rel_tol                  = 1.0e-06
		self.max_iter                 = 100
		self.sedimentlimit_flag       = 0
		self.sedimentlimit            = 0
		self.transfer_flag            = 0
		self.leakage_factor           = 10.0

		self.sediment_compressibility = 1.0e-08
		self.sediment_porosity        = 0.4
		self.sediment_thickness       = 20.0
		self.sediment_transmitivity   = 8.0e-04

		self.epl_compressibility      = 1.0e-08
		self.epl_porosity             = 0.4
		self.epl_initial_thickness    = 1.0
		self.epl_colapse_thickness    = 1.0e-3
		self.epl_thick_comp           = 1
		self.epl_max_thickness        = 5.0
		self.epl_conductivity         = 8.0e-02
		self.eplflip_lock             = 0
		
		return self
	# }}}
	def initialize(self,md): # {{{
		if np.all(np.isnan(self.basal_moulin_input)):
			self.basal_moulin_input=np.zeros((md.mesh.numberofvertices))
			print"      no hydrology.basal_moulin_input specified: values set as zero"

		return self
	# }}}
	def checkconsistency(self,md,solution,analyses): #{{{ 

		#Early return
		if 'HydrologyDCInefficientAnalysis' not in analyses and 'HydrologyDCEfficientAnalysis' not in analyses:
			return md

		md = checkfield(md,'fieldname','hydrology.water_compressibility','numel',[1],'>',0.)
		md = checkfield(md,'fieldname','hydrology.isefficientlayer','numel',[1],'values',[0,1])
		md = checkfield(md,'fieldname','hydrology.penalty_factor','>',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.penalty_lock','>=',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.rel_tol','>',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.max_iter','>',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.sedimentlimit_flag','numel',[1],'values',[0,1,2,3])
		md = checkfield(md,'fieldname','hydrology.transfer_flag','numel',[1],'values',[0,1])

		if self.sedimentlimit_flag==1:
			md = checkfield(md,'fieldname','hydrology.sedimentlimit','>',0.,'numel',[1])

		if self.transfer_flag==1:
			md = checkfield(md,'fieldname','hydrology.leakage_factor','>',0.,'numel',[1])

		md = checkfield(md,'fieldname','hydrology.basal_moulin_input','NaN',1,'Inf',1,'timeseries',1)
		md = checkfield(md,'fieldname','hydrology.spcsediment_head','Inf',1,'timeseries',1)
		md = checkfield(md,'fieldname','hydrology.sediment_compressibility','>',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.sediment_porosity','>',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.sediment_thickness','>',0.,'numel',[1])
		md = checkfield(md,'fieldname','hydrology.sediment_transmitivity','>=',0,'size',[md.mesh.numberofvertices])
		if self.isefficientlayer==1:
			md = checkfield(md,'fieldname','hydrology.spcepl_head','Inf',1,'timeseries',1)
			md = checkfield(md,'fieldname','hydrology.mask_eplactive_node','size',[md.mesh.numberofvertices],'values',[0,1])
			md = checkfield(md,'fieldname','hydrology.epl_compressibility','>',0.,'numel',[1])
			md = checkfield(md,'fieldname','hydrology.epl_porosity','>',0.,'numel',[1])
			md = checkfield(md,'fieldname','hydrology.epl_max_thickness','numel',[1],'>',0.)
			md = checkfield(md,'fieldname','hydrology.epl_initial_thickness','numel',[1],'>',0.)
			md = checkfield(md,'fieldname','hydrology.epl_colapse_thickness','numel',[1],'>',0.)
			md = checkfield(md,'fieldname','hydrology.epl_thick_comp','numel',[1],'values',[0,1])
			md = checkfield(md,'fieldname','hydrology.eplflip_lock','>=',0.,'numel',[1])
			if self.epl_colapse_thickness > self.epl_initial_thickness:
				md.checkmessage('Colapsing thickness for EPL larger than initial thickness')
			md = checkfield(md,'fieldname','hydrology.epl_conductivity','numel',[1],'>',0.)
	# }}}
	def marshall(self,prefix,md,fid): #{{{ 
		WriteData(fid,prefix,'name','md.hydrology.model','data',1,'format','Integer')
		WriteData(fid,prefix,'object',self,'fieldname','water_compressibility','format','Double')
		WriteData(fid,prefix,'object',self,'fieldname','isefficientlayer','format','Boolean')
		WriteData(fid,prefix,'object',self,'fieldname','penalty_factor','format','Double')
		WriteData(fid,prefix,'object',self,'fieldname','penalty_lock','format','Integer')
		WriteData(fid,prefix,'object',self,'fieldname','rel_tol','format','Double')
		WriteData(fid,prefix,'object',self,'fieldname','max_iter','format','Integer')
		WriteData(fid,prefix,'object',self,'fieldname','sedimentlimit_flag','format','Integer')
		WriteData(fid,prefix,'object',self,'fieldname','transfer_flag','format','Integer')
		if self.sedimentlimit_flag==1:
			WriteData(fid,prefix,'object',self,'fieldname','sedimentlimit','format','Double')

		if self.transfer_flag==1:
			WriteData(fid,prefix,'object',self,'fieldname','leakage_factor','format','Double')

		WriteData(fid,prefix,'object',self,'fieldname','basal_moulin_input','format','DoubleMat','mattype',1,'timeserieslength',md.mesh.numberofvertices+1,'yts',md.constants.yts)
		WriteData(fid,prefix,'object',self,'fieldname','spcsediment_head','format','DoubleMat','mattype',1,'timeserieslength',md.mesh.numberofvertices+1,'yts',md.constants.yts)
		WriteData(fid,prefix,'object',self,'fieldname','sediment_compressibility','format','Double')
		WriteData(fid,prefix,'object',self,'fieldname','sediment_porosity','format','Double')			
		WriteData(fid,prefix,'object',self,'fieldname','sediment_thickness','format','Double')
		WriteData(fid,prefix,'object',self,'fieldname','sediment_transmitivity','format','DoubleMat','mattype',1)		

		if self.isefficientlayer==1:	
			WriteData(fid,prefix,'object',self,'fieldname','spcepl_head','format','DoubleMat','mattype',1,'timeserieslength',md.mesh.numberofvertices+1,'yts',md.constants.yts)	
			WriteData(fid,prefix,'object',self,'fieldname','mask_eplactive_node','format','DoubleMat','mattype',1)
			WriteData(fid,prefix,'object',self,'fieldname','epl_compressibility','format','Double')			
			WriteData(fid,prefix,'object',self,'fieldname','epl_porosity','format','Double')			
			WriteData(fid,prefix,'object',self,'fieldname','epl_max_thickness','format','Double')
			WriteData(fid,prefix,'object',self,'fieldname','epl_initial_thickness','format','Double')			
			WriteData(fid,prefix,'object',self,'fieldname','epl_colapse_thickness','format','Double')
			WriteData(fid,prefix,'object',self,'fieldname','epl_thick_comp','format','Integer')			
			WriteData(fid,prefix,'object',self,'fieldname','epl_conductivity','format','Double')
			WriteData(fid,prefix,'object',self,'fieldname','eplflip_lock','format','Integer')
	# }}}
