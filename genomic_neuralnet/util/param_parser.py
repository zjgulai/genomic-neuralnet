from __future__ import print_function

import os
import sys

from argparse import ArgumentParser, SUPPRESS
from genomic_neuralnet.config import data
from subprocess import call

_parser = ArgumentParser()
_parser.add_argument('-s', '--species', default='arabidopsis', choices=data.keys(), help='Species')
_parser.add_argument('-t', '--trait', default='flowering', help='Trait')
_parser.add_argument('-v', '--verbose', action='store_true', help='Print more information')
_parser.add_argument('-f', '--force', action='store_true', help='Force re-fitting of model')
_parser.add_argument('--list', action='store_true', help='Print a list of traits for the chosen species and exit')
_parser.add_argument('--stats', action='store_true', help='Print stats about dataset and exit')
_parser.add_argument('--gpu', action='store_true', help='Run on GPU if available')
_parser.add_argument('--gpux', action='store_true', help=SUPPRESS) # Hidden argument for GPU paralellism.

_arguments = None
def get_arguments():
    global _arguments
    if _arguments is None:
        _arguments = _parser.parse_args()
        _handle_list_option(_arguments)
        _handle_show_stats_option(_arguments)
        allowed_traits = data[_arguments.species].keys()
        if not _arguments.trait in allowed_traits:
            msg = 'Trait not found. Expected one in list: [{}].'
            print(msg.format(', '.join(allowed_traits)))
            exit()
        _maybe_set_parallel_args(_arguments)
    return _arguments

def _maybe_set_parallel_args(args):
    """
    You cannot add Theano gpu parallelism flags
    after importing Theano, and we don't know when
    it will get imported. This adds them to
    the environment and re-calls this same command/script. 
    This provides a guarantee that we use the GPU 
    parallelism option no matter when Theano is
    imported.
    """
    if args.gpu and (not args.gpux):  
        # Set the GPU environment.
        os.environ['THEANO_FLAGS'] = 'floatX=float32,device=gpu,lib.cnmem=1'
        # Re-execute this process with the new environment.
        exit(call([sys.executable] + sys.argv + ['--gpux']))

def _handle_list_option(args):
    """
    Print a list of traits for the chosen species and exit.
    """
    if args.list:
        species, _ = get_species_and_trait()
        print(' '.join(data[species].keys()))
        exit()
    else:
        return

def _handle_show_stats_option(args):
    """ Should ."""
    if args.stats:
        species, trait = get_species_and_trait()
        definition = data[species][trait]
        markers = len(definition.markers)
        samples = len(definition.pheno)
        print('{} {} = {} markers X {} samples'.format(species, trait, markers, samples))
        exit()
    else:    
        return 

def get_should_force():
    """ Should force re-training of model."""
    args = get_arguments()
    return args.force

def get_is_on_gpu():
    """ 
    The gpux flag means we have the environment properly set
    for doing GPU compute.
    """
    args = get_arguments()
    return args.gpux

def get_markers_and_pheno():
    species, trait = get_species_and_trait()
    markers = data[species][trait].markers
    pheno = data[species][trait].pheno
    return markers, pheno

def get_species_and_trait():
    args = get_arguments()
    return args.species, args.trait

def get_verbose():
    args = get_arguments()
    return args.verbose
