# Dynamic Feedback System (DFS) Backend

## Short version

* PostgreSQL database
* PHP script
* Apache HTTP server

## Documentation

### Environment

Services with version number as of moment of writing. No specific requirements expect for JSON datatype in PostgreSQL (version greater than 9.2)

* PostgreSQL server 9.2
    * NB! Might be good idea to upgrade to at least 9.4, preferably to 9.6
* Apache HTTP server 2.4 with PHP, SSL
* PHP 5.4 with PDO, PGSQL

### Installation

1. Install and setup PostgreSQL server with password TCP access

2. Create a database

    * Create a role/user (application account) to the database for use with API
    * Create the following tables
        * Remember to grant at least SELECT and INSERT access to the application account for the tables

```sql
-- tables
CREATE TABLE courseunit (
    "courseUnitCode" text NOT NULL,
    "courseUnitName" text NULL,
    CONSTRAINT courseunit_pkey PRIMARY KEY ("courseUnitCode")
);

CREATE TABLE keyconcept (
    "courseUnitCode" text NULL,
    "keyConceptOrder" int4 NULL,
    "keyConceptName" text NULL
);

CREATE TABLE studentresponse (
    "courseUnitCode" text NULL,
    "studentNumber" text NULL,
    "timestamp" timestamp NULL,
    response json NULL
);
```

3. Setup HTTP server so that it can handle PHP and SSL

    * NB! Acquire SSL certificate and install it

4. Install PHP so that it has PDO and PGSQL modules

5. Copy `index.php` to a location served by the HTTP server

    * Put database server, port, database name, username and password in a file called `dfs.ini` (e.g. copy the template `dfs.ini.template` from repository and edit as reguired) to a location on HTTP server that can be read by the HTTP server process
    * Put full path of `dfs.ini` in place in `index.php` where it is mentioned

## TODO

* PHP script is very tiny and careless
* At least SQL injection risk should be taken care of before even any consideration of production use
