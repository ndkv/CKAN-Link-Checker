import os, csv
from json import load
import pudb

total_geo = 0
total_failed_geo = 0
failed_resources = []
failed_geo_resources = []

with open(os.getcwd() + '/failed_resources.csv') as f:
	# Collect failed URLs in a list
	for resource in f:
		try:
			res = resource.split(',')
			failed_url = unicode(res[1])
			failed_id = unicode(res[-1].rstrip())
			failed_resources.append({ 'url': failed_url, 'id': failed_id })
		except:
			print "Warning: cannot encode %s in Unicode" % resource.split(',')[1] 

for file in os.listdir(os.getcwd() + '/packages_json'):
	with open('packages_json/' + file) as package_f:
		# Open a package definition file
		package = load(package_f)
		try:
			# Retrieve metadata URI 
			metadata_uri = package['md_uri']
		except KeyError:
			# Some packages do not have a metadata URI, we assume these 
			# are stored in data.overheid.nl and not in Nationaal GeoRegister
			# and do not include them in analysis
			metadata_uri = ''

		if 'nationaalgeoregister' in metadata_uri:
			for resource in package['resources']:
				total_geo += 1

				# omit = ['None', 'dataset']
				# include = ['OGC:WMS', 'OGC:WFS', 'OGC:WMTS', 'OGC:WCS', 'INSPIRE Atom', 'website', 'download']
				# no_filter = ['OGC:WMS', 'OGC:WFS', 'OGC:WMTS', 'OGC:CSW', 'website', 'download', 'None', 'dataset']

				# if resource['protocol'] not in omit:
				# if resource['protocol'] in include:
				# if resource['protocol'] in no_filter:
					# Check whether current geo resource has failed the link checker
					# pudb.set_trace()


				#for failed_url in failed_urls:
				for failed_resource in failed_resources:
					if resource['id'] == failed_resource['id']:
						total_failed_geo += 1
						failed_geo_resources.append([resource['name'], resource['protocol'], failed_resource['url'], failed_resource['id']])
						failed_resources.remove(failed_resource)
						break

print total_geo, total_failed_geo

with open('failed_geo_resources.csv', 'w') as f_out:
	writer = csv.writer(f_out, delimiter=',', quotechar="'")

	for failed_geo_resource in failed_geo_resources:
		writer.writerow(failed_geo_resource)