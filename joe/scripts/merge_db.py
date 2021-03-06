#!/usr/bin/env python

import argparse, os, sys


parser = argparse.ArgumentParser(description='pluck candidates from my databse for whom we also have financial data')
parser.add_argument('--fn_cand_parse', type=str, help="keri's cand parse file", default='../../data/candidates/cand_parse.dat')
parser.add_argument('--fn_dw_data', type=str, help='my dwn database filename', default='../out/ALL.dat')
parser.add_argument('--fn_save', type=str, help='save to this file', default='../out/cand_parse_all_fresh.dat')
args = parser.parse_args()


def main():
    already_seen = set([])
    f_out = open(args.fn_save, 'w')

    with open(args.fn_dw_data, 'r') as f_dwn:
        peeps = [line.split() for line in f_dwn.readlines()[1:]]
    
    # since we're going to save only most recent score, 
    # reverse the database and parse it in that order
    peeps = list( reversed(peeps) )

    with open(args.fn_cand_parse, 'r') as f_cand_parse:
        cand_parse_raw = [line.split() for line in f_cand_parse.readlines()[1:]]

    for line in cand_parse_raw:
        # exclude senate people and those with label 'pres'
        state = line[-3]
        cand_ID = line[-1]

        if len(state) == 2 and state != 'None':
            last_name = line[1].lower()
            party = line[-2]

            # check to see if they are in my db
            for db_line in peeps:

                if last_name in db_line and state == db_line[3] and party == db_line[4]:

                    if not cand_ID in already_seen:
                        already_seen.add(cand_ID)
                        # bingo, we need to process them
                        line_to_write = '\t'.join(line) + '\t' + \
                                        '\t'.join(db_line[1:3]) + '\n'
                        f_out.write(line_to_write)
    f_out.close()


if __name__ == '__main__':
    main()
