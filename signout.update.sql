/*
 * signout.update.sql
 * Update the postgres schema for v0.2 of signout program
 * Copyright (C) 2020 Thomas Butterworth <dmr@davidrosenberg.me>
 *
 * Distributed under terms of the MIT license.
 */

ALTER TABLE service ADD COLUMN active boolean NOT NULL default TRUE;

ALTER TABLE signout
  ADD COLUMN starttime TIMESTAMP default NULL,
  ADD COLUMN ipaddress inet NOT NULL default '127.0.0.1',
  ADD COLUMN hosttimestamp VARCHAR(64) default NULL;




-- vim:et
