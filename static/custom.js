$(document).ready(function () {
    const tagifyInstances = {};



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
    
        // Add a blur event listener to validate and save the edited content
        inputField.on('blur', function () {
            const editedContent = inputField.val().trim();
    
            // Validate the edited content format based on the cell's class
            if ((cell.hasClass('days') && isValidDayFormat(editedContent)) ||
                (cell.hasClass('time') && isValidTimeFormat(editedContent))) {
                // Handle day or time format validation
                cell.text(editedContent);
            } else {
                // Display an error message and revert to the original content
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


    // Initialize Select2 for all rows with the '.blocked-times-select' class
    $('.blocked-times-select').select2({ width: '300px' });

    // Initialize Dragula for your table
    var drake = dragula([document.getElementById('class-table-body')]);



      // Function to convert an array to a string with a specified delimiter
      function arrayToString(arr, delimiter) {
        return arr.join(delimiter);
    }


    // Function to escape CSV field values
    function escapeCSVField(value) {
        if (value.includes('"')) {
            return '"' + value.replace(/"/g, '""') + '"';
        } else {
            return '"' + value + '"';
        }
    }

    // Function to convert an array to a string with a specified delimiter
    function arrayToString(arr, delimiter) {
        return arr.join(delimiter);
    }

    $('#load-schedule').on('click', function () {
        // Trigger the file input dialog
        $('#file-input').trigger('click');
    });

    // Handle the selected file when the user chooses one
    $('#file-input').on('change', function () {
        const selectedFile = this.files[0];
        if (selectedFile) {
            // Read the selected CSV file
            const reader = new FileReader();
            reader.onload = function (e) {
                const fileContent = e.target.result;
                const loadedData = parseCSV(fileContent);
                populateTable(loadedData);
                // Parse and process the CSV data (you can use a CSV parsing library)
                // Here, you might call a function to populate the table with the loaded data
                // For example: populateTableWithCSVData(csvData);
            };
            reader.readAsText(selectedFile);
        }
    });

    // Trigger the file input click when the "Load Table" button is clicked
    $('#load-table-button').on('click', function () {
        $('#file-input').click();
    });


    // Listen for "drag" event
    drake.on('drag', function (el) {
        // Apply the "dragging" class to the dragged row
        el.classList.add('dragging');
    });

    // Listen for "dragend" event
    drake.on('dragend', function (el) {
        // Remove the "dragging" class from the dragged row
        el.classList.remove('dragging');
    });

    var tableRows = $('.class-table-body .draggable-row');
    tableRows.each(function () {
        // Inside this function, "this" refers to the current table row
        $(this).on('dragenter', function () {
            // Highlight the row when the dragged element enters it
            $(this).addClass('highlighted-row');
        });

        $(this).on('dragleave', function () {
            // Remove the highlight when the dragged element leaves the row
            $(this).removeClass('highlighted-row');
        });
    });




    $('#class-table-body').on('change', '.tagify-input', function () {
        updateDataTags(this);
    });
    

    // Initialize Tagify for all rows with the '.tagify' class
    $('.tagify').each(function () {
        const sectionTitle = $(this).closest('tr').data('section-title');
        const trElement = $(this).closest('tr'); // Store a reference to the tr element
        tagifyInstances[sectionTitle] = new Tagify(this, {
            // Configure Tagify as needed

            callbacks: {
                // Callback when adding a tag
                add: function (e) {
                    // Access the tr element associated with this Tagify input
                    const tr = trElement;

                    // Get the clean value (array of tags) from Tagify
                    const cleanValue = e.detail.tagify.getCleanValue();

                    // Extract the tag values and join them with a comma
                    const tagValues = cleanValue.map(tag => tag.value);
                    const dataTagsValue = tagValues.join(', ');

                    // Update data-tags attribute of the parent tr with the tag values
                    tr.attr('data-tags', dataTagsValue);

                    // Your additional logic for tag addition here
                },
                // Callback when removing a tag
                remove: function (e) {
                    // Access the tr element associated with this Tagify input
                    const tr = trElement;

                    // Get the clean value (array of tags) from Tagify
                    const cleanValue = e.detail.tagify.getCleanValue();

                    // Extract the tag values and join them with a comma
                    const tagValues = cleanValue.map(tag => tag.value);
                    const dataTagsValue = tagValues.join(', ');

                    // Update data-tags attribute of the parent tr with the tag values
                    tr.attr('data-tags', dataTagsValue);

                    // Your additional logic for tag removal here
                }
            }
        });
    });




    $('#apply-constraints').on('click', function () {
        const classData = [];
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
                days: $(this).find('td:eq(10)').text(),
                timeslot: $(this).find('td:eq(11)').text(),
                restrictions: arrayToString(rowDataTags, ';'),
                blockedTimeSlots: arrayToString($(this).find('td:eq(13) select').val() || [], ';'),
            };

            classData.push(rowData);
        });

        
        // Send the data to the server for optimization
        const requestData = {
            classData: classData,
            userBlockedTimes: '',
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
    // Listen for "drop" event
    // Listen for "drop" event
    drake.on('drop', function (el, target, source, sibling) {
        // Remove the "target-row" class from the previously targeted row
        var prevTargetRow = document.querySelector('.target-row');
        if (prevTargetRow) {
            prevTargetRow.classList.remove('target-row');
        }

        // Get the dragged and dropped rows
        var draggedRow = $(el);
        var droppedRow = $(sibling);

        // Extract section names
        var draggedSection = draggedRow.data('section-title');
        var droppedSection = droppedRow.data('section-title');

        // Add the section name as a tag to the other row
        var tagifyDragged = tagifyInstances[draggedSection];
        var tagifyDropped = tagifyInstances[droppedSection];

        // Add the section name as a tag to both rows' Tagify instances
        tagifyDropped.addTags([draggedSection]);
        tagifyDragged.addTags([droppedSection]);

        // Optionally, you can update the data-tags attribute of both rows
        //droppedRow.attr('data-tags', draggedSection);
        //draggedRow.attr('data-tags', droppedSection);
    });





    function saveSchedule() {
        const classData = [];
        
        // Create headers
        const headers = [
            'Term', 'Section', 'Title', 'Location', 'Meeting Info',
            'Faculty', 'Available Capacity', 'Status', 'Credits',
            'Academic Level', 'Days', 'Timeslot', 'Restrictions', 'Blocked Time Slots'
        ];
    
        // Add headers to classData
        classData.push(headers);
    
        // Iterate over table rows and gather data
        $('#class-table-body tr').each(function () {
            const rowDataTags = $(this).data('tags') || [];
            
            // Ensure rowDataTags is an array
            const tagsArray = Array.isArray(rowDataTags) ? rowDataTags : [rowDataTags];
    
            const rowData = [
                escapeCSVField($(this).find('td:eq(0)').text()),
                escapeCSVField($(this).find('td:eq(1)').text()),
                escapeCSVField($(this).find('td:eq(2)').text()),
                escapeCSVField($(this).find('td:eq(3)').text()),
                escapeCSVField($(this).find('td:eq(4)').text()),
                escapeCSVField($(this).find('td:eq(5)').text()),
                escapeCSVField($(this).find('td:eq(6)').text()),
                escapeCSVField($(this).find('td:eq(7)').text()),
                escapeCSVField($(this).find('td:eq(8)').text()),
                escapeCSVField($(this).find('td:eq(9)').text()),
                escapeCSVField($(this).find('td:eq(10)').text()),
                escapeCSVField($(this).find('td:eq(11)').text()),
                arrayToString(tagsArray.map(escapeCSVField), ';'), // Escape tags
                arrayToString($(this).find('td:eq(13) select').val() || [], ';'),
            ];
    
            classData.push(rowData);
        });
    
        const csvData = classData.map(row => row.join(',')); // Join fields with commas
    
        const csvString = csvData.join('\n'); // Join rows with line breaks
    
        const blob = new Blob([csvString], { type: 'text/csv' });
    
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'schedule.csv';
    
        link.click();
    }

    // Function to parse CSV data
    function parseCSV(csvString) {
        // Separate the rows
        const lines = csvString.split(/(?:\r\n|\n)+/).filter(el => el.length !== 0);

        // Extract the headers
        const headers = lines.splice(0, 1)[0].split(",");

        // Define a regular expression to extract values
        const valuesRegExp = /(?:"([^"]*(?:""[^"]*)*)")|([^",]+)/g;

        // Initialize an array to store parsed data
        const data = [];

        for (let i = 0; i < lines.length; i++) {
            const element = {};
            let j = 0;

            while (matches = valuesRegExp.exec(lines[i])) {
                let value = matches[1] || matches[2];
                value = value.replace(/""/g, "\"");

                element[headers[j]] = value;
                j++;
            }

            data.push(element);
        }

        return data;
    }

    // Function to populate the table with data
    function populateTable(data) {
        $('#class-table-body').empty();

        // Define the predefined options for Blocked Time Slots
        const predefinedBlockedTimeSlots = [
            'MWF 8:00AM - 8:55AM',
            'MWF 9:05AM - 10:00AM',
            'MWF 10:10AM - 11:05AM',
            'MWF 11:15AM - 12:10PM',
            'MWF 12:20PM - 1:15PM',
            'MWF 1:25PM - 2:20PM',
            'MWF 2:30PM - 3:25PM',
            'MWF 3:35PM - 4:30PM',
            'TTh 8:00AM - 9:20AM',
            'TTh 9:30AM - 10:50AM',
            'TTh 11:00AM - 12:20PM',
            'TTh 12:30PM - 1:50PM',
            'TTh 2:00PM - 3:20PM',
            'TTh 3:30PM - 4:50PM',
        ];

        for (const rowData of data) {
            

            // Extract the fields from the rowData object
            const term = rowData.Term || '';
            const section = rowData.Section || '';
            const title = rowData.Title || '';
            const location = rowData.Location || '';
            const meetingInfo = rowData['Meeting Info'] || '';
            const faculty = rowData.Faculty || '';
            const availableCapacity = rowData['Available Capacity'] || '';
            const status = rowData.Status || '';
            const credits = rowData.Credits || '';
            const academicLevel = rowData['Academic Level'] || '';
            const days = rowData.Days || '';
            const timeslot = rowData.Timeslot || '';

            const row = $('<tr>').attr('data-section-name', section);

            // Split multivalued tags and restrictions using semicolons and trim spaces
            const restrictions = (rowData.Restrictions || '').split(';').map(tag => tag.trim());

            // Extract blocked time slots from "Blocked Time Slots" column and split them
            const blockedTimeSlots = (rowData['Blocked Time Slots'] || '').split(';').map(slot => slot.trim());

            row.append($('<td>').text(term));
            row.append($('<td>').text(section));
            row.append($('<td>').text(title));
            row.append($('<td>').text(location));
            row.append($('<td>').text(meetingInfo));
            row.append($('<td>').text(faculty));
            row.append($('<td>').text(availableCapacity));
            row.append($('<td>').text(status));
            row.append($('<td>').text(credits));
            row.append($('<td>').text(academicLevel));
            row.append($('<td>').text(days).addClass('editable-cell'));
            row.append($('<td>').text(timeslot).addClass('editable-cell'));

            // Create a cell for tags
            const tagsCell = $('<td>');
            const tagsInput = $('<input>').attr('type', 'text').addClass('tagify');
            tagsInput.val(restrictions.join(', '));
            tagsCell.append(tagsInput);
            row.append(tagsCell);

            // Create a cell for blocked time slots
            const blockedTimeslotsCell = $('<td>');
            const blockedTimeslotsSelect = $('<select>').addClass('blocked-times-select').attr('multiple', true);

            // Add predefined options to the select and select them based on CSV data
            for (const option of predefinedBlockedTimeSlots) {
                const isSelected = blockedTimeSlots.includes(option);
                blockedTimeslotsSelect.append($('<option>').text(option).prop('selected', isSelected));
            }

            blockedTimeslotsCell.append(blockedTimeslotsSelect);
            row.append(blockedTimeslotsCell);

            // Store the list of tags in the data-tags attribute for this row
            row.attr('data-tags', restrictions.join(','));

            // Append the row to the table body
            $('#class-table-body').append(row);

            // Initialize Tagify for the tags input
            const tagify = new Tagify(tagsInput[0], {
                // Configure Tagify as needed
            });

            // Store the Tagify instance in your tagifyInstances object
            tagifyInstances[section] = tagify;
        }

        // Initialize select2 for the blocked timeslots select
        $('.blocked-times-select').select2({ width: '300px' });
    }

    // ... (rest of your code)

});
