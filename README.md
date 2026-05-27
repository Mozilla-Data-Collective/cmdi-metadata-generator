A really barebones generator for CMDI records that can be imported into the Virtual Language Observatory

# Requirements

Requires a Mozilla Data Collective API key and the following libraries: 

* `datacollective-python` 
* `python-iso639`

# Usage

First make sure you have an MDC API key in your environment variables and if not set it:

```
$ export | grep MDC_API_KEY
MDC_API_KEY=ac5a...
```

Then you can run the tool in two modes:

For testing:

```
$ python3 generate-cmdi.py -s <DATASET_ID_OR_SLUG>
```

Will output the CMDI XML for a single dataset.

For example:

```
$ python3 generate-cmdi.py -s araina-text-corpus-occitan-aranese-68f5a63b
<?xml version="1.0" encoding="UTF-8"?>
<cmd:CMD xmlns:dcr="http://www.isocat.org/ns/dcr"
 xmlns:cmd="http://www.clarin.eu/cmd/1"
 xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning"

...
```

If you run the code without any arguments, it will fetch the latest `sitemap.xml` and output
records for all of the published datasets in the `records/` directory.

In addition, datasets that are in the `records/` directory but are not found in the latest `sitemap.xml`
will be marked to be removed by appending `.REMOVE` to the filename, e.g. `common-voice-scripted-speech-25-0-spanis-24092b75.xml.REMOVE`

These should be removed manually.
