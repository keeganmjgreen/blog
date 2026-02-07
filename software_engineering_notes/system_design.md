
# System Design

## Design Factors

- Number of users
- Request volume
- Read versus write frequency
- Latency
- Availability
- Reliability
- Data consistency
- Regionality

## Common Design Principles

- Use multiple service instances behind a load balancer (LB) (e.g., in Kubernetes), to handle high request volume with high availability.

- Cache database requests to decrease latency and load.

- Use client-side storage/caching of recently accessed content to decrease latency.

- Retry only failed parts of a large operation, rather than the entire operation, to decrease latency and load.

- Use retry mechanisms to increase reliability.
    - Backoff to decrease latency first, then decrease load.

- Use a CDN co-located with ISP infrastructure for read-heavy data storage, low-latency distribution, and high availability/reliability.

## Examples

### Dropbox

#### Design Factors

- Number of users: 600 million
- Request volume: 1 billion
- Read versus write frequency: More reads than writes
- Latency: Low
- Availability: High
- Reliability: High
- Data consistency: High
- Regionality: Worldwide

#### Design

Client-side components:

- Webapp
- Mobile app
- Desktop app for local file sync
    - Need component that watches for local file changes

Server-side components:

- API servers behind LB
- SQL database behind cache
- File upload queue (for high reliability/availability)
- Synchronization service
- File change event queues with queue management service
- File server, e.g., Amazon S3 storage

Database design:

- Users table
    - One-to-many with file and folder metadata tables (although files and folders can be shared with other users)
- Registered client devices table
    - Many-to-many with users (via association table)
    - One-to-many with user sessions table

File transfers and retries would be chunked, for low latency and high reliability. Need "chunker" and "de-chunker" components (client-side only?).

The file transfer pattern is a star pattern, with client devices syncing with the central file server and metadata database, rather than also being able to sync with each other. This allows for high data consistency.

File change events allow devices (both client- and server-side file storage) to download only changes, not entire files, allowing for low latency. A component may be needed (server-side only?) to diff newly uploaded file versions into change events. Per-device queues of file change events allow devices (including the file server) to quickly get up-to-date after being offline for a bit, allowing for high availability. For data accuracy and due to the fact that changes may build on each other, individual events cannot expire. The queue for a client device is deleted if it has been inactive for too long or completely emptied if there are too many enqueued events. There are two reasons for this. Firstly, to save server space. Secondly, if the client device comes back online, it may have to process a lot of change events for the same file, which may be slower than just downloading the latest version, hence deleting the queue. The queue management service would create queues for newly registered devices and delete the queues of inactive devices.

The synchronization service would handle merge conflicts due to divergent changesets by creating file copies ("current" version and "incoming" version).

The file server may store files in chunks.

### Twitter

#### Design Factors

- Number of users: 300 million active per month
- Request volume: 6000 tweets sent per second, 600,000 tweets read per second
- Read versus write frequency: Read-heavy
- Latency: Low
- Availability: High
- Reliability: High
- Data consistency: Eventual consistency
- Regionality: Worldwide

Each tweet is small (limited number of characters) but there are billions of them.

#### Design

Client-side components:

- Webapp
- Mobile app
- Other clients (e.g., desktop)

Server-side components:

- API servers behind LB
- Tweet event queue
- SQL database behind cache (Can/should use NoSQL database for high availability/reliability eventual consistency?)
- Search service and database
- Trends service and database

Database design:

- Users table
    - One-to-many with tweets
    - Many-to-many with self (via followers/following association table)
- Tweets table indexed on user ID and creation/modification timestamp, sorted by creation/modification timestamp

New tweets are sent to tweet event queues, SQL database, search service, and possibly trends service.

Tweet events are queued for pushing to followers via websocket, as long as they do not have too many followers (e.g., celerities).

The search service uses an inverted full text index in which significant words are tokenized and each word/token is mapped to tweets that contain it. Search results are sorted in descending order of popularity and number of words matching the query.

The trends service computes and stores trending hashtags or topics. It maintains a tweet/view count per hashtag/topic, per location. Options:

- Update incrementally:

    - In real-time (event-driven, after a tweet is posted): Tweet/view counts per will be both read- and write-heavy, so new tweet events should be queued before writing. Kafka and Kafka connect can be used.

    - Periodically (e.g., every minute): Update tweet counts based on new tweets and update view counts based on recently enqueued view events (e.g., within the past minute).

    In order to store trending hashtags/topics within a certain timeframe (e.g., the past week), these counts would have to be time series data (e.g., stored for the past week). Otherwise, high-count hashtags/topics from a year ago would be included.

- Update absolutely and periodically (e.g., every minute): Update tweet/view counts based on historical tweets and views within a certain timeframe (e.g., the past week). A disadvantage of this is having to store view events.

### Netflix

#### Design Factors

- Number of users: 200M
- Request volume:
    - Per user (on average):
        - 2 hours worth of video per day
        - 45 GB/month
            - Reasonable: 1 GB/movie / 1.5 h/movie * 2 h/day * 30 d/month = 40 GB/month
    - 300K petabytes/year
- Read versus write frequency: Read-heavy
- Latency: Low
- Availability: High
- Reliability: High
- Data consistency: Eventual consistency
- Regionality: Worldwide

#### Design

Client-side components:

- Smart TV app
- Mobile app
- Webapp
- Desktop app

Server-side components:

- Microservices behind two tiers of LBs and in-memory cache
    - First LB routes to second-tier Availability Zone LBs using static algorithm (round robin)
    - Each second-tier LB routes to API servers using dynamic algorithm (based on traffic)
- SQL database behind cache
- Video management service
- CDN (Open Connect) with copies of videos
- Recommendation service
- Billing service

Database design:

- Accounts
    - One-to-many with profiles
        - One-to-many with:
            - Watch history (archived/compressed over time)
            - Ratings
            - Watchlist
- Titles metadata

Video management service:

- Enqueues Netflix-uploaded videos.
- Chunks videos.
- Converts videos/chunks to different bitrates/resolutions and video formats using parallel workers.
- Stores videos/chunks in AWS S3.
- Distributes throughout the CDN.

### Event Ticketing System

Unsold tickets must be locked while a user is looking at buying them, until payment has been processed, otherwise there would be a risk that a user buys a ticket while another user is looking at them (or that a ticket is accidentally sold to two users).

### Search Auto-Complete

- Use trie data structure.
    - Store frequency of partial (and complete) search queries in nodes (and leaves).
    - Retrieve top $k$ partial or complete queries matching input from user so far, sorted in descending order of frequency.

### TinyURL

Such a service would shorten URLs entered by a user by storing the original URLs in a lookup table with the short URLs. When the short link is accessed by someone, the website would redirect them to the original link. This represents two main components:

- URL shortener. Generates a short URL, checks that it does not already exist (if the short URLs are so short that collisions are likely), and stores both the original and short URLs in a database. Using a hash function on the original URL itself is also an option. Creation timestamps and/or last-visited timestamps may be stored as well, for example to be able to purge old, unused URLs. Embedded NoSQL documents can be used to store timestamp metadata without having to do joins.

- URL redirector. For a given short URL, looks up original URLs in the database and redirects the webpage to it, returning a 404 page if the short URL does not exist (was entered incorrectly or deleted).

For such a service, eventual consistency is acceptable, and high availability and low latency is vital, suggesting a NoSQL database. It should have a BTree index on the short URL.

The service might also have the following features:

- User accounts (not just guests), to be able to manage and delete URLs.
- Checking URLs, on creation and/or access, for malicious content.
- Providing an API directly through the URL (e.g., prefixing the URL in the address bar with the service domain).

### An EV Charging System

Front-end components:

- Webapp (React)
- Mobile app (Node.js and React Native for cross-platform support)
- Charger touchscreen app (webapp in a locked-down browser)

Server-side components:

- Backend service
    - APIs:
        - Authentication API (interacts with authentication service)
        - Chargers API
        - Vehicles API
        - Charging sessions API
        - Billing API (interacts with billing service)
    - Multiple instances behind two load balancers for fail-over, per region
- Authentication service
    - Creates new accounts
    - Authenticates users
- Optimization service
    - Assigns vehicles to chargers (only for charging schedule reservations)
    - Determines optimal charging schedules (per-site) to peak-shave or minimize TOU electricity costs
    - Regularly re-runs the charging scheduling optimization problem for each charging site, to capture SoC changes, newly plugged-in vehicles, etc.
    - Stores solution (latest vehicle charging schedules) in database
- Charging service
    - Communicates with chargers via websocket
    - Multiple instances behind reverse proxy
    - Subscribes to vehicle charging schedules on event bus
    - Aligns charging states with charging schedules by starting and stopping charging transactions
    - Regularly receives charger state updates and publishes to event bus
- Billing service
    - Carries out pay-as-you-go transactions and credit purchase transactions
    - Maintains credits balance based on credit purchases and charging sessions

Flows:

- Sign-up flow
    - Client sends new user credentials (email address and password) to authentication service over HTTPS
    - Authentication service:
        - Checks that the email address is not already associated with an account
        - Runs the password through a hashing algorithm
        - Stores new user email address, hashed password, and other account information (e.g., parent company) in users table
- Sign-in flow
    - Client sends user credentials to authentication API over HTTPS
    - Authentication service:
        - Checks that the email address is associated with an account
        - Runs the password through a hashing algorithm
        - Checks that the hashed password matches that which is associated with the user email address
        - Returns a session ID or bearer token (depending on the client) which the client includes in subsequent requests to prove their identity
        - For charger touchsreen / webapp:
            - The session state is stored in Redis or other database
            - The service checks that session IDs originated from the same client IP address, to avoid CSRF
            - Charger touchscreen sessions time out after a short time (e.g., 1 minute) (can be extended) or when a vehicle unplugs
        - For mobile app:
            - Bearer token expires after a longer time (e.g., 1 month)
- Unscheduled charge session flow
    - In any order: The user plugs into charger at charging site, and signs in (on a charger touchscreen, webapp, or mobile app if necessary)
    - If the user plugs 
    - The user enters their desired delta SoC and preferred departure time
        - Recent preferences are stored for convenient access
        - If the SoC is not transferred via OCPP, the user is prompted to enter the current SoC manually
    - The energy delta and charging duration are calculated based on the user's preferences and vehicle information (vehicles API)
        - If the charging duration conflicts with another user's reserved charging session (charging sessions API), the user is instructed to find a charger whose display indicates sufficient availability
        - If the user is on a credits plan (as opposed to a pay-as-you-go plan), the system checks that the user has enough credits to cover the energy delta (billing API), accounting for TOU electricity rates if necessary
    - If not using a charger touchscreen, the client fetches charging sites and chargers (chargers API), and the user selects a charging site and charger
        - The charging site can be inferred based on device location, if available
        - If the VIN is transferred via the OCPP connection and the VIN is associated with a specific user, then both the charging site and charger can be determined
        - Recent charging sites and chargers are stored (and cached) for convenient access
        - Charging sites are recommended based on availability, then by either recency or proximity (depending on whether device location is available)
        - Chargers are then recommended based on availability (reservation schedule versus the calculated charging duration)
    - The user starts the charging session (charging sessions API) via the UI
    - Charging sessions API:
        - Re-checks for scheduling conflicts
        - Re-checks against the user's credits balance
    - Waits for optimization service to re-run and eventually push commands to charging service (asynchronously, via event bus)
    - When the charger reports SoC greater than or equal to desired SoC, or when user unplugs, the charging services publishes a message to an event bus with the completed charging session
    - The billing service, which subscribes to the completed charging sessions event bus, charges the user or decrements their credits balance
    - The backend service, which subscribes to the completed charging sessions event bus, notifies the user via their platform's push notification service once the desired SoC is reached
- Charge session reservation flow
    - Assumes first-come-first serve reservations
    - The user selects a charging site
    - The user enters their expected arrival time, desired delta SoC, and preferred departure time
    - The user submits the charging session reservation (charging sessions API)
    - Optimization service:
        - Re-runs charger assignment optimization problem
        - Stores charger assignments in database
    - Client fetches assigned charger from charging sessions API prior to expected arrival time
