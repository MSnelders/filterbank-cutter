## filterbank-cutter
A command-line python script that cuts [sigproc filterbank](http://sigproc.sourceforge.net/) (see http://sigproc.sourceforge.net/sigproc.pdf for the documentation) files in frequency. 

## Useage
1. Copy the script to your local machine.
2. Run the following to see all the options:
   ```sh
   python burst_toa_converter.py --help
   ```
   
## Requirements
* [Numpy](https://numpy.org/)
* [PRESTO](https://github.com/scottransom/presto/) 
* PRESTO's filterbank.py needs to be in your $PATH.
 
## Example
```sh
readfile infile.fil
Assuming the data is a SIGPROC filterbank file.

1: From the SIGPROC filterbank file 'infile.fil':
                            ...
         Central freq (MHz) = 6126.46484375    
          Low channel (MHz) = 3877.9296875     
         High channel (MHz) = 8375             
        Channel width (MHz) = 2.9296875        
         Number of channels = 1536
      Total Bandwidth (MHz) = 4500             
```
```sh
-------------------------------------
This program comes with absolutely no warrenty.
You have used the following input values:
Station: Effelsberg, X = 4033947.2355 m, Y = 486990.7943 m, Z = 4900431.0017 m
Source: SGR1935+2154, ra = 19h34m55.680s, DEC = +21d53m48.20s
DM = 332.7206 pc/cc, DM_constant = 4.14880568679703 GHz^2 cm^3 pc^-1 ms
Reference frequency = 1400.0 MHz
MJD-input timescale: utc
Start of the dataset(s): [56789.12345, 56789.12345, 56789.12345]
Burst timestamps (seconds): [0.0, 123.11, 99.87]
-------------------------------------
Saving DataFrame to results.pkl
-------------------------------------
                MJD_start   tstamp_ref_freq_sec   mjd_topo_ref_freq_utc   mjd_topo_inf_freq_utc   mjd_bary_inf_freq_utc   mjd_bary_inf_freq_tdb
0  56789.1234499999991385    0.0000000000000000  56789.1234499999991385  56789.1234418485837523  56789.1249510153138544  56789.1257286229738384
1  56789.1234499999991385  123.1099999999999994  56789.1248748842554050  56789.1248667328400188  56789.1263759965077043  56789.1271536041676882
2  56789.1234499999991385   99.8700000000000045  56789.1246059027762385  56789.1245977513608523  56789.1261069967295043  56789.1268846043894882
```

## Contributing
Please open an issue or send me an email.

## Contact
Mark Snelders - m dot p dot snelders at uva dot nl  
Project Link: [github.com/MSnelders/FRB-Burst-TOA](https://github.com/MSnelders/FRB-Burst-TOA)
