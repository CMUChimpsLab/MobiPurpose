import sqlite3
import os
import subprocess
import chardet
from urllib.parse import unquote
import time
from datetime import datetime
import sys

class traffic():
	def __init__(self):
		self.host = ''
		self.path = ''
		self.package = ''
		self.creation_time = ''
		self.version = 0
		self.data = ''
		self.filename = ''

def check_db_files_existance(device_serial):
	print(' '.join(['adb','-s',device_serial,'shell','cd','/sdcard/packets','&&','ls']))
	outbytes = subprocess.check_output(['adb','-s',device_serial,'shell','cd','/sdcard/packets','&&','ls'])
	if b'schedule.db' in outbytes:
		return True
	else:
		return False
	# print(outbytes)

def pullData(device_serial):
	# print(' '.join(['adb','-s',device_serial,'shell','su','-c','cp','/data/data/app.greyshirts.sslcapture/databases/schedule.db','/sdcard']))
	# subprocess.call(['adb','-s',device_serial,'shell','su','-c','cp','/data/data/app.greyshirts.sslcapture/databases/schedule.db','/sdcard'])
	if not os.path.isdir(device_serial):
		os.mkdir(device_serial)
	print(' '.join(['adb','-s',device_serial,'pull','/sdcard/packets/schedule.db',device_serial]))
	subprocess.call(['adb','-s',device_serial,'pull','/sdcard/packets/schedule.db',device_serial])
	print(' '.join(['adb','-s',device_serial,'pull','/sdcard/packets/upstream',device_serial]))
	subprocess.call(['adb','-s',device_serial,'pull','/sdcard/packets/upstream',device_serial])

def remove_schedule_db(device_serial):
	print(' '.join(['adb','-s',device_serial,'shell','rm','/sdcard/packets/schedule.db']))
	subprocess.call(['adb','-s',device_serial,'shell','rm','/sdcard/packets/schedule.db'])	
	print(' '.join(['adb','-s',device_serial,'shell','rm','-r','/sdcard/packets/upstream']))
	subprocess.call(['adb','-s',device_serial,'shell','rm','-r','/sdcard/packets/upstream'])	

def reinstall_packetcapture(device_serial):
	print(' '.join(['adb','-s', device_serial, 'uninstall','app.greyshirts.sslcapture']))
	subprocess.call(['adb','-s', device_serial, 'uninstall','app.greyshirts.sslcapture'])
	print(' '.join(['adb','-s', device_serial, 'install', '/home/chimps/Downloads/rewritten_sslcapture.apk']))
	subprocess.call(['adb','-s', device_serial, 'install', '/home/chimps/Downloads/rewritten_sslcapture.apk'])


def filter(app_main_name):
	filter_name = ['Packet Capture', 'Google Account Manager'\
	,'Google Play Store']
	if app_main_name in filter_name:
		return False
	return True

def check_prefix(line):
	prefix_list = ['Cookie:','GET','POST','Connection:',\
	'User-Agent:','Host:','Referer:','Accept-Encoding:','Accept-Language:',\
	'Referer:','X-Requested-With:','Accept:','Authorization:','API-Client:',\
	'Content-Encoding:','Content-Type:','Content-Length:','cache-control:',\
	'Origin:','Upgrade-Insecure-Requests:','content-type:','Cache-Control:',\
	'Pragma:','Transfer-Encoding:','Access-Control-Request-Method:','Cookie2',\
	'Content-Disposition:','OPTIONS']
	flag = True
	for prefix in prefix_list:
		if line.startswith(prefix):
			flag = False
			break
	return flag

def check_data_str(line):
	line = line.split('&')
	for field in line:
		if '=' not in field or ':' in field:
			return False
	return True

def parseTraffic(filename):
	traffic_list = []
	with open(filename,'rb') as f:
		content = f.readline()
		while content:
			content = content.strip(b'\r\n')
			encoding = chardet.detect(content)['encoding']
			next_line = ''
			if encoding and encoding == 'ascii':
				content = content.decode('ascii')
				content = unquote(content)
				# check_prefix(content)
				if content.startswith('POST') or content.startswith('GET') or content.startswith('OPTIONS'):
					url = content
					if url.startswith('POST'):
						# print('method:','POST')
						url = url[5:]
					elif url.startswith('GET'):
						# print('method:','GET')
						url = url[4:]
					elif url.startswith('OPTIONS'):
						url = url[8:]

					if url.endswith('HTTP/1.1'):
						url = url[:-8]

					pos = url.find('?')
					if pos != -1:
						path = url[:pos]
						# print('path:',path)
						# print('data:')
						data = url[pos+1:]
						data = data.split('&')
						data_str = ''
						for field in data:
							if '=' in field:
								field = field.split('=')
								data_str+="'"+field[0]+"':'"+field[1]+"',"
						data_str = data_str[:-1]
					else:
						path = url
						data_str = "''"
						# print('path:',path)
					new_traffic = traffic()
					new_traffic.path = path
					new_traffic.data = data_str
					new_traffic.filename = filename
					traffic_list.append(new_traffic)
					# print(content)
				elif content.startswith("Host: ") and len(traffic_list) > 0 and traffic_list[-1].host == '':
					traffic_list[-1].host = content[6:]
					# print('host:' ,content[6:])
				elif 'POST' in content and 'HTTP/1.1' in content:
					pos = content.find('POST')
					next_line = content[pos:]
					content = content[:pos]
				elif 'GET' in content and 'HTTP/1.1' in content:	
					pos = content.find('GET')
					next_line = content[pos:]
					content = content[:pos]

				if check_prefix(content) and check_data_str(content):
					if len(traffic_list) > 1:
						if traffic_list[-1].data == "''":
							traffic_list[-1].data = ''
						else:
							traffic_list[-1].data += ','
						content = content.split('&')
						for field in content:
							if '=' in field:
								field = field.split('=')
								traffic_list[-1].data+="'"+field[0]+"':'"+field[1]+"',"
						traffic_list[-1].data = traffic_list[-1].data[:-1]
						# print(traffic_list[-1].data)
				# if content.endswith('HTTP/1.1'):
				# 	print('#####',content)
				# else:
				# 	print('###',content)
			if next_line != '':
				content = str.encode(next_line)
			else:
				content = f.readline()
	return traffic_list
				

def processDB(device_serial):
	try:
		con = sqlite3.connect(os.path.join(device_serial,'schedule.db'))
		cur = con.cursor()
		cur.execute('SELECT * FROM capture;')
		rows = cur.fetchall()
		print('database row count',len(rows))
		# 0 id, 1 capture_time, 2 file_path, 3 server_ip, 4 server_port, 5 app main name, 6 app full name, 9 app package
		# check file size
		all_traffic_list = []
		for row in rows:
			creation_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(row[1]/1000))+'.%d'%(row[1]%1000)
			traffic_file_name = os.path.basename(row[2])+'.txt'
			traffic_file_path = os.path.join(device_serial,'upstream',traffic_file_name)
			if filter(row[5]):
				traffic_file_name = os.path.basename(row[2])+'.txt'
				traffic_file_path = os.path.join(device_serial,'upstream',traffic_file_name)
				# print(traffic_file_path)
				if os.path.isfile(traffic_file_path) and os.stat(traffic_file_path).st_size > 0:
					# print('{:->50}'.format('-'))
					
					# print(creation_time)
					# print(row[9],':',row[6])
					# print(str(row[0])+','+traffic_file_name+','+row[5]+','+row[9])
					traffic_list = parseTraffic(traffic_file_path)
					for i in range(0,len(traffic_list)):
						traffic_list[i].package = row[9]
						traffic_list[i].creation_time = creation_time
					all_traffic_list += traffic_list
		print('traffic count',len(all_traffic_list))

		out_file_path = os.path.join(device_serial,str(datetime.now())+'_'+str(len(all_traffic_list))+'_traffic.txt')
		with open(out_file_path,'w') as f:
			for tr in all_traffic_list:
				f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(tr.package,tr.version,tr.host,tr.path,tr.data,tr.creation_time))
		# for tr in all_traffic_list:
		# 	print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(tr.package,tr.version,tr.host,tr.path,tr.data,tr.creation_time, tr.filename))

	except sqlite3.Error as e:
		print('error')
		if con:
			con.rollback()
			print("Error %s:"%e.args[0])
	finally:
		if con:
			con.close()

def move_all_traffic_files():
	move_destination = '/home/chimps/Desktop/tmp/merge_result'
	outbytes = subprocess.check_output(['adb','devices'])
	outlines = outbytes.split(b'\n')
	for line in outlines:
		if b'List of devices attached' == line or len(line) < 2:
			continue
		device_serial = str(line.split(b'\t')[0],'utf-8')
		if os.path.isdir(device_serial):
			for filename in os.listdir(device_serial):
				if filename.endswith('traffic.txt'):
					print(['cp',os.path.join(device_serial, filename),move_destination])
					subprocess.call(['cp',os.path.join(device_serial, filename),move_destination])


def merge_traffic_files():
	move_destination = '/home/chimps/Desktop/tmp/merge_result'
	# find latest time
	latest_time = ''
	for filename in os.listdir(move_destination):
		if filename.startswith('traffic_'):
			traffic_time = filename.split('_')[1][:-4]
			if latest_time == '' or traffic_time > latest_time:
				latest_time = traffic_time

	current_time = datetime.now()
	merge_file_path = os.path.join(move_destination,'traffic_'+str(current_time)+'.txt')
	total_traffic_count = 0
	with open(merge_file_path,'a') as f1:
		for filename in os.listdir(move_destination):
			if filename.endswith('traffic.txt'):
				traffic_time = filename.split('_')[0]
				if traffic_time < latest_time:
					continue
				traffic_count = int(filename.split('_')[1])
				total_traffic_count += traffic_count
				with open(os.path.join(move_destination, filename),'r') as f2:
					contents = f2.readlines()
					f1.writelines(contents)

	if total_traffic_count > 0:
		with open(os.path.join(move_destination, 'log.txt'),'a') as f:
			f.write('{}\n\t{}:{}\n'.format(merge_file_path, 'traffic_count',str(total_traffic_count)))

if __name__ == '__main__':
	if len(sys.argv) == 2:
		device = sys.argv[1]
		pullData(device)
		processDB(device)
		remove_schedule_db(device)
		reinstall_packetcapture(device)
		exit()

	if len(sys.argv) == 1:
		move_all_traffic_files()
		merge_traffic_files()
		exit()
	# pullData('027de3d80b35d6bc')
	# processDB('027de3d80b35d6bc')
	# processDB()
	# parseTraffic('84B7N16223000400/upstream/capture1876135972.dat.txt')
	# device1 = '84B7N16531001384'
	# device2 = '84B7N16223000400'
	# device3 = '027de3d80b35d6bc'
	# device4 = '034f1e14f0b325a4'
	# device5 = '0665f8e0f0eca7b6'
	# device6 = '01aad2520c343c4a'
	# device7 = '04277eb813b70223'

	# device = device6
	# pullData(device)
	# processDB(device)
	# remove_schedule_db(device)
	# reinstall_packetcapture(device)
	# exit()