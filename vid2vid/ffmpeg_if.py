#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ffmpeg interfaces
"""
import os
import sys
import ffmpeg

def jpgs2gif( pattern, out='out.gif', framerate = 2 ): #scale='360x240', ):
    '''
    ffmpeg -f image2 -framerate 10 -i thumb/%001d.jpg -vf scale=480x240  out.gif

    setting framerate to a larger number increases animation speed
    scale is working but things aren't correct
    '''
    out, err = (
        ffmpeg
        .input( pattern, framerate=framerate, format='image2', hide_banner=None, loglevel='error' )
        #.filter( 'scale', scale )
        .output( out)
        .overwrite_output()
        .run( capture_stdout = True )
        )
    return out
    
        
def generate_thumbnail(in_filename, out_filename, time=0.1, width=360, stdout = False, stderr = False):
    '''
    Directly from ffmpeg-python examples
    https://github.com/kkroening/ffmpeg-python/blob/master/examples/get_video_thumbnail.py
    '''
    try:
        (
            ffmpeg
            .input(in_filename, ss=time, hide_banner=None, loglevel='error')
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=stdout, capture_stderr=stderr)
        )
    except ffmpeg.Error as e:
        print( 'borked' )
        return (str( e ) )#e.stderr.decode(), file=sys.stderr)

def generate_gif(in_filename, out_filename='out.gif', time=0.1, duration = 2.5, width=360, stdout = False, stderr = False):
    '''
    ffmpeg -ss 61.0 -t 2.5 -i input.mp4 -filter_complex "[0:v] palettegen" palette.png
    ffmpeg -ss 61.0 -t 2.5 -i input.mp4 -i palette.png -filter_complex "[0:v][1:v] paletteuse" out.gif
    '''
    if not out_filename.endswith( '.gif' ):
        out_filename += '.gif'
        
    # Palette generation, split paletteuse
    split = (
        ffmpeg
        .input(in_filename, ss=time, t=duration, hide_banner=None, loglevel='error')
        .filter( 'scale', 512, -1 )
        .split()
    )

    palette = (
        split[0]
        .filter( 'palettegen' )
    )

    try:
        (
            ffmpeg
            .filter( [split[1], palette], 'paletteuse' )
            .output( out_filename )
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        print( 'borked' )
        return (str( e ) ) #e.stderr.decode(), file=sys.stderr)

    
def probe_duration( fname ):
    '''
    Retrieve the media files duration
    '''
    probe = ffmpeg.probe(fname)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    return( float(video_info['duration']) )
    
def probe( fname ):
    probe = ffmpeg.probe(fname)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    num_frames = int(video_info['nb_frames'])
    return width, height, num_frames

def deep_probe( fname ):
    probe = ffmpeg.probe( fname )
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    import pdb
    pdb.set_trace()
    

def test_stream_media( fname, dev = '/dev/video20' ):
    '''
    'ffmpeg -re -i "{0}" -f v4l2 "{1}"'

    Setting -re was obtained from setting re=None
    https://github.com/kkroening/ffmpeg-python/issues/343
    '''
    print( 'Attempting to Stream: {} to {}'.format( fname, dev ) )
    width, height, num_frames = probe( fname )
    print( '{0}: w={1}, h={2}'.format( fname, width, height ) )
    inp = ffmpeg.input( fname, re=None ).output( dev, f='v4l2' )
    print( inp.compile() )

    process = (
        inp.run_async( pipe_stdout = True, pipe_stdin = False)
        )
    pdb.set_trace()
    out, err = process.communicate()

def create_sine_src(path='./sinewav.mp4', freq = 1000, duration = 5 ):
    '''
    '''
    src = "sine=frequency={}:duration={}".format( freq, duration )
    process=(
        ffmpeg
        .input( src, f='lavfi' )
        .output( path )
        .run_async( pipe_stdout = True, pipe_stdin = False )
        .overwrite_ouput()
        )
    out, err = process.communicate()

def create_test_src(path='./testsrc.mp4', duration = 30):
    '''
    ffmpeg -f lavfi -i testsrc -t 30 -pix_fmt yuv420p testsrc.m4p
    '''
    process = (
        ffmpeg
        .input( 'testsrc', f='lavfi', t= duration  )
        .output( path,
                 pix_fmt='yuv420p' )
        .run_async( pipe_stdout = True, pipe_stdin = False)
        )
    out, err = process.communicate()


def extract_key_frames( path = './testsrc.mp4', out_filename='thumbnails-%02d.jpeg' ):
    '''
    
    ffmpeg -skip_frame nokey -i 2.flv -vsync 0 -r 30 -f image2 thumbnails-%02d.jpeg
    '''
    out, err = (
        ffmpeg
        .input( src, skip_frame='nokey', vsync=0, r=30, format='image2' )
        .output( out_filename )
        .run( capture_stdout = True )
    )
    return out

def create_video_from_video( path = './testsrc.mp4', start = 0, end=10, out_filename='./output.mp4' ):
    '''
    https://stackoverflow.com/questions/18444194/cutting-the-videos-based-on-start-and-end-time-using-ffmpeg
    ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy output.mp4
    Explanation of the command:

        -i: This specifies the input file. In that case, it is (input.mp4).
        -ss: Used with -i, this seeks in the input file (input.mp4) to position.
        00:01:00: This is the time your trimmed video will start with.
        -to: This specifies duration from start (00:01:40) to end (00:02:12).
        00:02:00: This is the time your trimmed video will end with.
        -c copy: This is an option to trim via stream copy. (NB: Very fast)

    The timing format is: hh:mm:ss
    '''
    out, err = (
        ffmpeg
        .input( src, ss=start, to=end, c='copy', hide_banner = None, loglevel='error' )
        .ouput( out_filename )
        .run( capture_stdout = True )
    )
    return out

# Main
def main():
    testsrc = './testsrc.mp4'
    sinesrc = './sinesrc.mp4'
    create_sine_src( sinesrc )


# Standard biolerplate to call the main() function to begin the program
if __name__ == '__main__':
    main()
