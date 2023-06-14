# PROXY-SERVER

In this assignment, you will implement a web proxy that passes requests and data between multiple web clients and
web servers, concurrently (fork a process for each new client request). When you're done with the assignment, you
should be able to configure your web browser to use your personal proxy server as a web proxy that is capable of
handling the following tasks.
1. HTTP communications between client and server.
2. HTTPs communications between client and server.
3. Caching of popular content using at least two scheduling algorithms.
4. Content filtering (filtering rules should be configurable via admin console).
References:
 Guide to Network Programming Using Sockets
http://beej.us/guide/bgnet/
 HTTP Made Really Easy- A Practical Guide to Writing Clients and Servers
http://www.jmarshall.com/easy/http/
 Wikipedia page on fork()
https://en.wikipedia.org/wiki/Fork_(system_call)
