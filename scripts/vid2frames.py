#!/usr/bin/env python3
import os, sys
import pdb

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vid2vid.ffmpeg_if import *
from vid2vid.fsutil    import *


def main( args ):
    print( args )
    
    # Check paths
    if not os.path.exists( args.source ):
        sys.exit( '{} does not exist'.format( args.source ) )
        
    # Create output paths
    dname, fname = os.path.split( args.output )

    if not os.path.exists( dname ):
        mkdir_p( dname )
        assert( os.path.exists( dname ) )

    if fname == '':
        fname = 'thumbnails-%02d.jpeg'

    output = os.path.join( dname, fname )

    if args.probe:
        deep_probe( args.source )
        sys.exit(0)
        
    
    # Extract Frames
    if args.key:
        extract_key_frames( src = args.source,
                            out_filename = output )
    else:
        extract_all_frames( src = args.source,
                            out_filename = output )

    # Profit
    print( 'Enjoy the frames' )

# Standard biolerplate to call the main() function to begin the program
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser( description='Create test source mp4' )

    # Common parameters
    parser.add_argument( 'source', help='Input Source' )
    parser.add_argument( '-o', '--output', help='Output' )
    parser.add_argument( '-k', '--key', help='Only extract key frames',
                         action='store_true')
    parser.add_argument( '-p', '--probe', help='Probe file',
                         action='store_true' )
    parser.add_argument( '-v', '--verbose',
                         help   = 'Increase verbosity',
                         action ='store_true' )

    # Parse the arguments
    args = parser.parse_args()

    # Process the subcommand
    main( args )
