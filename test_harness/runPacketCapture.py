import sys
import subprocess
import os
import time
from datetime import datetime

facebook_login_script = 'droidbot_scripts/facebook_loggin.json'
apks_path = '/media/chimps/TOSHIBA EXT/apkdownload'

def checkVPN(device):
	try:
		outbytes = subprocess.check_output(['adb','-s',device, 'shell', 'ifconfig','tun0'],timeout=2)
	except KeyboardInterrupt:
		exit(1)
	except Exception as e:
		print(e)
		return False
	else:
		if b'tun0: No such device' in outbytes.strip(b'\r\n'):
			return False
		else:
			return True

def checkModel(device):
	# Nexus_6P | Nexus_5
	try:
		out_bytes = subprocess.check_output("adb devices -l | grep "+device+" | awk '{print $5}'",shell=True,timeout=2)
		return str(out_bytes)[8:-3]
	except Exception as e:
		print(e)

def getClickPosition(device):
	model = checkModel(device)
	if model == 'Nexus_6P':
		return 1212,164
	elif model == 'Nexus_5':
		return 890,127
	else:
		return None,None

def connect_packet_capture(device):
	x, y = getClickPosition(device)
	if x is None:
		return False

	try:
		subprocess.call(['adb', '-s', device, 'shell', 'am', 'start', 'app.greyshirts.sslcapture/ui.HomeActivity'],\
			timeout=4)
		time.sleep(5)
		subprocess.call(['adb', '-s', device, 'shell', 'input', 'tap', str(x), str(y)],\
			timeout=4)
	except KeyboardInterrupt:
		exit(1)
	except Exception as e:
		print(e)
		return False
	else:
		return True

def checkBatteryStatus(device):
	while True:
		try:
			outbytes = subprocess.check_output(['adb', '-s', device, 'shell', 'dumpsys', 'battery', '|', 'grep', 'level'])
			out_text = outbytes.strip(b'\n').strip(b'\r').split(b' ')
			battery_level = int(out_text[-1])
		except KeyboardInterrupt:
			exit(1)
		except Exception:
			# wait 1 second then 
			return 100
		else:
			return battery_level

def find(name):
	print('finding {} ...'.format(name))
	try:
		outbytes = subprocess.check_output(['find','/media/chimps/TOSHIBA EXT/apkdownload','-name',name],timeout=20)
	except KeyboardInterrupt:
		exit(1)
	except:
		print('Timeout or other exception')
		return ''
	else:
		return str(outbytes.split(b'\n')[0],'utf-8')

def runAPKs(apkNameFile, emulator, policy, timeout, script=''):
	name_file = open(apkNameFile, 'r')
	content = name_file.readlines()
	name_file.close()
	cnt = 0
	if os.path.dirname(apkNameFile) == '':
		out_file_name = emulator+'_'+apkNameFile
	else:
		dirname = os.path.dirname(apkNameFile)
		out_file_name = emulator+'_'+os.path.basename(apkNameFile)
		out_file_name = os.path.join(dirname, out_file_name)

	tested_apk = set()

	pre_time = time.time()
	if os.path.isfile(out_file_name):
		with open(out_file_name,'r') as f:
			apks = f.readlines()
		for apk in apks:
			apk = apk.strip('\n')
			apk = apk.split(' ')[0]
			tested_apk.add(apk)

	out_file = open(out_file_name,'a')
	for f in content:
		name = f.strip('\n')
		if name in tested_apk:
			continue
		apkPath = find(name)
		if apkPath == '':
			out_file.write(name+' fail\n')
			continue

		if not checkVPN(emulator):
			connect_packet_capture(emulator)

		while checkBatteryStatus(emulator) < 10:
			print('Battery level too low, sleep for 300 seconds')
			time.sleep(300)

		if runDroidbot(apkPath, emulator, policy, timeout, facebook_login_script) == 0:
			out_file.write(name+' success')
			# record running time
			current_time = time.time()
			delta = current_time-pre_time
			pre_time = current_time
			out_file.write(' '+str(delta)+' '+str(datetime.now()))
			out_file.write('\n')
		else:
			out_file.write(name+' fail\n')
	out_file.close()	


def runDroidbot(apkPath, emulator, policy, timeout, script = ''):
	command = "droidbot -d "+emulator+" -a "+apkPath+\
		" -policy "+policy+\
		" -timeout "+str(timeout)+' -grant_perm -keep_env -interval 2'
	if script:
		command += ' -script '+script
	print("RUN APP:", os.path.basename(apkPath))
	try:
		exit_code = subprocess.call(['droidbot','-d',emulator,'-a',apkPath,'-policy'\
			,policy,'-timeout',str(timeout),'-grant_perm','-keep_env','-interval','2','-script', script,'-o',os.path.join('droidbot_output',os.path.basename(apkPath)[:-4])], timeout=200)
	except KeyboardInterrupt:
		exit(1)
	except:
		print('runDroidbot timeout')
		return 0
	else:
		return exit_code

if len(sys.argv) == 3:
	apk_path = sys.argv[1]
	emulator = sys.argv[2]
	runAPKs(apkNameFile=apk_path, emulator=emulator, policy='dfs', timeout=180)
else:
	print('usage: python3 runPacketCapture.py [apk_lists] [device_serial]')