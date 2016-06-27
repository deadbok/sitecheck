/*
 * UI actions that do not belong to the table.
 * 
 * Copyright (c) 2016 Martin Bo Kristensen Grønholdt
 */

function req_ping()
{
	var host_names = $("#host:checked").map(function() {
		return this.value;
	}).get();
	protocol.ping(host_names)
}

function req_diff()
{
	var host_names = $("#host:checked").map(function() {
		return this.value;
	}).get();
	protocol.diff(host_names)
}

function toggle_connection()
{
	if (protocol.isopen)
	{
		protocol.close();
	}
	else
	{
		protocol.open();
	}
}
