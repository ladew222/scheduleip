$(document).ready(function () {
    // Initialize an empty list to store selected constraints
    let selectedConstraints = [];

    // Initialize lists to store user-generated restrictions and blocked times
    let userBlockedTimes = [];

    // Initialize Tagify for the "Restrictions" field
    const restrictionsField = document.querySelector('.tagify'); // Replace with the correct selector
    const tagify = new Tagify(restrictionsField, {
        // Configure Tagify as needed
    });

    // Initialize drag-and-drop for rows using dragula
    const rowContainer = document.querySelector('#class-table-body'); // Replace with your table body's ID
    const rowDragula = dragula([rowContainer]);

    rowDragula.on('drop', (el, target, source, sibling) => {
        const sectionTitle = el.dataset.sectionTitle;

        // Handle the drop event here
        // Example: You can add a tag to the "Restrictions" field using the Tagify instance
        tagify.addTags([sectionTitle]);

        // Update user-generated restrictions
        userBlockedTimes.push(sectionTitle);
    });

    // Handle the selection of blocked times
    $('#timeslot-list .ui-selected').on('click', function () {
        const selectedTime = $(this).text();

        // Toggle the selection and update the UI
        if ($(this).hasClass('blocked-time')) {
            $(this).removeClass('blocked-time');
            // Remove the time from the user-selected blocked times
            userBlockedTimes = userBlockedTimes.filter(time => time !== selectedTime);
        } else {
            $(this).addClass('blocked-time');
            // Add the time to the user-selected blocked times
            userBlockedTimes.push(selectedTime);
        }
    });

    // Handle the "Apply Constraints & Optimize" button click event
    $('#apply-constraints').on('click', function () {
        // Collect the selected timeslots
        const selectedTimeslots = $('#timeslot-list .ui-selected').map(function () {
            return $(this).text();
        }).get();

        // Send the user-selected blocked times to the server for processing
        const requestData = {
            userBlockedTimes: userBlockedTimes,
        };

        $.ajax({
            type: 'POST',
            url: '/optimize', // Replace with your endpoint for optimization
            data: JSON.stringify(requestData),
            contentType: 'application/json',
            success: function (response) {
                // Handle the optimization results
                // You can display the results on the page or perform any other actions
                console.log('Optimization successful:', response);
            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    });

    // Make the timeslot list selectable
    $('#timeslot-list').selectable();

    // Additional code for other interactions...
});
