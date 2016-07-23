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
    		console.log('New WebSockets connection open.');
    	    parent.isopen = true;
	    	if (cbs.onopen.host !== undefined)
	    	{
	    		cbs.onopen.host();
	    	}
	    	if (cbs.onopen.pattern !== undefined)
	    	{
	    		cbs.onopen.pattern();
	    	}
    	};
    
    	this.ws.onmessage = function(e)
    	{
    	    var json_data = JSON.parse(e.data);
    	    
    	    console.log("Message: " + e.data);

    	    parent.server_version = json_data.version;
    	     
    	    var i = 0;
    	    if (json_data.type === 'host')
    	    {
           	    // Run through the host names.
        	    if (json_data.length > -1)
        	    {
                	for (; i < json_data.length; i++)
                	{
                	    if (jQuery.isFunction(cbs.onadd.host))
                	    {
                	    	cbs.onadd.host(json_data.data[i]);
                	    }
                	}
        	    }
        	    else
        	    {
        	    	i = json_data.length;
        	    	do
        	    	{
        	    		if (jQuery.isFunction(cbs.onremove.host))
        	    		{
        	    			cbs.onremove.host(json_data.data[Math.abs(i) - 1]);
        	    		}
        	    		i++;
        	    	} while ( i < 0);
        	    }
    	    }
    	    
    	    if (json_data.type === 'pattern')
    	    {
           	    // Run through the pattern names.
        	    if (json_data.length > -1)
        	    {
                	for (; i < json_data.length; i++)
                	{
                	    if (jQuery.isFunction(cbs.onadd.pattern))
                	    {
                	    	cbs.onadd.pattern(json_data.data[i]);
                	    }
                	}
        	    }
        	    else
        	    {
        	    	i = json_data.length;
        	    	do
        	    	{
        	    		if (jQuery.isFunction(cbs.onremove.pattern))
        	    		{
        	    			cbs.onremove.pattern(json_data.data[Math.abs(i) - 1]);
        	    		}
        	    		i++;
        	    	} while ( i < 0);
        	    }
    	    }
        	    
	        // Last message.
    	    if ((json_data.length < 10) && (json_data.length > -1))
    	    {
    	    	if (json_data.type === 'host')
    	    	{
        	    	if (jQuery.isFunction(cbs.onlast.host))
            	    {
        	    		cbs.onlast.host();
            	    }
    	    	}
    	    	if (json_data.type === 'pattern')
    	    	{
        	    	if (jQuery.isFunction(cbs.onlast.pattern))
            	    {
        	    		cbs.onlast.pattern();
            	    }
    	    	}

    	    }
    	};
    
    	this.ws.onclose = function()
    	{
	    	if (cbs.onclose.host !== undefined)
	    	{
	    		cbs.onclose.host();
	    	}
	    	if (cbs.onclose.pattern !== undefined)
	    	{
	    		cbs.onclose.pattern();
	    	}
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

Protocol.prototype.get_info = function()
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "info", "type": "host", "param" : []}');
	}
};

Protocol.prototype.get_hosts = function(hosts)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "get", "type": "host", "param" : "' + JSON.stringify(hosts) + '"}');
	}
};

Protocol.prototype.get_all_hosts = function()
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "get", "type": "host",  "param" : [ "*" ]}');
	}
};

Protocol.prototype.add_hosts = function(hosts)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "add", "type": "host",  "param" : ' + JSON.stringify(hosts) + ' }');
	}

};

Protocol.prototype.remove_hosts = function(hosts)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "remove", "type": "host",  "param" : ' + JSON.stringify(hosts) + ' }');		
	}
};

Protocol.prototype.ping = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "ping", "type": "host",  "param" : ' + JSON.stringify(host_names) + ' }');		
	}
};

Protocol.prototype.diff = function(host_names)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "diff", "type": "host",  "param" : ' + JSON.stringify(host_names) + ' }');		
	}
};

Protocol.prototype.add_pattern = function(pattern)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "add", "type": "pattern",  "param" : [' + JSON.stringify(pattern) + '] }');
	}

};

Protocol.prototype.get_all_patterns = function()
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "get", "type": "pattern",  "param" : [ "*" ]}');
	}
};

Protocol.prototype.remove_patterns = function(patterns)
{
	if (this.supported && this.isopen)
	{
		this.ws.send('{ "action" : "remove", "type": "pattern",  "param" : ' + JSON.stringify(patterns) + ' }');		
	}
};
