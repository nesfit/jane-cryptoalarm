
require('./bootstrap');

var noty = require('noty');
noty.overrideDefaults({layout: 'topRight', timeout: 4000, theme: 'metroui', progressBar: false});

function disableOptions(select, cond, val) {
    $(select.options).filter(cond).prop('disabled', val);
}

$(document).ready(function() {
    $('input[name="address"]').blur(function() {
        var select = $('select[name="coin"]')[0];
        var val = $(this).val();

        // enable all options
        disableOptions(select, function(index, item) {return true;}, false);

        $.get('/api/identify', {address: val}, function(response) {
            if(!response.status) {
                new noty({text: 'Address of unknown format, please select manually', type: 'warning'}).show();
            } else if (response.coins) {
                // disable not matched options
                disableOptions(select, function(index, item) {return !response.coins.includes(item.text.toLowerCase());}, true);
                if(response.coins.length == 1) {
                    // select only available option
                    $(select.options).filter(':enabled').prop('selected', true);
                    new noty({text: 'Address identified as ' + response.coins[0], type: 'success'}).show();
                } else {
                    new noty({text: 'Address matches multiple coins, please select one manually', type: 'info'}).show();
                }
            }
        });
    });
});