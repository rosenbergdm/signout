/*
 * signout.sql
 * schema for the MSKCC intern signout webpage database schema
 * Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
 *
 * Distributed under terms of the MIT license.
 */

DROP TABLE IF EXISTS signout;
DROP TABLE IF EXISTS service;

CREATE TABLE service (
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(128) NOT NULL,
  type VARCHAR(8)
);

CREATE TABLE signout (
  id SERIAL PRIMARY KEY NOT NULL,
  intern_name VARCHAR(64) NOT NULL,
  intern_callback VARCHAR(16) NOT NULL,
  service INT REFERENCES service(id) NOT NULL,
  oncall BOOLEAN NOT NULL DEFAULT FALSE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  addtime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completetime TIMESTAMP default NULL
);


INSERT INTO service (name, type) VALUES ('Breast, Intern #1', 'NF9132');
INSERT INTO service (name, type) VALUES ('Breast, Intern #2', 'NF9132');
INSERT INTO service (name, type) VALUES ('Breast, Sub-Intern', 'NF9132');
INSERT INTO service (name, type) VALUES ('Breast, APP', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI A, Intern #1', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI A, Intern #2', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI A, Intern #3', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI B, Intern #1', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI B, Intern #2', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI B, Intern #3', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI B, Sub-Intern', 'NF9132');
INSERT INTO service (name, type) VALUES ('STR, Intern #1', 'NF9133');
INSERT INTO service (name, type) VALUES ('STR, Intern #2', 'NF9133');
INSERT INTO service (name, type) VALUES ('STR, Sub-Intern #1', 'NF9133');
INSERT INTO service (name, type) VALUES ('STR, NP', 'NF9133');
INSERT INTO service (name, type) VALUES ('Gen Med, Intern #1', 'NF9133');
INSERT INTO service (name, type) VALUES ('Gen Med, Intern #2', 'NF9133');
INSERT INTO service (name, type) VALUES ('Gen Med, Intern #3', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia A, Intern #1', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia A, Intern #2', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia A, Intern #3', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia A, NP', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia A, Sub-Intern', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia B, Intern #1', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia B, Intern #2', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia B, NP', 'NF9133');
INSERT INTO service (name, type) VALUES ('Leukemia B, Sub-Intern', 'NF9133');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #1', 'NF9133');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #2', 'NF9133');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #3', 'NF9133');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #3', 'NF9133');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Sub-Intern', 'NF9133');

-- DUMMY VALUES FOR TESTING

-- vim:et
