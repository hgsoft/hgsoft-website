(function() {
    "use strict";
    var website = openerp.website;
    var _t = openerp._t;
    var notification_msg = _t("Success : Product has been added to your shopping cart.");
	$(document).ready(function () {
		var url = window.location.href;
		if (url.search('added') > 0){
			$('.js_sale').prepend("<div id ='myAlert' class ='alert alert-danger' width='50%'><a href = '#' class = 'close' data-dismiss = 'alert'>&times;</a><strong><center>" + notification_msg + "</center></strong></div>");
		}
	});
})();
