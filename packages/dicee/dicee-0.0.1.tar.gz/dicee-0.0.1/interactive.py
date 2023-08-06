from core import KGE

model = KGE('Experiments/2023-02-14 12:13:30.891171')

answer_set, intermediate_results = model.predict_conjunctive_query(entity='<http://www.benchmark.org/family#F9M167>',
                                                                   relations=['<http://www.benchmark.org/family#hasSibling>',
                                                                              '<http://www.benchmark.org/family#hasSibling>'], topk=3,
                                                                   show_intermediate_results=True)
for k, v in intermediate_results.items():
    print(k, v)
exit(1)
import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 0, 0.1  # mean and standard deviation
s = np.random.normal(mu, sigma, 1000)

print(s)
exit(1)
Z = np.array([1, 1, 1, 2, 2, 4, 5, 6, 6, 6, 7, 8, 8])
X, F = np.unique(Z, return_index=True)
F = F / X.size

plt.plot(X, F)
plt.show()

exit(1)
from core import KGE

pre_trained_kge = KGE(path_of_pretrained_model_dir='Experiments/2023-01-05 14:24:50.493071')

x = pre_trained_kge.predict_conjunctive_query(entity='alga',
                                              relations=['isa',
                                                         'causes'], topk=1)
print(x)
exit(1)

from core import KGE

# (1) Load a pretrained ConEx on DBpedia
pre_trained_kge = KGE(path_of_pretrained_model_dir='Experiments/2022-12-27 08:50:57.165285')

print(pre_trained_kge)

print(type(pre_trained_kge.get_entity_embeddings(['body_part_organ_or_organ_component'])))
exit(1)
m = pre_trained_kge.triple_score(head_entity=["http://dbpedia.org/resource/Albert_Einstein"],
                                 relation=["http://dbpedia.org/ontology/birthPlace"],
                                 tail_entity=["http://dbpedia.org/resource/Ulm"])  # tensor([0.9309])
print(m)
exit(1)
from core import KGE

# Train a model on Family Dataset
pre_trained_kge = KGE(path_of_pretrained_model_dir='Experiments/2022-12-08 11:46:33.654677')

# Question: Whom a sibling of F9M167 is  married to ?
# Setup (1) Who is a sibling of F9M167?
# <http://www.benchmark.org/family#F9M167> <http://www.benchmark.org/family#hasSibling> <http://www.benchmark.org/family#F9F141> .
# <http://www.benchmark.org/family#F9M167> <http://www.benchmark.org/family#hasSibling> <http://www.benchmark.org/family#F9M157> .
# Step (2)Whom entities obtained in (2) are married to
# <http://www.benchmark.org/family#F9F141> <http://www.benchmark.org/family#married> <http://www.benchmark.org/family#F9M142> .
# <http://www.benchmark.org/family#F9M157> <http://www.benchmark.org/family#married> <http://www.benchmark.org/family#F9F158> .
# ANSWER: <http://www.benchmark.org/family#F9M142> or <http://www.benchmark.org/family#F9F158>
res = pre_trained_kge.predict_conjunctive_query(entity='<http://www.benchmark.org/family#F9M167>',
                                                relations=['<http://www.benchmark.org/family#hasSibling>',
                                                           '<http://www.benchmark.org/family#married>'], k=1)
# print(res) => {'<http://www.benchmark.org/family#F9M142>'}
