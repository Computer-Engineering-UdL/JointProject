document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.querySelector('.select-input select');
    const gridContainer = document.getElementById('gridContainer');


    // Function to create grid items from select options
    function populateGrid() {
        // Clear any existing grid items
        gridContainer.innerHTML = '';

        // Create grid items
        Array.from(selectElement.options).forEach(option => {
            const value = option.value;

            // Skip the "no selected" option (e.g., if value is empty or a placeholder like "0")
            if (!value || value === "No seleccionat") {
                return;
            }

            console.log('Value:', value); // Check the value being used
            const imgSrc = imageUrls[value];
            console.log('Image URL:', imgSrc);

            const div = document.createElement('div');
            div.className = 'gridItem';

            // Create an image element
            const img = document.createElement('img');
            img.src = imgSrc;
            img.alt = option.textContent;

            // Create a text node for the option text
            const text = document.createTextNode(option.textContent);

            div.appendChild(img);
            div.appendChild(text);

            div.dataset.value = option.value;

            // Event listener to handle click event on grid items
            div.addEventListener('click', function() {
                // Update select element to the clicked option
                selectElement.value = option.value;
                alert('Selected: ' + option.textContent);
            });

            gridContainer.appendChild(div);
        });
    }

    // Populate the grid when the page loads
    populateGrid();
});
