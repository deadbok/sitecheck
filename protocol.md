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

The server sends data in blocks of 10. Only the last message will contain
less than 10 data entries. If the total number of data entries is divisible by
10, a message with 0 entries will be send as the last.

	{
		"version" : "x.y.z",
		"total": 0,
		"type": "",
		"length" : >-1,
		"data" : [ { data } ]
	}
  
`length` is the number of hosts in the response. `data` is the list of
data. `type` is the type of object to work on, either `pattern` or `host`.

*If `length` is negative, the data has been removed*. 

	{
		"version" : "x.y.z",
		"total": 0,
		"type": "",
		"length" : < 0,
		"data" : [ data_ids ]
	}
	
`data_ids` is a list of data id's that has been removed.

### Special info response ###

	{
		"version" : "x.y.z",
		"total": 0,
		"type": "host",
		"length" : 0,
		"data" : [ ]
	}
