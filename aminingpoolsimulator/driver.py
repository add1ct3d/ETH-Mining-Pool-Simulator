'''
Simulator for the bitcoin solo-block pool attack
'''

import shlex
import sys
import os
import argparse
import logging
import datetime
import time
from aminingpoolsimulator.pool import MiningPool

def main():
    '''
    Just process commandline arguments to run sim appropriately
    '''

    logging.basicConfig(filename='mining_pool_sim_{}.log'.format(int(time.time())), level=logging.INFO)
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    parser = argparse.ArgumentParser()
    parser.add_argument("num_honest_miners",
                        help="number of honest miners to run sim with",
                        type=int)
    parser.add_argument("num_malicious_miners",
                        help="number of malicious miners to run sim with",
                        type=int)
    parser.add_argument("hash_rates_file",
                        help="file with distribution of hashrates")
    parser.add_argument("num_blocks_to_find",
                        help="Number of blocks to simulate",
                        type=int)
    parser.add_argument("round_length",
                        help="Length of each round (in seconds) \
                              Length of time between malicious strategy update",
                        type=int)
    parser.add_argument("shares_per_second",
                        help="How many shares each miner should get per second",
                        type=int)
    parser.add_argument("attack_type",
                        help="What attack to run. Options are: COST, SPITE, SCORCHED_EARTH",
                        type=str)
    parser.add_argument("seed",
                        help="Seed used to determine the values generated by random and numpy.random",
                        type=int)
    parser.add_argument("-v", "--verbose", help="increase logger verbosity",
                        action="store_true")
    parser.add_argument("--attack_params",
                        help="Attack-specific parameters.",
                        default='',
                        type=str)
    parser.add_argument("file_name",
                        help="File to output data to",
                        type=str)
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if os.path.isfile(args.hash_rates_file) is not True:
        print("hash rates file given is not a real file, exiting")
        sys.exit(1)

    logger.info("New pool simulation on: {0}".format(datetime.datetime.now()))
    logger.info(' '.join(shlex.quote(arg) for arg in sys.argv))
    logger.info("Sim of {0} honest miners and {1} malicious miners".format(args.num_honest_miners, args.num_malicious_miners))
    logger.info("Simulating: {0} blocks being found by pool".format(args.num_blocks_to_find))

    pool = MiningPool(args.num_honest_miners, args.num_malicious_miners,
                      args.hash_rates_file, args.round_length,
                      args.num_blocks_to_find,
                      args.shares_per_second,
                      args.attack_type,
                      args.seed,
                      args.attack_params)

    pool.find_all_blocks()
    logger.debug("All rounds finished, printing general stats below:")
    pool.write_final_stats()


if __name__ == "__main__":
    main()
