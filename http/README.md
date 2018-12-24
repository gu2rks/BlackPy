HTTP can be characterized as follows:
* Uses textual control messages 
* Transfers binary data files 
* Can download or upload data 
* Incorporates caching

four major request types:
* GET:
Requests a document; server responds by sending status information followed by a copy of the document
* HEAD:
Requests status information; server responds by sending status information, but does not send a copy of the document
* POST:
Sends data to a server; the server appends the data to a specified item (e.g., a message is appended to a list)
* PUT:
Sends data to a server; the server uses the data to completely replace the specified item (i.e., overwrites the previous data)

GET request has the following form:
```
GET /item version CRLF
```
 * __item__ gives the URL for the item being requested, 
 * __version__ specifies a version of the protocol (usually HTTP/1.0 or HTTP/1.1).
 * __CRLF__ denotes two ASCII characters, carriage return and linefeed that are used to signify the end of a line of text.

```
 When using HTTP, a browser sends version information which allows a server to choose the highest version of the protocol that the browser and server both understand.
 ```

General format of lines in a basic response header:
```
HTTP/1.0 status_code status_string CRLF
Server: server_identification CRLF Last-Modified: date_document_was_changed CRLF Content-Length: datasize CRLF
Content-Type: document_type CRLF CRLF
````
# by runing getHeader.py