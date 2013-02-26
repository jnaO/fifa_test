drop table if exists entries;
CREATE TABLE IF NOT EXISTS entries (
  _id                 integer primary key autoincrement,
  _title              string not null,
  _text               string not null
);
