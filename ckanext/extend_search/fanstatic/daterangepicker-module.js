this.ckan.module('daterangepicker-module', function ($, _) {
    return {
        initialize: function() {

            // Add hidden <input> tags #ext_startdate and #ext_enddate,
            // if they don't already exist.
            var form = $(".search-form");
            if ($("#ext_startdate").length === 0) {
                $('<input type="hidden" id="ext_startdate" name="ext_startdate" />').appendTo(form);
            }
            if ($("#ext_enddate").length === 0) {
                $('<input type="hidden" id="ext_enddate" name="ext_enddate" />').appendTo(form);
            }

            // Get the start/end date search parameters and convert to Dates
            // Also populate the search facets for start/end date if we need to
            var ext_startdate = null;
            var ext_enddate = null;

            if(getURLParameter("ext_startdate")) {
                ext_startdate = new Date(getURLParameter("ext_startdate"));

                //Convert to ISO string (for resubmission to solr)
                var iso_start = ext_startdate.toISOString();
                $('#ext_startdate').val(iso_start);

                //Convert to Date string (for display purposes)
                var startDateString = ext_startdate.toDateString();
                $('#ext_startdate_after').text(startDateString);
            }
            if(getURLParameter("ext_enddate")) {
                ext_enddate = new Date(getURLParameter("ext_enddate"));

                //Convert to ISO string (for resubmission to solr)
                var iso_end = ext_enddate.toISOString();
                $('#ext_enddate').val(iso_end);

                //Convert to Date string (for display purposes)
                var endDateString = ext_enddate.toDateString();
                $('#ext_enddate_after').text(endDateString);
            }

            //Initialise the daterange picker textbox with the previously searched daterange
            if(ext_startdate && ext_enddate)
            {
                var startDateString = ext_startdate.toDateString();
                var endDateString = ext_enddate.toDateString();
                $('#daterange').val(startDateString + ' - ' + endDateString);
            }


            // Add a date-range picker widget to the <input> with id #daterange
           $('input[id="daterange"]').daterangepicker({
                ranges: {
                   'Today': [moment().startOf('day'), moment().endOf('day')],
                   'Yesterday': [moment().startOf('day').subtract('days', 1), moment().endOf('day').subtract('days', 1)],
                   'Last 7 Days': [moment().startOf('day').subtract('days', 6), moment().endOf('day')],
                   'Last 30 Days': [moment().startOf('day').subtract('days', 29), moment().endOf('day')],
                   'This Month': [moment().startOf('month'), moment().endOf('month')],
                   'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')],
                   'Last Year': [moment().subtract('year', 1).startOf('year'), moment().subtract('year', 1).endOf('year')]
                },
                startDate: moment().startOf('day'),
                endDate: moment().startOf('day'),
                showDropdowns: true,
                timePicker: true
            },
            function(start, end) {
                // Bootstrap-daterangepicker calls this function after the user
                // picks a start and end date.
                $('#daterange').val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

                // that Solr understands.
                start = start.format('YYYY-MM-DDTHH:mm:ss') + 'Z';
                end = end.format('YYYY-MM-DDTHH:mm:ss') + 'Z';

                // Set the value of the hidden <input id="ext_startdate"> to
                // the chosen start date.
                $('#ext_startdate').val(start);

                // Set the value of the hidden <input id="ext_enddate"> to
                // the chosen end date.
                $('#ext_enddate').val(end);

                // Submit the <form id="dataset-search">.
                $(".search-form").submit();
            });


            // Returns url parameter of given name (if it exists)
            function getURLParameter(name) {
                return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
            }

        }
    }
});
