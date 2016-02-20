import numpy as np
import os
import csv

new_csv_name = raw_input("Please type in the new csv name and press 'Enter': ")
f = raw_input("Please type in the path you want to start from and press 'Enter': ")

print('Starting to walk down directories')
# e.g. first run from os.path.expanduser('~/Dropbox/deep-retina/saved')
walker = os.walk(f, topdown=True)
architecture_name = 'architecture.json'
performance_name = 'performance.csv'

models_parsed = 0
all_models = []
for dirs, subdirs, files in walker:
    if architecture_name in files:
        # Parse README.md
        readme_path = path[0] + '/' + readme_name
        f = open(readme_path, 'r')
        description = f.readlines()
        path_components = readme_path.split('/')
        for idd, d in enumerate(description):
            if d.find('Cell') >= 0:
                cells = d[:-1]
            elif d.find('Stimulus') >= 0:
                experiment = description[idd+1][:-1]
                stimulus = description[idd+2][:-1]
        
        # Parse performance.csv
        performance_path = path[0] + '/' + 'performance.csv'
        h = open(performance_path, 'r')
        stats = csv.reader(h)
        all_rows = []
        for row in stats:
            all_rows.append(row)
        num_epochs = len(all_rows) - 1 # -1 for the header
        
        # skip models for which we have no performance data
        if num_epochs >= 1:
            table = np.array(all_rows)
            just_numbers = table[1:, :].astype('float')

            model = {
                'type': description[0][2:-1],
                'date': description[1][3:-1],
                'machine': path_components[-3],
                'folder': path_components[-2],
                'stimulus': stimulus,
                'experiment': experiment,
                'cells': cells,
                'epochs': num_epochs,
                'max_train_cc': np.max(just_numbers, axis=0)[2],
                'mean_train_cc': np.mean(just_numbers, axis=0)[2],
                'max_test_cc': np.max(just_numbers, axis=0)[3],
                'mean_test_cc': np.mean(just_numbers, axis=0)[3],
            }
            all_models.append(model)
            models_parsed += 1
            print('Saved model %i' %(models_parsed))
        
header = {}
for k in sorted(all_models[0].keys()):
    header[k] = k

all_models.insert(0, header)

g = open(new_csv_name,'w')
w = csv.DictWriter(g, all_models[0].keys())
w.writerows(all_models)
g.close()