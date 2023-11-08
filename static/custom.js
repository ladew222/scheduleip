$(document).ready(function () {
    const tagifyInstances = {};


    $(".restrict-button").click(function () {
        // Find the closest row to the clicked button
        var $closestRow = $(this).closest("tr");
    
        // Extract the section title from the data-section-title attribute
        var sectionTitle = $closestRow.data("section-title");
    
        // Get all rows with checkboxes
        var $rowsWithCheckboxes = $("tr:has(.restrict-checkbox)");
    
        // Iterate through each row with a checkbox
        $rowsWithCheckboxes.each(function () {
            var $row = $(this);
    
            // Find the checkbox in the current row
            var $checkbox = $row.find(".restrict-checkbox");
    
            // Check if the checkbox is checked
            if ($checkbox.prop("checked")) {
                // Find the input elements with the class "tagify-input" in the current row
                var $tagifyInputs = $row.find(".tagify-input");
    
                // Add the section title as a tag to each input element in the current row
                $tagifyInputs.each(function () {
                    var $input = $(this);
    
                    // Add the section title as a tag
                    $input.tagify("add", sectionTitle);
                });
            }
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
        const sectionTR = $(this).closest('tr')
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
            const tagsString = cleanValue.map(tag => tag.value).join(', ');
            // Access the parent <tr> element using sectionTR
            sectionTR.data('tags', tagsString);
            console.log('Removed tag in parent <tr>:', sectionTR);
            // Additional actions can be performed here
        });

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
});




 