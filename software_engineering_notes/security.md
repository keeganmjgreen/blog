# Security

## API Keys and Tokens

An **API key** serves as long-lived authentication of an application that must be manually revoked. An `apiKey` can be specified in a query parameter, header, or cookie.

A **bearer token** (e.g., JSON Web Token, Opaque token, Refresh token) serves to authenticate a user only and should automatically expire at the end of the user's session. A bearer token can be specified in a `"Authorization": "Bearer <token>"` header.

API keys and tokens must be securely transmitted (via HTTPS) and securely stored. Servers must verify the token if it is signed and check expiration and revocation statuses.

### JSON Web Token (JWT)

JSON Web Token (JWT) is an optionally-signed, optionally-encrypted representation of some security claim, for example, that a specific user has authenticated themself / logged in as admin. When a user logs in, the client (e.g., the user's web browser) sends an HTTP request and the server responds with the JWT. The client can then provide the JWT, when making subsequent requests to the server, to show that they are authenticated.

A JWT consists of a header, payload, and signature:

- The header is a JSON object that specifies the signing algorithm used to generate the signature, and that the token is a JWT.

- The payload is a JSON object that contains the security claims.

- The signature proves that the server generated the JWT. The server generates a JWT by encrypting the header and payload using the signing algorithm and with a secret that only the server knows.

Only the server can generate the JWT because only it knows the secret. The secret cannot be reverse-engineered from the JWT because the signing algorithm is irreversible. The server can check whether it issued a JWT provided by a client by taking its header and payload and running them through the signing algorithm (specified in the header) with the secret, and checking that the resulting signature matches.

If the secret is a private key, and the client knows the corresponding public key, then the client can also verify the server's identity. This follows an *asymmetric key algorithm*. In an archaic *symmetric key algorithm*, the client would also know the private key, by which they would be able to verify that a JWT's claim(s) were sent by the server.

## OAuth2

OAuth2 is a specification that defines ways to authenticate and authorize users.

It enables a user to safely authenticate with a third party. For example, authorizing an app or website to access your Google account data, without giving them your Google login credentials. It can also be used to log into an app or website via Google.

OAuth2 does not specify encryption, assumes HTTPS.

OAuth1 was very different, more complex, and specified encryption.

# References

- [What is a Bearer Token? Understanding API Authentication](https://blog.postman.com/what-is-a-bearer-token/)
- [JSON Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token)
- [Public-key_cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)
