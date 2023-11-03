$(document).ready(function () {
    // Initialize an empty list to store selected constraints
    let selectedConstraints = [];

    // Initialize lists to store user-generated restrictions and blocked times
    let userBlockedTimes = [];

    // Initialize drag-and-drop for rows using dragula
    const rowContainer = document.querySelector('#class-table-body'); // Replace with your table body's ID
    const rowDragula = dragula([rowContainer]);

    rowDragula.on('drag', (el) => {
        // Add the 'dragging' class to the dragged element
        el.classList.add('dragging');
    });
    

    rowDragula.on('drop', (el, target, source, sibling) => {
        const sectionTitle = el.dataset.sectionTitle;

        // Handle the drop event here
        // Example: You can add a tag to the "Restrictions" field
        const restrictionsField = $(el).find('.tagify')[0];
        const tagify = new Tagify(restrictionsField, {
            // Configure Tagify as needed
        });
        tagify.addTags([sectionTitle]);

        // Update user-generated restrictions
        userBlockedTimes.push(sectionTitle);
    });

    // Initialize Select2 for the multi-select dropdowns with the .blocked-times-select class
    $('.blocked-times-select').select2({ width: '300px' });

    // Handle changes in any of the multi-select dropdowns
    $('.blocked-times-select').on('change', function () {
        const selectedTimeslots = $(this).val();

        // Update user-selected blocked times
        userBlockedTimes = selectedTimeslots || [];

        // Log the selected timeslots (you can remove this)
        console.log('Selected Timeslots:', userBlockedTimes);
    });


    // Handle the "Apply Constraints & Optimize" button click event
    $('#apply-constraints').on('click', function () {
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
