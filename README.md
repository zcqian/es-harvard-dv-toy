# Demo project using Elastic Search

Demo for using ES and flask to implement search API for data formatted similar to Harvard Dataverse data.


## How to use the API
Setup and data upload is omitted, it is not difficult to figure out using the source code and the tests.

### Request a single document by @id
To request a single document, make an HTTP `GET` request to `/data` with the `id` parameter as the full URLencoded id. For instance, `GET /data?id=https%3A%2F%2Fdoi.org%2F10.11588%2Fdata%2F0HJAJS`.

In the future, you will be able to request a single document with the short DOI number and id, without the prefixes. But for now, you will need to use the matching id exactly as it is.

### Searching

To search, make an HTTP `GET` request to `/search`, with the body being a JSON dictionary, explained later.

If you want to filter the results according to the name of the funder, 
use a query string with the parameter `facet`, for instance, 
`/search?facet=International+Affairs+Agency` means to filter only funder names 
that is exactly "International Affair Agency" (case insensitive, and IAA is a fictional agency).
Make sure it has been proplerly URLencoded.

#### Query body JSON dictionary
It is a flat JSON dictionary (no nesting), each key means querying a field, 
and can point to a string or a list of strings. 
You can omit a key or leave the string empty if you don't want to query that parameter/field.

All keys are queried using the `AND` relationship, while for each query in a key (string in a list), 
they are queries using the `OR` relationship. Inside the string, each word is related by `AND` relationship.

So, take for instance the query below, 
```json
{
  "name": ["Literatur", "Distance Effects"],
  "author": "Trautmann"
}
```
it means the **author** field must contain "Trautmann",
 while (`AND`) the **name** field must contain 1) "Literatur" `OR` 2) both "Distance" `AND` "Effects"

The following is a table explaining the meaning of each possible/usable key:

| Key          | Query field                                           |
| ------------ | ----------------------------------------------------- |
| `q`          | all fields in the document, entire document           |
| `name`       | name                                                  |
| `description`| description                                           |
| `keywords`   | anything in keywords                                  |
| `publisher`  | name of publisher                                     |
| `provider`   | name of provider                                      |
| `creator`    | anything in the creator object (name and affiliation) |
| `author`     | anything in the author object (name and affiliation)  |
| `citation`   | anything in the list of objects in citation           |