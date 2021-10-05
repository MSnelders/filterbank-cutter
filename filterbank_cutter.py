#!/usr/bin/env python

# Program that will cut a filterbank file in frequency. Written by Kenzie Nimmo and Mark Snelders (Feb 2021) with inspiration from Patrick Lazarus. It has been tested with python 2.7, but it probably works with other versions aswell. 
# v1: cut based on frequency limits
# v2: cut based on frequency limits OR channel number(s)

from argparse import ArgumentParser
import numpy as np
import copy
import os

# try to import the filterbank module
try:
    import filterbank
    print("Imported filterbank")
except ImportError:
    try:
        from presto import filterbank
        print("Imported filterbank from PRESTO")
    except ImportError:
        raise ImportError('Cannot find the filterbank.py module')

def main(args):   
    # check if outfile already exists
    if os.path.exists(args.outname):
        raise ValueError("Ouput file already exists.")

    # read in filterbank file
    infile = args.infile
    print("Reading original filterbank file {}".format(infile))
    fil_org = filterbank.FilterbankFile(infile)
    
    # Check if input is valid:
    if (args.chan_no_L is not None) or (args.chan_no_H is not None):
        if (args.lo_freq is not None) or (args.hi_freq is not None):
            raise ValueError("If low and/or high channel NUMBER are given, --lo_freq and --hi_freq must be None")
    
    # Check if input is valid:
    if (args.lo_freq is not None) or (args.hi_freq is not None):
        if (args.chan_no_L is not None) or (args.chan_no_H is not None):
            raise ValueError("If low and/or high channel FREQUENCY are given, --chan_no_L and --chan_no_H must be None")
    
    # read in filterbank file
    infile = args.infile
    print("Reading original filterbank file {}".format(infile))
    fil_org = filterbank.FilterbankFile(infile)

    # Some checks for frequency
    maxfreq = np.max(fil_org.frequencies)
    minfreq = np.min(fil_org.frequencies)
    if (args.hi_freq is not None and args.hi_freq >= maxfreq) or\
            (args.lo_freq is not None and args.lo_freq <= minfreq):
                raise ValueError("The requested high/low frequencies are beyond what is already in the filterbank file. Either change those options to valid ones or leave it blank.\n Requested values: {}-{} MHz, current values: {}-{} MHz".format(args.lo_freq, args.hi_freq, minfreq, maxfreq))
    if (float == type(args.hi_freq) == type(args.lo_freq)):
        if args.lo_freq >= args.hi_freq:
            raise ValueError("High frequency must be greater than low frequency")

    if (int == type(args.chan_no_H) == type(args.chan_no_L)):
        if args.chan_no_L >= args.chan_no_H:
            raise ValueError("High frequency channel number must be greater than low frequency channel number.")

    # check if chan_no_L is valid
    if (int == type(args.chan_no_L)) and (args.chan_no_L < 0):
        raise ValueError("Low frequency channel number must be equal or greater than 0.")
    
    # check if chan_no_H is valid
    if (int == type(args.chan_no_H)) and (args.chan_no_H > (fil_org.nchan - 1)):
        raise ValueError("Requested high channel number ({}) is greater than the amount of channels (minus 1) available ({})".format(args.chan_no_H, fil_org.nchan - 1))

    # Determine lo/hi channels to write to file
    # low chan/freq
    if (int == type(args.chan_no_L)):
        lochan = args.chan_no_L
    elif (float == type(args.lo_freq)):
        lochan = np.argmin(np.abs(fil_org.frequencies - args.lo_freq))
    else:
        print("Do I get here? lochan")
        lochan = np.argmin(fil_org.frequencies)

    # high chan/freq
    if (int == type(args.chan_no_H)):
        hichan = args.chan_no_H
    elif (float == type(args.hi_freq)):
        hichan = np.argmin(np.abs(fil_org.frequencies - args.hi_freq))
    else:
        print("Do I get here? hichan")
        hichan = np.argmax(fil_org.frequencies)

    # flip if lo > hi:
    if lochan > hichan:
        lochan, hichan = hichan, lochan
    
    # We do the plus +1 because of indexing. I.e., say you leave both -L and -H empty, you essentially create a copy of a filterbank. 
    # This could mean that e.g. the orignal filterbank has 256 channels, the lowest channel is 0 and the highest channel is 255. 
    # so 255 - 0 is not 256, and therefore you need to add the + 1. 
    new_nchans = hichan - lochan + 1
    # final check, possibly redundant
    if new_nchans <= 0:
        raise ValueError("Bad number of channels to be written ({}). Check low/high frequencies.".format(new_nchans))

    print("Will extract")
    print("    {} channels ({} to {} incl.)".format(new_nchans, lochan, hichan))
    print("    (Original num chans: {})".format(fil_org.nchans))

    header_org = fil_org.header 
    h_size  = fil_org.header_size

    # copy original header, will update it before writing to new file
    out_header = copy.deepcopy(header_org)
    
    #get info needed to extract data from original filterbank file
    nbits = header_org['nbits']
    nchan = fil_org.nchan
    nspec = fil_org.nspec
    dtype = fil_org.dtype
    
    # getting the original data
    with open(infile, 'rb') as f:
        print("Extacting data from {}".format(infile))
        f.seek(h_size, os.SEEK_SET)
        data = np.fromfile(f, dtype=dtype, count=nspec*nchan).reshape(nspec, nchan)

    if f.closed:
        print("{} has been succesfully closed".format(infile))
    else:
        print("The data has been read in, but {} is not properly closed.".format(infile))
    
    print("Cutting down some of the frequency channels")
    spectra = data[:, lochan:(hichan+1)]
    print("Output spectra has shape: {}".format(spectra.shape))


    # Create output file
    print("Creating output file: {}".format(args.outname))

    out_header['nchans'] = new_nchans
    out_header['fch1'] = fil_org.frequencies[lochan]
    
    print("Writing data to new filterbank file")
    filterbank.create_filterbank_file(args.outname, out_header, spectra=spectra, mode='write', nbits=nbits)
    
    return

if __name__ == '__main__':
    parser = ArgumentParser(description="A program which will truncate a filterbank file in frequency. It finds the frequency channels which are closest to the --lo_freq and --hi_freq. Therefore depending on your channel widths it is possible that the bandwidth of the output file is slightly larger than hi_freq - lo_freq. The program is dependent on filterbank.py (which should come with PRESTO). For now only works with 8- or 16-bit integers or 32-bit float. If the data is 1- or 2-bit, digifil can be used to write that file into an 8-bit one. Expected memory useage is two times the input filterbank size.")
    parser.add_argument("-L", "--lo_freq", dest="lo_freq", type=float,
                    help="Desired low frequency (in MHz) for output file. Note: "
                        "actual low frequency will be rounded to the nearest"
                        "channel (Default: Don't truncate low-freq channels)",
                    default=None)
    parser.add_argument("-H", "--hi_freq", dest="hi_freq", type=float,
                    help="Desired high frequency (in MHz) for output file. Note: "
                        "actual high frequency will be rounded to the nearest"
                        "channel (Default: Don't truncate high-freq channels)",
                    default=None)
    parser.add_argument("-chan_L", "--chan_no_L", dest="chan_no_L", type=int,
            help="Desired lower channel number (inclusive!) default: None. If given, must be int",
                    default=None)
    parser.add_argument("-chan_H", "--chan_no_H", dest="chan_no_H", type=int,
            help="Desired higher channel number (inclusive!) default: None. If given, must be int",
                    default=None)
    parser.add_argument("-o", "--outname", dest='outname', action='store', required=True,
                    help="The name of the output file.")
    parser.add_argument("-i", "--infile", dest='infile', action='store', required=True,
                    help="The name of the input file.")
    args = parser.parse_args()

    main(args)









