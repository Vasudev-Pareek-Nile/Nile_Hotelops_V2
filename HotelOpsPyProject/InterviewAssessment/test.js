
    <script>
        $(document).ready(function() {
            // Set AID in hidden fields when opening the modal
            $('.button-group').on('click', '.btn', function() {
                var $buttonGroup = $(this).closest('.button-group'); // Get the closest button group
                var AID = $buttonGroup.find('.aid-hidden').val(); // Find the associated AID
                var OID = $buttonGroup.find('.oid-hidden').val(); // Find the associated AID

        
                // Determine which button was clicked
                if ($(this).attr('id') === 'approveBtn') {
                    $('#approveAID').val(AID);
                    $('#approveOID').val(OID);

                    $('#approveModal').css('display', 'block');
                } else if ($(this).attr('id') === 'holdBtn') {
                    $('#holdAID').val(AID);
                    $('#holdOID').val(OID);

                    
                    $('#holdModal').css('display', 'block');
                } else if ($(this).attr('id') === 'rejectBtn') {
                    $('#rejectAID').val(AID);
                    $('#rejectOID').val(OID);

                    $('#rejectModal').css('display', 'block');
                }
            });
        
            // Close modals
            $('.close, .btn-secondary').on('click', function() {
                $('.modal').css('display', 'none');
            });
        
            // AJAX call for Approve
            $('#approveSubmitBtn').on('click', function() {
                var remarks = $('#approveRemarks').val();
                var AID = $('#approveAID').val();
                var OID = $('#approveOID').val();

                if (!remarks) {
                    alert('Please provide remarks.');
                    return;
                }
                $.ajax({
                    url: "/InterviewAssessment/InterviewAssementCEO/",
                    type: 'GET',
                    data: {
                        'AID': AID,
                        'OID':OID,
                        'Status': 'Approved',
                        'Remarks': remarks
                    },
                    success: function(response) {
                        alert(response.message);
                        $('#approveModal').css('display', 'none');
                        location.reload();  // Refresh the page
                    },
                    error: function(xhr, status, error) {
                        alert('An error occurred: ' + error);
                    }
                });
            });
        
            // AJAX call for Hold
            $('#holdSubmitBtn').on('click', function() {
                var remarks = $('#holdRemarks').val();
                var AID = $('#holdAID').val();
                var OID = $('#holdOID').val();


                if (!remarks) {
                    alert('Please provide remarks.');
                    return;
                }
                $.ajax({
                    url: "/InterviewAssessment/InterviewAssementCEO/",
                    type: 'GET',
                    data: {
                        'AID': AID,
                        'OID':OID,
                        
                        'Status': 'Hold',
                        'Remarks': remarks
                    },
                    success: function(response) {
                        alert(response.message);
                        $('#holdModal').css('display', 'none');
                        location.reload();  // Refresh the page
                    },
                    error: function(xhr, status, error) {
                        alert('An error occurred: ' + error);
                    }
                });
            });
        
            // AJAX call for Reject
            $('#rejectSubmitBtn').on('click', function() {
                var remarks = $('#rejectRemarks').val();
                var AID = $('#rejectAID').val();
                var OID = $('#rejectOID').val();


                if (!remarks) {
                    alert('Please provide remarks.');
                    return;
                }
                $.ajax({
                    url: "/InterviewAssessment/InterviewAssementCEO/",
                    type: 'GET',
                    data: {
                        'AID': AID,
                        'OID':OID,

                        'Status': 'Rejected',
                        'Remarks': remarks
                    },
                    success: function(response) {
                        alert(response.message);
                        $('#rejectModal').css('display', 'none');
                        location.reload();  // Refresh the page
                    },
                    error: function(xhr, status, error) {
                        alert('An error occurred: ' + error);
                    }
                });
            });
        });
        </script>
        <script>
            $(document).on('click', '.reject-btn', function (e) {
    e.preventDefault();

    const AID = $(this).data('aid');
    const OID = $(this).data('oid');

    $.ajax({
        url: "{% url 'RejectInterviewAssement' %}",
        type: "GET",
        data: {
            AID: AID,
            OID: OID
        },
        success: function (response) {
            alert(response.message); // Show success message
            location.reload(); // Refresh the page
        },
        error: function (xhr) {
            const response = JSON.parse(xhr.responseText);
            alert(response.message); // Show error message
            location.reload(); // Refresh the page
        }
    });
});

        </script>
        <script>
            $(document).ready(function () {
    // Handle the click event for the "Close Assessment" button
    $("#closeSubmitBtn").on("click", function () {
        // Retrieve the necessary data from the modal
        let AID = $("#closeAID").val();
        let OID = $("#closeOID").val();
        let remarks = $("#closeRemarks").val();

        // Validate the input data
        if (!AID || !OID || !remarks.trim()) {
            alert("Please fill in all required fields.");
            return;
        }

        // Send the AJAX POST request
        $.ajax({
            url: "InterviewAssement/CloseInterviewAssement/", // Replace with the actual URL
            method: "GET", // Should be GET as per your Django function
            data: {
                AID: AID,
                OID: OID
            },
            beforeSend: function () {
                // Optionally, you can show a loading spinner or disable the button here
                $("#closeSubmitBtn").prop("disabled", true).text("Closing...");
            },
            success: function (response) {
                if (response.message) {
                    alert(response.message); // Show success message
                }
                // Optionally, close the modal and refresh the page or table
                $("#closeInterviewModal").modal("hide");
                location.reload(); // Refresh the page
            },
            error: function (xhr) {
                // Handle errors
                let errorMessage = xhr.responseJSON?.message || "An error occurred.";
                alert(errorMessage);
            },
            complete: function () {
                // Re-enable the button
                $("#closeSubmitBtn").prop("disabled", false).text("Close Assessment");
            }
        });
    });
});

        </script>
