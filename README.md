# Mochi to Anki Simple
A Python script for importing cards from Mochi to Anki.

## Prerequisites
- Python 3.7 or higher
- Mochi Pro Plan (required for API usage)
- Anki installed
- AnkiConnect plugin installed

## Setup
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
- Create a .env file in the project root
- Add your Mochi API key in the following format:
```
MOCHI_API_KEY="your_api_key"
```

## Usage
1. Log in to Mochi and retrieve your API key (Settings > API).
2. Start Anki and ensure AnkiConnect is enabled.
3. Run the script with the following command:
```bash
python main.py
```

## Script Process
1. Retrieve all deck information from Mochi.
2. Fetch all card information from each deck asynchronously.
3. Save the retrieved card data temporarily as a JSON file in the output/ directory.
4. Convert the JSON data to CSV format for Anki:
- Separate CSV files are created for each deck.
- Format: Question, Answer
- Save location: output/deck/deck_name.csv
5. Import the decks into Anki using AnkiConnect.

## Output Files
- JSON file: output/mochi_cards_full_data_[YYYYMMDDHHMM].json
- - Example: mochi_cards_full_data_202501221521.json
- CSV files: output/deck/[deck_name].csv
  - Separate CSV files are generated for each deck.

## File Structure
- main.py: Main script that orchestrates the entire process.
- get_all_mochi_cards.py: Retrieves deck and card information using Mochi API.
- export_mochi_cards_json.py: Temporarily saves fetched card data in JSON format.
- export_formatted_cards_csv.py: Converts JSON data to Anki-compatible CSV format.
- import_to_anki.py: Imports data into Anki using AnkiConnect.
- config.py: Configuration file.
- requirements.txt: List of required Python packages.
- output/: Directory for generated JSON and CSV files.
  - deck/: Subdirectory for converted CSV files.
