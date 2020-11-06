# Import
import Textharvester.textharvester as th

# Initialize Textharvester
downloader = th.TextHarvester()

# Start Downloading
#   Infile: File name of text files with links (link+\n)
#   Outfilecontent: File name of exported content.
#   Outfiledonelinks: File name of export links list from which the content was downloaded
#   Overwritecontent: Overwrite outfilecontent?
#   Overwritelinks: Overwrite outfiledonelinks?
#   Threads: How many threads do you want to run at a time?

downloader.downloader(
    infile="collected_links.txt",
    outfilecontent="content_out.txt",
    outfiledonelinks="links_downloaded_from.txt",
    overwritecontent=False,
    overwritelinks=False,
    threads=25,
)
