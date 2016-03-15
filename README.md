## Akka Spider

### Abstract

This project implements a standard spider using reactive programming, modeling the default actors

- Queue: Models a queue of work that need to be scheduler
- Downloader: multiple downloader actors to do the heavy lifting, download extract and normalize the relations
- Scheduler: Take work from the queue and send it to the downloaders.

```

  +--------------+              +----------------+                       XXXX
  | Scheduler    |              |------------------+              XXXXXXXX  XX
  |              +------------> || Downloader    | |             XX    XX    X
  +--------------+              +----------------+ | <-----------+X Web      XX
     ^                           +-----------------+             X           XX
     |                                   |                        XXX  XXXXXXX
     |        +--------------+           |                          XXXX
     +--------+  Queue       | <---------+
              +--------------+


```

### Scope

The application is a long running application, in a production implementation will write the output over a db and
other actors. Other actor may review the DB and decide what needs to be resscan.

At this implementation we cover:

- Basic downloader (img , links )
- Round robin scheduler
- Simulate a queue

```spider.py``` implement a PoC for those actors.


### Implementation

Python is use for a simple reason, programming speed.

In addition good set of know libraries are used at this project, to speed up the implementation I use libraries that I know, but
those can be easy replace by native modules.

### Setup


1. Configure python virtual env
```
git clone https://github.com/pegerto/akka-spider.git
virtualenv .
source bin/activate

```

2. Python 2.7 required, not tested with other versions

3. Install dependencies

```
pip install mock
pip install graphviz
pip install requests
pip install pykka
pip install bs4
```

### Execute

The application provides a small cli


```
usage: spider.py [-h] [-R] [--ndownloaders NDOWNLOADERS] [-w WRITE] url

Akka Spider

positional arguments:
  url                   URL seed, main url

optional arguments:
  -h, --help            show this help message and exit
  -R, --recursive-out-domain
                        Continue recursion out of the domain
  --ndownloaders NDOWNLOADERS
                        Number of downloaders
  -w WRITE, --write WRITE
                        Output file
```


### Example

* There is only one parameter that is seed url.
* The downloader and scheduler is a long running thread a terminal interruption is required to end.
* The output is write under ```output.dot``` if you ```-w``` is not present

```
python akka-spider/spider.py http://bbc.co.uk
cat output.dot
// Result
digraph {
	"http//bbc_co_uk"
[...]

```

Visualize the oput by converting the dot into a png

```
dot -Tpng output.dot > output.png
```