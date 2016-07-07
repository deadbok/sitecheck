# Site Check JSON state file format #

The server stores its internal state on disk using JSON format. Here is a quick
introduction to the format.

## JSON ###

	{
	    "server":{
	        "version":"x.y.x"
	    },
	    "hosts":[
	        {
	            "diff":"",
	            "ip": "www.xxx.yyy.zzz",
	            "msgs":[
	                {
	                    "matches":[
	                        {
	                            "msg":"",
	                            "score":""
	                        }
	                    ],
	                    "pattern":""
	                }
	            ],
	            "name":"",
	            "replyHost":"",
	            "state":"",
	            "state_msg":"",
	            "time":0
	        }
	    ],
	    "patterns":[
	        ""
	    ],
	    "plugins":{
	        "active":[
	            ""
	        ]
	    }
	}


## Root values ##

The root is an object with these possible members:

 * server
 * hosts
 * patterns
 * plugins
 
### server ###

Server related data, mostly server configuration.

#### version ####

The server version.

### hosts ###

List of all hosts that Site Status is currently mon.

### patterns ###

Data related to the pattern matching "engine".

### plugins ###

Data related to plug ins.

