/*
 * UI table functions.
 * 
 * Copyright (c) 2016 Martin Bo Kristensen Grønholdt
 */

//Select all checkboxes functionality.
$('#allhost').change(function()
{
    var checkboxes = $(this).closest('form').find(':checkbox');
    if ($(this).is(':checked'))
    {
	checkboxes.prop('checked', true);
    }
    else
    {
	checkboxes.prop('checked', false);
    }
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
			    $(
				    '#'
					    + $(this).attr('id').replace(
						    '_detail', '_expand'))
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
	
	//Reset a other headers.
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
	}
	//Trigger sort and render.
	sorted_keys = [];
	$('tbody[id$="_bodyl"]').remove();
	for (var host in hosts)
	{
		if (hosts.hasOwnProperty(host))
		{
			hosts[host].rendered = false;
		}
	}
	for (var host in hosts)
	{
		if (hosts.hasOwnProperty(host))
		{
			console.log('Render host: ' + host);
			render(hosts[host]);
		}
	}
}
