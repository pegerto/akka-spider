import time

import argparse
import requests
import logging
import random

from urlparse import urljoin, urlparse
from pykka import ThreadingActor, ActorRegistry
from bs4 import BeautifulSoup
from graphviz import Digraph

logger = logging.getLogger()
logging.basicConfig(filename='spider.log', level=logging.INFO)

class Queue(ThreadingActor):
    def __init__(self):
        super(Queue, self).__init__()
        self.queue = set()

    def push(self, url):
        self.queue.add(url)

    def pop(self):
        return self.queue.pop()

    def size(self):
        return len(self.queue)


class Downloader(ThreadingActor):
    def __init__(self, queue):
        super(Downloader, self).__init__()
        self.queue = queue

    def download(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                resources = map(lambda extracted_url: self._normalize(url, extracted_url), self._extract(r.text))
                for item in resources:
                    self.queue.push((url, item))
            else:
                logger.debug("Page return a unexpected status code %s", r.status_code)
        except requests.ConnectionError as e:
            logger.debug('Error connecting to %s web link inconsistent: (%s)', requests, e.message)

    @staticmethod
    def _extract(html):
        soup = BeautifulSoup(html, 'html.parser')
        resources = set()

        for tag, argument in [('a', 'href'), ('img', 'src'), ('link', 'href')]:
            for el in soup.find_all(tag):
                resources.add(el.get(argument))

        return resources

    @staticmethod
    def _normalize(url, resource):
        return urljoin(url, resource)


def _aux_scape_dot(text):
    return text.replace(':', "").replace('.','_')


def scheduler(queue, downloaders, scheduler_strategy, exclusion_filter):
    dot = Digraph(comment='Result')
    visited = set()
    try:
        print('Press Ctr+C to abort')
        while True:
            if queue.size().get() > 0:
                url = queue.pop().get()
                if url[1] not in visited and exclusion_filter(url[1]):
                    dot.node(_aux_scape_dot(url[1]))
                    if url[0] != url[1]:
                        dot.edge(_aux_scape_dot(url[0]), _aux_scape_dot(url[1]))
                    id = scheduler_strategy()
                    logger.info("Sending %s to downloader %s",url[1], id)
                    downloaders[id].download(url[1]).get()

                    visited.add(url[1])
            else:
                time.sleep(5)

    except KeyboardInterrupt:
        pass

    return dot


def main():
    parser = argparse.ArgumentParser(
        description='Akka Spider')
    parser.add_argument('url',
                        help='URL seed, main url')

    parser.add_argument('-R', '--recursive-out-domain', action="store_true",
                        help='Continue recursion out of the domain')
    parser.add_argument('--ndownloaders', type=int, default=4, help='Number of downloaders')
    parser.add_argument('-w', '--write',  default='output.dot', help='Output file')
    args = parser.parse_args()

    if urlparse(args.url).scheme == '':
        raise Exception('Input url should contain scheme')
        return
    else:
        seed = [(args.url, args.url)]


    # Start actors
    queue = Queue.start().proxy()
    downloaders = map(
        lambda x: Downloader.start(queue).proxy()
        , range(args.ndownloaders))

    for url in seed:
        queue.push(url).get()

    if args.recursive_out_domain:
        exclusion_filter = lambda url: True
    else:
        exclusion_filter = lambda url: urlparse(url).netloc.endswith(urlparse(args.url).netloc)

    dot = scheduler(queue,
                    downloaders,
                    lambda: random.randrange(len(downloaders)),
                    exclusion_filter)

    with open(args.write, 'w') as f:
        f.write(dot.source)

    # Clean up
    ActorRegistry.stop_all()

if __name__ == '__main__':
    main()
