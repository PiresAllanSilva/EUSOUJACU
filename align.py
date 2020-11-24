from modeller import *

env = environ()
aln = alignment(env)
mdl = model(env, file='template')
aln.append_model(mdl, align_codes='template', atom_files='template.pdb')
aln.append(file='query.ali', align_codes='query')
aln.align2d()
aln.write(file='query-template.ali', alignment_format='PIR')
