# Textharvester

![](textharvester_logo.PNG)

> A simple tool that collects massive amounts of links and text data from the internet.

TextHarvester is an easy-to-use tool for collecting and crawling urls from the Internet and downloading website content from collected urls into a text file. TextHarvester can be used to efficiently collect a lot of text for general purpose nlp.

## How does it work?

TextHarvester is a depth-first algorithm.

1. Collect Urls:
   1. Collect links from starting website url.
   2. Randomly (based on your parameters) chooses links from previous step and repeats previous step.
2. Download Content from collected urls.

**Diagram**

![Erm? The image is not rendering.](Diagram.PNG)

## Installation

From Source:

```sh
git clone https://github.com/techboy-coder/Textharvester.git
cd Textharvester && pip install --upgrade -r requirements.txt -q && pip install .
```

## Usage example

### Crawling and Url Collection
In the example below, you can see how to quickly collect links from a website. The links will be saved and can be used later to download the content from each link.

```python
import Textharvester.textharvester as th
crawler = th.TextHarvester(
    starturls="https://startsite.com",
    forcedomains=True,
    alloweddomainslist=["https://en.startsite.com"],
    limittotal=80,
)
crawler.harvest(threads=50, write="outfile_urls.txt")
# > This will create a outfile_urls.txt file with all urls it has collected.

```



### Download Content
In the example below, you can see how to quickly download content from all collected urls in the form of a text file.

```python
import Textharvester.textharvester as th
downloader = th.TextHarvester()
downloader.downloader(
    infile="outfile_urls.txt",
    threads=25,
)
# > Will create to new text files. One with content and one with scraped websites.

```

**Important for Windows users: The TextHarvester instance must be initialized inside your main loop and the downloader method must run in the main loop!**

_For more examples and usage, please refer to the Examples Folder._

## Documentation
Google Colab: https://colab.research.google.com/drive/1vpVg_bQzoKjZNX3-7DMUJ_5zLnnhGIkC?usp=sharing

## Purpose and Ethics

TextHarvester is a great tool to harvest massive amouts of text data. Please feel free to use this tool in your project.
Please Note: I do not take any responsibility for anything you do with this tool.


## Meta

© 2020 - Techboy-Coder – (https://github.com/techboy-coder)
