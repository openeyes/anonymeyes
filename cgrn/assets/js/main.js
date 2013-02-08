var asInitVals = new Array();

$(document).ready(function() {
	
	// Visual Acuity scale changes
	$('body').delegate('.visualacuitymethod', 'change', function() {
		var wrapper = $(this).closest('fieldset, tr');
		var empty_option = $('select.visualacuity option[value=""]', wrapper).first();
		$.ajax({
			url: '/anonymeyes/visualacuityreadings/'+$(this).val()+'/',
			success: function(data) {
				$('select.visualacuity', wrapper).html(empty_option.clone()).append(data)
				$('select.visualacuity', wrapper).val('');
			},
		});
	});
	
	// Datatables
	var datasets = $('#datasets').dataTable({
		bJQueryUI: true,
		sPaginationType: "full_numbers",
		aoColumns: [
		            null,
		            null,
                { "sType": "title-numeric" },
		            null,
                { "sType": "title-numeric" },
                { "sType": "title-numeric" },
		            { "bSortable": false }
		            ]
	});

	$("#datasets tfoot input").keyup(function() {
		datasets.fnFilter(this.value, $("#datasets tfoot input").index(this));
	});

	$("#datasets tfoot input").each(function(i) {
		asInitVals[i] = this.value;
	});
 
	$("#datasets tfoot input").focus(function() {
		if($(this).hasClass("search_init")) {
			$(this).removeClass("search_init");
			this.value = "";
		}
	});
 
	$("#datasets tfoot input").blur(function(i) {
		if(this.value == "") {
			$(this).addClass("search_init");
			this.value = asInitVals[$("#datasets tfoot input").index(this)];
		}
	});
	
	// Datepicker
	initDatepicker();

	// Help tips
	$('span.help').hoverIntent(
		function() {
			$(this).addClass('active');
		},
		function() {
			$(this).removeClass('active');
		}
	);
	
	// Nav
	$('header nav li').hover(
			function() {
				$(this).addClass('hover');
			},
			function() {
				$(this).removeClass('hover');
			}
	);
	
	// Wizard formset actions
	$('.formset .add-row').click(function() {
		return wizardAddForm(this);
	});
	$('.formset .delete-row').click(function() {
		return wizardDeleteForm(this);
	})

	// Management form type mutation
	$('form .management_type select').each(function() {
		updateManagementType(this);
	});
	$('form').delegate('.management_type select', 'change', function() {
		updateManagementType(this);
	});
	$('form .management_detail .surgery select').each(function() {
		updateManagementSurgery(this);
	});
	$('form').delegate('.management_detail .surgery select', 'change', function() {
		updateManagementSurgery(this);
	});

	// Outcome form mutation
	$('form .outcome_iop_detail .iop_control select').each(function() {
		updateOutcomeIOP(this);
	});
	$('form').delegate('.outcome_iop_detail .iop_control select', 'change', function() {
		updateOutcomeIOP(this);
	});
	
	
	// Lens status and extraction date dependency
	$("form select[name^='lens_status_']").each(function() {
		updateExtractionDate(this);
	});
	$("form select[name^='lens_status_']").change(function() {
		updateExtractionDate(this);
	});
	
	// EUA and Anaesthesia dependency
	updateAnaesthesia();
	$("form select#id_eua").change(function() {
		updateAnaesthesia();
	});

	// Inline forms
	initialiseInlineForms();

	$('form .inline_form_add').click(function(e) {
		addInlineForm(this);
		e.preventDefault();	
	});

	$('form').delegate('.inline_form_remove', 'click', function(e) {
		removeInlineForm(this);
		e.preventDefault();	
	});

});

function updateExtractionDate(element) {
	var side = $(element).attr('name').substring(12);
	var extraction_field = $('#id_lens_extraction_date_'+side);
	if($('option:selected', element).text() == 'Aphakia' || $('option:selected', element).text() == 'Pseudophakia') {
		extraction_field.closest('li').show();
	} else {
		extraction_field.closest('li').hide();
		extraction_field.val('');
	}
}

function updateAnaesthesia() {
	if($('form select#id_eua option:selected').text() == 'Yes') {
		$('form select#id_anaesthesia').closest('li').show();
	} else {
		$('form select#id_anaesthesia').closest('li').hide();
		$('form select#id_anaesthesia').val('');
	}
}

function initialiseInlineForms() {
	$('form .inline_form').each(function() {
		var rows = $('tbody tr', this);
		var empty_row = rows.last();
		empty_row.addClass('empty_row').hide();
		$('<p><a href="#" class="inline_form_add">Add</a></p>').insertAfter(this);
		var delete_fields = $('input[name$="-DELETE"]', rows);
		delete_fields.each(function() {
			if($(this).is(':checked')) {
				$(this).closest('tr').hide();
			} else {
				var name = $(this).attr('name');
				$(this).after('<a class="inline_form_remove" href="#">Delete</a>');
				$(this).replaceWith('<input class="delete" type="hidden" name="'+name+'" id="'+name+'"/>');				
			}
		});
		if(delete_fields.length) {
			$('thead th', this).last().html('');
		}
	});
}

function addInlineForm(add_link) {
	var inline_form = $(add_link).closest('fieldset').find('.inline_form');
	var empty_row = inline_form.find('.empty_row');
	var new_row = empty_row.clone().removeClass('empty_row');
	empty_row.before(new_row);
	new_row.addClass('new');
	new_row.show();
	updateInlineFormIndices(inline_form);
	initDatepicker();
}

function removeInlineForm(remove_link) {
	var inline_form = $(remove_link).closest('fieldset').find('.inline_form');
	var removed_row = $(remove_link).closest('tr');
	if(removed_row.hasClass('new')) {
		removed_row.remove();
		updateInlineFormIndices(inline_form);
	} else {
		removed_row.hide();
		$('input.delete', removed_row).val(1);		
	}
}

function updateInlineFormIndices(inline_form) {
	var total_forms_field = $(inline_form).closest('fieldset').find('input[name$="-TOTAL_FORMS"]').first();
	var regexp = /(.+)-TOTAL_FORMS$/;
	var prefix = regexp.exec(total_forms_field.attr('name'));
	var rows = $('tbody tr', inline_form);
	total_forms_field.val(rows.length);
	rows.each(function(index, row) {
		updateInlineFormRowIndices(row,prefix[1],index);
	});
}

function updateInlineFormRowIndices(tr, prefix, index) {
	var id_regex = new RegExp('(' + prefix + '-\\d+)');
	var replacement = prefix + '-' + index;
	$(tr).find('input,select,textarea,label').each(function() {
		if($(this).attr("for")) {
			$(this).attr("for", $(this).attr("for").replace(id_regex, replacement));
		}
		if(this.id) {
			this.id = this.id.replace(id_regex, replacement);
		}
		if(this.name) {
			this.name = this.name.replace(id_regex, replacement);
		}
	});
}

// Update Management Type fields
function updateManagementType(field) {
	var details = $(field).closest('tr').find('.management_detail');
	$('.detail', details).hide();
	var comments = $(field).closest('tr').find('.management_comments');
	$('span', comments).hide();
	var type = $('option:selected', field).text();
	switch(type) {
		case 'Surgery':
			$('.surgery', details).show();
			$('span', comments).show();
			$('.complication select', details).val('');
			break;
		case 'Complication':
			$('.complication', details).show();
			$('span', comments).show();
			$('.surgery select', details).val('');
			$('.adjuvant select', details).val('');
			$('.stage select', details).val('');
			break;
		default:
			$('.complication select', details).val('');
			$('select', details).val('');
			$('textarea', comments).val('');
	}
	
}

// Update Management Surgery fields
function updateManagementSurgery(field) {
	var adjuvant_field = $(field).closest('td').find('.adjuvant');
	var stage_field = $(field).closest('td').find('.stage');
	var surgery_id = $('option:selected', field).val();
	if(management_surgery_adjuvant_map[surgery_id] == 'True') {
		$(adjuvant_field).show();
	} else {
		$(adjuvant_field).hide();
		$('select', adjuvant_field).val('');
	}
	if(management_surgery_stage_map[surgery_id] == 'True') {
		$(stage_field).show();
	} else {
		$(stage_field).hide();
		$('select', stage_field).val('');
	}
}

function updateOutcomeIOP(field) {
	var agents_field = $(field).closest('td').find('.iop_agent');
	var iop_control = $(field).val();
	if(iop_control == 'True') {
		$(agents_field).show();
	} else {
		$(agents_field).hide();
		$('select', agents_field).val('');
	}
}

function initDatepicker() {
	$(".datepicker").each(function() {
		$(this).removeClass('hasDatepicker');
		$(this).datepicker({
			changeMonth : true,
			changeYear : true,
			dateFormat : 'dd/mm/yy',
		});
	});
	$(".datepicker.past").datepicker("option", "maxDate", "+0D");
	$(".datepicker.past").datepicker("option", "yearRange", "-100:+0");
}

function updateElementIndex(el, prefix, ndx) {
	var id_regex = new RegExp('(' + prefix + '-\\d+)');
	var replacement = prefix + '-' + ndx;
	if ($(el).attr("for"))
		$(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
	if (el.id)
		el.id = el.id.replace(id_regex, replacement);
	if (el.name)
		el.name = el.name.replace(id_regex, replacement);
}

function wizardAddForm(btn) {
	var prefix = $(btn).closest('form').find('input[name="patient_wizard-current_step"]').val();
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	var row = $('.formset ul:first').clone(false).get(0);
	$(row).insertAfter($('.formset ul:last')).removeClass('hidden');
	$(row).children().not(':last').children().each(function() {
		updateElementIndex(this, prefix, formCount);
		$(this).val('');
	});
	$(row).find('.delete-row').click(function() {
		wizardDeleteForm(this, prefix);
	});
	$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
	initDatepicker();
	return false;
}

function wizardDeleteForm(btn) {
	var prefix = $(btn).closest('form').find('input[name="patient_wizard-current_step"]').val();
	$(btn).closest('ul').remove();
	var forms = $('.formset ul');
	$('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
	for ( var i = 0, formCount = forms.length; i < formCount; i++) {
		$(forms.get(i)).children().not(':last').children().each(function() {
			updateElementIndex(this, prefix, i);
		});
	}
	return false;
}

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
	"title-numeric-pre": function(a) {
		var x = a.match(/title="*(-?[0-9\.]+)/)[1];
		return parseFloat( x );
	},
	"title-numeric-asc": function(a, b) {
		return ((a < b) ? -1 : ((a > b) ? 1 : 0));
	},
	"title-numeric-desc": function(a, b) {
		return ((a < b) ? 1 : ((a > b) ? -1 : 0));
	}
});
