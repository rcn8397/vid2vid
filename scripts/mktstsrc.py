#!/usr/bin/env python3
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vid2vid.ffmpeg_if import create_test_src
from vid2vid.ffmpeg_if import create_sine_src

def main( args ):
    if args.sine:
        create_sine_src(args.path, freq = args.freq, duration = args.time_duration )
    else:
        create_test_src(args.path, duration = args.time_duration )
    
# Standard biolerplate to call the main() function to begin the program
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser( description='Create test source mp4' )

    # Common parameters
    parser.add_argument( '-p', '--path', help='Output path (defaults: ./testsrc.mp4)', default = './testsrc.mp4' )
    parser.add_argument( '-t', '--time-duration',
                         help   = 'Duration of the test source(defaults: 6 min)',
                         default = 600 )
    parser.add_argument( '-f', '--freq',
                         help   = 'Frequency for sine source(defaults: 1000Hz)',
                         default = 1000 )

    parser.add_argument( '-s', '--sine',
                         help   = 'Create since source', 
                         action ='store_true' )

    parser.add_argument( '-v', '--verbose',
                         help   = 'Increase verbosity',
                         action ='store_true' )

    # Parse the arguments
    args = parser.parse_args()

    # Process the subcommand
    main( args )
