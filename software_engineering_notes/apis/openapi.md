# OpenAPI

[OpenAPI](https://www.openapis.org/what-is-openapi) is a standard for documenting:

- API keys.
- URL routes.
    - Supported HTTP methods.
    - Request parameters (payload JSON schemas, path and query parameters).
    - Response statuses and their meanings.
    - Response payload JSON schemas.

An OpenAPI Specification (OAS) is typically a YAML or JSON document.

An OAS can be used at all stages in an API's lifecycle:

- Requirements-building and API design: Supports drafting URL routes, methods, parameters, and responses without code or even choosing a language.

- Development: Supports generating boilerplate server code from the OAS, in many languages.

- Testing and usage: Documents the API in a standard, detailed way, whether the API is for an internal microservice or an external user. Allows generating client-side code.

- Maintenance: Makes it easy to keep the documentation up-to-date with the code and vice versa.

[Swagger](https://swagger.io/) is an commercial ecosystem that provides tools and enterprise support for the OpenAPI and AsyncAPI standards. When people say "Swagger API", they are referring to V3 of the OpenAPI standard, in which an OAS document is a `swagger_doc.yaml` file.

OpenAPI supports multiple security schemes, including an API key, bearer token HTTP Basic authentication, HTTP Digest, OAuth2, and OpenID Connect.

## Related

- [Arazzo](https://spec.openapis.org/arazzo/latest.html) is another OpenAPI standard, for documenting sequences of API calls to achieve certain goals (essentially, sequence diagrams).

- [Overlays](https://spec.openapis.org/overlay/v1.0.0.html) is another OpenAPI standard, for describing a set of changes or transformations to be applied or *overlaid* onto an OAS, such as to modify API descriptions before sharing with external users.

- [AsyncAPI](https://www.asyncapi.com/en) is a standard for documenting an event-driven architecture, including channels, operations, and components.
