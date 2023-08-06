<h1 align="center">SEO Keyword Research Tool 🔎</h1>

A simple Python SEO keywords suggestion tool tracking from Google engine that pulls data from Autocomplete, People Also Ask and Related Searches.

This tool uses [SerpApi](https://serpapi.com/) as a tool to parse data from Google search results. You can use provided API key that will be available after installation, however, it's purely for testing purposes to see if the tool fits your needs. If you'll be using it for your own purpose (personal or commercial), you have to use [your own SerpApi key](https://serpapi.com/manage-api-key).

## ⚙️Installation

```bash
$ pip install seo-keyword-research-tool
```

```bash
$ git clone https://github.com/chukhraiartur/seo-keyword-research-tool.git
```


## 🤹‍♂️Usage

#### Available CLI arugments:

```bash
$ python main.py -h
```

```lang-none
Extract keywrods from: Google Autocomplete, People Also Ask, and People Also Search and saves data to CSV/JSON/TXT.

optional arguments:
  -h, --help            show this help message and exit
  -q , --query          Search query (required).
  -e , --engines        Choices of engines to extract: Autocomplete (ac), Related Searches (rs), People Also Ask (rq). All engines are selected by default.
  -dl , --depth-limit   Depth limit for People Also Ask. Default is 0, first 2-4 results.
  -st , --save-to       Saves the results in the current directory in the selected format (CSV, JSON, TXT). Default CSV.
  -ak , --api-key       Your SerpApi API key: https://serpapi.com/manage-api-key. Default is a test API key to test CLI.
  -gd , --domain        Google domain: https://serpapi.com/google-domains. Default google.com.
  -gl , --country       Country of the search: https://serpapi.com/google-countries. Default us.
  -hl , --lang          Language of the search: https://serpapi.com/google-languages. Default en.

Found a bug? Open issue: https://github.com/chukhraiartur/seo-keyword-research-tool/issues
```

The `--depth-limit` argument for People Also Ask can be set from `0` to `4`. For each depth limit value, the number of results returned grows exponentially. Below is a table showing how the depth limit argument is affected:

| Depth limit | Number of results | Explanation |
|-------------|-------------------|-------------|
| 0 | 4 | Standard results |
| 1 | 12 | 4*2 = 8 + 4 = 12 |
| 2 | 36 | 8*3 = 24 + 12 = 36 |
| 3 | 108 | 24*3 = 72 + 36 = 108 |
| 4 | 324 | 72*3 = 216 + 108 = 324 |

📌Note: This is how the logic works for the `google.com` domain, on other domains the results may differ.

#### Simple example:

```bash
$ python main.py -q "starbucks coffee"
```

```json
{
  "auto_complete": [
    "starbucks coffee menu",
    "starbucks coffee cups",
    "starbucks coffee sizes",
    "starbucks coffee mugs",
    "starbucks coffee gear",
    "starbucks coffee beans",
    "starbucks coffee near me",
    "starbucks coffee traveler"
  ],
  "related_searches": [
    "starbucks near me",
    "starbucks coffee price",
    "starbucks coffee beans",
    "starbucks company",
    "starbucks coffee menu",
    "starbucks merchandise",
    "starbucks coffee bags"
  ],
  "related_questions": [
    "What is the most popular Starbucks coffee?",
    "What is the number 1 Starbucks drink?",
    "What is the Tiktok coffee from Starbucks?",
    "Why is Starbucks coffee so famous?"
  ]
}
```

#### Advanced example

This example will use [related questions API](https://serpapi.com/related-questions) engine with a depth limit value of 2, and saves data to JSON:

```bash
$ python main.py --api-key <your_serpapi_api_key> \
> -q "starbucks coffee" \
> -e rq \
> -dl 2 \
> -gd google.co.uk \
> -gl uk \
> -hl en \
> -st json \
```

```json
{
  "related_questions": [
    "What is the best coffee in Starbucks?",
    "What is a popular Starbucks coffee?",
    "What is the number 1 Starbucks drink?",
    "Is Starbucks expensive?",
    "What should I try at Starbucks for the first time?",
    "Which Starbucks coffee is best and sweet?",
    "What is famous in Starbucks in India?",
    "Which Starbucks drink is the best in India?",
    "Why is Starbucks famous?",
    "What should I order in Starbucks?",
    "What is the least bitter coffee at Starbucks?",
    "What's the creamiest coffee?",
    "Which Starbucks coffee is best in taste?",
    "Which Starbucks coffee is best and sweet?",
    "Which Starbucks coffee is best in India?",
    "Which Starbucks coffee is best for first time?",
    "Why is Starbucks famous?",
    "What should I order at Starbucks for the first time?",
    "What is the best Starbucks drink for a first time coffee drinker?",
    "What should I order in Starbucks?",
    "What should I try at Starbucks for the first time?",
    "What is the most famous Starbucks drink?",
    "Which Starbucks coffee is best in taste?",
    "What coffee orders for beginners?",
    "What is the best thing to get at Starbucks?",
    "Which Starbucks drink is best?",
    "Which coffee is best in Starbucks India?",
    "Which Starbucks coffee is best in taste?",
    "Is Dunkin or Starbucks better?",
    "What are the negatives of Starbucks?",
    "Who has stronger coffee Starbucks or Dunkin?",
    "Why do people prefer Starbucks?",
    "Why is Starbucks so much better than Dunkin?",
    "Is Starbucks coffee high quality?",
    "Why is Starbucks coffee so good?",
    "Do Starbucks employees get free food?"
  ]
}
```


<p align="center";>Sponsored by <a href="https://serpapi.com/">SerpApi</a> 🧡</p>
