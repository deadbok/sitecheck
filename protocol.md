# Site Check WebSocket protocol #

The client and server communicates over a WebSocket connection, using JSON
formatted messages.

## Request to the server ##

Request are send from the client, the server responds  when a ready.

### JSON messages structure ###

	{
		"action" : "",
		"type": "",
		"param" : [ "" ]
	}
		
`action` is the action that the server should perform.
`type` is the type of object to apply the action to/for.
`param` is a list of identifiers of objects to work on. 

### Actions ###

 * add: Add the objects listed in `param`.
 * remove: Remove the objects listed in `param`.
 * get: Get the data for the objects listed in `param`.

### `host` type specific actions ###

 * diff: Run a diff on the current and the last index page of the hosts listed
   in `param`.
 * ping: Ping the hosts listed in `param`

### Types ###

 * host:  Work on a host.
 * pattern: Work on a pattern.
   
### Parameters ###

 * For `host` type messages, `param` is a list of host names or the `*` wild
   card.
 * For `pattern` type messages, `param` is a list of patterns or the `*` wild
   card.

## Response from the server ##

The server sends hosts in blocks of 10. Only the last message will contain
less than 10 hosts. If the total number of hosts is divisible by 10, a message
with 0 hosts will be send as the last.

	{
		"version" : "0.0.0",
		"total_hosts": 0,
		"length" : >-1,
		"hosts" : [ { host_data } ]
	}
  
`length` is the number of hosts in the response. `hosts` is the list of host
data.

*If `length` is negative, the hosts has been removed*. 

	{
		"version" : "0.0.0",
		"total_hosts": 0,
		"length" : < 0,
		"hosts" : [ host_names ]
	}
	
`hosts` is the list of host names that has been removed.

### Host data ###

	{
        "diff": "",
        "ip": "",
        "msgs": [
            {
                "matches": [
                    {
                        "msg": "",
                        "score": ""
                    }
                ],
                "pattern": ""
            }
        ],
        "name": "",
        "replyHost": "",
        "state": "",
        "state_msg": "", 
        "time": 0
    }
