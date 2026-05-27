import cmdi_template
import datacollective, requests, sys, datetime, math, os
import iso639

dataset_id = sys.argv[1]

dataset_info = datacollective.get_dataset_details(dataset_id)

dataset_record = cmdi_template.fill_template(dataset_info)

os.makedirs('records/',exist_ok=True)

fd = open('records/' + dataset_info['slug'] + '.xml', 'w+')

print(dataset_record.strip(), file=fd)

fd.close()
