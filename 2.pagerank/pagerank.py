import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    keys = corpus.keys()
    res = {}
    for key in keys:
        res[key] = 0
    if corpus[page]:
        for linkpage in corpus[page]:
            res[linkpage] = damping_factor / len(corpus[page])
        for key in keys:
            res[key] += (1 - damping_factor) / len(keys)
    else:
        for key in keys:
            res[key] = 1 / len(keys)
    return res
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    start = random.choice(pages)
    samples = {}
    for page in pages:
        samples[page] = 0
    samples[start] += 1
    for i in range(1, n):
        model = transition_model(corpus, start, damping_factor)
        nextpage = random.choices(list(model.keys()), list(model.values()))[0]
        samples[nextpage] += 1
        start = nextpage
    for page in pages:
        samples[page] /= n
    return samples
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    n = len(pages)
    ranks = {}
    for page in pages:
        if corpus[page] == set():
            corpus[page] = set(pages) #A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
    for page in pages:
        ranks[page] = 1 / n
    while True:
        newranks = {}
        for page in pages:
            newranks[page] = (1 - damping_factor) / n
            for key in pages:
                if page in corpus[key]:
                    newranks[page] += damping_factor * ranks[key] / len(corpus[key])
            if (newranks[page] == (1 - damping_factor) / n):
                newranks[page] = 1 / n
        if all(abs(newranks[page] - ranks[page]) < 0.001 for page in pages):
            return newranks
        ranks = newranks
    #raise NotImplementedError


if __name__ == "__main__":
    main()
