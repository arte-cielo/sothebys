DROP TABLE IF EXISTS asta;
CREATE TABLE aste (
  guid CHAR(32) PRIMARY KEY,
  name VARCHAR(200),
  asta VARCHAR(25),
  dates VARCHAR(20),
  time TEXT
  location TEXT
  maxlot INTEGER(11),
  sales_number INTEGER(11),
  sale_total VARCHAR(30),
  update_date DATETIME
) DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS asta;
CREATE TABLE opere (
  guid CHAR(32) PRIMARY KEY,
  id_asta INTEGER(11) AUTO_INCREMENT,
  title TEXT,
  description TEXT,
  estimate VARCHAR(20),
  lot_sold VARCHAR(15),
  valuta VARCHAR(5),
  image_urls VARCHAR(100),
  image_path VARCHAR(100),
  image VARCHAR(100)
  url TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS artisti;
CREATE TABLE artisti (
  guid CHAR(32) PRIMARY KEY,
  author VARCHAR(100)
  name VARCHAR(25)
  surname VARCHAR(25)
  born VARCHAR(10)
  death VARCHAR(10)
  update_date VARCHAR(10)
) DEFAULT CHARSET=utf8;

