DROP TABLE IF EXISTS file;
DROP TABLE IF EXISTS fieldsettings;

CREATE TABLE file (
  file_id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  delimiter TEXT,

  filename TEXT not null
);

CREATE TABLE fieldsettings (
  field_id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_id INTEGER,
  column_name TEXT NOT NULL,
  column_type TEXT NOT NULL,
  FOREIGN KEY(file_id) REFERENCES file(file_id)
);