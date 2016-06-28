
/*
 * WebSocket communication with the server
 * 
 * Copyright (c) 2016 Martin Bo Kristensen Grønholdt
 */

function Protocol()
{
    if ("WebSocket" in window)
    {
	this.supported = true;
    }
    else
    {
	this.supported = false;
    }
    this.isopen = false;
}

Protocol.prototype.open = function()
{
    if (this.supported)
    {
    	// Open a socket.
    	this.ws = new WebSocket("ws://localhost:5683");
    	var parent = this;
    
    	this.ws.onopen = function()
    	{
        
    	    parent.onopen();
    	    this.send('{ "action" : "get", "hosts" : [ "*" ]}');
    	    parent.isopen = true;
    	};
    
    	this.ws.onmessage = function(e)
    	{
    	    var json_data = JSON.parse(e.data)
    	    // Run through the host names.
    	    for (var i = 0; i < json_data.length; i++)
    	    {
    	    	parent.onhost(json_data.hosts[i]);
    	    }
    	    // Last message.
    	    if (json_data.length < 10)
    	    {
    	    	parent.onlasthost();
    	    }
    	};
    
    	this.ws.onclose = function()
    	{
    	    parent.onclose();
    	    parent.isopen = false;
    	};

    }
    else
    {
    	alert("WebSockets are unsupported by your Browser! Site check will not work without them.");
    }
}

Protocol.prototype.close = function()
{
	this.ws.close();
}

Protocol.prototype.ping = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "ping", "hosts" : ' + JSON.stringify(host_names) + ' }');		
	}
}

Protocol.prototype.diff = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "diff", "hosts" : ' + JSON.stringify(host_names) + ' }');		
	}
}
