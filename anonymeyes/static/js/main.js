$(function() {
	$(".datepicker").datepicker({
		changeMonth : true,
		changeYear : true,
		dateFormat: 'dd/mm/yy',
	});
	$(".datepicker.past").datepicker("option", "maxDate", "+0D");
});
