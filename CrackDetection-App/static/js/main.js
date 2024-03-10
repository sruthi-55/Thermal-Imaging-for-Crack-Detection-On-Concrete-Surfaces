$(document).ready(function () {
    // Init
    image_paths = []
    $('.image-section').hide();
    $('.loader').hide();
    // $('.resClass').hide();
    //$('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').hide();
        $('#resClass').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Set a timeout for 1 minute (60000 milliseconds)
        setTimeout(function () {
            // Continue with the rest of the code after 1 minute
            // Make prediction by calling api /predict
            $.ajax({
                type: 'POST',
                url: '/predict',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: true,
                success: function (data) {
                    $('.loader').hide();

                    // Check if data and data.image_paths are defined
                    if (data && data.image_paths) {
                        // Clear existing result images
                        $('#result').empty();
                        $('#resClass').empty();
                        // Display the result images
                        for (var i = 0; i < data.image_paths.length; i++) {
                            // Append each image to the result div
                            $('#result').append('<img src="' + data.image_paths[i] + '" alt="Result Image ' + i + '">');
                        }
                        $('#resClass').append(data.result_class + " found");
                        $('#result').show();
                        $('#resClass').show();
                    } else {
                        console.error("Invalid response data:", data);
                    }
                },
                error: function (error) {
                    console.error("Error processing image:", error);
                }
            });
            $('#result').show();
            $('#resClass').show();
        }, 15000); 
    });
});
