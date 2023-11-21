 // Function to convert an array to a string with a specified delimiter
 function arrayToString(arr, delimiter) {
    return arr.join(delimiter);
}
// Function to update the calendar with events
function updateCalendar(events) {
    // Assuming you have a function to add events to your Simple Calendar
    // This is a pseudocode example, actual implementation may vary
    simpleCalendar.clearEvents(); // Clear existing events
    events.forEach(event => simpleCalendar.addEvent(event));
}


// Function to convert an array of objects to a CSV string
function convertToCSV(objArray) {
    const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray;
    let str = `${Object.keys(array[0]).map(value => `"${value}"`).join(",")}` + '\r\n';

    return array.reduce((str, next) => {
        str += `${Object.values(next).map(value => `"${value}"`).join(",")}` + '\r\n';
        return str;
    }, str);
}

// Function to download the CSV string as a file
function downloadCSV(csvContent, fileName) {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}



// Function to create an HTML table from the result array
function createResultsTable(data) {
    let table = '<table style="width:100%; border-collapse: collapse; border: 1px solid #ddd;">';
    table += '<tr style="background-color: #f4f4f4;"><th>Section Name</th<th>Instructor</th><th>Timeslot</th></tr>';

    data.forEach(item => {
        table += `<tr><td style="border: 1px solid #ddd; padding: 8px;">${item.section_name}</td><td style="border: 1px solid #ddd; padding: 8px;">${item.instructor}</td><td style="border: 1px solid #ddd; padding: 8px;">${item.timeslot}</td></tr>`;
    });

    table += '</table>';
    return table;
}

// Function to convert the array of objects into a semicolon-separated string
function valuesToString(arr) {
    return arr.map(obj => obj.value).join('; ');
}

// Function to get the checkbox value (1 or 0)
function getCheckboxValue($row) {
    const $checkbox = $row.find(".hold-checkbox");
    return $checkbox.prop("checked") ? 1 : 0;
}


$(document).ready(function () {
    const tagifyInstances = {};

    // Hold All Button Click Event
    $('#hold-all').on('click', function () {
        $(".hold-checkbox").prop("checked", true);
    });

    var calendarEl = document.getElementById('full-calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuration options go here
        initialView: 'timeGridWeek',
        eventColor: '#378006',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridDay,timeGridWeek' // Buttons for day and week views
        },
    });
    calendar.render();

    // Function to gather data from the table and initiate the CSV download
    $('#save-schedule').on('click', function() {
        const classData = [];
        $('#class-table-body tr').each(function() {
            const rowDataTags = tagifyInstances[$(this).data('section-title')].value;
            let restrictionsResultString = valuesToString(rowDataTags);
            const holdValue = getCheckboxValue($(this));

            const rowData = {
                section: $(this).find('td:eq(0)').text(),
                title: $(this).find('td:eq(1)').text(),
                minCredit: $(this).find('td:eq(2)').text(),
                secCap: $(this).find('td:eq(3)').text(),
                room: $(this).find('td:eq(4)').text(),
                bldg: $(this).find('td:eq(5)').text(),
                weekDays: $(this).find('td:eq(6)').text(),
                csmStart: $(this).find('td:eq(7)').text(),
                csmEnd: $(this).find('td:eq(8)').text(),
                faculty1: $(this).find('td:eq(9)').text(),
                hold: holdValue,
                restrictions: restrictionsResultString,
                blockedTimeSlots: arrayToString($(this).find('td:eq(12) select').val() || [], ';'),
            };

            classData.push(rowData);
        });

        const csvData = convertToCSV(classData);
        downloadCSV(csvData, 'class_schedule.csv');
    });


    $("#show-table").click(function () {
        $("#class-table").show();
       // $("#optimization-results").hide();
    });

    $(".restrict-button").click(function () {
        // Get all rows with checkboxes
        var $rowsWithCheckboxes = $("tr:has(.restrict-checkbox)");
    
        // Create an array to store the section titles of all checked rows
        var checkedSectionTitles = [];
    
        // Iterate through each row with a checkbox
        $rowsWithCheckboxes.each(function () {
            var $row = $(this);
    
            // Find the checkbox in the current row
            var $checkbox = $row.find(".restrict-checkbox");
    
            // Check if the checkbox is checked
            if ($checkbox.prop("checked")) {
                // Extract the section title from the data-section-title attribute of the current row
                var sectionTitle = $row.data("section-title");
    
                // Push the section title to the array of checked section titles
                checkedSectionTitles.push(sectionTitle);
                

            }
            
        });

        
    
        // Iterate through each section title in the checkedSectionTitles array
        checkedSectionTitles.forEach(function (sectionTitle) {
            // Find the Tagify instance for the current section title
            const tagifyInstance = tagifyInstances[sectionTitle];

            // Iterate through all other checked section titles
            checkedSectionTitles.forEach(function (otherSectionTitle) {
                if (otherSectionTitle !== sectionTitle) {
                    // Add the other section title as a tag to the Tagify instance
                    tagifyInstance.addTags([otherSectionTitle]);
                }
            });
        });

        $(".restrict-checkbox").prop('checked', false);
    });

    $('#export-csv').on('click', function() {
        // Extract data from DataTable
        const data = dataTable.rows().data().toArray();
        let csvContent = "data:text/csv;charset=utf-8,";

        // Header row
        csvContent += dataTable.columns().header().toArray().map(e => $(e).text()).join(",") + "\r\n";

        // Data rows
        data.forEach(function(rowArray) {
            let row = rowArray.join(",");
            csvContent += row + "\r\n";
        });

        // Download the CSV file
        downloadCSV(csvContent, 'datatable_export.csv');
    });
    
    
    

    $('.blocked-times-select').select2({ width: '300px' });

    // Initialize DataTable
    const dataTable = $('#class-table').DataTable({
        // DataTable configuration options here
        paging: false,
        searching: true,
        ordering: true,
        columns: [
            { title: 'Sections' },
            { title: 'Title' },
            { title: 'Min Credit' },
            { title: 'Sec Cap' },
            { title: 'Room' },
            { title: 'Bldg' },
            { title: 'Week Days' },
            { title: 'CSM start' },
            { title: 'CSM end' },
            { title: 'Faculty1' },
            { title: 'holdValue' },
            { title: 'Restrictions' },
            { title: 'Blocked Time Slots' },
            { title: 'Select' },
            { title: 'Actions' }
        ],
    });

    // Select all Tagify inputs and initialize Tagify for each
    $('.tagify-input').each(function () {
        // Get the parent <tr> element's unique identifier (data-section-title)
        const sectionTitle = $(this).closest('tr').data('section-title');
        const sectionTR = $(this).closest('tr');
        // Initialize Tagify for this input
        const tagify = new Tagify(this, {
            // Tagify configuration options here
        });

        // Set up callbacks for this Tagify instance
        tagify.on('add', function (e) {
            const cleanValue = e.detail.tagify.getCleanValue();
            // Create a comma-separated string from the array values
            const tagsString = cleanValue.map(tag => tag.value).join(', ');
            // Access the parent <tr> element using sectionTR
            sectionTR.data('tags', tagsString);
            console.log('Added tag in parent <tr>:', sectionTR);
            // Additional actions can be performed here
        });

        tagify.on('remove', function (e) {
            const cleanValue = e.detail.tagify.getCleanValue();
            // Create a comma-separated string from the array values
            const tagsString = cleanValue.map(tag => tag.value).join('; ');
            // Access the parent <tr> element using sectionTR
            sectionTR.data('tags', tagsString);
            console.log('Removed tag in parent <tr>:', sectionTR);
            // Additional actions can be performed here
        });

        // Store the Tagify instance in your tagifyInstances object
        tagifyInstances[sectionTitle] = tagify;
    });

    // Optional: Save table data to CSV
    $('#save-csv').on('click', function () {
        // Extract data from DataTable
        const data = dataTable.data().toArray();

        // Create a CSV string
        const csvContent = data.map(row => row.join(',')).join('\n');

        // Create a Blob and download link
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'schedule.csv';
        link.click();
    });


    $('#apply-constraints').on('click', function () {
        const classData = [];
        $('#class-table-body tr').each(function () {

            const rowDataTags = tagifyInstances[$(this).data('section-title')].value
            let resultString = valuesToString(rowDataTags);
            const holdValue = getCheckboxValue($(this));
    
            const rowData = {
                section: $(this).find('td:eq(0)').text(),
                title: $(this).find('td:eq(1)').text(),
                minCredit: $(this).find('td:eq(2)').text(),
                secCap: $(this).find('td:eq(3)').text(),
                room: $(this).find('td:eq(4)').text(),
                bldg: $(this).find('td:eq(5)').text(),
                weekDays: $(this).find('td:eq(6)').text(),
                csmStart: $(this).find('td:eq(7)').text(),
                csmEnd: $(this).find('td:eq(8)').text(),
                faculty1: $(this).find('td:eq(9)').text(),
                hold: holdValue,
                restrictions: resultString,
                blockedTimeSlots: arrayToString($(this).find('td:eq(12) select').val() || [], ';'),
            };
    
            classData.push(rowData);
        });

        // Collect penalty parameters
        const classPenalty = $('#class-penalty').val();
        const movePenalty = $('#move-penalty').val();
        const blockedSlotPenalty = $('#blocked-slot-penalty').val();
        const holdPenalty = $('#hold-penalty').val();
        
    
        // Send the data to the server for optimization
        const requestData = {
            classData: classData,
            userBlockedTimes: '',
            classPenalty: classPenalty,
            movePenalty: movePenalty,
            blockedSlotPenalty: blockedSlotPenalty,
            holdPenalty: holdPenalty,
            };
    
        $.ajax({
            type: 'POST',
            url: '/optimize', // Replace with your endpoint for optimization
            data: JSON.stringify(requestData),
            contentType: 'application/json',
            success: function (response) {
                // Handle the optimization results
                console.log('Optimization successful:', response);
                $("#optimization-results").fadeIn(1000); // Fade in slowly over 1 second
                $("#class-table").fadeOut(1000); // Fade out slowly over 1 second
                // Display the results in the 'results-list' div
                $('#results-list').empty(); // Clear any previous results
                if (response.message === 'Success') {
                    $('#results-list').append('<p>' + createResultsTable(response.scheduled_sections) + '</p>');
                } else {
                    $('#results-list').html('<p>Error: ' + response.message + '</p>');
                }
                 // Check if calendar events are available in the response
                if (response.calendar_events) {
                    // Clear any existing events in the calendar
                    calendar.removeAllEvents();

                    // Add new events to the calendar
                    response.calendar_events.forEach(event => {
                        calendar.addEvent({
                            title: event.section_name, // Assuming 'section_name' is used as the event title
                            start: event.start,
                            location: event.room,
                            description: event.instructor,
                            end: event.end,
                            color: event.color, 
                            extendedProps: {
                                department: 'BioChemistry'
                              },
                        });
                    });

                    // Render or rerender the calendar
                    calendar.render();
                } else {
                    console.error('No calendar events in response');
                }

            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    });
    
    
});
