from bs4 import BeautifulSoup as bs
import urllib2
import time
import cProfile

class BadInputError(Exception):
    pass


def main_game(link1, link2):
    # if not "wikipeida.org" in link1 or not "wikipedia.org" in link2:
    #     print "badinput"
    #     raise BadInputError("Not a valid wikipedia.org link")

    print "Starting at %s, Ending at %s" % (link1, link2)

    covered = []
    game_play_recursion(link1, link2, covered, 0)


def find_links(link, covered):
    """Finds other links, returns them in a list"""
    soup = bs(urllib2.urlopen(link).read())

    covered.append(extract_from_link(link))

    return [wiki.get('href') for wiki in soup.find_all('a')
            if wiki.get('href') and "/wiki/" in wiki.get('href')
            if "//" not in wiki.get('href')
            if "File" not in wiki.get('href')
            if "Wikipedia" not in wiki.get('href')
            if "Category" not in wiki.get('href')
            if "Talk" not in wiki.get('href')
            if "Special" not in wiki.get('href')
            if "Portal" not in wiki.get('href')
            if "Main_Page" not in wiki.get('href')
            if "Help" not in wiki.get('href')
            if extract(wiki.get('href')) not in covered]


def game_play_recursion(link1, link2, covered, depth, MAX_ALLOWED=5):
    if depth > MAX_ALLOWED:
        return None

    if link1 == link2:
        return link2

    links = find_links(link1, covered)

    for link in links:
        answer = game_play_recursion(next_link(link), link2, covered,
                                     depth+1, MAX_ALLOWED)
        if answer:
            print answer
            return answer

    return None


def extract(topic):
    """part of find_links"""
    return topic.replace('/wiki/', "")


def extract_from_link(link):
    """part of find_links"""
    return link.replace('http://en.wikipedia.org/wiki/', "")


def next_link(found):
    return "http://en.wikipedia.org" + found


def quick_test(link="http://en.wikipedia.org/wiki/Apple"):
    covered = []
    find_links(link, covered)


def simple():
    main_game("http://en.wikipedia.org/wiki/Yogurt", "http://en.wikipedia.org/wiki/Seleucid_Empire")


if __name__ == '__main__':
    cProfile.run('simple()', 'restats')
