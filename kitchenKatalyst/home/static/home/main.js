document.getElementById('grocery-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    var itemNumber = document.getElementById('numberValue');
    var itemName = document.getElementById('nameValue');
    var itemDate = document.getElementById('dateValue');
    
    var numbValue = itemNumber.value.trim();
    var namValue = itemName.value.trim(); 
    var dtValue = itemDate.value.trim();// Trim leading/trailing spaces
    
    if (numbValue !== '' && namValue !== '' && dtValue !== '') {
        addItemToList(numbValue, namValue, dtValue);
        
        // Clear input fields after adding item
        itemNumber.value = '';
        itemName.value = '';
        itemDate.value = '';
    }
});

function addItemToList(numbValue, namValue, dtValue) {
    var itemList = document.getElementById('item-list');

    // Create table row
    var row = document.createElement('tr');

    // Create and append table cells for number, name, and date
    var numberCell = document.createElement('th');
    numberCell.setAttribute('scope', 'row');
    numberCell.textContent = numbValue;

    var nameCell = document.createElement('td');
    nameCell.textContent = namValue;

    var dateCell = document.createElement('td');
    dateCell.textContent = dtValue;

    // Create remove button cell
    var removeButtonCell = document.createElement('tr');

    // Create the remove button
    var removeButton = document.createElement('button');
    removeButton.classList.add('remove-btn');

    removeButton.innerHTML = '<i class="material-icons">delete</i>';
    removeButton.style.backgroundColor = 'red';

    // Add event Listener to remove the item when the button is clicked
    removeButton.addEventListener('click', function() {
        itemList.removeChild(row);
    });

    // Append the remove button to the cell
    removeButtonCell.appendChild(removeButton);

    // Append table cells to the row
    row.appendChild(numberCell);
    row.appendChild(nameCell);
    row.appendChild(dateCell);
    row.appendChild(removeButtonCell);

    // Append the row to the item list
    itemList.appendChild(row);
}
