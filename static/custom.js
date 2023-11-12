 // Function to convert an array to a string with a specified delimiter
 function arrayToString(arr, delimiter) {
    return arr.join(delimiter);
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
    });
    
    
    

    $('.blocked-times-select').select2({ width: '300px' });

    // Initialize DataTable
    const dataTable = $('#class-table').DataTable({
        // DataTable configuration options here
        paging: true,
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
                // Display the results in the 'results-list' div
                $('#results-list').empty(); // Clear any previous results
                if (response.message === 'Optimization complete') {
                    $.each(response.results, function (index, result) {
                        // Append each result to the 'results-list' div
                        $('#results-list').append('<p>' + result + '</p>');
                    });
                } else {
                    $('#results-list').html('<p>Error: ' + response.error + '</p>');
                }


            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    });
    
    
});
