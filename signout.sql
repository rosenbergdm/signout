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


INSERT INTO service (name, type) VALUES ('Breast, Intern #1', 'SOLID');
INSERT INTO service (name, type) VALUES ('Breast, Intern #2', 'SOLID');
INSERT INTO service (name, type) VALUES ('Breast, Intern #3', 'SOLID');
INSERT INTO service (name, type) VALUES ('Breast, Sub-Intern', 'SOLID');
INSERT INTO service (name, type) VALUES ('Breast, APP', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI A, Intern #1', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI A, Intern #2', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI A, Intern #3', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI B, Intern #1', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI B, Intern #2', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI B, Intern #3', 'SOLID');
INSERT INTO service (name, type) VALUES ('GI B, Sub-Intern', 'SOLID');
INSERT INTO service (name, type) VALUES ('GU, Intern #1', 'SOLID');
INSERT INTO service (name, type) VALUES ('GU, Intern #2', 'SOLID');
INSERT INTO service (name, type) VALUES ('GU, Intern #3', 'SOLID');
INSERT INTO service (name, type) VALUES ('GU, Sub-Intern #1', 'SOLID');
INSERT INTO service (name, type) VALUES ('GU, NP', 'SOLID');
INSERT INTO service (name, type) VALUES ('Gen Med, Intern #1', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Gen Med, Intern #2', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Gen Med, Intern #3', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia A, Intern #1', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia A, Intern #2', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia A, Intern #3', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia A, NP', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia A, Sub-Intern', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia B, Intern #1', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia B, Intern #2', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia B, NP', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Leukemia B, Sub-Intern', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #1', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #2', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #3', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Intern #3', 'LIQUID');
INSERT INTO service (name, type) VALUES ('Lymphona Green, Sub-Intern', 'LIQUID');

-- DUMMY VALUES FOR TESTING
INSERT INTO signout(intern_name, intern_callback, service) VALUES ('Thomas Butterworth', '773-240-3395', 1);
INSERT INTO signout(intern_name, intern_callback, service, addtime) VALUES (
  'Christina Butterworth', 'p8281', 3, current_timestamp + interval '10 minutes');
INSERT INTO signout(intern_name, intern_callback, service, oncall, addtime) VALUES (
  'Schiller Butterworth', 'x9100', 11, TRUE, current_timestamp + interval '15 minutes' + interval '3 seconds');

-- vim:et
