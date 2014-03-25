this.ckan.module('custodianpicker-module', function($, _) {
    return {
        initialize: function() {

            // Add hidden <input> tag #ext_cust_id if it doesn't already exist.
            var form = $(".search-form");
            if ($("#ext_cust_id").length === 0) {
                $('<input type="hidden" id="ext_cust_id" name="ext_cust_id" />').appendTo(form);
            }

            var ext_cust_id = null

            //Display custodian search param after search ?
            if(getURLParameter("ext_cust_id")) {
                ext_cust_id = getURLParameter("ext_cust_id");
                $('#ext_cust_id').val(ext_cust_id);
                $('#ext_cust_after').text(ext_cust_id);
            }

            //Initialise selectlist with url param ext_cust_id
            if(ext_cust_id)
            {
                //Initialise dropdown
                $('#cust_id option[user="ext_cust_id"]')

                //$('#cust_id option:eq(ext_cust_id)).attr('selected', "selected")
            }

            //Event listener for when a user is selected from the list
            $("#cust_id").on('change', function () {

                    $('#ext_cust_id').val($(this).attr('value'));

                    // Submit the <form id="dataset-search">.
                    $(".search-form").submit();
                })

            // Returns url parameter of given name (if it exists)
            function getURLParameter(name) {
                return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
            }

        }
    }
});
