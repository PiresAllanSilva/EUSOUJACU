# Loop refinement of an existing model
from modeller import *
from modeller.automodel import *
#from modeller import soap_loop

log.verbose()
env = environ()

#directories for input atom files
env.io.atom_file_directory = ['.','../atom_files']

#Create a new class based on 'loopmodel' so that we can redefine
#select_loop_atoms (necessary)
class MyLoop(loopmodel):
	#This routine picks the residues to be refined by loop modelling
	def select_loop_atoms(self):
		#One loop from residue 19 to 28 inclusive
		return selection(self.residue_range('19:', "28:'))
		#Two loops simultaneously
		#return selection(self.residue_range('19:','28:')),
		#		self.residue_range('38:', '42:'))
m = MyLoop(env,
	inimodel='ifdx.B99990001.pdb',   #initial model of the target
	sequence='ifdx',		 #code of the target
	loop_assess_methods=assess.DOPE) #asses loops with DOPE score
#	loop_asses_methods=soap_loop.Scorer()) #asses with SOAP-Loop
m.loop.starting_model = 1
m.loop.ending_model = 100
m.loop.md_level = refine.very_fast #loop refinement method: slow, fast, very_fast
m.make()
