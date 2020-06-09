# pyndex: the python reconstructor for the FTSE Russell US indexes.

## What is it?
pyndex is a Python package developed to reconstruct the Russell US indexes. It is based on the results of the following paper:

## Main features
Here are the main features of pyndex:

## Where to get it
The source code is currently hosted in the following GitHub repository folder: 

Binary installers for the latest released version are available at the Python package index and on conda.

```bash
# conda
conda install pandas
```

```bash
# or PyPI
pip install pandas
```

## License
The software is distributed under GNU General Public License v3.0.

## Usage

The package can reconstruct the Russell 1000, 2000 and 3000 index. The index to be reconstructed is passed via the argument **index** as "1000", "2000" and "3000"
respectively. The oldest year supported is 1989. 

First, start your connection to the WRDS database. 
```bash
>>> import wrds
>>> db = wrds.Connection()
Loading library list...
Done
```
Then pass your WRDS connection to the package along with the parameters year and index.
```bash
>>> import pyndex as px
>>> index = px.Index.from_wrds(db, year = 2010, index = "3000")
>>> calendar = px.Index.get_calendar(year = 2010)
```
The method **px.Index.from_wrds()** will return a pandas MultiIndex DataFrame containing the index weights identified by **permno,permco** and **cusip**.
The method **px.Index.get_calendar()** will return the index reconstruction calendar for the corresponding year.

 
## Getting Help
For any usage or installation questions, please get in touch with Alessandro Micheli at
am1118@ic.ac.uk .



