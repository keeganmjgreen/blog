# MongoDB

[MongoDB](https://www.mongodb.com/docs/) is a document database, or "NoSQL" database, meaning that it stores *documents* within *collections*. This is as opposed to a traditional relational/SQL database, which stores records within tables. Documents and collections are analogous to records and tables in a relational database.

A collection's documents do not need to have a specific set of fields and a field does not need to have a specific type. In a relational database, this would mean potentially different columns for each table record, and potentially columns without a data type.

Complex field types are better-supported and more common/encouraged than in a relational database. Arrays are better-supported. Storage of objects is natively supported, rather than having to store a JSON or JSONB column for which a JSON schema cannot be natively enforced. This encourages nesting/embedding data rather than storing data across tables linked through foreign key constraints. This means that related data are stored together and more intuitively, without the mental or computational load of needing to use a join between related tables.

Documents can be one-to-one with classes/structs in code, reducing the mental load of mapping to tables (whether manual or using an ORM).

Queries can be written in JSON.

Document schemas can be written in JSON schema.

Documents can be written and read in JSON, and are stored in BSON. [BSON](https://bsonspec.org/) is a binary encoding of JSON-like documents that also extends JSON with additional data types including `Date` and `BinData`. Because JSON's types are a subset of BSON's, regular JSON cannot be converted to or from BSON. Instead, Extended JSON (EJSON) is used, which uses an object representation of the more complex types. EJSON can written in either *canonical mode*, which uses object representations that perfectly preserve all BSON types, or *relaxed mode*, which uses some object representations that are more readable at the expense of type preservation. Some object representations are the same between canonical and relaxed modes.

Unique documents are identified by a built-in `_id` field of type [ObjectId](https://www.mongodb.com/docs/manual/reference/bson-types/#objectid).

## Relationships Between Documents

A **one-to-one** relationship between documents A and B can be implemented either by embedding document B in document A, or by including a reference to document B in document A. If the two documents belong to the same collection, references must be used to avoid storing duplicate data and possibly to avoid trying to store infinitely-nested documents.

An ***optional* one-to-one** relationship can be implemented by making the field in document A nullable.

A **one-to-many** relationship can similarly be represented by using an array.

A **many-to-many** relationship between documents A and B must be represented by an additional collection of documents, each of which stores references to documents A and B. This is analogous to an association table in a relational database.

## Embedding Versus Referencing Data

**Embedding data:** Embedding documents (or arrays or documents) is a way of structuring data that follows a *denormalized* data model, in contrast to the *normalized* data model of a relational database. Duplication of data happens if the same document is embedded in multiple parent documents. Such duplication results in simpler and more performant data retrieval. And while storing embedded documents does result in atomic writes, duplicated data occupies more storage space and will cause writes to be less performant, as they then have to keep all copies up-to-date. Furthermore, if retrieving only the embedded document is often desired, then performance would be better if the embedded documents were instead stored in a separate collection.

**Referencing data:** Referencing documents is a way of structuring data that follows a normalized data model, like that of a relational database. Rather than copying related documents, links to related documents are made. While this does result in more complicated and less performant data retrieval, it also occupies less storage space and makes writes more performant, as they only have to update one copy.

## Performance Considerations

Performance may be improved on a large collection of small documents by grouping them via embedding into fewer, larger documents. Whether this grouping is practical depends on the nature of the data and whether the application would be able to use it in a grouped form. Such grouping allows sequential reads and fewer random disk accesses. If the small documents are able to be grouped by common field(s), then this will also reduce the size of any indexes on those fields.

Performance may be improved by splitting up a collection into multiple collections based on field values. There is no significant performance cost to having many collections. It may be faster to process documents spanning multiple collections than to process all the documents in one collection.

Reads for which no index is available are not only slow but also consume a lot of memory.

### Indexes

Indexes are used to make queries more efficient by avoiding scanning all documents in a collection, analogous to how indexes in a relational database avoid scanning all records in a table. However, indexes also make writes less efficient as indexes on a collection must be updated for every write to that collection.

A *single-field index* can exist on the `id_` field (as is the case by default) or any other field of a top-level or embedded document.

A *compound index* exists on one or more fields. The order of fields matters due to the underlying BTree-based implementation.

- To make an efficient compound index, the fields should be ordered depending on how they will be queried, generally following the Equality, Sort, Range (ESR) guideline. Fields that will be filtered on based on whether they equal (E) a certain value should generally come first (in any order), followed by fields on which documents will be sorted (S), followed by fields that will be filtered on based on whether they lie within a certain one- or two-sided range.

- Each compound index may contain one *hashed index field*.

- An *index prefix* of an $n$-field compound index consists of the first $i \leq n$ fields of the compound index. Index prefixes are themselves indexes that are used to make queries on those fields more efficient, without having to explicitly define indexes on those fields. Other subsets of a compound index's fields can also be used to make queries more efficient, but less effectively and only as long as the query does not try to sort on an index field without first filtering based on equality with all preceding index fields.

Indexes are specified with either an ascending sort order (`1`) or a descending sort order (`-1`) for each field.

Special indexes:

- Geospacial index.
- Text index.

Further reading:

- [Sparse indexes](https://www.mongodb.com/docs/manual/core/index-sparse/#std-label-index-type-sparse)
- [Unique indexes](https://www.mongodb.com/docs/manual/core/index-unique/#std-label-index-type-unique)
- [Using indexes to sort query results.](https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/#std-label-sort-index-nonprefix-subset)
- [The ESR (Equality, Sort, Range) guideline](https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/#std-label-esr-indexing-guideline)
- [Indexing strategies](https://www.mongodb.com/docs/manual/applications/indexes/#std-label-indexing-strategies)

## Miscellaneous

- A *capped collection* is like a FIFO queue and is efficient for accessing recent documents.

- The *working set* is the database's most frequently used data and is used to avoid reading from disk where possible.

- For each database, a namespace (`.ns`) file contains its metadata, including indexes and collections.

## Further Reading

- Exercise: [Enforce Data Consistency with Embedding](https://www.mongodb.com/docs/manual/data-modeling/enforce-consistency/embed-data/#std-label-enforce-consistency-embedding)
- [Database Triggers](https://www.mongodb.com/docs/atlas/atlas-ui/triggers/database-triggers/#std-label-atlas-database-trigger)
- [Data Consistency](https://www.mongodb.com/docs/manual/data-modeling/data-consistency/#std-label-data-modeling-data-consistency)
- [Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/#std-label-schema-validation-overview)
- [Handle Duplicate Data](https://www.mongodb.com/docs/manual/data-modeling/handle-duplicate-data/#std-label-data-modeling-duplicate-data)
- [Welcome to MongoDB Shell (mongosh)](https://www.mongodb.com/docs/mongodb-shell/)
