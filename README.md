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


#### Implementation

Python is use for a simple reason, programming speed.

In addition good set of know libraries are used at this project, to speed up the implementation I use libraries that I know, but
those can be easy replace by native modules.

### Setup

```

```
pip install mock
pip install graphviz


dot -Tpng input.dot > output.png
