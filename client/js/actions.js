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
	protocol.ping(host_names);
}

function req_diff()
{
	var host_names = $("#host:checked").map(function() {
		return this.value;
	}).get();
	protocol.diff(host_names);
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
//Import hosts from a file
$('#importOK').click(
		function(e) {
			var file = $('#importFile')[0].files[0];
			console.log("File name: " + file);
		    var reader = new FileReader();
			
	    	reader.onload = function(e)
	    	{
	        	console.log('File loaded');
	        	var hosts = e.target.result.split('\n');
	        	for ( var i = 0; i < hosts.length; i++)
	        	{
	        		//Strip of comments
	        		if (hosts[i][0] == '#')
	        		{
	        			hosts.splice(i, 1);
	        		}
	        	}
	        	protocol.add_hosts(hosts);
	    	};
	    	reader.readAsText(file);
		});

$('#addHostButton').click(
		function() {
			$('#addHostModal').modal('show');
		});

$('#addhostok').click(
		function() {
			protocol.add_hosts([ $('#newhost').val() ]);
		});

$('#removeHostButton').click(
		function() {
			var host_names = $("#host:checked").map(function() {
				return this.value;
			}).get();
			$('#removeHostList').html((host_names).join(' '));
			$('#removeHostModal').modal('show');
		});

$('#removeHostYes').click(
		function() {
			var host_names = $("#host:checked").map(function() {
				return this.value;
			}).get();
			protocol.remove_hosts(host_names);
		});

$('#addPatternButton').click(
		function() {
			$('#addPatternModal').modal('show');
		});

$('#addPatternOK').click(
		function() {
			var pattern = {};
			pattern.name = $('#newpatternname').val();
		    pattern.type = $('[name="newpatterntype"]:checked').val();
		    pattern.pattern = $('#newpattern').val();
			protocol.add_pattern(pattern);
		});

$('#removePatternYes').click(
		function() {
			protocol.remove_patterns([$(this).attr('name')]);
		});

$('#editPatternOK').click(
		function() {
		    //Get old name
		    var old_name = $('#editPatternOK').attr('name');
		    
			var pattern = {};
			pattern.name = $('#editpatternname').val();
		    pattern.type = $('[name="editpatterntype"]:checked').val();
		    pattern.pattern = $('#editpattern').val();
			
		    if (old_name !== pattern.name)
		    {
		    	protocol.remove_patterns([old_name]);
		    }
		    protocol.add_pattern(pattern);
		});

