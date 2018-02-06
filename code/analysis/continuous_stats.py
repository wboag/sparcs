
import sys
import os
from collections import defaultdict
import pylab as pl
import numpy as np

from data_reader import read_sparcs



def main():

    allowed = ['Length of Stay', 'Total Charges', 'Total Costs', 'cost per day', 'charge per day']
    try:
        if sys.argv[1] == 'all':
            data = []
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            home_dir = os.path.dirname(parent_dir)
            crawl_dir = os.path.join(home_dir, 'data')
            for filename in os.listdir(crawl_dir):
                if filename.endswith('.csv'):
                    d = read_sparcs(os.path.join(crawl_dir, filename))
                    data += d
        else:
            data = read_sparcs(sys.argv[1])

        col = sys.argv[2]
        if col not in allowed: raise Exception('oops')
    except Exception, e:
        print e
        print '\n\tusage: python %s <SPARCS.csv|all> <%s> [--plot] [--stats]\n' % (sys.argv[0],'|'.join(allowed))
        exit(1)

    bins = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))

    for row in data:
        diagnosis = row['CCS Diagnosis Description']
        race = row['Race']
        severity = row['APR Severity of Illness Description']

        gender = row['Gender']
        age = row['Age Group']
        insurance = row['Source of Payment 1']
        los = row['Length of Stay']
        zip_code = row['Zip Code - 3 digits']
        procedure = row['CCS Procedure Description']

        if race == 'Other Race': continue
        if race == 'Multi-racial': continue

        if col == 'cost per day':
            val = row['Total Costs'] / row['Length of Stay']
        elif col == 'charge per day':
            val = row['Total Charges'] / row['Length of Stay']
        else:
            val = row[col]

        bins[diagnosis][race][severity].append(val)



    for diagnosis,_ in sorted(bins.items(), key=participants):
        print diagnosis
	for severity in ['Minor', 'Moderate', 'Major', 'Extreme']:
            # graphing speedup
            if participants((_,bins[diagnosis])) < 1000:
                continue

	    print '\t', severity

            # How big should the x-axis be to fit 90% of the cases?
            pool = []
            for race in bins[diagnosis].keys():
                pool += bins[diagnosis][race][severity]

            if len(pool) == 0: 
                continue

            clip_val = sorted(pool)[int(.9*len(pool))]

	    #for race in bins[diagnosis].keys():
	    for race in ['White', 'Black/African American']:
                if len(bins[diagnosis][race][severity]) == 0:
                    continue

		#print '\t\t', race
                vals = bins[diagnosis][race][severity]

                # clip the values to a max
                vals = [ min(v,clip_val) for v in vals ]

                #print '\t\t\t', sorted(vals)

                num = len(vals)
                median = sorted(vals)[num/2]
                np_vals = np.array(vals)
                mean = np_vals.mean()
                std  = np_vals.std()
                if '--stats' in sys.argv:
                    print '\t\t%-25s: n=%5d\tmedian=%6d\tmean=%10.3f\tstd=%9.3f' % (race,num,median,mean,std)

                # visualize
		color = race.split('/')[0]
		#pl.hist(vals, color=color, normed=1)
		pl.hist(vals, color=color, normed=0)

            if '--plot' in sys.argv:
                pl.xlabel(sys.argv[2])
                pl.ylabel('Number of individuals')
                pl.title('%s for %s %s' % (sys.argv[2],severity,diagnosis))
                pl.grid(True)

                pl.show()

        print



def participants(t):
    val = 0
    for race_vals in t[1].values():
        for severity_vals in race_vals.values():
            val += len(severity_vals)
    return val



if __name__ == '__main__':
    main()
