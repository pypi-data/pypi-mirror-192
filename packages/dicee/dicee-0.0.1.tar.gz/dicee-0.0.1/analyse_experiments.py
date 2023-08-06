import os
import json

# (1) Give a path of Experiments folder
input_str_path = 'Experiments/'

# (2) Get all subfolders
sub_folder_str_paths = os.listdir(input_str_path)

results = dict()

experiments = []
for path in sub_folder_str_paths:
    try:
        with open(input_str_path + path + '/configuration.json', 'r') as f:
            config = json.load(f)
            config = {i: config[i] for i in
                      ['model', 'embedding_dim', 'num_epochs', 'batch_size', 'lr', 'callbacks', 'scoring_technique',
                       'path_dataset_folder', 'p', 'q']}
    except:
        print('Exception occured at reading config')
        continue

    try:
        with open(input_str_path + path + '/report.json', 'r') as f:
            report = json.load(f)
            report = {i: report[i] for i in ['Runtime']}
    except:
        print('Exception occured at reading report')
        continue

    try:
        with open(input_str_path + path + '/eval_report.json', 'r') as f:
            eval_report = json.load(f)
            #print(eval_report)
            #exit(1)
            #eval_report = {i: str(eval_report[i]) for i in ['Train', 'Val', 'Test']}
    except:
        print('Exception occured at reading eval_report')
        continue

    config.update(eval_report)
    config.update(report)
    experiments.append(config)

    # exit(1)
    # results.setdefault(config['model'], [str(config) + '\n' + str(eval_report) + '\n' + str(report)]).append(str(config) + '\n' + str(eval_report) + '\n' + str(report))

import pandas as pd


model_name=[]
path_dataset_folder=[]
mrr=[]
hit_1=[]
hit_10=[]
hit_3=[]
pq=[]

for i in experiments:
    if i['model'] != 'CLf':
        model_name.append(i['model'])
        path_dataset_folder.append(i['path_dataset_folder'])
        mrr.append(i['Test']['MRR'])
        hit_1.append(i['Test']['H@1'])
        hit_3.append(i['Test']['H@3'])
        hit_10.append(i['Test']['H@10'])
        pq.append(str(i['p'])+','+str(i['q']))

    else:
        pass

df = pd.DataFrame(dict(model_name=model_name,MRR=mrr,hit1=hit_1,hit3=hit_3,hit10=hit_10,dataset=path_dataset_folder))

print(df.to_latex(index=False))
exit(1)
df = pd.DataFrame(experiments[0])

print(df)
exit(1)
for k, v in results.items():
    for i in v:
        print('\n')
        print(i)
        print(type(i))
        exit(1)
