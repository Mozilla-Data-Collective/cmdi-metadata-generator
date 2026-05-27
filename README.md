A really barebones generator for CMDI records that can be imported into the Virtual Language Observatory

# Requirements

Requires a Mozilla Data Collective API key and the following libraries: 

* `datacollective-python` 
* `python-iso639`

# Usage

```
$ python3 generate-cmdi.py <DATASET_ID_OR_SLUG>
```

# Output

Outputs into the `records/` subdirectory.

