# Neural Retrieval for Description Logic Concept Learning
from collections import Counter
import itertools
from core import KGE
import torch

model = KGE('Experiments/2023-02-11 16:20:07.437826', compute_range_and_domain=True)

# s, type Mother
# s, r , x
# http://www.benchmark.org/family#F2F14
pos = ["http://www.benchmark.org/family#F2F14",
       "http://www.benchmark.org/family#F2F12",
       "http://www.benchmark.org/family#F2F19",
       "http://www.benchmark.org/family#F2F26",
       "http://www.benchmark.org/family#F2F28",
       "http://www.benchmark.org/family#F2F36",
       "http://www.benchmark.org/family#F3F52",
       "http://www.benchmark.org/family#F3F53",
       "http://www.benchmark.org/family#F5F62"
    , "http://www.benchmark.org/family#F6F72"
    , "http://www.benchmark.org/family#F6F79"
    , "http://www.benchmark.org/family#F6F77"
    , "http://www.benchmark.org/family#F6F86"
    , "http://www.benchmark.org/family#F6F91"
    , "http://www.benchmark.org/family#F6F84"
    , "http://www.benchmark.org/family#F6F96"
    , "http://www.benchmark.org/family#F6F101"
    , "http://www.benchmark.org/family#F6F93"
    , "http://www.benchmark.org/family#F7F114"
    , "http://www.benchmark.org/family#F7F106"
    , "http://www.benchmark.org/family#F7F116"
    , "http://www.benchmark.org/family#F7F119"
    , "http://www.benchmark.org/family#F7F126"
    , "http://www.benchmark.org/family#F7F121"
    , "http://www.benchmark.org/family#F9F148"
    , "http://www.benchmark.org/family#F9F150"
    , "http://www.benchmark.org/family#F9F143"
    , "http://www.benchmark.org/family#F9F152"
    , "http://www.benchmark.org/family#F9F154"
    , "http://www.benchmark.org/family#F9F141"
    , "http://www.benchmark.org/family#F9F160"
    , "http://www.benchmark.org/family#F9F163"
    , "http://www.benchmark.org/family#F9F158"
    , "http://www.benchmark.org/family#F9F168"
    , "http://www.benchmark.org/family#F10F174"
    , "http://www.benchmark.org/family#F10F179"
    , "http://www.benchmark.org/family#F10F181"
    , "http://www.benchmark.org/family#F10F192"
    , "http://www.benchmark.org/family#F10F193"
    , "http://www.benchmark.org/family#F10F186"
    , "http://www.benchmark.org/family#F10F195"
       ]
neg = ["http://www.benchmark.org/family#F6M99"
    , "http://www.benchmark.org/family#F10F200"
    , "http://www.benchmark.org/family#F9F156"
    , "http://www.benchmark.org/family#F6M69"
    , "http://www.benchmark.org/family#F2F15"
    , "http://www.benchmark.org/family#F6M100"
    , "http://www.benchmark.org/family#F8F133"
    , "http://www.benchmark.org/family#F3F48"
    , "http://www.benchmark.org/family#F2F30"
    , "http://www.benchmark.org/family#F4F55"
    , "http://www.benchmark.org/family#F6F74"
    , "http://www.benchmark.org/family#F10M199"
    , "http://www.benchmark.org/family#F7M104"
    , "http://www.benchmark.org/family#F9M146"
    , "http://www.benchmark.org/family#F6M71"
    , "http://www.benchmark.org/family#F2F22"
    , "http://www.benchmark.org/family#F2M13"
    , "http://www.benchmark.org/family#F9F169"
    , "http://www.benchmark.org/family#F5F65"
    , "http://www.benchmark.org/family#F6M81"
    , "http://www.benchmark.org/family#F7M131"
    , "http://www.benchmark.org/family#F7F129"
    , "http://www.benchmark.org/family#F7M107"
    , "http://www.benchmark.org/family#F10F189"
    , "http://www.benchmark.org/family#F8F135"
    , "http://www.benchmark.org/family#F8M136"
    , "http://www.benchmark.org/family#F10M188"
    , "http://www.benchmark.org/family#F9F164"
    , "http://www.benchmark.org/family#F7F118"
    , "http://www.benchmark.org/family#F2F10"
    , "http://www.benchmark.org/family#F6F97"
    , "http://www.benchmark.org/family#F7F111"
    , "http://www.benchmark.org/family#F9M151"
    , "http://www.benchmark.org/family#F4M59"
    , "http://www.benchmark.org/family#F2M37"
    , "http://www.benchmark.org/family#F1M1"
    , "http://www.benchmark.org/family#F9M142"
    , "http://www.benchmark.org/family#F4M57"
    , "http://www.benchmark.org/family#F9M170"
    , "http://www.benchmark.org/family#F5M66"
    , "http://www.benchmark.org/family#F9F145"
       ]
# {x | e type x \in G}
# range_of_type = model.get_range_of_relation('<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>')
pos = {'<' + i + '>' for i in pos}
neg = {'<' + i + '>' for i in neg}
relations = [i for i in model.relation_to_idx.keys() if 'inverse' not in i and 'family#' in i]


def batch_type_prediction(input_individuals, relation="<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"):
    # (1) Predict scores.
    scores = model.predict(head_entities=[i for i in input_individuals],
                           relations=[relation for _ in range(len(input_individuals))])
    # (2) Compute average score for all tail entities gtiven all heads and a relation
    avg_scores = scores.mean(dim=0).flatten()
    # (3) Returns entities in descending order of scores
    return sorted([(k, avg_scores[v]) for k, v in model.entity_to_idx.items()], key=lambda x: x[1], reverse=True)


def relation_type_prediction(input_individuals, role):
    entities_given_relation = batch_type_prediction(input_individuals, role)
    return batch_type_prediction([i for i, _ in entities_given_relation])


def compute_f1(retrieval_results, pos, neg):
    tp = len(retrieval_results.intersection(pos))
    fp = len(neg.intersection(retrieval_results))
    tn = len(neg - retrieval_results)
    return tp / (tp + 0.5 * (tn + fp))


class NamedConcept:
    def __init__(self, str_name):
        self.str = str_name
        self.quality = -1.0
        self.individuals = set()

    def __str__(self):
        return f"NC: {self.str}\tQuality:{self.quality:.3f}\t|Indv|:{len(self.individuals)}"


class URConcept:
    def __init__(self, role, filler):
        self.role = role
        self.filler = filler
        self.str = f'ALL{self.role}.{self.filler.str}'
        self.quality = -1.0
        self.individuals = set()

    def __str__(self):
        return f"URC: {self.str}\tQuality:{self.quality:.3f}\t|Indv|:{len(self.individuals)}"

class IntersectConcept:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.quality = -1.0
        self.individuals = self.a.individuals.intersection(self.b.individuals)


    def __str__(self):
        return f"Intersect: {self.a.str}\t AND \t{self.b.str}\t Quality:{self.quality}"
def retrieval_func(concept):
    if isinstance(concept, NamedConcept):
        # All triples having str_name_concept as object
        triples_with_type_infos = model.train_set[
            model.train_set[:, 1] == model.relation_to_idx['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>']]
        return {model.idx_to_entity[i] for i in
                set(triples_with_type_infos[triples_with_type_infos[:, 2] == model.entity_to_idx[concept.str]][:, 0])}
    elif isinstance(concept, URConcept):
        result = set()
        triples_with_relation_infos = model.train_set[model.train_set[:, 1] == model.relation_to_idx[concept.role]]
        for idspo in triples_with_relation_infos:
            ids, _, ido = idspo
            if model.idx_to_entity[ido] in concept.filler.individuals:
                result.add(model.idx_to_entity[ids])
        return result
    else:
        print('WRONG')
        exit(1)

# Build goal concept
female=NamedConcept("<http://www.benchmark.org/family#Female>")
female.individuals = retrieval_func(female)
female.quality = compute_f1(female.individuals, pos, neg)
print(female)

person=NamedConcept("<http://www.benchmark.org/family#Person>")
person.individuals = retrieval_func(person)

forall_hassibling_person=URConcept(role="<http://www.benchmark.org/family#hasSibling>",filler=person)
forall_hassibling_person.individuals = retrieval_func(forall_hassibling_person)
forall_hassibling_person.quality = compute_f1(forall_hassibling_person.individuals, pos, neg)

print(forall_hassibling_person)


print(compute_f1(forall_hassibling_person.individuals.intersection(female.individuals), pos, neg))
exit(1)
selected_named_concepts = []
# Top10 results. E.g., mean(score_(i type Female),score_(j type Female))
for str_concept, score in batch_type_prediction(pos)[:10]:
    x = NamedConcept(str_concept)
    x.individuals = retrieval_func(x)
    x.quality = compute_f1(x.individuals, pos, neg)
    selected_named_concepts.append(x)

restrictions=[]
for rel in relations:
    for str_concept, score in relation_type_prediction(pos, rel)[:10]:
        filler = NamedConcept(str_concept)
        filler.individuals = retrieval_func(filler)
        urc = URConcept(role=rel, filler=filler)
        urc.individuals = retrieval_func(urc)
        urc.quality = compute_f1(urc.individuals, pos, neg)
        if urc.quality == 0:
            continue
        restrictions.append(urc)


search_tree=selected_named_concepts+restrictions
search_tree.sort(key=lambda x: x.quality, reverse=True)


asd=[]
for i in search_tree:
    for j in search_tree:
        if i==j:
            continue
        ij=IntersectConcept(i,j)
        ij.quality = compute_f1(ij.individuals, pos, neg)
        if ij.quality == 0:
            continue
        asd.append(ij)

search_tree.extend(asd)
search_tree.sort(key=lambda x: x.quality, reverse=True)
for i in search_tree:
    print(i)
exit(1)
for rel in relations:
    sum_scores = model.predict(head_entities=[i for i in pos],
                               relations=[rel for _ in range(len(pos))]).mean(dim=0).flatten()
    results = []
    for k, v in model.entity_to_idx.items():
        results.append((k, sum_scores[v]))
    results.sort(key=lambda x: x[1], reverse=True)

    selected_top_10_entities = []
    for ent, s in results[:10]:
        selected_top_10_entities.append(ent)

    print(rel)
    for i in batch_type_prediction(selected_top_10_entities)[:10]:
        print(i)
    exit(1)

results = []
for k, v in model.entity_to_idx.items():
    results.append([k, avg_scores[v]])
results.sort(key=lambda x: x[1], reverse=True)

exit(1)

# first_hop_prediction()

# find_first_hop_role_predictions
relations = [i for i in model.relation_to_idx.keys() if 'inverse' not in i and 'family#' in i]
for rel in relations:
    # e \in E^+ [e rel ?]
    results = first_hop_prediction(entities=pos)
    for i in results[:10]:
        print(i)

    exit(1)
exit(1)
# (1) Predict types of positives
scores = model.predict(head_entities=[i for i in pos],
                       relations=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>" for _ in range(len(pos))])

top_predicted_named_concepts = []
# (2) Average (1) per each type
for entity, score in zip(model.entity_to_idx.keys(), scores.mean(dim=0)):
    # Threshold for the prediction
    if score > 0.2:
        top_predicted_named_concepts.append((entity, score))

top_predicted_named_concepts.sort(key=lambda x: x[1], reverse=True)
for i in top_predicted_named_concepts:
    print(i)

exit(1)

# Select triples having subclassof as a relation

concept_hierarchy = [[model.idx_to_entity[i[0]], model.idx_to_entity[i[2]]] for i in model.train_set[
    model.train_set[:, 1] == model.relation_to_idx['<http://www.w3.org/2000/01/rdf-schema#subClassOf>']]]
set_of_named_concepts = set(itertools.chain(*concept_hierarchy))

similarty = []
for i in set_of_named_concepts:
    scores_i = model.predict(relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"], tail_entity=[i])
    for j in set_of_named_concepts:
        if i == j:
            continue
        scores_j = model.predict(relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"], tail_entity=[j])
        cosine = float(
            (scores_i @ scores_j) / (torch.sqrt(torch.sum(scores_i ** 2)) * torch.sqrt(torch.sum(scores_j ** 2))))

        similarty.append((i, j, cosine))

similarty.sort(key=lambda x: x[-1], reverse=True)

for i in similarty:
    print(i)

exit(1)
# Find similarity between named concepts
scores, preds = model.predict(relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"], tail_entity=[i])


def neural_retrieval_func(name_concept: NamedConcept, topk=10):
    # All triples having str_name_concept as object
    scores, preds = model.predict_topk(relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"],
                                       tail_entity=[name_concept.str], topk=topk)
    return set(preds)  # {}{preds[i] for i, score in enumerate(scores) if score >= 0.99}


search_tree = set()
for i in set_of_named_concepts:
    x = NamedConcept(i)
    x.predicted_individuals = neural_retrieval_func(x)
    x.predicted_quality = compute_f1(x.predicted_individuals, pos, neg)
    x.individuals = retrieval_func(x)
    x.quality = compute_f1(x.individuals, pos, neg)
    search_tree.add(x)

# search_tree.sort(key=lambda x: x.predicted_quality, reverse=True)
unions = set()
intersections = set()
for i in search_tree:
    for j in search_tree:
        ij = i.union_operator(j)
        ij.predicted_quality = compute_f1(ij.predicted_individuals, pos, neg)
        ij.quality = compute_f1(ij.individuals, pos, neg)
        if ij.predicted_quality > 0:
            unions.add(ij)
        ij = i.intersection_operator(j)
        ij.predicted_quality = compute_f1(ij.predicted_individuals, pos, neg)
        ij.quality = compute_f1(ij.individuals, pos, neg)
        if ij.predicted_quality > 0:
            intersections.add(ij)

search_tree.update(unions)
search_tree.update(intersections)
print(len(search_tree))
for i in search_tree:
    print(i)
exit(1)


def find_roles_of_entities(ent):
    roles = set()
    for i in ent:
        idx_i = model.entity_to_idx[i]
        # relations occur with a positive individual
        roles.update(set(model.train_set[model.train_set[:, 0] == idx_i][:, 1]))
    return {model.idx_to_relations[i] for i in roles if '_inverse' not in model.idx_to_relations[i]}


def find_types_of_entities(ent):
    concepts = set()
    for i in ent:
        idx_i = model.entity_to_idx[i]
        cbd = model.train_set[model.train_set[:, 0] == idx_i]
        concepts.update(
            set(cbd[cbd[:, 1] == model.relation_to_idx['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>']][:, 2]))
    return {model.idx_to_entity[i] for i in concepts}


def predict_types_of_entities(ent: list[str], topk=25):
    results = []
    for e in ent:
        _, i = model.predict_topk(head_entity=[e],
                                  relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"], topk=topk)
        results.extend(i)
    return {k for k, v in Counter(results).most_common(topk)}


# Related Concepts
# positive_concepts = find_types_of_entities(pos)
# negative_concepts = find_types_of_entities(neg)
# candidate_concepts = positive_concepts - negative_concepts
# non_candidate_concepts = negative_concepts - positive_concepts
# print(f'Found concepts of positives:{positive_concepts}')
# print(f'Found concepts of negatives:{negative_concepts}')
# print('Found candidate concepts')
# print(candidate_concepts)
# print('Found non candidate Concepts')
# print(non_candidate_concepts)


positive_concepts = predict_types_of_entities(pos)
negative_concepts = predict_types_of_entities(neg)
candidate_concepts = positive_concepts - negative_concepts
non_candidate_concepts = negative_concepts - positive_concepts

print(f'Number of predicted concepts of positives:{len(positive_concepts)}')
for i in positive_concepts:
    print(f'{i} F1:{compute_f1(retrieval_func(i), pos=pos, neg=neg)}')

print(f'Number of predicted concepts of negatives:{len(negative_concepts)}')
for i in negative_concepts:
    print(f'{i} F1:{compute_f1(retrieval_func(i), pos=pos, neg=neg)}')

print(f'Number of candidate concepts :{len(candidate_concepts)}')
for i in candidate_concepts:
    print(f'{i} F1:{compute_f1(retrieval_func(i), pos=pos, neg=neg)}')

print(f'Number of non candidate concepts :{len(non_candidate_concepts)}')
for i in non_candidate_concepts:
    print(f'{i} F1:{compute_f1(retrieval_func(i), pos=pos, neg=neg)}')

exit(1)

print(f'Predicted concepts of negatives:{negative_concepts}')
print('Predicted candidate concepts')
print(candidate_concepts)
print('Predicted non candidate Concepts')
print(non_candidate_concepts)
exit(1)


def first_hop_type_predictions(examples, predictor, topk=10):
    hop_results = []
    filtered_results = set()
    # (1) For each example, extract topk predictions
    for e in examples:
        _, i = predictor.predict_topk(head_entity=[e],
                                      relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"], topk=topk)
        hop_results.extend(i)

    # (2) filter less frequent predictions
    for k, v in dict(Counter(hop_results)).items():
        if v > (len(examples) / 2):
            filtered_results.add(k)
    return filtered_results


print('Concepts found in the first-hop of E^+')
pred_pos = first_hop_type_predictions(pos, model)
print(pred_pos)
# relations_given_a_subjec
print('Roles found in the first-hop of E^+')
relations = set()
for i in pos:
    idx_i = model.entity_to_idx[i]
    # relations occur with a positive individual
    relations.update(set(model.train_set[model.train_set[:, 0] == idx_i][:, 1]))
# Remove inverses
relations = {model.idx_to_relations[i] for i in relations if '_inverse' not in model.idx_to_relations[i]}

print(relations)
exit(1)

for i in pred_pos:
    print(i)

    scores, entities = model.predict_topk(relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"],
                                          tail_entity=[i], topk=model.num_entities)
    preds = [entities[i] for i, score in enumerate(scores) if score >= 0.99]
    print(f'Predicted {i}: entities {len(preds)}')

exit(1)

print('First Hop E^- predictions')
pred_neg = first_hop_type_predictions(neg, model)
print(pred_neg)

exit(1)
one_hop_predictions = list()
for e in pos:
    scores = [(c, float(
        model.triple_score(head_entity=[e], relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"],
                           tail_entity=[c]))) for c in concepts]

    one_hop_predictions.append((e, scores))

print(one_hop_predictions[0])
print(len(one_hop_predictions))
exit(1)

for i in one_hop_predictions:
    print(i)
    exit(1)

exit(1)
types = []
for e in set(results):
    scores, entities = model.predict_topk(head_entity=[e],
                                          relation=["<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"], topk=3)
    if '<http://www.w3.org/2002/07/owl#Ontology>' in entities or "<http://www.w3.org/2002/07/owl#Class>" in entities:
        types.append(e)

print(types)
