import sys

if len(sys.argv) == 3:
	apps_list_path = sys.argv[1]
	phone_num = int(sys.argv[2])

	with open(apps_list_path,'r') as f:
		content = f.readlines()

	total_lines = len(content)
	each_lines = int(total_lines/phone_num)
	for i in range(phone_num):
		st = i*each_lines
		en = (i+1)*each_lines if i < phone_num-1 else total_lines
		with open(str(i)+'_app_list.txt','w') as f:
			for line in content[st:en]:
				f.write(line)
else:
	print('usage: python3 separate_app_list.py [app_list] [number]')