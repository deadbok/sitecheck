#Site Check WebSocket protocol.#

The client and server communicates over a WebSocket connection, using JSON
formatted messages.

##Request to the server.##

Request are send from the client, the server responds asynchroniously when a
response is ready.

###JSON messages structure###

	{
		"action" : "",
		"hosts" : [ "" ]
	}
	
`action` is the action that the server should perform. `hosts` is a list of
host to perform the action on. Only the `*` wildcard is supported
	
###Actions###

 * add
 * diff
 * get
 * ping
 
####add####

Add the hosts listed in `hosts`.
 
####diff####

Run a diff on the current and the last index page of the hosts listed in
`hosts`.

####get####

Get the data for the hosts listed in `hosts`.

####ping####

Ping the hosts listed in `hosts`

##Response from the server##

	{
		"length" : 0,
		"hosts" : [ "" ]
	}
  
`length` is the number of hosts in the response. `hosts` is the list of host
data.