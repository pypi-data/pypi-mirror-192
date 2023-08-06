TODO
====

MetabolomicStudy/Study
----------------------

This is going to be the base class to analyze raw data. The goal is to make
feature detection, feature filtering before feature correspondence,
feature correspondence and Data matrix creation as easy as possible for the
user.

### User input

The input to create this class should be:

1. Sample metadata: a DataFrame with sample information. Each row is an analyzed
   sample. The following fields should be available:
    * name: Filename without the extension.
    * id: a unique value specifying the biological sample used. 
    * Sample group: 
    * kind: 
    * order: int
    * batch
    * dilution
    * raw data path
2. Compound metadata: a DataFrame with compound information. Used to target
specific compounds in the samples:
   * name: name of the compound
   * formula: neutral chemical formula of the compound
   * adduct: adduct formula ("[M+Na]+")
   * rt: Expected retention time for the compound
3. Polarity
4. Instrument
5. Separation
6. Ms data mode

### Goals

1. ~~Perform feature detection with untargeted/targeted approaches.~~
2. ~~Perform feature filtration on a sample basis (SNR, peak width, etc...).~~
3. ~~Perform feature correspondence.~~
4. Annotate isotopes and adducts.  
5. ~~Create DataContainers.~~
6. Input missing data.
7. ~~Explore Raw data (ie. Chromatograms / MS spectra)~~
8. ~~Consume the smallest amount of memory possible. Once a sample is analyzed, 
   ROI data should be saved to disk.~~
9. ~~Make easy to add new samples to an existent Assay (don't process all samples
   again).~~
   

Miscellaneous
-------------

* Refactor RoiProcessor: During feature detection, more than 90 % of the time
 is spent in building ROIs. I found that it is probably a better idea to use a
 chromatogram-based approach for ROI creation. m/z seeds should be estimated
 from the file and the ROI is simply a chromatogram with associated m/z values
 for each scan. This approach is also much more efficient, reducing feature
 detection from 25 s to 5-10 s. 
    
* Filters: Refactor code.
* _names: This module should be removed. Update 2022-06-07: constants are being
 moved to the _constants module. 

DataContainer
-------------

* use underscores for reserved names.
* Remove reset functionality. It does more harm than good. This functionality
can be achieved saving the data to disk and reloading.
* Rename to DataMatrix or some similar name.
* Validate groups, order, batch, name and id values through the use of 
  properties.
* Pipeline vs Filter object? Think about pros and cons. 
* Add examples to method docstrings (e.g remove)

Chemistry
---------

* ~~Integrate chem module.~~ Done.
* Download periodic table from a repo.
* Convert isotopic data into a JSON and save it into the .tidyms directory
* ~~Fix formula generator when there are only elements with positive (or negative)
  defects.~~ Done
  
  
lcms
----
* ~~test accumulate spectra profile~~
* ~~test data with multiple MS levels.~~

Docs
----
* ~~Update quickstart~~
* ~~add requests to projects setup.py~~