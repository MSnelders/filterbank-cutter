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
python filterbank_cutter.py -L 5200.00 -H 7800.0 -i infile.fil -o outfile.fil
Imported filterbank from PRESTO
Reading original filterbank file infile.fil
Will extract
    889 channels (196 to 1084 incl.)
    (Original num chans: 1536)
Extacting data from infile.fil
infile.fil has been succesfully closed
Cutting down some of the frequency channels
Output spectra has shape: (174734, 889)
Creating output file: outfile.fil
Writing data to new filterbank file
```
```sh
readfile outfile.fil 
Assuming the data is a SIGPROC filterbank file.

1: From the SIGPROC filterbank file 'outfile.fil':
                            ...
         Central freq (MHz) = 6500             
          Low channel (MHz) = 5199.21875       
         High channel (MHz) = 7800.78125       
        Channel width (MHz) = 2.9296875        
         Number of channels = 889       
      Total Bandwidth (MHz) = 2604.4921875     

```

## Contributing
Please open an issue or send me an email.

## Contact
Mark Snelders - m dot p dot snelders at uva dot nl  
Project Link: [github.com/MSnelders/filterbank-cutter/](https://github.com/MSnelders/filterbank-cutter/)
