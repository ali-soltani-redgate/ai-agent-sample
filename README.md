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

## Running Tests

Run tests from the project root directory using:

```bash
python -m pytest step_1_call_llm_directly/test_main.py
```

Or to run all tests with verbose output:

```bash
python -m pytest -v
```

### Why `python -m pytest`?

Using `python -m pytest` instead of just `pytest` is important because:

- **Adds current directory to PYTHONPATH**: Ensures Python can find your project modules
- **Uses correct interpreter**: Guarantees you're using the pytest installed in your virtual environment
- **Prevents import errors**: Avoids `ModuleNotFoundError` when importing project modules in tests

### Test Strategy

The tests use mocking to avoid calling the actual LLM API:

- **Faster execution**: No network calls or API latency
- **No costs**: Avoids consuming API credits during testing
- **Deterministic**: Tests produce consistent results
- **Offline testing**: Tests run without internet connection

The mocks verify that the LLM is called with correct parameters while allowing you to control the responses for predictable testing.

## Security Note

- Never commit your `.env` file to version control
- The `.env` file is already listed in `.gitignore` to prevent accidental commits
- Use `.env.example` as a template for required environment variables
