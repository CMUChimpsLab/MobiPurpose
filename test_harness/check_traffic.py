import os
path = '/home/chimps/Desktop/tmp/merge_result'
package_set = set()
traffic_count = 0
for file_name in os.listdir(path):
	if file_name.startswith('traffic'):
		fullpath = os.path.join(path,file_name)
		with open(fullpath) as f:
			content = f.readline()
			while content:
				traffic_count += 1
				content = content.split('\t')
				package_set.add(content[0])
				content = f.readline()
print('traffic count', traffic_count)
print('unique package name',len(package_set))
