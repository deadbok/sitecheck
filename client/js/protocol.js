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
    
    var loc = window.location, new_uri;
    if (loc.protocol === "https:")
    {
        this.uri = "wss:";
    }
    else
    {
    	this.uri = "ws:";
    }
    this.uri += "//" + loc.host + ":5683";
}

Protocol.prototype.open = function(callbacks)
{
    if (this.supported)
    {
    	// Open a socket.
    	this.ws = new WebSocket(this.uri);
    	var parent = this;
    	var cbs = callbacks;
    
    	this.ws.onopen = function()
    	{
    	    parent.isopen = true;
    	    if (jQuery.isFunction(callbacks.onopen))
    	    {
    	    	cbs.onopen();
    	    }
    	};
    
    	this.ws.onmessage = function(e)
    	{
    	    var json_data = JSON.parse(e.data);

    	    parent.server_version = json_data.version;
    	    
       	    // Run through the host names.
        	for (var i = 0; i < json_data.length; i++)
        	{
        	    if (jQuery.isFunction(cbs.onhost))
        	    {
        	    	cbs.onhost(json_data.hosts[i]);
        	    }
        	}
        	    
	        // Last message.
    	    if (json_data.length < 10)
    	    {
    	    	if (jQuery.isFunction(cbs.onlasthost))
        	    {
    	    		cbs.onlasthost();
        	    }
    	    }
    	};
    
    	this.ws.onclose = function()
    	{
    		cbs.onclose();
    	    parent.isopen = false;
    	};

    }
    else
    {
    	alert("WebSockets are unsupported by your Browser! Site check will not work without them.");
    }
};

Protocol.prototype.close = function()
{
	this.ws.close();
};

Protocol.prototype.get_hosts = function(hosts)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "get", "hosts" : "' + JSON.stringify(hosts) + '"}');
	}
};

Protocol.prototype.get_all_hosts = function()
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "get", "hosts" : [ "*" ]}');
	}
};

Protocol.prototype.add_hosts = function(hosts)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "add", "hosts" : ' + JSON.stringify(hosts) + ' }');
	}

};

Protocol.prototype.ping = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "ping", "hosts" : ' + JSON.stringify(host_names) + ' }');		
	}
};

Protocol.prototype.diff = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "diff", "hosts" : ' + JSON.stringify(host_names) + ' }');		
	}
};

Protocol.prototype.remove = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "remove", "hosts" : ' + JSON.stringify(host_names) + ' }');		
	}
};
