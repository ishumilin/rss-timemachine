# RSS Time Machine

This script fetches and processes previously archived versions of a given website's RSS feed through the Wayback Machine. It handles retries, parses the RSS content, and outputs the final list of RSS entries as a JSON file.

## Features
- Retrieves archived RSS feed data from the Wayback Machine.
- Parses the RSS feed and extracts entries.
- Cleans up HTML content within the entries.
- Saves the processed entries to a JSON file.

## Prerequisites

- Python 3.x
- Required Python packages which can be installed using:
 ```sh
 pip install -r requirements.txt
 ```

## Usage

To use the script, run the following command:

```sh
python fetch_rss_feed.py [feed_url]
```

For example:
```sh
python fetch_rss_feed.py example.com/rss
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
