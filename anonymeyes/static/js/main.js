$(function() {
	$(".datepicker").datepicker({
		changeMonth : true,
		changeYear : true,
		dateFormat : 'dd/mm/yy',
	});
	$(".datepicker.past").datepicker("option", "maxDate", "+0D");
	$(".datepicker.past").datepicker("option", "yearRange", "-100:+0");

	$('.formset .add-row').click(function() {
		return addForm(this);
	});
	$('.formset .delete-row').click(function() {
		return deleteForm(this);
	})

});

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
	var row = $('.formset ul:first').clone(true).get(0);
	$(row).insertAfter($('.formset ul:last')).removeClass('hidden');
	$(row).children().not(':last').children().each(function() {
		updateElementIndex(this, prefix, formCount);
		$(this).val('');
	});
	$(row).find('.delete-row').click(function() {
		deleteForm(this, prefix);
	});
	$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
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
