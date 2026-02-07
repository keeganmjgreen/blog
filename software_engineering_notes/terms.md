# Terminology

- **Distributed** means a system that can run across multiple machines, often with an orchestration module for receiving and delegating tasks and collecting their outputs. Example: Kubernetes. Individual machines are often called nodes, and a group of machines is often called a cluster. An individual machine can be a bare-metal server, a VM, or a container. Machines can span datacenters and geo-regions.

- **Elastic** means a system that can scale up and down quickly, in particular by allocating and deallocating machines in a distributed architecture.

- **Fault-tolerant** may mean that a distributed system can handle the failure of an individual machine by reassigning the failed machine's current and would-be future tasks to the system's other machines.

- **Redis:** In-memory key-value database, often used as a distributed cache or message broker.

- **Scalable** means a system that can handle a large computational load (perform an arbitrarily large computation or an arbitrarily large number of computations) without an exponential increase of compute time, e.g., due to poor computational complexity.

    - **Scaling horizontally** means handling a large computational load by running the computation(s) across multiple machines, i.e., in a distributed system.
    - **Scaling vertically** means handling a large computational load by running the computation(s) on a machine with more resources (CPU, memory, etc.).

- **Three-Layer Application** = DB + compute layer + load balancer.

- **Websocket** is a communication protocol that, unlike HTTP1, offers bidirectional communication. With websocket, messages can be pushed to clients rather than having clients poll for new messages.

# Database Terminology

- **ACID transactions:** Prioritize accuracy and validity.

    - Atomicity: Either all database operations in a transaction are applied, or none are (in the case of an error), thereby avoiding partial updates or invalid data.

    - Consistency: The data in a database cannot exist in an invalid state (e.g., violating foreign-key constraints), because transactions will fail if an invalid state is attempted.

    - Isolation: Transactions affecting the same table at the same time leave the database in the same state as it would be in if the transactions were executed sequentially. If a slow transaction fails while a fast transaction on the same data succeeds, the fast transaction depends on the failed transaction which must be undone (write-write contention). The database must be restored to the last valid state (prior to the slow, failed transaction) after which the fast transaction must be reapplied.

    - Durability: The database's data is maintained even if the database server crashes or there is a power failure. Transactions that are in progress, however, will be lost.

- Data **cardinality** can refer to the relationships between unique data (one-to-one, one-to-many, etc.). **High cardinality data** refers to a data set (e.g., a field or column) with many unique values (e.g., timestamps), whereas **low cardinality data** refers to a data set with repeated values (e.g., categories).

- **Eventual consistency:** Prioritize high availability and low latency by avoiding transactions waiting on each other.

- **Replication**, in an SQL database system, introduces additional database servers called "replicas" or "followers". These can serve as backup for the "leader" database server or offload some read requests from the leader. Writes are sent to the leader and copied writes to the followers.

- Database **[sharding](https://aws.amazon.com/what-is/database-sharding/) and partitioning:** Sharding is across servers, partitioning is within a server. Data can be sharded or partitioned by an ID or by a hash. Data can also be sharded by geographic region.
