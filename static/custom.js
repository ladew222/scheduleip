$(document).ready(function () {
    // Initialize an empty list to store selected constraints
    const selectedConstraints = [];
    
    // Initialize an object to store user changes
    const userChanges = {};

    // Make the table rows draggable
    $('.draggable-row').draggable({
        helper: 'clone',  // Clone the row when dragging
        opacity: 0.5,     // Set the opacity of the dragged row
        revert: 'invalid', // Revert if not dropped in a valid target
    });

    // Handle the "Move" button click event
    $('.move-class').on('click', function () {
        // Get the class ID and new time slot from the clicked row
        const classId = $(this).closest('.class-row').data('class-id');
        const newTimeSlot = '';  // Set the new time slot here

        // Store the user change in the userChanges object
        userChanges[classId] = newTimeSlot;

        // Remove the row from the table
        $(this).closest('.class-row').remove();
    });

    // Handle the "Hard Constraint" button click event
    $('.hard-constraint').on('click', function () {
        // Get the class ID from the clicked row
        const classId = $(this).closest('.class-row').data('class-id');

        // Add the class ID to the selectedConstraints list with the "Hard Constraint" action
        selectedConstraints.push({ id: classId, action: 'Hard Constraint' });

        // Remove the row from the table
        $(this).closest('.class-row').remove();
    });

    // Handle the "Apply Constraints & Optimize" button click event
    $('#apply-constraints').on('click', function () {
        // Send the selected constraints and user changes to the server for processing
        const requestData = {
            constraints: selectedConstraints,
            userChanges: userChanges,
        };

        $.ajax({
            type: 'POST',
            url: '/optimize', // Replace with your endpoint for optimization
            data: JSON.stringify(requestData),
            contentType: 'application/json',
            success: function (response) {
                // Handle the optimization results
                // You can display the results on the page or perform any other actions
                console.log(response);
            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    });
});
