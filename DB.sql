-- Tables

BEGIN;

--                  TABLES
    
-- products
CREATE TABLE product (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "barcode"       INTEGER         NULL,
    "article"       VARCHAR(25)     NULL,
    "code"          INTEGER         NULL,
    "position"      INTEGER         NULL,
    "name"          VARCHAR(200)    NOT NULL,
    "product_class" INTEGER         NOT NULL
                                    REFERENCES customer( id ),
    "manufacturer"  VARCHAR(100)    NOT NULL,
    "season"        VARCHAR(25)     NULL,
    "color"         VARCHAR(25)     NULL,
    "size"          INTEGER         NULL,
    "image"         VARCHAR(255)    NULL,
    "structure"     VARCHAR(255)    NULL,
    "reserve"       INTEGER         NULL,
    "description"   TEXT            NULL,
    "weight"        INTEGER         NULL,
    "dimensions"    VARCHAR(100)    NULL,
    "promotion"     VARCHAR(255)    NULL,
    "price"         DECIMAL(10, 2)  NULL,
    "popularity"    INTEGER         NULL,
    "note"          TEXT            NULL,
    "timestamp"     DATETIME        NOT NULL,
    "modtime"       DATETIME        NULL
);

CREATE TABLE product (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "name"          VARCHAR(200)    NOT NULL
);

-- orders
CREATE TABLE purchase_order (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "timestamp"     DATETIME        NOT NULL,     
    "customer_id"   INTEGER         NOT NULL
                                    REFERENCES customer( id ),
    "delivery"      VARCHAR(25)     NOT NULL,
    "payment"       VARCHAR(25)     NOT NULL,
    "note"          TEXT            NULL,
    "price"         DECIMAL(10, 2)  NOT NULL,
    "satisfied"     BOOLEAN         NOT NULL
);

-- ordered product
CREATE TABLE ordered_product (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "product_id"    INTEGER         NOT NULL
                                    REFERENCES product( id ),   
    "customers_order_id"   INTEGER  NOT NULL
                                    REFERENCES customers_order( id ),
    "quantity"      INTEGER         NOT NULL,      
    "price"         DECIMAL(10, 2)  NOT NULL,
    "satisfied"     BOOLEAN         NOT NULL
);


-- customers 
CREATE TABLE customer (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,   
    "email"         VARCHAR(75)     NOT NULL,
    "name"          VARCHAR(100)    NULL,
    "brests"        INTEGER         NULL,
    "chest"         INTEGER         NULL,
    "hips"          INTEGER         NULL,
    "promotion"     VARCHAR(255)    NULL,
    "promotioin_modifier"     DECIMAL    NULL,    
    "registration_time"   DATETIME        NOT NULL
);

-- addresses
CREATE TABLE adress (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "customer_id"   INTEGER         NOT NULL
                                    REFERENCES customer( id ),
    "city"          VARCHAR(25)     NULL,
    "adress"        VARCHAR(25)     NULL,
    "fax"           INTEGER         NULL,
    "phone"         INTEGER         NOT NULL
);

-- news
CREATE TABLE news (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "title"         VARCHAR(255)    NOT NULL,
    "text"          TEXT            NULL,
    "author"        VARCHAR(100)    NOT NULL,
    "date"          DATETIME        NOT NULL
);

-- reviews
CREATE TABLE review (
    "id"            INTEGER         NOT NULL
                                    PRIMARY KEY AUTOINCREMENT,
    "title"         VARCHAR(255)    NOT NULL,
    "text"          TEXT            NULL,
    "author"        VARCHAR(100)    NOT NULL,
    "email"         VARCHAR(75)     NOT NULL,
    "date"          DATETIME        NOT NULL
);


--                  INDEXES

-- customers_order -> customer
CREATE INDEX "order_to_customer" on customers_order("customer_id");

-- ordered_product -> product
CREATE INDEX "ordered_product_to_product" on ordered_product("product_id");

-- ordered_product -> customers_order
CREATE INDEX "ordered_product_to_customers_order" on ordered_product("customers_order_id");

-- adress -> customer
CREATE INDEX "adress_to_customer" on adress("customer_id");

COMMIT;
