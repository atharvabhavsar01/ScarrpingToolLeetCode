# LeetCode Scraper

A Python-based script to scrape problem data from LeetCode and save it locally as a JSON file.

## Features
- Fetches latest LeetCode problem data via GraphQL API.
- Saves the fetched questions into a JSON file.
- Logs progress and errors to the console for debugging.

## Requirements
- Python 3.8+
- `pip` (Python package manager)
- An active internet connection

## Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

- **Windows (PowerShell)**
```bash
venv\Scripts\Activate
```

- **MacOS/Linux**
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the scraper**
```bash
python main.py
```

## Output
- The fetched questions will be saved into `leetcode_questions.json` in the project root directory.

## Notes
- Do **NOT** commit the `venv/` folder to git. Instead, use `.gitignore` to exclude it.
- The script uses LeetCode's public API, which may change without notice. If the query fails, check the API's latest schema.

## License
This project is licensed under the MIT License.
