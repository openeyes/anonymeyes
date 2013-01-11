$(function() {
	initDatepicker();

	$('.formset .add-row').click(function() {
		return addForm(this);
	});
	$('.formset .delete-row').click(function() {
		return deleteForm(this);
	})

	$('form .management_type select').each(function() {
		updateManagementType(this);
	});
	
	$('form .management_type select').change(function() {
		updateManagementType(this);		
	});
	
	$('form .management_detail .surgery select').each(function() {
		updateManagementSurgery(this);
	});
	
	$('form .management_detail .surgery select').change(function() {
		updateManagementSurgery(this);		
	});

});

function updateManagementType(field) {
	var details = $(field).closest('tr').find('.management_detail');
	$('.detail', details).hide();
	var type = $('option:selected', field).text();
	switch(type) {
		case 'Surgery':
			$('.surgery', details).show();
			$('.complication select', details).val('');
			break;
		case 'Complication':
			$('.complication', details).show();
			$('.surgery select', details).val('');
			$('.adjuvant select', details).val('');
			break;
		default:
			$('.complication select', details).val('');
			$('.surgery select', details).val('');
			$('.adjuvant select', details).val('');
	}
	
}

function updateManagementSurgery(field) {
	var adjuvant_field = $(field).closest('td').find('.adjuvant');
	$(adjuvant_field).hide();
	var surgery_id = $('option:selected', field).val();
	if(management_surgery_adjuvant_map[surgery_id] == 'True') {
		$(adjuvant_field).show();
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

function addForm(btn) {
	var prefix = $(btn).closest('form').find('input[name="patient_wizard-current_step"]').val();
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	var row = $('.formset ul:first').clone(false).get(0);
	$(row).insertAfter($('.formset ul:last')).removeClass('hidden');
	$(row).children().not(':last').children().each(function() {
		updateElementIndex(this, prefix, formCount);
		$(this).val('');
	});
	$(row).find('.delete-row').click(function() {
		deleteForm(this, prefix);
	});
	$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
	initDatepicker();
	return false;
}

function deleteForm(btn) {
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
