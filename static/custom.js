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
            const tagsString = cleanValue.map(tag => tag.value).join(', ');
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
});
