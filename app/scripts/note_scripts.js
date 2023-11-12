function openNav() {
    document.getElementById("navbar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("navbar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

// Create a Spellchecker instance
var spell = new Spellchecker();

// Function to check spelling and update UI
function checkSpelling() {
    var textarea = document.getElementById('noteTextarea');
    var words = textarea.value.split(/\s+/);

    // Clear previous highlights
    textarea.classList.remove('misspelled');

    // Check spelling and highlight misspelled words
    for (var i = 0; i < words.length; i++) {
        if (!spell.isMisspelled(words[i])) {
            // Highlight misspelled words
            textarea.classList.add('misspelled');
        }
    }
}

document.getElementById('noteTextarea').addEventListener('input', checkSpelling);


function toggleDropdown() {
    var dropdown = document.getElementById("myDropdown");
    dropdown.classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}



function updateWordCount() {
    var noteTextarea = document.getElementById('noteTextarea');
    var wordCount = countWords(noteTextarea.value);
    alert('Word Count: ' + wordCount);  // You can replace this with your preferred way of displaying the word count
}

function countWords(text) {
    var words = text.split(/\s+/);
    return words.length;
}
