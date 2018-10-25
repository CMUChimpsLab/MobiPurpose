# TrafficCollector
1. runPacketCapture.py  
	usage: `python3 runPacketCapture.py [apk_lists] [device_serial]`  
	This script will run apps one by one, connect Packet Capture if VPN connection is lost,stop the process for 5 minutes if battery level is too low.

2. processDB.py   
	usage1: `python3 processDB.py [device_serial]`  

	If the device serial is given, this script will copy the traffic data out of the device, process the traffic data and database to extract package, host, path and data, uninstall PacketCapture to delete the collected traffic data, and reinstall PacketCapture.

	usage2: `python3 processDB.py`   
	If the device serial is not given, this script will copy all the processed traffic files to ~/Desktop/merge_result, add them up to one single file and add log to ~/Desktop/merge_result/log.txt

3. check_traffic.py
	usage: `python3 check_traffic.py`  
	This script will check current collected traffic and print out the traffic count and unique package count.

4. separate_app_list.py
	usage: `python3 separate_app_list.py [app_list] [number]`  
	This script will separate the given app lists into \[number\] parts equally.


### Data Collection Workflow:

For every device:
1. Conncect Packet Capture manually. Make sure VPN service has started. If VPN service can't start, try to reboot the device and connect again.
2. Open a new command line window. Run `python3 runPacketCapture.py app_list device_serial`.
3. After some time, we need to process the raw traffic data in Packet Capture.   
	(1) Open Packet Capture, click the widget on the top right corner. Click Setting. Click Open source license. And then wait for the traffic data to be copied into sdcard.  
	(2) In command line window, run `adb -s device_serial logcat | grep PacketCapture`. This command will show the progress of step 1. When 'Done exporting packets.' and 'Done exporting packets.' appear on the screen, it means all data has been copied to sdcard.  
	(3) In command line window, run `python3 processDB.py device_serial`. This command will process the traffic data files for one device, and reinstall Packet Capture.  

4. When all devices' data has been processed, run `python3 processDB.py`, then we can get one traffic file containing all newly collected traffic.
5. To continue data collection, you need to go through the welcome screen of Packet Capture manually.

