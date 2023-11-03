const tagifyInstances = {};
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
    rowDragula.on('dragend', (el) => {
        // Remove the 'dragging' class from the dragged element
        el.classList.remove('dragging');
    });
    rowDragula.on('dragenter', (el, target, source, sibling) => {
        // Add the 'target-row' class to the potential drop target row
        target.classList.add('target-row');
    });
    
    rowDragula.on('dragleave', (el, target, source, sibling) => {
        // Remove the 'target-row' class from the previous target row when leaving
        target.classList.remove('target-row');
    });

    
    // Initialize Tagify for all rows with the '.tagify' class
    $('.tagify').each(function() {
        const rowId = $(this).closest('tr').attr('id'); // Get the row's ID
        tagifyInstances[rowId] = new Tagify(this, {
            // Configure Tagify as needed
        });
    });

    // Function to handle updates to the data-tags attribute
    function updateDataTags(el) {
        const sectionTitle = el.dataset.sectionTitle;
        const tagify = el.tagify; // Get the Tagify instance

        // Get the current tags in the input
        const currentTags = tagify.value.map(tag => tag.value);

        // Check if the sectionTitle is in the current tags
        if (!currentTags.includes(sectionTitle)) {
            // Add the sectionTitle as a tag
            tagify.addTags([sectionTitle]);

            // Update the data-tags attribute for the row
            const rowDataTags = $(el).data('tags') || [];
            rowDataTags.push(sectionTitle);
            $(el).data('tags', rowDataTags);
        }
    }

    // Handle changes to Tagify inputs (manual tag additions)
    $('.tagify-input').on('change', function () {
        updateDataTags(this);
    });

    rowDragula.on('drop', (el, target, source, sibling) => {
        const sectionTitle = el.dataset.sectionTitle;
    
        // Handle the drop event here
        // Example: You can add a tag to the "Restrictions" field
        const restrictionsField = $(el).find('.tagify')[0];
        const tagify = new Tagify(restrictionsField, {
            // Configure Tagify as needed
        });
    
        // Check if a tag with the same sectionTitle already exists
        const existingTags = tagify.value.map(tag => tag.value);
        if (!existingTags.includes(sectionTitle)) {
            // Add the sectionTitle as a tag only if it doesn't exist
            tagify.addTags([sectionTitle]);
    
            // Update the data-tags attribute for the row
            const rowDataTags = $(el).data('tags') || [];
            rowDataTags.push(sectionTitle);
            $(el).data('tags', rowDataTags);
        }
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


    $('#apply-constraints').on('click', function () {
        // Gather the data from the table
        const classData = [];
        $('#class-table-body tr').each(function () {
            const rowDataTags = $(this).data('tags') || []; // Retrieve the tags from data-tags attribute
    
            const rowData = {
                term: $(this).find('td:eq(0)').text(),
                section: $(this).find('td:eq(1)').text(),
                title: $(this).find('td:eq(2)').text(),
                location: $(this).find('td:eq(3)').text(),
                meetingInfo: $(this).find('td:eq(4)').text(),
                faculty: $(this).find('td:eq(5)').text(),
                availableCapacity: $(this).find('td:eq(6)').text(),
                status: $(this).find('td:eq(7)').text(),
                credits: $(this).find('td:eq(8)').text(),
                academicLevel: $(this).find('td:eq(9)').text(),
                restrictions: rowDataTags, // Use the retrieved tags
                blockedTimeSlots: $(this).find('td:eq(11) select').val() || [],
            };
            classData.push(rowData);
        });
    
        // Send the data to the server for optimization
        const requestData = {
            classData: classData,
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
