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
