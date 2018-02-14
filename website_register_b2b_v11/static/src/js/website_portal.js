
odoo.define('website_register_b2b_v11.index', function(require) {
    'use strict';
    
    
    $('#id_country').change(function() {
        alert("id_country ALTERADO")
        var vals = { country_id: $(this).val() };
        ajax.jsonRpc("/page/register/get_states", 'call', vals)
            .then(function(data) {
                var selected = $('#input_state_id').val();
                $('#select_state_id').find('option').remove().end();
                $('#select_state_id').append('<option value="">Estado...</option>');
                $.each(data, function(i, item) {
                    $('#select_state_id').append($('<option>', {
                        value: item[0],
                        text: item[1],
                        selected: item[0]==selected?true:false,
                    }));
                });
            });
    });
    
});
