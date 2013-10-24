if (typeof django == "undefined") {
    var django = {
        "jQuery": $.noConflict()
    };
};

var bitFields = function() {
	return {
		toggleBit: function(field_id, mask, bit) {
			var field = django.jQuery(field_id);
			var val = parseInt(field.val(), 10) ^ parseInt(mask, 10);
			django.jQuery(field).val(val);
			django.jQuery(bit).toggleClass('on');
		},
		setButtons: function(field_id, value) {
			var intval = parseInt(value, 10);
			console.dir(django.jQuery(field_id).find("[data-value='1']"));
			if (intval & 1) {
				django.jQuery(field_id).find("[data-value='1']").addClass('on');
			} else {
				django.jQuery(field_id).find("[data-value='1']").removeClass('on');
			}
			if (intval & 2) {
				django.jQuery(field_id).find("[data-value='2']").addClass('on');
			} else {
				django.jQuery(field_id).find("[data-value='2']").removeClass('on');
			}
			if (intval & 4) {
				django.jQuery(field_id).find("[data-value='4']").addClass('on');
			} else {
				django.jQuery(field_id).find("[data-value='4']").removeClass('on');
			}
			if (intval & 8) {
				django.jQuery(field_id).find("[data-value='8']").addClass('on');
			} else {
				django.jQuery(field_id).find("[data-value='8']").removeClass('on');
			}
			if (intval & 16) {
				django.jQuery(field_id).find("[data-value='16']").addClass('on');
			} else {
				django.jQuery(field_id).find("[data-value='16']").removeClass('on');
			}
		},
		init: function() {
		    var bitfields = document.getElementsByClassName('vBitField');
		    for (var i = 0; i<bitfields.length; i++){
		        bitFields.setButtons('#'+bitfields[i].id, bitfields[i].value);
		    }
		}
	};
}();
django.jQuery().ready(bitFields.init);