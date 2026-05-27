import datacollective, requests, sys, datetime, math, os
import iso639

FORMAT_TO_MIME = {
'.tar.gz': 'application/gzip',
'.tsv': 'text/tab-separated-values',
'.wav': 'audio/wav',
'.WAV': 'audio/wav',
'CHA': 'text/plain',                    
'CHA.TSV': 'text/tab-separated-values',
'CONLL-2003': 'text/plain',             
'csv': 'text/csv',
'CSV': 'text/csv',
'DOCX': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'FLAC': 'audio/flac',
'GLTFwithDracocompression': 'model/gltf+json', 
'JASONL': 'application/json',   
'JPEG': 'image/jpeg',
'JPG': 'image/jpeg',
'JSON': 'application/json',
'JSONL': 'application/json',
'LOG': 'text/plain',
'Markdown(.md)': 'text/markdown',
'mp3': 'audio/mpeg',
'MP3': 'audio/mpeg',
'MP3.TSV': 'audio/mpeg',
'MP4': 'video/mp4',
'N-Triples': 'application/n-triples',
'OGG': 'audio/ogg',
'parquet': 'application/vnd.apache.parquet',
'PARQUET': 'application/vnd.apache.parquet',
'PDF': 'application/pdf',
'SQLITE': 'application/x-sqlite3',
'SRT': 'text/plain; charset=utf-8',
'TEXTGRID': 'text/plain',  
'TRJS': 'application/json',   
'TRS': 'text/plain',    # check this one
'tsv': 'text/tab-separated-values',
'TSV': 'text/tab-separated-values',
'txt': 'text/plain',
'TXT': 'text/plain',
'wav': 'audio/wav',
'WAV': 'audio/wav',
'WEBM': 'video/webm',
'WEBM&TSV': 'video/webm', 
'XLSX': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
'XSLX': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
'ZIP': 'application/zip'
}

TEMPLATE = """
<?xml version="1.0" encoding="UTF-8"?>
<cmd:CMD xmlns:dcr="http://www.isocat.org/ns/dcr"
 xmlns:cmd="http://www.clarin.eu/cmd/1"
 xmlns:vc="http://www.w3.org/2007/XMLSchema-versioning"
 xmlns:cue="http://www.clarin.eu/cmd/cues/1"
 xmlns:cue_old="http://www.clarin.eu/cmdi/cues/1"
 xmlns="http://www.clarin.eu/cmd/1/profiles/clarin.eu:cr1:p_1381926654571"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.clarin.eu/cmd/1 https://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/1.x/profiles/clarin.eu:cr1:p_1381926654571/xsd" CMDVersion="1.2">
    <cmd:Header>
        <cmd:MdCreator>Mozilla Data Collective</cmd:MdCreator>
        <cmd:MdCreationDate>2006-05-04</cmd:MdCreationDate>
        <!--<cmd:MdSelfLink>{SelfLink0}</cmd:MdSelfLink>--> <!-- TBD: A unique link to the CMDI record -->
        <cmd:MdProfile>clarin.eu:cr1:p_1381926654571</cmd:MdProfile>
        <cmd:MdCollectionDisplayName>Mozilla Data Collective</cmd:MdCollectionDisplayName>
    </cmd:Header>
    <cmd:Resources>
        <cmd:ResourceProxyList>
            <cmd:ResourceProxy id="ID001">
                <cmd:ResourceType>Resource</cmd:ResourceType>
                <cmd:ResourceRef>{ResourceUrl0}</cmd:ResourceRef>
            </cmd:ResourceProxy>
        </cmd:ResourceProxyList>
        <cmd:JournalFileProxyList />
        <cmd:ResourceRelationList />
    </cmd:Resources>
    <cmd:Components>
        <Corpus>
            <CLARIN-D-metadata>
                <Name>{Name0}</Name>
                <Title>{Title0}</Title>
                <Description>{Description0}</Description>
                <ResourceClass>{ResourceClass0}</ResourceClass>
                <Organisation>{Organisation0}</Organisation>
                <DistributionType>{DistributionType0}</DistributionType>
                <PublicationYear>{PublicationYear0}</PublicationYear>
		{FORMAT}
                {ISO}
            </CLARIN-D-metadata>
        </Corpus>
    </cmd:Components>
</cmd:CMD>
"""

TEMPLATE_FORMAT = """
                <Format>{Format0}</Format>
"""

TEMPLATE_ISO = """
                <ISO639>
                    <iso-639-3-code>{aaa}</iso-639-3-code>
                </ISO639>
"""

dataset_id = sys.argv[1]

dataset_info = datacollective.get_dataset_details(dataset_id)

print(dataset_info)
		# {'id': 'cmkwvpu7s0032mo07jpk20pj1', 'slug': 'greek-phd-theses-corpus-v1-0-849fac7f', 'name': 'Greek PhD Theses Corpus v1.0', 'shortDescription': None, 'longDescription': 'The Greek PhD Theses Corpus is a large-scale, AI-ready text dataset consisting of 55,423 Greek doctoral dissertations produced between 1975 and 2025. It represents the most comprehensive and technically homogenized collection of Greek PhD-level academic writing assembled to date.\n\nThe corpus combines full dissertation texts with rich, structured metadata, processed through a modern, GPU-accelerated pipeline that includes advanced OCR, markdown normalization, and extensive quality assurance. \n\n', 'sizeBytes': '7540341366', 'createdAt': '2026-01-27T17:37:28.120Z', 'organization': {'name': 'EELLAK - GreekFOSS', 'slug': 'eellak-greekfoss-e683acde'}, 'locale': 'gr-GR', 'task': 'NLP', 'license': 'Creative Commons Attribution Non Commercial Share Alike 4.0 International (CC-BY-NC-SA-4.0)', 'licenseAbbreviation': 'CC-BY-NC-SA-4.0', 'format': 'JASONL', 'datasetUrl': 'https://datacollective.mozillafoundation.org/datasets/cmkwvpu7s0032mo07jpk20pj1'}

dataset_record = TEMPLATE

dataset_record = dataset_record.replace('{ResourceUrl0}',dataset_info['datasetUrl'])
dataset_record = dataset_record.replace('{Name0}', dataset_info['name'])
dataset_record = dataset_record.replace('{Title0}', dataset_info['name'])
#dataset_record = dataset_record.replace('{License0}', dataset_info['license'])
dataset_record = dataset_record.replace('{ResourceClass0}', 'resourceBundle')
dataset_record = dataset_record.replace('{Description0}', dataset_info['longDescription'])
organisation_name = dataset_info['organization']['name']
if organisation_name == None:
	organisation_name = "MDC Community"
dataset_record = dataset_record.replace('{Organisation0}', organisation_name)
dataset_record = dataset_record.replace('{PublicationYear0}', dataset_info['createdAt'].split('-')[0])
dataset_record = dataset_record.replace('{DistributionType0}', 'PUB')
formats = []
for format_ in dataset_info['format'].split(','):
	format_ = format_.strip()
	if format_ in FORMAT_TO_MIME:
		formats.append(FORMAT_TO_MIME[format_])

format_tags = ""
for format_ in formats:
	format_tags += TEMPLATE_FORMAT.replace('{Format0}', format_)
dataset_record = dataset_record.replace('{FORMAT}', format_tags.strip())

locales = []
for locale in dataset_info['locale'].split(','):
	if '-' in locale:
		locale = locale.split('-')[0]
	lang = iso639.Language.match(locale)
	locales.append(lang.part3)

locale_tags = ""
for locale in locales:
	locale_tags += TEMPLATE_ISO.replace('{aaa}', locale)
dataset_record = dataset_record.replace('{ISO}', locale_tags.strip())

#{'id': 'cmn2h5zd801h3o1075tita1ap', 'slug': 'common-voice-scripted-speech-25-0-czech-a54711a9', 'name': 'Common Voice Scripted Speech 25.0 - Czech', 'shortDescription': 'A collection of read speech recordings in Czech.', 'longDescription': 'A collection of read speech recordings in Czech (Čeština).', 'createdAt': '2026-03-23T00:56:08.780Z', 'isPaid': False, 'basePriceCents': None, 'currency': None, 'locale': 'cs', 'license': 'Creative Commons Zero v1.0 Universal (CC0-1.0)', 'licenseAbbreviation': 'CC0-1.0', 'task': 'ASR', 'format': 'MP3', 'organization': {'name': 'Common Voice', 'slug': 'test-2d27eebd', 'platformFeeRate': None}, 'datasetSubmission': {'id': 'cmn27itzz015bmm07iebhk47v', 'createdBy': 'cmmoxjcia01crl807f7lpq1f0'}, 'filename': 'common-voice-scripted-speech-25-0-czech-a54711a9.tar.gz', 'datasetUrl': 'https://mozilladatacollective.com/datasets/cmn2h5zd801h3o1075tita1ap', 'sizeBytes': '5970163541', 'pricing': {'isPaid': False, 'basePriceCents': None, 'currency': None, 'platformFeeRate': None, 'platformFeeCents': None, 'totalPriceCents': None}}

os.makedirs('records/',exist_ok=True)

fd = open('records/' + dataset_info['slug'] + '.xml', 'w+')

print(dataset_record.strip(), file=fd)

fd.close()
