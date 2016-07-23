/*
 * UI pattern setting functions.
 * 
 * Copyright (c) 2016 Martin Bo Kristensen Grønholdt
 */

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

function addPattern(pattern)
{
	if (pattern.name === null)
	{
		pattern.name = 'null';
	}
	//Generate CSS safe id.
	pattern.id = pattern.name.replace('.', '_').replace('-', '_').replace(' ', '_');

	//Escape the pattern
	pattern.pattern_escape = escapeHtml(pattern.pattern);
	
	pattern.rendered = false;
	
	//Add to the internal representation.
	patterns[pattern.name] = pattern;
}

function removePattern(pattern)
{
	if (pattern.rendered)
	{
		$('#' + pattern.id).remove();
	}
	delete patterns[pattern.name];
}

//Insert a pattern entry in the table, sorting them on the go.
function renderPattern(pattern)
{
	var pattern_html = "";
	//Remove the previous entry if there is one.
	if (pattern.rendered)
	{
		$('#' + pattern.id).remove();
		pattern.rendered = false;
		
	}
	
	pattern_html = pattern_tmpl.render(pattern);
	$('#pattern_body').append(pattern_html);
	pattern.rendered = true;

	//Bind the remove function.
	$('#remove_' + pattern.id + '_button').click(function()
	{
		var id = $(this).attr('id').replace('remove_', '').replace('_button', '');
		var name = $('#' + id).attr('name');
		
		$('#removePatternYes').attr('name', name)
		$('#removePatternView').html(name);
		$('#removePatternModal').modal('show');
	});
	
	//Bind the edit function.
	$('#edit_' + pattern.id + '_button').click(function()
	{
		var id = $(this).attr('id').replace('edit_', '').replace('_button', '');
		var name = $('#' + id).attr('name');
		
		$('#editPatternOK').attr('name', name)
		$('#editpatternname').val(name);
		$('#editpatterntype' + patterns[name].type).prop('checked', true);
		$('#editpattern').val(patterns[name].pattern);
		$('#editpatterntscore' + patterns[name].score ).prop('checked', true);
		$('#editPatternModal').modal('show');
	});
}
