# Site Check JSON state file format #

The server stores its internal state on disk using JSON format. Here is a quick
introduction to the format.

## JSON ###

	{
	    "server":{
	        "version":"x.y.x"
	        "msg":"",
			 "msg_state":""
	    },
	    "hosts":[
	        {
	            "diff":"",
	            "ip": "www.xxx.yyy.zzz",
	            "msgs":[
	                {
	                    "matches":[
	                        {
	                            "string":"",
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

 * version
 * msg
 * msg_state

#### version ####

The server version.

#### msg ####

Any message from the server about its state-

#### msg_state ####

`good`, `neutral`, or `bad`.

### hosts ###

List of all hosts that Site Status is currently working with.

 * diff
 * ip
 * msgs
 * name
 * reply_host
 * state
 * state_msg
 * time
 
#### diff ####

Data from a unified diff of the last and current index page.

#### ip ####

IP address of the host.
	            
#### msgs ####

Messages from the active plug-ins and the pattern matcher.

 * matches
 * pattern
 
##### matches #####

Pattern matches in diff.

 * string
 * score
 
###### string ######

Part of the line where a match is found.

###### score ######

`good`, `neutral`, or `bad` indicating the score of the match.

##### pattern #####

Pattern for the matches in `matches`
 
#### name ####

The name of the host.

#### reply_host ####

The name of the replying host.

#### state ####

`good`, `neutral`, or `bad` indicating the overall status.

#### state_msg ####

Global state description.

#### time ####

Last time a request to the host was made.  
 
### patterns ###

Data related to the pattern matching "engine".

### plugins ###

Data related to plug ins.

