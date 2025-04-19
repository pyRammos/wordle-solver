# Wordle Solver

A Python-based web application that helps solve Wordle puzzles.

## Features

- Input your Wordle guesses and see the results
- Mark letters as correct (green), present (yellow), or absent (gray)
- Get suggestions for your next guess
- See how many possible words remain

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd wordle-solver
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Start the application:
```
python app.py
```

2. Open your web browser and go to `http://127.0.0.1:5000`

3. Enter your Wordle guesses and mark the results by clicking on each letter to cycle through the states:
   - Gray: Letter is not in the word
   - Yellow: Letter is in the word but in the wrong position
   - Green: Letter is correct and in the right position

4. Click "Solve" to get suggestions for your next guess

## Word List

The application uses a dictionary of 5-letter English words. By default, it will:
1. Try to use the system dictionary at `/usr/share/dict/words` (filtering for 5-letter words)
2. If that's not available, it will use a built-in list of common 5-letter words

## Deployment

### Traditional Deployment

To deploy this application to a production server:

1. Set up a web server (like Nginx or Apache)
2. Configure it to proxy requests to Gunicorn
3. Run the application with Gunicorn:
```
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

### Docker Deployment

You can also run this application using Docker:

1. Build the Docker image:
```
docker build -t wordle-solver .
```

2. Run the container:
```
docker run -p 5000:5000 wordle-solver
```

Or use Docker Compose:
```
docker-compose up -d
```

## License

This project is open source and available under the MIT License.
