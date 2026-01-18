# AI Agent Sample

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to the `.env` file
   - Get your API key from [Anthropic Console](https://console.anthropic.com/settings/keys)

## Running the Application

```bash
python main.py
```

## Security Note

- Never commit your `.env` file to version control
- The `.env` file is already listed in `.gitignore` to prevent accidental commits
- Use `.env.example` as a template for required environment variables
