# Import
import Textharvester.textharvester as th

# Initialize Textharvester
#   Starturl: Where to start crawling from. [String or List]
#   Forcedomains & Alloweddomainslist: Do you want to only crawl specific domains? Specify here. [Bool; List]
#   Depth: How deep do you want to crawl the site/s? [Int]
#   Limittotal: How many sites in queue? It's a good idea to keep this under 300 for very quick crawling. [int]

crawler = th.TextHarvester(
    starturls="https://startsite.com",
    forcedomains=True,
    alloweddomainslist=["https://en.startsite.com"],
    depth=4,
    limittotal=80,
)

# Start Harvesting and Collecting Urls
#   Threads: How many urls do you want to crawl at a time? [Int]
#   Write: Where do you want to store all saved urls? [String]
#   Overwrite: Do you want to overwrite the file? [Bool]
crawler.harvest(threads=50, write="outfile_urls.txt", overwrite=True)
# > This will create a outfile_urls.txt file with all urls it has collected.
