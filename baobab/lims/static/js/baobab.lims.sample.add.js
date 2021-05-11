function BaobabSampleView() {

    var that = this;

    that.load = function () {
        // disable browser auto-complete
        $('input[type=text]').prop('autocomplete', 'off');

        $('#Project_uid').focus(function() {
            var uid = $(this).val();
            var element = $("#Kit");
            filterKitByProject(element, "getParentUID", uid);
        });

        $('input[type=submit]').on('click', function (event) {
            var path = window.location.href.split('/base_view')[0] + '/update_boxes';
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: path,
                data: {'locTitle': $('#StorageLocation').val()}
            }).done(function (data) {
                console.log(data);
            })
        })
        $('#archetypes-fieldname-GeoLocCountry').change(function() {
            var geo_loc_country = $('#GeoLocCountry');
            var dropdown = $('#GeoLocState');
            populate_dropdowns(dropdown, 'states', {'country': geo_loc_country.val()});
        });
        $('#archetypes-fieldname-GeoLocState').change(function() {
            var geo_loc_country = $('#GeoLocCountry');
            var geo_loc_state = $('#GeoLocState');
            var dropdown = $('#GeoLocDistrict');
            populate_dropdowns(
                dropdown, 'getDistricts',
                {'country': geo_loc_country.val(),
                 'state': geo_loc_state.val()});
        });

    };

    function filterKitByProject(element, filterKey, filterValue) {
        var query = $.parseJSON($(element).attr('base_query'));
        query[filterKey] = filterValue;
        var options = $.parseJSON($(element).attr('combogrid_options'));
        $(element).attr('base_query', $.toJSON(query));
        $(element).attr("combogrid_options", $.toJSON(options));
        //referencewidget_lookups($(element));

        options.url = window.location.href.split("/edit")[0] + "/" + options.url;
        options.url = options.url + "?_authenticator=" + $("input[name='_authenticator']").val();
        options.url = options.url + "&catalog_name=" + $(element).attr("catalog_name");
        options.url = options.url + "&base_query=" + $.toJSON(query);
        options.url = options.url + "&search_query=" + $(element).attr("search_query");
        options.url = options.url + "&colModel=" + $.toJSON($.parseJSON($(element).attr("combogrid_options")).colModel);
        options.url = options.url + "&search_fields=" + $.toJSON($.parseJSON($(element).attr("combogrid_options"))['search_fields']);
        options.url = options.url + "&discard_empty=" + $.toJSON($.parseJSON($(element).attr("combogrid_options"))['discard_empty']);
        options.force_all = "false";
        $(element).combogrid(options);
        $(element).attr("search_query", "{}");
    }

    function populate_dropdowns(dropdown, populate_type, data){
        var url_path = portal_url + '/ajax_get_' + populate_type;
        if (populate_type == 'getDistricts'){
            var url_path = portal_url + '/'+ populate_type;
        }

         $.ajax({
             dataType: "json",
             contentType: 'application/json',
             data: data,
             url: url_path,
             success: function (data) {
                 $(dropdown).empty();
                 $(dropdown).append($('<option>').val('').text(''));
                 $.each(data, function() {
                    $.each(this, function(key, value){
                        $(dropdown).append($('<option>').val(key).text(value));
                    });
                });
             },
             error: function (jqXHR, textStatus, errorThrown) {

             }
         });
    }
}
