/*
 * UI table functions.
 * 
 * Copyright (c) 2016 Martin Bo Kristensen Grønholdt
 */

//Select all checkboxes functionality.
$('#allhost').change(function()
{
    $('[class="host"]').prop('checked', this.checked);
});


function expand_all()
{
    $(this).toggleClass('glyphicon-collapse-up glyphicon-collapse-down');
    if ($(this).hasClass('glyphicon-collapse-up'))
    {
	$('tr[id$="_detail"]')
		.each(
			function()
			{
			    $(this).collapse('show');
			    $('#' + $(this).attr('id').replace(
						    '_detail', '_expand'))
				    .removeClass(
					    'glyphicon-collapse-up glyphicon-collapse-down');
			    $('#' + $(this).attr('id').replace('_detail', '_expand'))
				    .addClass('glyphicon-collapse-up');
			});
    }
    else
    {
	$('tr[id$="_detail"]')
		.each(
			function()
			{
			    $(this).collapse('hide');
			    $('#' + $(this).attr('id').replace(
						    '_detail', '_expand'))
				    .removeClass(
				    		'glyphicon-collapse-up glyphicon-collapse-down');
			    $('#' + $(this).attr('id').replace(
						    '_detail', '_expand'))
				    .addClass('glyphicon-collapse-down');
			});
    }
}

function select_sort()
{
	//Get the value name from the id.
	sort_value = $(this).attr('id').replace('_header', '');
	
	//Reset all other headers.
	var current_id = $(this).attr('id');
	$('span[id$="_header"]').each(function()
	{
		if ($(this).attr('id') != current_id)
		{
    		$(this).children('#arrow').removeClass('sort-active');
    		$(this).children('#arrow').addClass('sort-inactive');
    		$(this).children('#arrow').removeClass('glyphicon-chevron-up');
    		$(this).children('#arrow').addClass('glyphicon-chevron-down');
		}
	});
	//Check if selection is currently inactive.
	if ($(this).children('#arrow').hasClass('sort-inactive'))
	{
		//Make active.
		$(this).children('#arrow').toggleClass('sort-inactive sort_active');
		sort_order = 1;
	}
	else
	{
		//Time to become inactive?
		if ($(this).children('#arrow').hasClass('glyphicon-chevron-up'))
		{
			$(this).children('#arrow').toggleClass('sort-inactive sort_active');
			sort_value = undefined;
		}
		$(this).children('#arrow').toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
		sort_order = -1;
	}
	//Trigger sort and render.
	sort_keys = [];
	$('tbody[id$="_body"]').remove();
	for (var host in hosts)
	{
		if (hosts.hasOwnProperty(host))
		{
			hosts[host].rendered = false;
			//render(hosts[host]);
			setTimeout(renderHost.bind(null, hosts[host]), 0);
		}
	}
}

//Stolen from: http://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery
var entityMap = {
		"&": "&amp;",
		    "<": "&lt;",
		    ">": "&gt;",
		    '"': '&quot;',
		    "'": '&#39;',
		    "/": '&#x2F;'
		    };

function escapeHtml(string)
{
	return String(string).replace(/[&<>"'\/]/g, function (s)
		{
			return entityMap[s];
		});
}
//End of swag

function addHost(host)
{
	if (host.name === null)
		host.name = 'null';
	//Generate CSS safe id.
	host.id = host.name.replace('.', '_').replace('-', '_');
	//Generate IP sort key.
	if ((host.ipaddr == 'Unknown') || (host.ipaddr === undefined) || (host.ipaddr === null))
	{
		host.ipaddr = 'Unknown';
		host.ip_value = 0;
	}
	else
	{
		var ip_split = host.ipaddr.split('.');
		host.ip_value = ip_split[0]*0x1000000 + ip_split[1]*0x10000 + ip_split[2]*0x100 + ip_split[3]*1;
	}
	//Generate time sort key.
	if ((host.time === undefined) || (host.time == 'Never'))
	{
		host.time = 0;	
	}
	//UNIX time to human readable
	host.time_value = host.time;
	if (host.time === 0)
	{
		host.time = "Never";
	}
	else
	{
    	dt = new Date(host.time * 1000); 
    	host.time = new Date(host.time * 1000).format('H:i:s j/n-Y');
	}
	//Escape the diff
	host.diff_escape = escapeHtml(host.diff);
	
	//Check if this is a new host.
	if (hosts[host.name] !== undefined)
	{
		//It is not, copy values for UI state from the old one.
		host.visible = hosts[host.name].visible;
		host.rendered = hosts[host.name].rendered;
	}
	else
	{
		//Init UI state.
		host.visible = false;
		host.rendered = false;
	}
	//Data has been updated since last render.
	host.updated = true;
	
	//Add to the internal representation.
	hosts[host.name] = host;
	
	$('#n_hosts').html(Object.keys(hosts).length);
}

function removeHost(host)
{
	if (host.rendered)
	{
		$('tbody[id$="' + host.id + '_body"]').remove();
	}
	delete hosts[host.name];
	
	var index = sort_keys.indexOf(host.name);
	sort_keys.splice(index, 1);
	
	$('#n_hosts').html(Object.keys(hosts).length);
}

//Insert a host entry in the table, sorting them on the go.
function renderHost(host)
{
	var host_html = "";
	//Remove the previous entry if there is one.
	if (host.rendered)
	{
		$('tbody[id$="' + host.id + '_body"]').remove();
		host.rendered = false;
		
	}
	
	if (sort_value === undefined)
	{
		//No sort just append.
		sort_keys.push(host.name);
		host_html = host_row_tmpl.render(host);
		$('#host_table').append(host_html);
	}
	else
	{
		var sort_host = function(a, b)
		{
			switch(sort_value)
			{
				case 'name':
					return a[sort_value].localeCompare(b[sort_value]);
				case 'ip_value':
					if ( a[sort_value] < b[sort_value])
					{
						return -1;
					}
					else if (a[sort_value] === b[sort_value])
					{
						return 0;
					}
					else
					{
						return 1;
					}
					break;
				case 'state':
					return a[sort_value].localeCompare(b[sort_value]);
				case 'replyHost':
					return a[sort_value].localeCompare(b[sort_value]);
				case 'time_value':
					if ( a[sort_value] < b[sort_value])
					{
						return -1;
					}
					else if (a[sort_value] === b[sort_value])
					{
						return 0;
					}
					else
					{
						return 1;
					}
					break;
				case undefined:
					return -1;
				default: console.log('Unknown sort entry: ' + sort_value);
			}
		};

		if ( sort_keys.length === 0 )
		{
			//First entry.
			sort_keys.push(host.name);
			host_html = host_row_tmpl.render(host);
			$('#host_table').append(host_html);
		}
		else
		{
			
			var sorted = false;
			var i = 0;
			var last_res;
			
			while ( (!sorted) && (i < sort_keys.length ) )
			{
				//Save the current sort value.
				var res = sort_host(hosts[sort_keys[i]], host) * sort_order;

				//If we're at the end, just append
				if ( (sort_keys.length === ( i + 1)) && ( res < 1) )
				{
					sort_keys.push(host.name);
					host_html = host_row_tmpl.render(host);
					$('#host_table').append(host_html);
					sorted = true;
				}
				else
				{
					if ( res > -1 )
					{
						//Insert before
						host_html = host_row_tmpl.render(host);
						$('tbody[id$="' + hosts[sort_keys[i]].id + '_body"]').before(host_html);
						sort_keys.splice(i, 0, host.name);
						sorted = true;	
					}
				}
				i++;
			}
		}
	}
	//Host is visible.
	host.visible = true;
	//Host is in the table.
	host.rendered = true;
	//Host has no new data.
	host.updated = false;
	//Bind the collapse function.
	$('#' + host.id + '_expand').click(function()
	{
		$(this).toggleClass('glyphicon-collapse-up glyphicon-collapse-down');
		
		var detail = $(this).attr('id').replace('_expand', '_detail');
		$('#' + detail).collapse('toggle');
		
		 
		hljs.highlightBlock($('#' + detail.replace('_detail', '_diff_code')).get(0));
	});
	//Uncheck the all checkbox
	$('#allhost').prop('checked', false);
}
