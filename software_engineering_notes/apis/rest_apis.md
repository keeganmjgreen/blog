# REST APIs

REST stands for REpresentational State Transfer.

A *REST API*, or *RESTful API* is simply an API that follows the REST principles.

A REST API can use HTTP (most common) or any other communication protocol.

A REST API allows a client to perform stateless CRUD operations on resources via URL routes that are mapped to said resources.

REST principles do not specify an HTTP method for each CRUD operation, but the following are the de-facto standard:

- `POST` for creating a new resource.
- `GET` for reading resource(s).
- `PATCH` for partially updating a resource, `PUT` for fully updating.
- `DELETE` for deleting a resource.

Resource representations that are returned by the server should be defined as cacheable or non-cacheable, specifying whether the client can keep using an older one or they should send new requests for the latest resource representations.

Following HATEOAS (Hypermedia as the engine of application state), server responses should include hyperlinks to other, related resources for the sake of client convenience.

*Stateless* means that the server itself is stateless, does not store information in memory, and does not need to in order to handle requests. This means that the server can be scaled to multiple instances, any of which can handle any request.

Note: If the database in which resources' information is stored has replicas, then replication may need to be fast in order to handle subsequent write operations on the same resource across replicas, to avoid 404s or data inconsistencies.

## References

- [What is REST API?](https://cloud.google.com/discover/what-is-rest-api)
