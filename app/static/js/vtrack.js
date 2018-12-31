/* app/static/js/vtrack.js */

// function to reset fields and launch the modal form
var addVehicle = function () {
    $('input[name=vid]').val("");
    $('#vin').val("");
    $('#tag').val("");
    $('#year').val("");
    $('#make').val("");
    $('#model').val("");

    // trigger the modal
    $('#modal-vehicles-form').modal('show');
};


$(document).ready(function () {

    // function to get data from the database and populate modal form fields
    $(function () {
        $('.editVehicle').click(function () {
            // save the record id
            var vehicle_id = $(this).data('id');
            $.ajax({
                url: '/vehicles/getVehicleById',
                data: { id: vehicle_id },
                type: 'POST',
                success: function (response) {
                    // populate the modal form fields
                    if (vehicle_id != "") {
                        $('input[name=vid]').val(response.id);
                        $('#vin').val(response.vin);
                        $('#tag').val(response.tag);
                        $('#year').val(response.year);
                        $('#make').val(response.make);
                        $('#model').val(response.model);
                    }
                    // trigger the modal
                    $('#modal-vehicles-form').modal('show');
                },
                error: function (error) {
                    alert(error);
                }
            });
        });
    });

});