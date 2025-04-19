document.addEventListener('DOMContentLoaded', function() {
    const guessesContainer = document.getElementById('guesses-container');
    const addGuessButton = document.getElementById('add-guess');
    const solveButton = document.getElementById('solve');
    const resultsDiv = document.getElementById('results');
    const possibleCountElement = document.getElementById('possible-count');
    const bestGuessElement = document.getElementById('best-guess');
    const suggestionsList = document.getElementById('suggestions-list');
    
    // Status cycle: empty -> absent -> present -> correct -> absent...
    const statuses = ['', 'absent', 'present', 'correct'];
    
    // Add event listeners to the initial guess row
    setupGuessRow(guessesContainer.querySelector('.guess-row'));
    
    // Add another guess row
    addGuessButton.addEventListener('click', function() {
        const newRow = createGuessRow();
        guessesContainer.appendChild(newRow);
        setupGuessRow(newRow);
        
        // Scroll to the new row
        newRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Focus on the input field
        const input = newRow.querySelector('.word');
        if (input) input.focus();
    });
    
    // Solve button click
    solveButton.addEventListener('click', function() {
        // Collect all guesses and their results
        const guessRows = guessesContainer.querySelectorAll('.guess-row');
        const guesses = [];
        
        for (const row of guessRows) {
            const wordInput = row.querySelector('.word');
            const word = wordInput.value.trim().toLowerCase();
            
            // Skip if word is not 5 letters
            if (word.length !== 5) continue;
            
            const letterResults = row.querySelectorAll('.letter-display');
            const result = Array.from(letterResults).map(letter => {
                if (letter.classList.contains('correct')) return 'correct';
                if (letter.classList.contains('present')) return 'present';
                if (letter.classList.contains('absent')) return 'absent';
                return '';
            });
            
            // Skip if not all letters have a status
            if (result.includes('')) continue;
            
            guesses.push({ word, result });
        }
        
        // If no valid guesses, alert the user
        if (guesses.length === 0) {
            alert('Please enter at least one valid guess with all letters marked.');
            return;
        }
        
        // Send to server
        fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ guesses }),
        })
        .then(response => response.json())
        .then(data => {
            // Display results
            possibleCountElement.textContent = `Possible words remaining: ${data.possible_count}`;
            
            // Display best guess
            bestGuessElement.textContent = data.best_guess || "No suggestion available";
            
            // Make best guess clickable
            bestGuessElement.onclick = function() {
                useWordAsNextGuess(data.best_guess);
            };
            
            // Clear previous suggestions
            suggestionsList.innerHTML = '';
            
            // Add other suggestions (excluding best guess)
            const otherSuggestions = data.suggestions.filter(word => word !== data.best_guess);
            otherSuggestions.forEach(word => {
                const li = document.createElement('li');
                li.textContent = word;
                li.onclick = function() {
                    useWordAsNextGuess(word);
                };
                suggestionsList.appendChild(li);
            });
            
            // Show results
            resultsDiv.classList.remove('hidden');
            
            // If only one word left, show a success message
            if (data.possible_count === 1) {
                bestGuessElement.textContent = data.best_guess.toUpperCase() + " (SOLVED!)";
                bestGuessElement.style.backgroundColor = "#6aaa64";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while solving. Please try again.');
        });
    });
    
    // Function to use a suggested word as the next guess
    function useWordAsNextGuess(word) {
        // Create a new row if needed
        let lastRow = guessesContainer.querySelector('.guess-row:last-child');
        const lastInput = lastRow.querySelector('.word');
        
        // If the last row already has content, create a new row
        if (lastInput.value.trim() !== '') {
            lastRow = createGuessRow();
            guessesContainer.appendChild(lastRow);
            setupGuessRow(lastRow);
        }
        
        // Set the word in the input field
        const input = lastRow.querySelector('.word');
        input.value = word;
        
        // Trigger the input event to update the letter displays
        const event = new Event('input', { bubbles: true });
        input.dispatchEvent(event);
        
        // Scroll to the new row
        lastRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Focus on the first letter display for marking
        const firstLetterDisplay = lastRow.querySelector('.letter-display');
        if (firstLetterDisplay) {
            setTimeout(() => {
                firstLetterDisplay.focus();
            }, 300);
        }
    }
    
    // Function to create a new guess row
    function createGuessRow() {
        const row = document.createElement('div');
        row.className = 'guess-row';
        
        row.innerHTML = `
            <div class="word-input">
                <input type="text" class="word" maxlength="5" placeholder="Enter 5-letter word">
            </div>
            <div class="result-input">
                <div class="letter-result" data-index="0">
                    <div class="letter-display" tabindex="0"></div>
                </div>
                <div class="letter-result" data-index="1">
                    <div class="letter-display" tabindex="0"></div>
                </div>
                <div class="letter-result" data-index="2">
                    <div class="letter-display" tabindex="0"></div>
                </div>
                <div class="letter-result" data-index="3">
                    <div class="letter-display" tabindex="0"></div>
                </div>
                <div class="letter-result" data-index="4">
                    <div class="letter-display" tabindex="0"></div>
                </div>
            </div>
        `;
        
        return row;
    }
    
    // Function to set up event listeners for a guess row
    function setupGuessRow(row) {
        const wordInput = row.querySelector('.word');
        const letterDisplays = row.querySelectorAll('.letter-display');
        
        // Update letter displays when word input changes
        wordInput.addEventListener('input', function() {
            const word = this.value.toUpperCase();
            
            // Update letter displays
            for (let i = 0; i < 5; i++) {
                letterDisplays[i].textContent = word[i] || '';
            }
        });
        
        // Toggle letter status on click - using only mousedown to prevent double triggering
        letterDisplays.forEach(display => {
            // Use a flag to track if we're handling a touch event
            let touchHandled = false;
            
            // For mouse users - only trigger on mousedown, not on click
            display.addEventListener('mousedown', function(e) {
                // Skip if this was triggered by a touch event
                if (touchHandled) return;
                
                e.preventDefault();
                cycleLetterStatus(this);
                e.stopPropagation();
            });
            
            // For touch devices
            display.addEventListener('touchend', function(e) {
                touchHandled = true;
                setTimeout(() => { touchHandled = false; }, 300); // Reset after a short delay
                
                e.preventDefault();
                cycleLetterStatus(this);
                e.stopPropagation();
            });
            
            // Prevent click from firing after mousedown
            display.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
            });
            
            // Allow keyboard navigation and activation
            display.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    cycleLetterStatus(this);
                }
            });
        });
    }
    
    // Separate function to cycle letter status
    function cycleLetterStatus(element) {
        // Only allow toggling if there's a letter
        if (!element.textContent.trim()) return;
        
        // Find current status
        let currentIndex = 0;
        for (let i = 0; i < statuses.length; i++) {
            if (element.classList.contains(statuses[i])) {
                currentIndex = i;
                break;
            }
        }
        
        // Remove current status
        if (statuses[currentIndex]) {
            element.classList.remove(statuses[currentIndex]);
        }
        
        // Add next status
        const nextIndex = (currentIndex + 1) % statuses.length;
        if (statuses[nextIndex]) {
            element.classList.add(statuses[nextIndex]);
        }
    }
});
