from nltk.tree import Tree
t1 = Tree.fromstring('(ROOT (S (NP (PRP I)) (VP (VBD solved) (NP (DT the) (NN problem)) (PP (IN on) (NP (DT the) (NN bus)))) (. .)))')
#t1.draw()
t2 = Tree.fromstring('(ROOT (S    (NP (PRP I))    (VP (VBD solved)      (NP (DT the) (NN problem))      (PP (IN in)        (NP (DT the) (NN bus))))    (. .)))')
#t2.draw()
t3 = Tree.fromstring('(ROOT (S    (NP (PRP I))    (VP (VBD solved)      (NP (DT the) (NN problem))      (PP (IN about)        (NP (DT the) (NN bus))))    (. .)))')
#t3.draw()
t4 = Tree.fromstring('(ROOT  (S    (NP (PRP I))    (VP (VBD solved)      (NP (DT the) (NN problem))      (PP (IN with)        (NP (DT the) (NN bus))))    (. .)))')
t4.draw()
