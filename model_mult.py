from modeller import *
from modeller.automodel import *

env = environ()
a = automodel(env, alnfile='Target-Template.ali',
              knowns=('Template1','Template2','Template3'), sequence='Target',
		assess_methods=(assess.DOPE,
                              #soap_protein_od.Scorer(),
                              assess.GA341))
a.starting_model = 1
a.ending_model = 2000
a.make()

