## Read ME

### Data set released on Nov. 2018.

Download link: https://cmu.box.com/s/uwx90gwknygclykcp3k0gaphkd0f24p8

This txt file contains more than 2 million unique intercepted traffic requests. 

Each line in the file records the traffic request information: app (string), version (string), host (string), path (string), and data (dict). 

Here is an example:

```
{"data": {"maxResults": "100 "}, "path": "/heard/v1/matches/music", "py/object": "datatypes.trafficrequest.TrafficRequest", "version": "0", "app": "com.google.android.ears", "host": "www.googleapis.com"}
```




Please cite: 

@article{jinmobipurpose
 author = {Jin, Haojian and Liu, Minyi and Dodhia, Kevan and Li, Yuanchun and Srivastava, Gaurav and Fredrikson, Matthew and Agarwal, Yuvraj and Hong, Jason I.},
 title = {"Why are they collecting my data?": Inferring the Purposes of Network Traffic in Mobile Apps},
 journal = {Proc. ACM Interact. Mob. Wearable Ubiquitous Technol.},
 issue_date = {December 2018},
 year = {2019},
 publisher = {ACM},
 address = {New York, NY, USA},
}