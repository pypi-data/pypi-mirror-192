# ensembl_assembly
Search and download Ensembl data such as genome assemblies and gene annotations

This program will produce a tabular-like format with the metadata for the genomes matching user criteria.
It may also download desired data to a local folder.

## Installation
Install through conda:

```conda install -c mmariotti ensembl_assembly```

Or, alternatively, through pip:

```pip install ensembl_assembly```

## Usage
By default, the program will show information for all available genome assemblies (most recent release).
To see options, run with:

ensembl_assembly.py -h

## Dependencies

- pandas
- [easyterm](https://easyterm.readthedocs.io/)

These are automatically installed through the conda or pip installation procedure.





