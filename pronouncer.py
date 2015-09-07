import argparse
import pickle
import glob

from alignment import *
from classifier import *

if __name__ == "__main__":
    ### parse command-line arguments
    parser = argparse.ArgumentParser()

    ### what to do
    parser.add_argument('--train_alignment', action='store_true')
    parser.add_argument('--run_alignment', action='store_true')

    parser.add_argument('--train_classifier', action='store_true')
    parser.add_argument('--run_classifier', action='store_true')

    parser.add_argument('--crossval_classifier', action='store_true')
    parser.add_argument('--test_classifier_depth', action='store_true')


    ### general arguments
    parser.add_argument('--corpus', default='cmudict', choices=['cmudict'])
    parser.add_argument('--stress', default='unstressed', choices=['unstressed','stressed','binarystress'])
    parser.add_argument('--subset', action='store_true')

    ### cluster-specific arguments
    parser.add_argument('--barley_cluster', action='store_true')
    args = parser.parse_args()

    if args.barley_cluster:
        with open('kerberos.txt') as f:
            kerberos_cmd = f.read().strip()
    else:
        kerberos_cmd = None


    em_model_fname = alignment_training.construct_model_fname(args.corpus,
                                                              args.stress,
                                                              args.subset)
    if args.train_alignment and not len(glob.glob(em_model_fname)):
        # train the ViterbiAligner model, saving each iteration as we go
        em = train_alignment(corpus=args.corpus,
                             stress=args.stress,
                             subset=args.subset,
                             kerberos_cmd=kerberos_cmd)

    alignments_fname = alignment_training.construct_alignments_fname(args.corpus,
                                                                     args.stress,
                                                                     args.subset)
    if args.run_alignment and len(glob.glob(em_model_fname)):
        # align all words
        align_all_words(corpus=args.corpus,
                        stress=args.stress,
                        subset=args.subset)

    if args.train_classifier and len(glob.glob(alignments_fname)):
        alignments = load_alignments(args.corpus, args.stress, args.subset)
        dtree = train_classifier(alignments)

    if args.crossval_classifier and len(glob.glob(alignments_fname)):
        alignments = load_alignments(args.corpus, args.stress, args.subset)
        accuracies = crossval_classifier(alignments)
        print accuracies

    if args.test_classifier_depth and len(glob.glob(alignments_fnames)):
        pass
