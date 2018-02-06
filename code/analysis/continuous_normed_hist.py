
import sys
import os
from collections import defaultdict
import pylab as pl

from data_reader import read_sparcs



def main():

    allowed = ['Length of Stay', 'Total Charges', 'Total Costs']
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
        print '\n\tusage: python %s SPARCS.csv <%s>\n' % (sys.argv[0],'|'.join(allowed))
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

        key = row[col]
        bins[diagnosis][race][severity].append(key)



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
            clip_val = sorted(pool)[int(.9*len(pool))]

            # Create 10 bins to fit in that window
            unit = clip_val / 10
            thresholds = [unit*i for i in range(11)]
            buckets = defaultdict(lambda:defaultdict(int))
            for race in ['White', 'Black/African American']:
                for val in bins[diagnosis][race][severity]:
                    # put anything at or above the limit into the rightmost bucket
                    #      (slightly smaller than limit => falls within bucket)
                    if val >= clip_val:
                        val = clip_val-.01
                    # put it in one of the 10 buckets
                    ind = int(val/unit)
                    #bucket = '<$%d' % (thresholds[ind+1])
                    bucket = int(thresholds[ind+1])
                    buckets[race][bucket] += 1

            # Normalize black bins and white bins to each be %s
            normed_buckets = defaultdict(lambda:defaultdict(int))
            for race,hist in buckets.items():
                Z = float(sum(hist.values()))
                normed_hist = { bucket:(val/Z) for bucket,val in hist.items() }
                normed_buckets[race].update(normed_hist)

            # For each bin, do WHITE-BLACK to see the diff
            diff_hist = {}
            for bucket in normed_buckets['White'].keys():
                white = normed_buckets['White'][bucket]
                black = normed_buckets['Black/African American'][bucket]
                diff = white - black
                diff_hist[bucket] = diff

            xy = sorted(diff_hist.items())
            labels,diffs = zip(*xy)
            inds = range(len(labels))

            pl.bar(inds, diffs)
            pl.xticks(inds, labels)

            '''
	    for race in bins[diagnosis].keys():
		print '\t\t', race
                vals = bins[diagnosis][race][severity]

                # clip the values to a max
                vals = [ min(v,clip_val) for v in vals ]

                #print '\t\t\t', sorted(vals)

                # visualize
		color = race.split('/')[0]
		pl.hist(vals, color=color, normed=1)
            '''

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
