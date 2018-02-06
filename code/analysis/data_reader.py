
import re

def read_sparcs(csv):
    data = []
    with open(csv, 'r') as f:
        lines = f.readlines()
        labels = re.findall('"(.*?)"', lines[0])

        num_labels = len(labels)
        for i,line in enumerate(lines[1:]):
            toks = re.findall('"(.*?)"', line)
            assert len(toks) == num_labels, toks

            var = {label:tok for label,tok in zip(labels,toks)}
            '''
            print var
            print
            #exit()
            '''

            if var['Length of Stay'] == '120 +':
                var['Length of Stay'] = '120'

            int_cols = ['Length of Stay',]
            for col in int_cols:
                var[col] = float(var[col])

            float_cols = ['APR Severity of Illness Code', 'Total Charges', 'Total Costs']
            for col in float_cols:
                var[col] = float(var[col])

            data.append(var)
    return data

