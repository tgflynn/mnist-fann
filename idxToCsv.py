#!/usr/bin/env python

import os
import sys
import struct
from optparse import OptionParser

def readChar( f ):
    bytes = f.read( 1 )
    val = struct.unpack( 'B', bytes )[0]
    return val

def readUInt( f ):
    bytes = f.read( 4 )
    val = struct.unpack( '>I', bytes )[0]
    return val

def convertOrdinalToBinary( ordinal, nclasses ):
    out = [ 0.1 ] * nclasses
    out[ordinal] = 0.9
    return out

def readLabelsFile( filename ):
    data = { 'labels' : [] }
    classes = set()
    classMap = {}
    invClassMap = {}
    f = file( filename, 'rb' )
    magic = readUInt( f )
    #print "magic = %08X" % ( magic )
    nitems = readUInt( f )
    #print "nitems = %d" % ( nitems )
    for i in range( nitems ):
        label = readChar( f )
        #print "label = %d" % ( label )
        classes.add( label )
        data['labels'].append( label )
    data['nclasses'] = len( classes )
    classList = list( classes )
    classList.sort()
    classMap = dict( [ [ classList[i], i ] for i in range( len( classes ) ) ] )
    invClassMap = dict( [ [ i, classList[i] ] for i in range( len( classes ) ) ] )
    data['classMap'] = classMap
    data['invClassMap'] = invClassMap
    f.close()
    return data

def readImagesFile( filename ):
    print "Reading images file"
    data = { 'images' : [] }
    f = file( filename, 'rb' )
    magic = readUInt( f )
    print "magic = %08X" % ( magic )
    nitems = readUInt( f )
    nrows = readUInt( f )
    ncolumns = readUInt( f )
    data['nitems'] = nitems
    data['nrows'] = nrows
    data['ncolumns'] = ncolumns
    print "nitems = %d, nrows = %d, ncolumns = %d" % ( nitems, nrows, ncolumns )
    for i in range( nitems ):
        image = []
        for rowidx in range( nrows ):
            row = []
            for colidx in range( ncolumns ):
                pval = readChar( f )
                row.append( pval )
            image.append( row )
        #print "label = %d" % ( label )
        data['images'].append( image )
    f.close()
    return data

def makeDatasetFile( images, labels, filename ):
    if len( images['images'] ) != len( labels['labels'] ):
        raise Exception( 'makeDatasetFile: input/label length mismatch' )
    ninstances = len( images[ 'images' ] )
    f = file( filename, 'w' )
    ninputs = images['nrows'] * images['ncolumns']
    noutputs = labels['nclasses']
    classMap = labels['classMap']
    for i in range( ninputs ):
        f.write( "X%d," % ( i ) )
    f.write( "Y\n" )
    for i in range( ninputs ):
        f.write( "FLOAT," )
    f.write( "INT\n" )
    for i in range( ninstances ):
        x = reduce( lambda a,b: a+b, images['images'][i] )
        y = classMap[ labels['labels'][i] ]
        f.write( '%s' % ( reduce( lambda a,b: a+b, [ '%f,' % ( val / 255. ) for val in x ] ) ) )
        f.write( '%d\n' % ( y ) )
    f.close()
    
def makeFANNFile( images, labels, filename ):
    if len( images['images'] ) != len( labels['labels'] ):
        raise Exception( 'makeFANNFile: input/label length mismatch' )
    ninstances = len( images[ 'images' ] )
    f = file( filename, 'w' )
    ninputs = images['nrows'] * images['ncolumns']
    noutputs = labels['nclasses']
    classMap = labels['classMap']
    f.write( "%d %d %d\n" % ( len( images['images'] ), ninputs, noutputs ) )
    for i in range( ninstances ):
        x = reduce( lambda a,b: a+b, images['images'][i] )
        y = convertOrdinalToBinary( classMap[ labels['labels'][i] ], noutputs )
        f.write( '%s\n' % ( reduce( lambda a,b: a+b, [ '%f ' % ( val / 255. ) for val in x ] ) ) )
        f.write( '%s\n' % ( reduce( lambda a,b: a+b, [ '%f ' % ( val ) for val in y ] ) ) )
    f.close()

if __name__ == "__main__":

    oparser = OptionParser()

    oparser.add_option( "-i",
                        "--images-file",
                        dest = "imagesFile",
                        action = "store" )

    oparser.add_option( "-l",
                        "--labels-file",
                        dest = "labelsFile",
                        action = "store" )

    oparser.add_option( "-o",
                        "--output-file",
                        dest = "outputFile",
                        action = "store" )

    oparser.add_option( "-f",
                        "--output-format",
                        default = "DATASET_CSV",
                        dest = "outputFormat",
                        action = "store" )

    (options, args) = oparser.parse_args()

    if not options.labelsFile:
        print 'ERROR: No labels file specified'
        sys.exit( -1 )

    if not options.imagesFile:
        print 'ERROR: No images file specified'
        sys.exit( -1 )

    if not options.outputFile:
        print 'ERROR: No output file specified'
        sys.exit( -1 )

    labels = readLabelsFile( options.labelsFile )
    images = readImagesFile( options.imagesFile )

    if options.outputFormat == 'FANN':
        makeFANNFile( images, labels, options.outputFile )
    elif options.outputFormat == "DATASET_CSV":
        makeDatasetFile( images, labels, options.outputFile )
