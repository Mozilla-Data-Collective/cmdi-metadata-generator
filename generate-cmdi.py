import cmdi_template
import datacollective, requests, sys, datetime, math, os, glob, time
import xml.etree.ElementTree as ET

RECORDS_DIR = 'records/'
RATE_LIMIT_DELAY = 0.5 # There is a generic rate limit of 200 requests / minute

def estimate_end(last, now, window_len, current, total):
	# get n secs per dataset, multiply by datasets pending	
	pending = total - current
	secs_dataset = (now - last) / window_len

	return pending * secs_dataset

namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

res = requests.get('https://mozilladatacollective.com/sitemap.xml')

root = ET.fromstring(res.text)

if len(sys.argv) == 3 and sys.argv[1] == '-s':
	dataset_id = sys.argv[2]
	
	dataset_info = datacollective.get_dataset_details(dataset_id)
	
	dataset_record = cmdi_template.fill_template(dataset_info)
	print(dataset_record.strip())
	sys.exit(0)
elif len(sys.argv) != 1:
	print('Usage: generate-cmdi.py [-s DATASET_ID_OR_SLUG]')
	sys.exit(-1)
	

os.makedirs(RECORDS_DIR,exist_ok=True)

existing_records = [i.split('/')[1].replace('.xml','') for i in glob.glob(RECORDS_DIR + '/*.xml')]

total_datasets = 0 
print('Found %d existing records' % (len(existing_records)))
for url in root.findall('ns:url', namespace):
	loc = url.findall('ns:loc', namespace)[0]
	if '/datasets/' in loc.text:
		total_datasets += 1

found_datasets = 0
secs = datetime.timedelta(seconds=0)
last = datetime.datetime.now()
found_records = []
for url in root.findall('ns:url', namespace):
	loc = url.findall('ns:loc', namespace)[0]
	if '/datasets/' in loc.text:
		dataset_id = loc.text.split('/')[4]
		dataset_info = datacollective.get_dataset_details(dataset_id)
		
		dataset_record = cmdi_template.fill_template(dataset_info)
		filename_xml = RECORDS_DIR + dataset_info['slug'] + '.xml'

		fd = open(filename_xml, 'w+')
		print(dataset_record.strip(), file=fd)
		fd.close()

		if found_datasets % 5 == 0:
			now = datetime.datetime.now()
			secs = estimate_end(last, now, 5, found_datasets, total_datasets)			
			last = now

		found_records.append(dataset_info['slug'])
		found_datasets+=1
		zf = len(str(total_datasets))
		pc = int((found_datasets/total_datasets)*100)
		prog = '[%s%%] %s/%s' % (str(pc).zfill(2), str(found_datasets).zfill(zf), str(total_datasets).zfill(zf)) + ' %s' % str(datetime.timedelta(seconds=secs.seconds))
		#prog = '%s/%s' % (str(found_datasets).zfill(zf), str(total_datasets).zfill(zf)) 
		print('\b' * len(prog)+ prog, file=sys.stderr, end='')
		sys.stderr.flush()
		time.sleep(RATE_LIMIT_DELAY)

print()
missing_records = set(existing_records) - set(found_records)

removed = 0
for record in missing_records:
	def rn(record):
		return RECORDS_DIR + '/' + record + '.xml'
	os.rename(rn(record), rn(record) + '.REMOVED')
	removed += 1

if removed > 0:
	print(f'Marked {removed} records for removal, remember to delete them manually: rm {RECORDS_DIR}/*.REMOVED')
