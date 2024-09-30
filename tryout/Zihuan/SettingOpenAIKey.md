# Setting OpenAI API Key On Your Computer

## On Mac

1. Open the terminal.
2. Set the environment variable temporarily (only for the session):
   > $ export OPENAI_API_KEY="your-api-key-here" '
3. Apply the changes:
   > $ source ~/.zshrc
4. Check
   > $ echo $OPENAI_API_KEY

## On Windows

1. Open Command Prompt (search for "cmd" in the Start menu).
2. Set the environment variable temporarily: set OPENAI_API_KEY="your-api-key-here"
3. Set it permanently:
   + Open Control Panel > System and Security > System.
   + Click Advanced system settings on the left.
   + In the System Properties window, click Environment Variables.
   + Under User variables, click New.
   + Set the Variable name to OPENAI_API_KEY and Variable value to your API key.
   + Click OK to save and apply the settings.
