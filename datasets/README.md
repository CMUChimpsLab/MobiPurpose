## Read ME


### Data set released on Nov. 2018.

[Raw data set download link](https://cmu.box.com/s/uwx90gwknygclykcp3k0gaphkd0f24p8)

This txt file contains more than 2 million unique intercepted traffic requests. 

Each line in the file records a single traffic request entry: app (string), version (string), host (string), path (string), and data (dict). 

Here is an example:

<pre>
{
  "data": {
    "maxResults": "100 "
  },
  "path": "/heard/v1/matches/music",
  "py/object": "datatypes.trafficrequest.TrafficRequest",
  "version": "0",
  "app": "com.google.android.ears",
  "host": "www.googleapis.com"
}
</pre>

### Processed Data set with predicted purpose.

[the traffic requests with classified data type and inferred purpose.](https://cmu.box.com/s/tlnsk6blcs6hp25cww8nogp70w1uzn9m)

Each line inside the file is a json string of a classified request.

<pre>
{ app:  
version: 
host:
path:
data: {key1: val1 | type1 | purpose1, key2: val2 | type2 | purpose2, ...}
}
</pre>


### The apps used in our experiment

[The list of App descriptions](https://cmu.box.com/s/gdt6ccpi6rbq57mdywv5uzanermia7lw)

[The list of App package names](https://cmu.box.com/s/y389k63nh2m3me7egn0xhtwy4idjcn0o)

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