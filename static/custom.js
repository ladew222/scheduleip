

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

    // Initialize Select2 for all rows with the '.blocked-times-select' class
    $('.blocked-times-select').select2({ width: '300px' });
    
    // Initialize Dragula for your table
    var drake = dragula([document.getElementById('class-table-body')]);
    
    // Function to escape CSV field values
    function escapeCSVField(value) {
        // If the value contains double quotes, escape them by doubling them
        if (value.includes('"')) {
            return '"' + value.replace(/"/g, '""') + '"';
        } else {
            return '"' + value + '"';
        }
    }
    

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


    // Function to parse CSV data
    function parseCSV(csvString) {
        const lines = csvString.split('\n');
        const data = [];

        for (let i = 0; i < lines.length; i++) {
            const row = lines[i].split(',');
            const rowData = row.map(unescapeCSVField);
            data.push(rowData);
        }

        return data;
    }

    // Function to unescape CSV field values
    function unescapeCSVField(value) {
        return value.replace(/^"|"$/g, '').replace(/""/g, '"');
    }


    function saveSchedule() {
        const classData = [];
    
        // Iterate over table rows and gather data
        $('#class-table-body tr').each(function () {
            const rowDataTags = $(this).data('tags') || [];
    
            const rowData = {
                term: escapeCSVField($(this).find('td:eq(0)').text()),
                section: escapeCSVField($(this).find('td:eq(1)').text()),
                title: escapeCSVField($(this).find('td:eq(2)').text()),
                location: escapeCSVField($(this).find('td:eq(3)').text()),
                meetingInfo: escapeCSVField($(this).find('td:eq(4)').text()),
                faculty: escapeCSVField($(this).find('td:eq(5)').text()),
                availableCapacity: escapeCSVField($(this).find('td:eq(6)').text()),
                status: escapeCSVField($(this).find('td:eq(7)').text()),
                credits: escapeCSVField($(this).find('td:eq(8)').text()),
                academicLevel: escapeCSVField($(this).find('td:eq(9)').text()),
                days: escapeCSVField($(this).find('td:eq(10)').text()),
                timeslot: escapeCSVField($(this).find('td:eq(11)').text()),
                restrictions: arrayToString(rowDataTags.map(escapeCSVField), ';'), // Escape tags
                blockedTimeSlots: arrayToString($(this).find('td:eq(13) select').val() || [], ';'),
            };
    
            classData.push(rowData);
        });
    
        const csvData = classData.map(row => [
            row.term, row.section, row.title, row.location, row.meetingInfo,
            row.faculty, row.availableCapacity, row.status, row.credits,
            row.academicLevel, row.days, row.timeslot, row.restrictions,
            row.blockedTimeSlots,
        ].join(',')); // Escape each field
    
        const csvString = csvData.join('\n');
    
        const blob = new Blob([csvString], { type: 'text/csv' });
    
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'schedule.csv';
    
        link.click();
    }
    




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

        // Add the section name as a tag to both rows
        var tagifyDragged = tagifyInstances[draggedSection];
        var tagifyDropped = tagifyInstances[droppedSection];

        tagifyDragged.addTags([droppedSection]);
        tagifyDropped.addTags([draggedSection]);
    });

    // Function to convert an array to a string with a specified delimiter
    function arrayToString(arr, delimiter) {
        return arr.join(delimiter);
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
    });


    // Trigger the file input click when the "Load Table" button is clicked
    $('#load-table-button').on('click', function () {
        $('#file-input').click();
    });
    
    // Function to populate the table with loaded data and update selected tags and multi-selects
    function populateTable(data) {
        $('#class-table-body').empty();

        for (const rowData of data) {
            const row = $('<tr>');

            // Assuming that multivalued tags and restrictions are stored as strings with semicolon separators
            const term = rowData[0];
            const section = rowData[1];
            const title = rowData[2];
            const location = rowData[3];
            const meetingInfo = rowData[4];
            const faculty = rowData[5];
            const availableCapacity = rowData[6];
            const status = rowData[7];
            const credits = rowData[8];
            const academicLevel = rowData[9];
            const days = rowData[10];
            const timeslot = rowData[11];

            // Split multivalued tags and restrictions using semicolons and trim spaces
            const restrictions = rowData[12].split(';').map(tag => tag.trim());
            const blockedTimeSlots = rowData[13].split(';').map(slot => slot.trim());

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
            row.append($('<td>').text(days));
            row.append($('<td>').text(timeslot));

            const tagsCell = $('<td>');
            const tagsInput = $('<input>').attr('type', 'text').addClass('tagify');
            tagsInput.val(restrictions.join(', '));
            tagsCell.append(tagsInput);
            row.append(tagsCell);

            const blockedTimeslotsCell = $('<td>');
            const blockedTimeslotsSelect = $('<select>').addClass('blocked-times-select').attr('multiple', true);

            for (const option of blockedTimeSlots) {
                blockedTimeslotsSelect.append($('<option>').text(option).attr('selected', true));
            }

            blockedTimeslotsCell.append(blockedTimeslotsSelect);
            row.append(blockedTimeslotsCell);

            $('#class-table-body').append(row);

            const tagify = new Tagify(tagsInput[0], {
                // Configure Tagify as needed
            });

            tagifyInstances[section] = tagify;
        }

        $('.blocked-times-select').select2({ width: '300px' });

        function updateDataTags(el) {
            const sectionTitle = el.dataset.sectionTitle;
            const tagify = tagifyInstances[sectionTitle];

            const currentTags = tagify.value.map(tag => tag.value);

            if (!currentTags.includes(sectionTitle)) {
                tagify.addTags([sectionTitle]);
                const rowDataTags = $(el).data('tags') || [];
                rowDataTags.push(sectionTitle);
                $(el).data('tags', rowDataTags);
            }
        }

        $('#class-table-body').on('change', '.tagify-input', function () {
            updateDataTags(this);
        });
    }


    // Initialize Tagify for all rows with the '.tagify' class
    $('.tagify').each(function () {
        const sectionTitle = $(this).closest('tr').data('section-title');
        tagifyInstances[sectionTitle] = new Tagify(this, {
            // Configure Tagify as needed
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


    // Add a new row to the table
    $('#add-class-button').on('click', function () {
        const newRow = $('<tr>');
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td contenteditable="true">'));
        newRow.append($('<td>'));

        const tagsCell = $('<td>');
        const tagsInput = $('<input>').attr('type', 'text').addClass('tagify');
        tagsCell.append(tagsInput);
        newRow.append(tagsCell);

        const blockedTimeslotsCell = $('<td>');
        const blockedTimeslotsSelect = $('<select>').addClass('blocked-times-select').attr('multiple', true);
        blockedTimeslotsCell.append(blockedTimeslotsSelect);
        newRow.append(blockedTimeslotsCell);

        $('#class-table-body').append(newRow);

        // Initialize Tagify for the new row
        const sectionTitle = newRow.find('td:eq(1)').text();
        tagifyInstances[sectionTitle] = new Tagify(tagsInput[0], {
            // Configure Tagify as needed
        });

        $('.blocked-times-select').select2({ width: '300px' });
    });

    // Remove selected rows from the table
    $('#remove-class-button').on('click', function () {
        $('#class-table-body input:checked').closest('tr').remove();
    });
});
