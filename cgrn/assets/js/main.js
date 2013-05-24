var asInitVals = new Array();

$(document).ready(function() {
	
	$('.header-banner').waypoint('sticky');
	
	// Print
	$('.print_page').click(function(e) {
		window.print();
		e.preventDefault();
	});
	
	// Autosize
	$('.autosize').autosize();
	
	// Show DOB day/month fields if they contain data
	$('form .dob #id_dob_day').each(function() {
		if($(this).val() != '') {
			$(this).parent().show();
		}
	});
	$('form .dob #id_dob_month').each(function() {
		if($(this).val() != '') {
			$(this).parent().show();
		}
	});
	
	// Visual Acuity scale changes
	$('.visualacuityscale').each(function() {
		if($('option', this).length <= 2) {
			$(this).closest('.visualacuityscalewrapper').hide();
		}
	});
	$('body').delegate('.visualacuitymethod', 'change', function() {
		updateVisualAcuityScales(this);
	});
	$('body').delegate('.visualacuityscale', 'change', function() {
		updateVisualAcuityReadings(this);
	});
	
	// Visual Acuity not recorded
	$('.visualacuity').each(function() {
		updateCorrection(this);
	});
	$('body').delegate('.visualacuity', 'change', function() {
		updateCorrection(this)
	});
	
	// Diagnosis cascade
	$('.diagnosisgroup').each(function() {
		updateDiagnosis(this);
	});
	$('body').delegate('.diagnosisgroup', 'change', function() {
		updateDiagnosis(this)
	});
	
	// Ethnic group
	updateEthnicGroupComment();
	$('#id_ethnic_group').change(function() {
		updateEthnicGroupComment()
	});
	
	// History
	updateHistoryComment();
	$('#id_history').change(function() {
		updateHistoryComment()
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

	// Lens status and extraction date dependency
	$("form select[name^='lens_status_']").each(function() {
		updateExtractionDate(this);
	});
	$("form select[name^='lens_status_']").change(function() {
		updateExtractionDate(this);
	});
	
	// No IOP Agents
	$('.iopagents input').change(function() {
		var wrapper = $(this).closest('.iopagents');
		if($(this).val() == 1 && $(this).is(':checked')) {
			$('input:not([value="1"])', wrapper).prop('checked', false);
		} else if($(this).val() != 1 && $(this).is(':checked')) {
			$('input[value="1"]', wrapper).prop('checked', false);
		} else if($(this).val() != 1 && $(this).is(':not(:checked)')) {
			if($('input:checked', wrapper).length == 0) {
				$('input[value=1]', wrapper).prop('checked', true);
			}
		}
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

function updateVisualAcuityScales(element) {
	var wrapper = $(element).closest('fieldset, tr');
	var method_id = $(element).val();
	var empty_option = $('select.visualacuityscale option[value=""]', wrapper).first();
	if(method_id) {
		$.ajax({
			url: '/anonymeyes/visualacuityscales/'+method_id+'/',
			success: function(data) {
				var scale_field = $('select.visualacuityscale', wrapper);
				scale_field.html(empty_option.clone()).append(data);
				scale_field.val('');
				if($('select.visualacuityscale option', wrapper).length == 2) {
					$('.visualacuityscalewrapper', wrapper).hide();
					scale_field.val($('option[value!=""]:first', scale_field).val());
					scale_field.trigger('change');
				} else {
					$('.visualacuityscalewrapper', wrapper).show();
				}
			},
		});
	} else {
		$('select.visualacuityscale', wrapper).html(empty_option.clone());
		$('select.visualacuityscale', wrapper).val('');
		$('.visualacuityscalewrapper', wrapper).hide();
	}
}

function updateVisualAcuityReadings(element) {
	var wrapper = $(element).closest('fieldset, tr');
	var scale_id = $(element).val();
	var empty_option = $('select.visualacuity option[value=""]', wrapper).first();
	if(scale_id) {
		$.ajax({
			url: '/anonymeyes/visualacuityreadings/'+scale_id+'/',
			success: function(data) {
				$('select.visualacuity', wrapper).html(empty_option.clone()).append(data);
				$('select.visualacuity', wrapper).val('');
			},
		});
	} else {
		$('select.visualacuity', wrapper).html(empty_option.clone());
		$('select.visualacuity', wrapper).val('');
	}	
}

function updateCorrection(element) {
	var correction_wrapper = $(element).closest('li').find('.correctionwrapper');
	var fixation_wrapper = null;
	if(correction_wrapper.hasClass('both')) {
		fixation_wrapper = $(element).closest('fieldset,tr').find('.fixationwrapper');
	}
	if(!$(element).val() || $('option:selected', element).text() == 'Not recorded') {
		$('select', correction_wrapper).val('');
		correction_wrapper.hide();
		if(fixation_wrapper) {
			$('select', fixation_wrapper).val('');
			fixation_wrapper.hide();
		}
	} else {
		correction_wrapper.show();
		if(fixation_wrapper) {
			fixation_wrapper.show();
		}
	}
}

function updateHistoryComment() {
	var history = $('#id_history option:selected').text().toLowerCase();
	if(history == 'yes') {
		$('#id_history_comment').show();
	} else {
		$('#id_history_comment').hide();
		$('#id_history_comment').val('');
	}
}

function updateEthnicGroupComment() {
	var ethnic_group = $('#id_ethnic_group option:selected').text().toLowerCase();
	if(ethnic_group.indexOf('other') != -1 || ethnic_group.indexOf('mixed') != -1) {
		$('#id_ethnic_group_comment').show();
	} else {
		$('#id_ethnic_group_comment').hide();
		$('#id_ethnic_group_comment').val('');
	}
}

function updateDiagnosis(element) {
	var wrapper = $(element).closest('li');
	var side = $(element).attr('data-side');
	var diagnosis_field = $('.diagnosis[data-side="'+side+'"]', wrapper).first();
	var diagnosis_comment_field = $('.diagnosis_comment', wrapper).first();
	var diagnosis_group_text = $('option:selected', element).text();
	var empty_option = $('<option value="">---------</option>');
	if($(element).val()) {
		$.ajax({
			url: '/anonymeyes/diagnoses/'+$(element).val()+'/',
			success: function(data) {
				if(data.length == 1) {
					// Single result, so we'll use a hidden field
					var new_diagnosis_field = $('<input type="hidden" class="diagnosis" />');
					new_diagnosis_field.attr('id', diagnosis_field.attr('id'))
						.attr('name', diagnosis_field.attr('name'))
						.attr('data-side', side)
						.attr('value', data[0].pk);
					$(diagnosis_field).replaceWith(new_diagnosis_field);
				} else {
					// More than one result so we need a dropdown
					var new_diagnosis_field = $('<select class="diagnosis" />');
					var new_value = null;
					new_diagnosis_field.attr('id', diagnosis_field.attr('id'))
						.attr('name', diagnosis_field.attr('name'))
						.attr('data-side', side)
						.append(empty_option);
					$(data).each(function() {
						new_diagnosis_field.append($('<option value="'+this.pk+'">'+this.fields.name+'</option>'));
						if(diagnosis_field.val() == this.pk) {
							new_value = this.pk;
						}
					});
					new_diagnosis_field.val(new_value);
					$(diagnosis_field).replaceWith(new_diagnosis_field);
				}
				$(diagnosis_field).show();
				
				if(diagnosis_group_text == 'Other' || diagnosis_group_text == 'Unknown') {
					$(diagnosis_comment_field).show();
				} else {
					$(diagnosis_comment_field).val('');
					$(diagnosis_comment_field).hide();
				}
			},
		});
	} else {
		$(diagnosis_field).html(empty_option);
		$(diagnosis_field).val('');
		$(diagnosis_field).hide();
		$(diagnosis_comment_field).val('');
		$(diagnosis_comment_field).hide();
	}
}

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
	$('textarea', comments).hide();
	var type = $('option:selected', field).text();
	switch(type) {
		case 'Surgery':
			$('.complication select', details).val('');
			$('.surgery', details).show();
			$('.agents select', details).val('');
			$('textarea', comments).show();
			break;
		case 'Complication':
			$('.complication', details).show();
			$('.surgery select', details).val('');
			$('.adjuvant select', details).val('');
			$('.stage select', details).val('');
			$('.agents select', details).val('');
			$('textarea', comments).show();
			break;
		case 'Medication':
			$('.complication select', details).val('');
			$('.surgery select', details).val('');
			$('.adjuvant select', details).val('');
			$('.stage select', details).val('');
			$('.agents', details).show();
			$('textarea', comments).val('');
			break;
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

function initDatepicker() {
	$(".datepicker").each(function() {
		$(this).removeClass('hasDatepicker');
		$(this).datepicker({
			changeMonth : true,
			changeYear : true,
			dateFormat : 'yy-mm-dd',
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
