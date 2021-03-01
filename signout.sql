--
-- signout.sql
-- schema for the MSKCC intern signout webpage database schema
-- Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
--
-- Distributed under terms of the MIT license.
--

DROP TABLE IF EXISTS signout;
DROP TABLE IF EXISTS service;
DROP TABLE IF EXISTS nightfloat;
DROP TABLE IF EXISTS assignments;

CREATE TABLE service (
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(128) NOT NULL,
  type VARCHAR(8) NOT NULL,
  active boolean NOT NULL default TRUE
);

CREATE TABLE signout (
  id SERIAL PRIMARY KEY NOT NULL,
  intern_name VARCHAR(64) NOT NULL,
  intern_callback VARCHAR(16) NOT NULL,
  service INT REFERENCES service(id) NOT NULL,
  oncall BOOLEAN NOT NULL DEFAULT FALSE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  addtime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  starttime TIMESTAMP default NULL,
  completetime TIMESTAMP default NULL,
  ipaddress inet NOT NULL default '127.0.0.1',
  hosttimestamp VARCHAR(64) default NULL,
  hostuseragent VARCHAR(64) default NULL
);

CREATE TABLE nightfloat (
  id SERIAL PRIMARY KEY NOT NULL,
  firstname VARCHAR(64) NOT NULL,
  lastname VARCHAR(64) NOT NULL,
  fullname VARCHAR(128) NOT NULL,
  callback VARCHAR(12) NOT NULL
);

CREATE TABLE assignments (
  id SERIAL PRIMARY KEY NOT NULL,
  dayofyear INTEGER NOT NULL,
  type VARCHAR(8) NOT NULL,
  nightfloat INT REFERENCES nightfloat(id)
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
INSERT INTO service (name, type) VALUES ('Lymphoma Green, Sub-Intern', 'NF9133');
INSERT INTO service (name, type) VALUES ('GI C, APP #1', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI C, APP #2', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI C, APP #3', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI C, APP #4', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI D, APP #1', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI D, APP #2', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI D, APP #3', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI D, APP #4', 'NF9132');
INSERT INTO service (name, type) VALUES ('GI A, Sub-Intern', 'NF9132');
INSERT INTO service (name, type) VALUES ('Lymphoma Green, APP', 'NF9133');


-- Nightfloat callback numbers 2020-2021 {{{
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Ericka', 'Billups', 'Ericka Billups', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Marnie', 'Frith', 'Marnie Frith', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Claudia', 'Beville', 'Claudia Beville', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Brandon', 'Fowkes', 'Brandon Fowkes', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Lavada', 'Golay', 'Lavada Golay', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Lezlie', 'Judd', 'Lezlie Judd', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Trena', 'Cressey', 'Trena Cressey', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Kory', 'Gabbert', 'Kory Gabbert', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Hermelinda', 'Mullikin', 'Hermelinda Mullikin', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Willodean', 'Delafuente', 'Willodean Delafuente', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Thomas', 'Butterworth', 'Thomas Butterworth', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Melodi', 'Simonetti', 'Melodi Simonetti', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Frances', 'Steed', 'Frances Steed', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Youlanda', 'Zajicek', 'Youlanda Zajicek', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Piper', 'Rolan', 'Piper Rolan', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Cherly', 'Caso', 'Cherly Caso', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Jacalyn', 'Crews', 'Jacalyn Crews', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Dawna', 'Cost', 'Dawna Cost', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Emerita', 'Casoelli', 'Emerita Casoelli', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Weldy', 'Nubia', 'Marg Brazelton', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Evonne', 'Granda', 'Evonne Granda', '+13125551212');
INSERT INTO nightfloat (firstname, lastname, fullname, callback) values ('Marchelle', 'Goode', 'Marchelle Goode', '+13125551212');
--- }}}

-- Nightfloat assignments 2020-2021 {{{
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (357, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (357, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (358, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (358, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (359, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (359, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (360, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (360, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (361, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (361, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (362, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (362, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (363, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (363, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (364, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (364, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (365, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (365, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (366, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (366, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (1, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (1, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (2, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (2, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (3, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (3, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (4, 'NF9132', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (4, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (5, 'NF9132', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (5, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (6, 'NF9132', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (6, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (7, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (7, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (8, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (8, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (9, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (9, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (10, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (10, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (11, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (11, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (12, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (12, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (13, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (13, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (14, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (14, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (15, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (15, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (16, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (16, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (17, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (17, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (18, 'NF9132', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (18, 'NF9133', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (19, 'NF9132', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (19, 'NF9133', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (20, 'NF9132', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (20, 'NF9133', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (21, 'NF9132', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (21, 'NF9133', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (22, 'NF9132', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (22, 'NF9133', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (23, 'NF9132', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (23, 'NF9133', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (24, 'NF9132', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (24, 'NF9133', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (25, 'NF9132', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (25, 'NF9133', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (26, 'NF9132', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (26, 'NF9133', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (27, 'NF9132', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (27, 'NF9133', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (28, 'NF9132', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (28, 'NF9133', (SELECT id from nightfloat where fullname = 'Brandon Fowkes'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (29, 'NF9132', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (29, 'NF9133', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (30, 'NF9132', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (30, 'NF9133', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (31, 'NF9132', (SELECT id from nightfloat where fullname = 'Dawna Cost'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (31, 'NF9133', (SELECT id from nightfloat where fullname = 'Cherly Caso'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (32, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (32, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (33, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (33, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (34, 'NF9132', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (34, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (35, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (35, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (36, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (36, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (37, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (37, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (38, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (38, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (39, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (39, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (40, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (40, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (41, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (41, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (42, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (42, 'NF9133', (SELECT id from nightfloat where fullname = 'Evonne Granda'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (43, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (43, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (44, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (44, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (45, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (45, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (46, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (46, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (47, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (47, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (48, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (48, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (49, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (49, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (50, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (50, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (51, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (51, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (52, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (52, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (53, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (53, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (54, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (54, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (55, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (55, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (56, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (56, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (57, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (57, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (58, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (58, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (59, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (59, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (60, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (60, 'NF9133', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (61, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (61, 'NF9133', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (62, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (62, 'NF9133', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (63, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (63, 'NF9133', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (64, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (64, 'NF9133', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (65, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (65, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (66, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (66, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (67, 'NF9132', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (67, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (68, 'NF9132', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (68, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (69, 'NF9132', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (69, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (70, 'NF9132', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (70, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (71, 'NF9132', (SELECT id from nightfloat where fullname = 'Marnie Frith'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (71, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (72, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (72, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (73, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (73, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (74, 'NF9132', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (74, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (75, 'NF9132', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (75, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (76, 'NF9132', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (76, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (77, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (77, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (78, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (78, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (79, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (79, 'NF9133', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (80, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (80, 'NF9133', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (81, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (81, 'NF9133', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (82, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (82, 'NF9133', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (83, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (83, 'NF9133', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (84, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (84, 'NF9133', (SELECT id from nightfloat where fullname = 'Lezlie Judd'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (85, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (85, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (86, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (86, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (87, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (87, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (88, 'NF9132', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (88, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (89, 'NF9132', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (89, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (90, 'NF9132', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (90, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (91, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (91, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (92, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (92, 'NF9133', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (93, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (93, 'NF9133', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (94, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (94, 'NF9133', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (95, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (95, 'NF9133', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (96, 'NF9132', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (96, 'NF9133', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (97, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (97, 'NF9133', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (98, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (98, 'NF9133', (SELECT id from nightfloat where fullname = 'Jacalyn Crews'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (99, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (99, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (100, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (100, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (101, 'NF9132', (SELECT id from nightfloat where fullname = 'Ericka Billups'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (101, 'NF9133', (SELECT id from nightfloat where fullname = 'Marchelle Goode'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (102, 'NF9132', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (102, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (103, 'NF9132', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (103, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (104, 'NF9132', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (104, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (105, 'NF9132', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (105, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (106, 'NF9132', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (106, 'NF9133', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (107, 'NF9132', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (107, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (108, 'NF9132', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (108, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (109, 'NF9132', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (109, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (110, 'NF9132', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (110, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (111, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (111, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (112, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (112, 'NF9133', (SELECT id from nightfloat where fullname = 'Trena Cressey'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (113, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (113, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (114, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (114, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (115, 'NF9132', (SELECT id from nightfloat where fullname = 'Willodean Delafuente'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (115, 'NF9133', (SELECT id from nightfloat where fullname = 'Frances Steed'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (116, 'NF9132', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (116, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (117, 'NF9132', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (117, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (118, 'NF9132', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (118, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (119, 'NF9132', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (119, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (120, 'NF9132', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (120, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (121, 'NF9132', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (121, 'NF9133', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (122, 'NF9132', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (122, 'NF9133', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (123, 'NF9132', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (123, 'NF9133', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (124, 'NF9132', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (124, 'NF9133', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (125, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (125, 'NF9133', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (126, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (126, 'NF9133', (SELECT id from nightfloat where fullname = 'Piper Rolan'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (127, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (127, 'NF9133', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (128, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (128, 'NF9133', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (129, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (129, 'NF9133', (SELECT id from nightfloat where fullname = 'Emerita Casoelli'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (130, 'NF9132', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (130, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (131, 'NF9132', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (131, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (132, 'NF9132', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (132, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (133, 'NF9132', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (133, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (134, 'NF9132', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (134, 'NF9133', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (135, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (135, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (136, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (136, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (137, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (137, 'NF9133', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (138, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (138, 'NF9133', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (139, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (139, 'NF9133', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (140, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (140, 'NF9133', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (141, 'NF9132', (SELECT id from nightfloat where fullname = 'Lavada Golay'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (141, 'NF9133', (SELECT id from nightfloat where fullname = 'Hermelinda Mullikin'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (142, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (142, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (143, 'NF9132', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (143, 'NF9133', (SELECT id from nightfloat where fullname = 'Augustina Poor'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (144, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (144, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (145, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (145, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (146, 'NF9132', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (146, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (147, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (147, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (148, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (148, 'NF9133', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (149, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (149, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (150, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (150, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (151, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (151, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (152, 'NF9132', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (152, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (153, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (153, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (154, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (154, 'NF9133', (SELECT id from nightfloat where fullname = 'Youlanda Zajicek'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (155, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (155, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (156, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (156, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (157, 'NF9132', (SELECT id from nightfloat where fullname = 'Melodi Simonetti'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (157, 'NF9133', (SELECT id from nightfloat where fullname = 'Thomas Butterworth'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (158, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (158, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (159, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (159, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (160, 'NF9132', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (160, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (161, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (161, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (162, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (162, 'NF9133', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (163, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (163, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (164, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (164, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (165, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (165, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (166, 'NF9132', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (166, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (167, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (167, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (168, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (168, 'NF9133', (SELECT id from nightfloat where fullname = 'Kory Gabbert'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (169, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (169, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (170, 'NF9132', (SELECT id from nightfloat where fullname = 'Marg Brazelton'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (170, 'NF9133', (SELECT id from nightfloat where fullname = 'Claudia Beville'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (171, 'NF9132', (SELECT id from nightfloat where fullname = 'Nubia Weldy'));
INSERT INTO assignments (dayofyear, type, nightfloat) VALUES (171, 'NF9133', (SELECT id from nightfloat where fullname = 'Maxwell Bartels'));

--- }}}

UPDATE SERVICE SET active = FALSE;
UPDATE SERVICE SET active = TRUE where id in (42,  38,  37,  34,  33,  30,  29,  28,  25,  24,  23,  21,  20,  19,  17,  16,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   2,   1);



-- DUMMY VALUES FOR TESTING
-- INSERT INTO signout (intern_name, intern_callback, service, oncall, addtime) VALUES ('Nancie Hogg', 'x3002', '5', FALSE, current_timestamp + interval '51 minutes' + interval '4 seconds');

-- vim: ft=sql :
