# HTTP-MySQL-Connection-Server

Wanted to create a project early in 2019 - so here it comes!

Simple Python3 HTTP Server, that connects to a MySQL database and will (soon) be able to perform simple CRUD operations

# How to use it?

Well, in its current version, it expects POST request with data in either JSON or urlencoded format. The request must contain two fields - type and query (both lowercase). 

# Type

It's quite easy:
  0 - SELECT
  1 - [will very soon be] INSERT
  
Enjoy!
