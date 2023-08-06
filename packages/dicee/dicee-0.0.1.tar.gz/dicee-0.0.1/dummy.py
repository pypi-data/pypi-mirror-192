from core import KGE
import torch
pre_trained_kge = KGE(path_of_pretrained_model_dir='Experiments/2023-01-09 13:37:41.464353')
print(pre_trained_kge)
x = pre_trained_kge.predict_conjunctive_query(entity='alga',
                                              relations=['isa',
                                                         'causes'],topk=3)
print(x)
exit(1)

# Train the pretrained model on a single datapoint
pre_trained_kge.train_triples(head_entity=["acquired_abnormality"],
                              relation=['location_of'],
                              tail_entity=["acquired_abnormality"],
                              iteration=1,
                              optimizer=torch.optim.Adam(params=pre_trained_kge.parameters(), lr=0.01),
                              labels=[0.0])

second = pre_trained_kge.triple_score(head_entity=["acquired_abnormality"],
                                 relation=['location_of'],
                                 tail_entity=["acquired_abnormality"])
assert second<first
exit(1)

# Add this one to  KGE to pplot stuff
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

df = pd.read_csv('Experiments/2022-12-17 20:51:16.549685/Pyke_entity_embeddings.csv', header=None, index_col=0)
names = df.index.tolist()
X_embedded = TSNE(n_components=2, learning_rate='auto',
                  init='random', perplexity=3).fit_transform(df.values)
assert len(names) == len(X_embedded)
fig, ax = plt.subplots(figsize=(18, 18))
ax.scatter(X_embedded[:, 0], X_embedded[:, 1])
for i, txt in enumerate(names):
    x, y = X_embedded[i]
    ax.annotate(txt, (x, y))
plt.show()

exit(1)
from core import KGE

# (1) Load a pretrained KGE model on KGs/Family
pre_trained_kge = KGE(path_of_pretrained_model_dir='Experiments/2022-12-13 11:16:51.287113')

x = pre_trained_kge.predict_topk(
    head_entity=["<http://www.benchmark.org/family#F9M167>", "<http://www.benchmark.org/family#F9F141>"],
    tail_entity=["<http://www.benchmark.org/family#F9F141>", "<http://www.benchmark.org/family#F9M167>"])

print(x)
exit(1)
# (2) Answer the following conjunctive query question: To whom a sibling of F9M167 is married to?
# (3) Decompose (2) into two query
# (3.1) Who is a sibling of F9M167? => {F9F141,F9M157}
# (3.2) To whom a results of (3.1) is married to ? {F9M142, F9F158}
x = pre_trained_kge.predict_conjunctive_query(entity='<http://www.benchmark.org/family#F9M167>',
                                              relations=['<http://www.benchmark.org/family#hasSibling>',
                                                         '<http://www.benchmark.org/family#married>'], k=1)

print(x)
