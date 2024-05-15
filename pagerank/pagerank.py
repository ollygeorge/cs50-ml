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
    output = {}
    if len(corpus[page]) > 0:
        for linked_page in corpus:
            output[linked_page] = (1 - damping_factor) / len(corpus)
        for linked_page in corpus[page]:
            output[linked_page] += damping_factor/len(corpus[page])
    else:
        for page in corpus:
            output[page] = 1 / len(corpus)
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = []
    output = {}
    for page in corpus:
        pages.append(page)
        output[page] = 0
    initial_sample = random.choice(pages)
    distribution = transition_model(corpus, initial_sample, damping_factor)
    pages = []
    probability = []
    for page in distribution:
        output[page] = distribution[page]
        pages.append(page)
        probability.append(distribution[page])
    for i in range(n - 1):
        next_sample = random.choices(pages, probability)[0]
        distribution = transition_model(corpus, next_sample, damping_factor)
        pages = []
        probability = []
        for page in distribution:
            output[page] += distribution[page]
            pages.append(page)
            probability.append(distribution[page])
    for page in corpus:
        output[page] /= n
    return output


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    tolerance = 0.001
    output_iter = {}
    N = len(corpus)
    for page in corpus:
        output_iter[page] = 1/N
    
    iterations = 0
    while True:
        output_new = {}
        for page in corpus:
            sum_page_rank = 0
            for link in corpus:
                if page in corpus[link]:
                    sum_page_rank += output_iter[link] / len(corpus[link])
            output_new[page] = (1 - damping_factor) / len(corpus) + damping_factor * sum_page_rank

        # Check convergence
        converged = True
        for page in corpus:
            if abs(output_new[page]-output_iter[page]) > tolerance:
                converged = False
                break
        if converged:
            break

        output_iter = output_new
        iterations += 1

    # Normalize PageRank values to make sure they add to 1
    sum_page_rank = 0
    for page in corpus:
        print(output_iter[page])
        sum_page_rank += output_iter[page]

    output_normalized = {} 
    for page in corpus:
        output_normalized[page] = output_iter[page] / sum_page_rank

    return output_normalized





if __name__ == "__main__":
    main()
