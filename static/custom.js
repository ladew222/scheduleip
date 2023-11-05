

$(document).ready(function () {
    const tagifyInstances = {};

    
    // Initialize Dragula for your table
    var drake = dragula([document.getElementById('class-table-body')]);



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

    // Listen for "dragenter" event
    drake.on('dragenter', function (el, target) {
        // Add the "target-row" class to the target row
        target.classList.add('target-row');
    });

    // Listen for "dragleave" event
    drake.on('dragleave', function (el, target) {
        // Remove the "target-row" class from the target row
        target.classList.remove('target-row');
    });


    // Listen for "drop" event
    drake.on('drop', function (el, target, source, sibling) {
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
                days: $(this).find('td:eq(10)').text(),
                timeslot: $(this).find('td:eq(11)').text(),
                restrictions: arrayToString(rowDataTags, ';'),
                blockedTimeSlots: arrayToString($(this).find('td:eq(13) select').val() || [], ';'),
            };

            classData.push(rowData);
        });

        const csvData = classData.map(row => [
            row.term, row.section, row.title, row.location, row.meetingInfo,
            row.faculty, row.availableCapacity, row.status, row.credits,
            row.academicLevel, row.days, row.timeslot, row.restrictions,
            row.blockedTimeSlots,
        ].join(','));

        const csvString = csvData.join('\n');

        const blob = new Blob([csvString], { type: 'text/csv' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'schedule.csv';

        link.click();
    }

    $('#save-schedule').on('click', saveSchedule);

    // Handle loading table data from a CSV file
    $('#load-table-button').on('click', function () {
        $('#file-input').click();
    });

    // Function to populate the table with loaded data and update selected tags and multi-selects
    function populateTable(data) {
        $('#class-table-body').empty();

        for (const rowData of data) {
            const row = $('<tr>');

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
            row.append($('<td>').text(rowData.days));
            row.append($('<td>').text(rowData.timeslot));

            const tagsCell = $('<td>');
            const tagsInput = $('<input>').attr('type', 'text').addClass('tagify');
            tagsInput.val(rowData.restrictions.join(', '));
            tagsCell.append(tagsInput);
            row.append(tagsCell);

            const blockedTimeslotsCell = $('<td>');
            const blockedTimeslotsSelect = $('<select>').addClass('blocked-times-select').attr('multiple', true);

            for (const option of rowData.blockedTimeSlots) {
                blockedTimeslotsSelect.append($('<option>').text(option).attr('selected', true));
            }

            blockedTimeslotsCell.append(blockedTimeslotsSelect);
            row.append(blockedTimeslotsCell);

            $('#class-table-body').append(row);

            const tagify = new Tagify(tagsInput[0], {
                // Configure Tagify as needed
            });

            tagifyInstances[rowData.section] = tagify;
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

    $('#file-input').on('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const fileContent = event.target.result;
                const loadedData = parseCSV(fileContent);
                populateTable(loadedData);
            };
            reader.readAsText(file);
        }
    });

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

        // Implement your constraint logic here and update the table accordingly
        // For example, you can filter and hide rows based on constraints
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
