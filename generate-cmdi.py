import cmdi_template
import datacollective, requests, sys, datetime, math, os
import xml.etree.ElementTree as ET

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
	sys.exit(0)
elif len(sys.argv) != 1:
	print('Usage: generate-cmdi.py [-s DATASET_ID_OR_SLUG]')
	sys.exit(-1)
	

os.makedirs('records/',exist_ok=True)
total_datasets = 0 
for url in root.findall('ns:url', namespace):
	loc = url.findall('ns:loc', namespace)[0]
	if '/datasets/' in loc.text:
		total_datasets += 1

found_datasets = 0
secs = datetime.timedelta(seconds=0)
last = datetime.datetime.now()
for url in root.findall('ns:url', namespace):
	loc = url.findall('ns:loc', namespace)[0]
	if '/datasets/' in loc.text:
		dataset_id = loc.text.split('/')[4]
		dataset_info = datacollective.get_dataset_details(dataset_id)
		
		dataset_record = cmdi_template.fill_template(dataset_info)

		fd = open('records/' + dataset_info['slug'] + '.xml', 'w+')
	
		print(dataset_record.strip(), file=fd)
	
		fd.close()

		found_datasets+=1
		zf = len(str(total_datasets))
		pc = int((found_datasets/total_datasets)*100)
		prog = '[%s%%] %s/%s' % (str(pc).zfill(2), str(found_datasets).zfill(zf), str(total_datasets).zfill(zf)) + ' %s' % str(datetime.timedelta(seconds=secs.seconds))
		#prog = '%s/%s' % (str(found_datasets).zfill(zf), str(total_datasets).zfill(zf)) 
		print('\b' * len(prog)+ prog, file=sys.stderr, end='')
		sys.stderr.flush()
