import g4f
from undetected_chromedriver import Chrome, ChromeOptions
from g4f.Provider import (
    Bard,
    Poe,
    AItianhuSpace,
    MyShell,
    PerplexityAi,
)

options = ChromeOptions()
options.add_argument("--incognito")
webdriver = Chrome(options=options, headless=True)
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    provider=g4f.Provider.PerplexityAi,
    messages=[{"role": "user", "content": "Are you GPT4?"}],
        proxy="http://127.0.0.1:10809",
    webdriver=webdriver
)
print(response)
webdriver.quit()