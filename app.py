from flask import Flask, render_template, request, jsonify
import json
import os
import collections
import math

app = Flask(__name__)

# Load word list
def load_words():
    # Check if we have the downloaded word list
    if os.path.exists('words_alpha.txt'):
        words = []
        with open('words_alpha.txt', 'r') as f:
            for word in f:
                word = word.strip().lower()
                if len(word) == 5 and word.isalpha():
                    words.append(word)
        
        # Save processed list for faster loading next time
        with open('word_list.json', 'w') as f:
            json.dump(words, f)
        
        return words
    
    # If not, check if we have a processed word list
    if os.path.exists('word_list.json'):
        with open('word_list.json', 'r') as f:
            return json.load(f)
    
    # If not, create one from system dictionary if available
    words = []
    try:
        with open('/usr/share/dict/words', 'r') as f:
            for word in f:
                word = word.strip().lower()
                if len(word) == 5 and word.isalpha():
                    words.append(word)
    except FileNotFoundError:
        # Fallback to a small sample list
        words = ["about", "above", "abuse", "actor", "adapt", "admit", "adopt", "after", "again", "agree", 
                "ahead", "alarm", "album", "alert", "alike", "alive", "allow", "alone", "along", "alter", 
                "among", "anger", "angle", "angry", "apart", "apple", "apply", "arena", "argue", "arise", 
                "array", "aside", "asset", "avoid", "award", "aware", "badly", "baker", "bases", "basic", 
                "basis", "beach", "began", "begin", "begun", "being", "below", "bench", "billy", "birth", 
                "black", "blame", "blind", "block", "blood", "board", "boost", "booth", "bound", "brain", 
                "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke", "brown", "build", 
                "built", "buyer", "cable", "calif", "carry", "catch", "cause", "chain", "chair", "chart", 
                "chase", "cheap", "check", "chest", "chief", "child", "china", "chose", "civil", "claim", 
                "class", "clean", "clear", "click", "clock", "close", "coach", "coast", "could", "count", 
                "court", "cover", "craft", "crash", "cream", "crime", "cross", "crowd", "crown", "curve", 
                "cycle", "daily", "dance", "dated", "dealt", "death", "debut", "delay", "depth", "doing", 
                "doubt", "dozen", "draft", "drama", "drawn", "dream", "dress", "drill", "drink", "drive", 
                "drove", "dying", "eager", "early", "earth", "eight", "elite", "empty", "enemy", "enjoy", 
                "enter", "entry", "equal", "error", "event", "every", "exact", "exist", "extra", "faith", 
                "false", "fault", "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed", 
                "flash", "fleet", "floor", "fluid", "focus", "force", "forth", "forty", "forum", "found", 
                "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny", "giant", "given", 
                "glass", "globe", "going", "grace", "grade", "grand", "grant", "grass", "great", "green", 
                "gross", "group", "grown", "guard", "guess", "guest", "guide", "happy", "harry", "heart", 
                "heavy", "hence", "henry", "horse", "hotel", "house", "human", "ideal", "image", "index", 
                "inner", "input", "issue", "japan", "jimmy", "joint", "jones", "judge", "known", "label", 
                "large", "laser", "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal", 
                "level", "lewis", "light", "limit", "links", "lives", "local", "logic", "loose", "lower", 
                "lucky", "lunch", "lying", "magic", "major", "maker", "march", "maria", "match", "maybe", 
                "mayor", "meant", "media", "metal", "might", "minor", "minus", "mixed", "model", "money", 
                "month", "moral", "motor", "mount", "mouse", "mouth", "movie", "music", "needs", "never", 
                "newly", "night", "noise", "north", "noted", "novel", "nurse", "occur", "ocean", "offer", 
                "often", "order", "other", "ought", "paint", "panel", "paper", "party", "peace", "peter", 
                "phase", "phone", "photo", "piece", "pilot", "pitch", "place", "plain", "plane", "plant", 
                "plate", "point", "pound", "power", "press", "price", "pride", "prime", "print", "prior", 
                "prize", "proof", "proud", "prove", "queen", "quick", "quiet", "quite", "radio", "raise", 
                "range", "rapid", "ratio", "reach", "ready", "refer", "right", "rival", "river", "robin", 
                "roger", "roman", "rough", "round", "route", "royal", "rural", "scale", "scene", "scope", 
                "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet", "shelf", 
                "shell", "shift", "shirt", "shock", "shoot", "short", "shown", "sight", "since", "sixth", 
                "sixty", "sized", "skill", "sleep", "slide", "small", "smart", "smile", "smith", "smoke", 
                "solid", "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed", "spend", 
                "spent", "split", "spoke", "sport", "staff", "stage", "stake", "stand", "start", "state", 
                "steam", "steel", "stick", "still", "stock", "stone", "stood", "store", "storm", "story", 
                "strip", "stuck", "study", "stuff", "style", "sugar", "suite", "super", "sweet", "table", 
                "taken", "taste", "taxes", "teach", "teeth", "terry", "texas", "thank", "theft", "their", 
                "theme", "there", "these", "thick", "thing", "think", "third", "those", "three", "threw", 
                "throw", "tight", "times", "tired", "title", "today", "topic", "total", "touch", "tough", 
                "tower", "track", "trade", "train", "treat", "trend", "trial", "tried", "tries", "truck", 
                "truly", "trust", "truth", "twice", "under", "undue", "union", "unity", "until", "upper", 
                "upset", "urban", "usage", "usual", "valid", "value", "video", "virus", "visit", "vital", 
                "voice", "waste", "watch", "water", "wheel", "where", "which", "while", "white", "whole", 
                "whose", "woman", "women", "world", "worry", "worse", "worst", "worth", "would", "wound", 
                "write", "wrong", "wrote", "yield", "young", "youth"]
    
    # Save processed list
    with open('word_list.json', 'w') as f:
        json.dump(words, f)
    
    return words

print("Loading word list...")
WORDS = load_words()
print(f"Loaded {len(WORDS)} 5-letter words")

# Common starting words that are generally good first guesses
STARTER_WORDS = ["crane", "adieu", "stare", "roate", "raise", "slate", "trace", "salet", "caret", "soare"]

@app.route('/')
def index():
    return render_template('index.html')

def calculate_letter_frequencies(words):
    """Calculate letter frequencies in the given word list"""
    letter_freq = collections.defaultdict(int)
    for word in words:
        # Count each letter only once per word
        for letter in set(word):
            letter_freq[letter] += 1
    return letter_freq

def calculate_position_frequencies(words):
    """Calculate letter frequencies by position in the given word list"""
    position_freq = [collections.defaultdict(int) for _ in range(5)]
    for word in words:
        for i, letter in enumerate(word):
            position_freq[i][letter] += 1
    return position_freq

def calculate_word_score(word, letter_freq, position_freq, possible_words):
    """Calculate a score for a word based on letter frequencies and uniqueness"""
    # Avoid words with repeated letters for maximum information gain
    unique_letters = set(word)
    if len(unique_letters) < len(word):
        penalty = 1.0 - (len(unique_letters) / len(word)) * 0.5
    else:
        penalty = 1.0
    
    # Score based on letter frequencies
    letter_score = sum(letter_freq[letter] for letter in unique_letters)
    
    # Score based on position frequencies
    position_score = sum(position_freq[i][letter] for i, letter in enumerate(word))
    
    # Combine scores
    return (letter_score + position_score * 0.5) * penalty

def get_best_guess(possible_words, previous_guesses=None):
    """Get the best next guess based on the current possible words"""
    if not previous_guesses:
        previous_guesses = []
    
    # If this is the first guess, return a good starter word
    if not previous_guesses and len(possible_words) > 100:
        for starter in STARTER_WORDS:
            if starter in possible_words:
                return starter
        # If no starter words in possible_words, continue with algorithm
    
    # If only a few words left, just return the first one
    if len(possible_words) <= 2:
        return possible_words[0]
    
    # Calculate letter frequencies
    letter_freq = calculate_letter_frequencies(possible_words)
    position_freq = calculate_position_frequencies(possible_words)
    
    # Score each word
    word_scores = []
    for word in possible_words:
        if word in previous_guesses:
            continue  # Skip words we've already guessed
        score = calculate_word_score(word, letter_freq, position_freq, possible_words)
        word_scores.append((word, score))
    
    # Sort by score (highest first)
    word_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return the highest scoring word
    return word_scores[0][0] if word_scores else possible_words[0]

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    guesses = data.get('guesses', [])
    
    # Start with all words
    possible_words = WORDS.copy()
    previous_guesses = []
    
    for guess in guesses:
        word = guess['word'].lower()
        previous_guesses.append(word)
        result = guess['result']
        
        # Filter words based on the feedback
        new_possible = []
        for candidate in possible_words:
            valid = True
            
            # Check each position
            for i in range(5):
                letter = word[i]
                
                # Green - letter must be in this position
                if result[i] == 'correct':
                    if candidate[i] != letter:
                        valid = False
                        break
                
                # Yellow - letter must be in the word but not in this position
                elif result[i] == 'present':
                    if letter not in candidate or candidate[i] == letter:
                        valid = False
                        break
                
                # Gray - letter must not be in the word
                # (unless it appears elsewhere in the word and is marked as correct or present)
                elif result[i] == 'absent':
                    # Check if this letter appears elsewhere in the guess with a different result
                    appears_elsewhere = False
                    for j in range(5):
                        if i != j and word[j] == letter and (result[j] == 'correct' or result[j] == 'present'):
                            appears_elsewhere = True
                            break
                    
                    # If it doesn't appear elsewhere with a different result, it shouldn't be in the candidate
                    if not appears_elsewhere and letter in candidate:
                        valid = False
                        break
            
            if valid:
                new_possible.append(candidate)
        
        possible_words = new_possible
    
    # Get the best next guess
    best_guess = get_best_guess(possible_words, previous_guesses) if possible_words else ""
    
    # Suggest the next best guesses (including the best one)
    suggestions = possible_words[:10]
    
    return jsonify({
        'possible_count': len(possible_words),
        'suggestions': suggestions,
        'best_guess': best_guess
    })

if __name__ == '__main__':
    # In production, debug should be False
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
