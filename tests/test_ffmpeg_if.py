import os
import sys
import pdb

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vid2vid import ffmpeg_if
from vid2vid import fsutil
        
m = './testsrc.mp4'


def test_create_src():
    ffmpeg_if.create_test_src( m, duration = 300 )


def test_thumbnail():
    duration = ffmpeg_if.probe_duration( m )
    print( 'duration: {}'.format( duration ) )
    timestamp = lambda duration, step: ( ( duration/step ) - ( 0.5 * ( duration * 0.25 ) ) )

    # Make 4 thumbnails for previewing
    for i in range( 4, 0, -1 ):
        step = 5 - i
        ts = timestamp( duration, step )
        outpath = '{}_{:03}.jpg'.format( 'preview', i )
        print( 'Generating preview {} @ {} seconds: {}'.format( step, outpath, ts ) )
        ffmpeg_if.generate_thumbnail( m , outpath, time = ts )

    ffmpeg_if.jpgs2gif( 'preview_%03d.jpg' )

def test_gif():
    print( 'Generating gif' )
    duration = ffmpeg_if.probe_duration( m )
    print( 'duration: {}'.format( duration ) )
    timestamp = lambda duration, step: ( ( duration/step ) - ( 0.5 * ( duration * 0.25 ) ) )

    ffmpeg_if.generate_gif( m, 'test.gif', time = timestamp( duration, 3 ), duration =3 )
    
def test_probe():
    print( ffmpeg_if.probe( m ) )
    print( ffmpeg_if.probe_duration( m ) )

def test_extract_key_frames():
    print( 'Exracting key frames' )
    fsutil.mkdir_p( 'key_frames' )
    ffmpeg_if.extract_key_frames( src = m, out_filename = os.path.join( 'key_frames', 'thumb-%02d.jpeg' ) )

def test_extract_all_frames():
    print( 'Exracting all frames' )
    fsutil.mkdir_p( 'all_frames' )
    ffmpeg_if.extract_key_frames( src = m, out_filename = os.path.join( 'all_frames', 'thumb-%02d.jpeg' ) )


def test_create_video_from_frames():
    path = os.path.join( 'key_frames', '*.jpeg' )
    ffmpeg_if.create_video_from_frames( path, out_filename = os.path.join( 'key_frames', 'test.mp4' ) )


def test_create_video_from_frames_filter():
    path = os.path.join( 'key_frames', '*.jpeg' )
    ffmpeg_if.create_video_from_frames_filter( path, out_filename = os.path.join( 'key_frames', 'test_blend.mp4' ) )

    
def main():
    test_create_src()
    test_probe()
    test_thumbnail()
    test_gif()
    test_extract_key_frames()
    test_extract_all_frames()    
    test_create_video_from_frames()
    test_create_video_from_frames_filter()    
    
if __name__ == '__main__':
    main()
