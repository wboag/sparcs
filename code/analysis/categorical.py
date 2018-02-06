
import sys
import os
from collections import defaultdict

from data_reader import read_sparcs



def main():

    allowed = ['Emergency Department Indicator', 'Abortion Edit Indicator', 'APR MDC Code', 'APR DRG Description', 'Age Group', 'Discharge Day of Week', 'Gender', 'APR Medical Surgical Description', 'Source of Payment 1', 'Zip Code - 3 digits', 'Type of Admission', 'Patient Disposition', 'APR MDC Description', 'CCS Diagnosis Description', 'CCS Diagnosis Code', 'Facility Name', 'Facility ID', 'APR Risk of Mortality', 'APR DRG Code', 'Discharge Year', 'Admit Day of Week', 'CCS Procedure Description', 'Ethnicity', 'CCS Procedure Code']
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

    bins = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:defaultdict(int))))

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
        bins[diagnosis][race][severity][key] += 1



    for diagnosis,_ in sorted(bins.items(), key=participants):
        print diagnosis
        for race in bins[diagnosis].keys():
            print '\t', race
            for severity in ['Minor', 'Moderate', 'Major', 'Extreme']:
                print '\t\t', severity

                # normalizing constant
                Z = float(sum(bins[diagnosis][race][severity].values()))

                for val,count in sorted(bins[diagnosis][race][severity].items(), key=lambda t:t[1])[-5:]:
                    print '\t\t\t(%4d) %.3f %s' % (count, count/Z, val)
                print
        print



def participants(t):
    val = 0
    for race_vals in t[1].values():
        for severity_vals in race_vals.values():
            val += sum(severity_vals.values())
    return val



if __name__ == '__main__':
    main()
