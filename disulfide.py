# Comparative modeling by the automodel class
from modeller import *              # Load standard Modeller classes
from modeller.automodel import *    # Load the automodel class

# Redefine the special_patches routine to include the additional disulfides
# (this routine is empty by default):
class MyModel(automodel):
    def special_patches(self, aln):
        # A disulfide between residues 8 and 45:
        self.patch(residue_type='DISU', residues=(self.residues['15'],
                                                  self.residues['41']))
        self.patch(residue_type='DISU', residues=(self.residues['18'],
                                                  self.residues['36']))
        self.patch(residue_type='DISU', residues=(self.residues['24'],
                                                  self.residues['44']))
        self.patch(residue_type='DISU', residues=(self.residues['28'],
                                                  self.residues['46']))
	

log.verbose()    # request verbose output
env = environ()  # create a new MODELLER environment to build this model in
env.io.hetatm=1
# directories for input atom files
env.io.atom_files_directory = ['.', '../atom_files']

a = MyModel(env,
            alnfile  = 'query-template.ali',     # alignment filename
            knowns   = ('template'),              # codes of the templates
            sequence = 'query',
	    assess_methods=(assess.DOPE, assess.GA341))              # code of the target
a.starting_model= 1                 # index of the first model
a.ending_model  = 100                 # index of the last model
                                    # (determines how many models to calculate)
a.make()                            # do the actual comparative modeling
