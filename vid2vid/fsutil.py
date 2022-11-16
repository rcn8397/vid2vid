# -*- coding: utf-8 -*-
"""File System - tools
"""

import os
import errno

def mkdir_p( path ):
    '''
    mkdir -p functional equivalent
    '''
    try:
        os.makedirs( path )
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir( path ):
            pass
        else:
            raise

def discover( path, patterns, excludes =['.git', '.svn'] ):
     is_xcl = lambda x, xcl : any( e in x for e in xcl )
     is_ext = lambda f, ext : any( f.endswith( e ) for e in ext )
     matches = []
     for root, dirs, files in os.walk( path ):#, topdown=True ):
          files= [ f for f in files if not f.startswith( '.' ) ]
          dirs = [ d for d in dirs  if not d.startswith( '.' ) ]
          if is_xcl( root, excludes ):
               # Skip excluded directories
               continue
          for fname in files:
             if is_ext( fname.lower(), patterns ):
                 match = os.path.join( root, fname )
                 matches.append( match )
     return matches

def find( path, patterns ):
     '''
     Find all files with ext patterns
     '''
     is_ext = lambda f, ext : any( f.endswith( e ) for e in ext )
     matches = []
     for root, dirs, files in os.walk( path, topdown=True ):
         for filename in files:
             if is_ext( filename.lower(), patterns ):
                 match = os.path.join( root, filename )
                 matches.append( match )
     return matches

# Attempt to get a list of a filesystem subtree from a string
def list_dir( path = None ):
    dirlist = []
    if path is None:
        path = '.'
    try:
        dirlist = os.listdir( path )
    except Exception as e:
        pass
    return dirlist
