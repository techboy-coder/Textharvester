from boilerpipe.extract import Extractor
import tqdm
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import re
import requests
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool
from sys import stdout
import random
import collections
import warnings

warnings.filterwarnings("ignore")


def webpage_miner(url):
    """Tries to return content from url/site as a string

    Args:
        url (str): Get the content from this url

    Returns:
        str: Content from url
    """
    try:
        URL = str(url)
        extractor = Extractor(extractor="ArticleExtractor", url=URL)
        out = extractor.getText()
        return [str(out), url]
    except Exception as e:
        pass


def flatten(xs):
    result = []
    if isinstance(xs, (list, tuple)):
        for x in xs:
            result.extend(flatten(x))
    else:
        result.append(xs)
    return result


class TextHarvester:
    def __init__(
        self,
        starturls="example.com",
        forcedomains=False,
        alloweddomainslist=[],
        depth=1,
        removepercent=None,
        limittotal=300,
    ):
        """This is a class to quickly crawl the internet for links and optionally save them

        Args:
            starturls (str, list): [Url/s to start crawling from]. Defaults to "http://example.webscraping.com/".
            forcedomains (bool, optional): [Do you want all crawling to be limited on domains defined in alloweddomainslist?]. Defaults to False.
            alloweddomainslist (list, optional): [Only crawl these urls. Only works if forcedomains is True]. Defaults to [].
            depth (int, optional): [How many layers deep do you want to crawl the web]. Defaults to 1.
            removepercent ([type], optional): [Randomly removes percent (0 to 1) from urls]. Defaults to None.
            limittotal (int, optional): [Max queue of urls. Good idea to keep low (100 - 600) for quick crawling]. Defaults to 300.
        """
        # Starturl
        if type(starturls) == str:
            self.starturls = [starturls]
        elif type(starturls) == list:
            self.starturls = starturls
        else:
            print("[-] Please Change Starturls to a String or List of Strings.")
            self.starturls = "http://example.webscraping.com/"

        # Depth
        self.depth = depth if type(depth) == int else 1

        # removepercent
        if type(removepercent) == float:
            if removepercent > 0 and removepercent < 1:
                self.removepercent = removepercent
        else:
            self.removepercent = 0.5

        # Limittotal
        if type(limittotal) == int and limittotal > 0:
            self.limittotal = limittotal
        elif limittotal is None:
            self.limittotal = None
        else:
            print(
                "[-] Limittotal can only be None or a number above 0. Setting to 300."
            )
            self.limittotal == 300
        # Alloweddomains
        self.alloweddomains = alloweddomainslist
        for i, j in enumerate(self.alloweddomains):
            self.alloweddomains[i] = urlparse(j).netloc

        # Forcedomains

        self.forcedomains = forcedomains

    # This function gets all urls on a webpage.
    def single_crawl(self, urlitem: str):
        """This function gets all urls on a webpage.

        Args:
            urlitem (str): Webpage to get all urls on

        Returns:
            list: Return a list of all found links ("a"-tags) on webpage.
        """
        # print("Item: ", urlitem)
        try:
            hdr = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 ",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
                "Accept-Encoding": "none",
                "Accept-Language": "en-US,en;q=0.8",
                "Connection": "keep-alive",
            }
            try:
                req = Request(urlitem, headers=hdr)
                html_page = urlopen(req)
                soup = BeautifulSoup(html_page, "lxml")
                links = [
                    requests.compat.urljoin(urlitem, link.get("href"))
                    for link in soup.findAll("a")
                ]
                links = [x for x in links if "#" not in x]
            except Exception as e:
                # print(e)
                pass
            return links

        except:
            pass

    # The following functions are only helper functions for single_crawl() and multicrawl()
    # They are not made to be used separatly.

    def flatten_list(self, l: list):
        result = []
        if isinstance(l, (list, tuple)):
            for x in l:
                result.extend(flatten(x))
        else:
            result.append(l)
        return result

    def rem_duplicate(self, l: list):
        return list(set(l))

    def rem_nones(self, l: list):
        return [x for x in l if x is not None]

    def remove(self, l, n):
        return random.sample(l, int(len(l) * (1 - n)))

    # Main function which you will be running

    def harvest(
        self, threads=10, write="harvested_links.txt", overwrite=True, doreturn=False
    ):
        """Main crawl function

        Args:
            threads (int): [description]
            write (None/False or Filename.txt): Do you want to write your results to a file. Format: Links + \n
            overwrite (bool): Append or Overwrite File
            doreturn (bool): Return list of collected urls from function?
        """
        # Init
        depth = self.depth
        limittotal = self.limittotal
        linkslist = self.starturls
        linkstotal = []
        alloweddomains = self.alloweddomains
        stored_exception = False
        try:
            for cnt in range(depth):
                print("\n")
                print("RECURSIVE EXPLORATION DEPTH: {}\r".format(cnt + 1), end="")
                print("\n")
                lnt = len(linkslist)
                if lnt > limittotal:
                    lnt = limittotal
                    linkslist = linkslist[0:lnt]
                pool = ThreadPool(threads)
                for subcount, i in enumerate(
                    pool.imap_unordered(self.single_crawl, linkslist)
                ):
                    try:
                        if self.forcedomains:
                            try:
                                for j in alloweddomains:
                                    i = [x for x in i if j in x]
                            except:
                                pass
                        linkslist.append(i)
                        proc = "{}/{}".format(subcount, lnt)
                        try:
                            print("\r{} Harvesting...".format(proc), end="  ", sep="")
                        except:
                            pass
                        if subcount >= limittotal:
                            break
                    except Exception as e:
                        pass

                pool = None
                linkslist = self.flatten_list(linkslist)
                # linkslist = flatten(linkslist)
                linkslist = self.rem_duplicate(linkslist)
                linkslist = self.rem_nones(linkslist)
                # linkslist = [s for s in linkslist if any(x in s for x in alloweddomains)]
                linkstotal.extend(linkslist)
                linkstotal = list(set(linkstotal))
                # linkstotal = self.rem_duplicate(linkslist)
                random.shuffle(linkslist)
                # print(len(linkslist))
                print("\n")
                print("Unique links collected till now: ", len(linkstotal))
                # print(type(self.removepercent))
                if not int(len(linkslist) * (1 - self.removepercent)) < 1:
                    # print(type(self.removepercent), ": ", self.removepercent)
                    linkslist = self.remove(linkslist, self.removepercent)
                if stored_exception:
                    break
        except KeyboardInterrupt:
            stored_exception = sys.exc_info()
        linkstotal = self.rem_duplicate(linkstotal)
        print("Total unique links:", len(linkstotal))
        if write is not None:
            o = "w" if overwrite else "a"
            with open("{}".format(str(write)), o, buffering=20 * 6) as f:
                for item in linkslist:
                    try:
                        f.write("%s\n" % item)
                    except:
                        pass
            print("File Saved as {}".format(str(write)))
        if doreturn:
            return linkslist

    def downloader(
        self,
        infile: str,
        outfilecontent: str,
        outfiledonelinks: str,
        overwritecontent: bool,
        overwritelinks: bool,
        threads: int,
    ):
        """[summary]

        Args:
            infile (str): Output txt file from webspider or text file with links with format linkurl + \n
            outfilecontent (str): Textfilename of downloaded content from urls from infile.
            outfiledonelinks (str): Textfilename of all urls from which content was downloaded.
            overwritecontent (bool): Overwrite outfilecontent if existing?
            overwritelinks (bool): Overwrite outfiledonelinks if existing?
            threads (int): How many threads. To many may crash the system. 30 Threads worked for me
        """
        donelist = []
        writelist = []
        all_links = open("{}".format(infile)).read().split("\n")
        all_links = list(set(all_links))

        p = Pool(threads)
        inlist = all_links
        random.shuffle(inlist)
        lnt = len(inlist)
        for cnt, i in enumerate(p.imap(webpage_miner, inlist)):
            proc = "{}/{}".format(cnt, lnt)
            try:
                print("\r{} Writing...".format(proc), end="  ", sep="")
            except:
                pass
            try:
                writelist.append(i[0])
                donelist.append(i[1])
            except:
                pass

        print("Total Length:", len(writelist))
        ocontent = "w" if overwritecontent else "a"
        with open("{}".format(outfilecontent), ocontent, buffering=200 * 6) as f:
            for item in writelist:
                try:
                    f.write("%s\n" % item)
                except:
                    pass
        olinks = "w" if overwritelinks else "a"
        with open("{}".format(outfiledonelinks), olinks, buffering=200 * 6) as n:
            for item in donelist:
                try:
                    n.write("%s\n" % item)
                except:
                    pass
        print("File Saved")
        print("Done")
