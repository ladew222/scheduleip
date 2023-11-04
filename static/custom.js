const tagifyInstances = {};
$(document).ready(function () {


    $('.editable-cell').on('click', function () {
        const cell = $(this);
        const originalContent = cell.text().trim();

        // Create an input field with the original content
        const inputField = $('<input type="text">');
        inputField.val(originalContent);

        // Replace the cell's content with the input field
        cell.html(inputField);

        // Focus on the input field
        inputField.focus();

        // Add a blur event listener to save the edited content when the input field loses focus
        inputField.on('blur', function () {
            const editedContent = inputField.val().trim();

            // Validate the edited content format based on the cell's class
            if (cell.hasClass('days') && isValidDayFormat(editedContent)) {
                // Handle day format validation (e.g., MWF or TTh)
                cell.text(editedContent);
            } else if (cell.hasClass('time') && isValidTimeFormat(editedContent)) {
                // Handle time format validation (e.g., "09:05AM - 10:00AM")
                cell.text(editedContent);
            } else {
                // Display an error message and keep the input field for further editing
                inputField.addClass('error');
                inputField.val(originalContent);
                setTimeout(function () {
                    inputField.removeClass('error');
                }, 2000); // Remove error class after 2 seconds
            }
        });
    });

    // Function to validate day format
    function isValidDayFormat(dayString) {
        const dayRegex = /^(MWF|TTh)$/i; // Match "MWF" or "TTh" case-insensitively
        return dayRegex.test(dayString);
    }

    // Function to validate time format
    function isValidTimeFormat(timeString) {
        const timeRegex = /^(0?[1-9]|1[0-2]):[0-5][0-9][APap][Mm] - (0?[1-9]|1[0-2]):[0-5][0-9][APap][Mm]$/;
        return timeRegex.test(timeString);
    }
    function parseCSV(csvContent) {
        // Split the CSV content into lines
        const lines = csvContent.trim().split('\n');
        
        // Define an array to store the parsed data
        const parsedData = [];
        
        // Loop through each line
        for (const line of lines) {
            // Split the line into values based on commas
            const values = line.split(',');
            
            // Create an object for each row based on your data structure
            const rowData = {
                term: values[0],
                section: values[1],
                title: values[2],
                location: values[3],
                meetingInfo: values[4],
                faculty: values[5],
                availableCapacity: values[6],
                status: values[7],
                credits: values[8],
                academicLevel: values[9],
                restrictions: values.slice(10), // Assuming restrictions start from index 10
                blockedTimeSlots: [], // You can populate this based on your needs
            };
            
            // Push the rowData object to the parsedData array
            parsedData.push(rowData);
        }
        
        return parsedData;
    }
    
    
    function saveSchedule() {
        const classData = [];
        
        // Iterate over table rows and gather data
        $('#class-table-body tr').each(function () {
            const rowDataTags = $(this).data('tags') || [];
    
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
                restrictions: rowDataTags,
                blockedTimeSlots: $(this).find('td:eq(11) select').val() || [],
            };
            
            classData.push(rowData);
        });
        
        // Create a CSV representation of classData
        const csvData = classData.map(row => [
            row.term,
            row.section,
            row.title,
            row.location,
            row.meetingInfo,
            row.faculty,
            row.availableCapacity,
            row.status,
            row.credits,
            row.academicLevel,
            row.restrictions.join(', '), // Convert tags array to a comma-separated string
            row.blockedTimeSlots.join(', '), // Convert blockedTimeSlots array to a comma-separated string
        ].join(','));
    
        // Join rows with line breaks to form a CSV string
        const csvString = csvData.join('\n');
    
        // Create a Blob object for the CSV data
        const blob = new Blob([csvString], { type: 'text/csv' });
    
        // Create a download link
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'schedule.csv'; // Set the desired filename
    
        // Trigger a click event on the link to initiate the download
        link.click();
    }
    

    // Attach the saveSchedule function to the "Save Schedule" button click event
    $('#save-schedule').on('click', function () {
        saveSchedule();
    });

    

        
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

    // Add a click event listener to the "Load Schedule" button
    $('#load-schedule').on('click', function () {
        // Create a hidden file input element
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.csv'; // Set the accepted file type to CSV

        // Trigger the file input dialog
        fileInput.click();

        // Handle the selected file when the user chooses one
        fileInput.addEventListener('change', function () {
            const selectedFile = fileInput.files[0];
            if (selectedFile) {
                // Read the selected CSV file
                const reader = new FileReader();
                reader.onload = function (e) {
                    const csvData = e.target.result;
                    // Parse and process the CSV data (you can use a CSV parsing library)
                    // Here, you might call a function to populate the table with the loaded data
                    // For example: populateTableWithCSVData(csvData);
                };
                reader.readAsText(selectedFile);
            }
        });
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

     // Delegated event handler for manual tag additions
     $('#class-table-body').on('change', '.tagify-input', function () {
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
    // Add a change event listener to the file input element
    $('#file-input').on('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            // Read the contents of the selected file as text
            const reader = new FileReader();
            reader.onload = function (event) {
                const fileContent = event.target.result;
                // Parse the CSV content and populate the table
                const loadedData = parseCSV(fileContent);
                populateTable(loadedData);
            };
            reader.readAsText(file);
        }
    });

    // Trigger the file input click when the "Load Table" button is clicked
    $('#load-table-button').on('click', function () {
        $('#file-input').click();
    });
    // Function to populate the table with loaded data and update selected tags and multi-selects
    function populateTable(data) {
        // Clear existing table data (you may need to adjust this based on your table structure)
        $('#class-table-body').empty();

        // Create an object to store tagify instances for each row
        const tagifyInstances = {};

        // Populate the table with the loaded data
        for (const rowData of data) {
            const row = $('<tr>');

            // Assuming you have a specific order of columns in your table
            row.append($('<td>').text(rowData.term));
            row.append($('<td>').text(rowData.section));
            row.append($('<td>').text(rowData.title));
            row.append($('<td>').text(rowData.location));
            row.append($('<td>').text(rowData.meetingInfo));
            row.append($('<td>').text(rowData.faculty));
            row.append($('<td>').text(rowData.availableCapacity));
            row.append($('<td>').text(rowData.status));
            row.append($('<td>').text(rowData.credits));
            row.append($('<td>').text(rowData.academicLevel));

            // Create a cell for tags
            const tagsCell = $('<td>');

            // Create an input element for tags and initialize it with the data
            const tagsInput = $('<input>').attr('type', 'text').addClass('tagify');
            tagsInput.val(rowData.restrictions.join(', ')); // Assuming restrictions is an array of tags

            // Append the input element to the cell
            tagsCell.append(tagsInput);

            // Append the cell to the row
            row.append(tagsCell);

            // Create a cell for blocked timeslots (assuming it's a multi-select)
            const blockedTimeslotsCell = $('<td>');

            // Create a select element for blocked timeslots and initialize it with the data
            const blockedTimeslotsSelect = $('<select>').addClass('blocked-times-select').attr('multiple', true);

            // Add options to the select based on the data (assuming blockedTimeSlots is an array of options)
            for (const option of rowData.blockedTimeSlots) {
                blockedTimeslotsSelect.append($('<option>').text(option).attr('selected', true));
            }

            // Append the select element to the cell
            blockedTimeslotsCell.append(blockedTimeslotsSelect);

            // Append the cell to the row
            row.append(blockedTimeslotsCell);

            // Add the row to the table body
            $('#class-table-body').append(row);

            // Initialize Tagify for the tags input in this row
            const tagify = new Tagify(tagsInput[0], {
                // Configure Tagify as needed
            });

            // Store the Tagify instance for this row
            tagifyInstances[rowData.section] = tagify;
        }

        // Initialize Select2 for the multi-select dropdowns with the .blocked-times-select class
        $('.blocked-times-select').select2({ width: '300px' });

        // Function to handle updates to the data-tags attribute
        function updateDataTags(el) {
            const sectionTitle = el.dataset.sectionTitle;
            const tagify = tagifyInstances[sectionTitle]; // Get the Tagify instance

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

        // Delegated event handler for manual tag additions
        $('#class-table-body').on('change', '.tagify-input', function () {
            updateDataTags(this);
        });
    }


    
    
    
    // Make the timeslot list selectable
    $('#timeslot-list').selectable();

    // Additional code for other interactions...
});
