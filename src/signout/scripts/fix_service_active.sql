-- For v0.3 upgrade
-- fix_service_active.sql
-- Set which services are currently active as of 2/26/21
-- Copyright (c) David M. Rosenberg 2020-2021 --

-- Set which services are for which NF groups
BEGIN TRANSACTION;
  UPDATE service set type='NF9132' where name like 'STR%';
  UPDATE service set type='NF9132' where name like 'Breast%';
  UPDATE service set type='NF9132' where name like 'GI%';
  UPDATE service set type='NF9133' where name like 'Leukemia%';
  UPDATE service set type='NF9133' where name like 'Lymphoma%';
  UPDATE service set type='NF9133' where name like 'Gen Med%';
END TRANSACTION;

-- NF 9132=GI, Breast, STR
BEGIN TRANSACTION;
  UPDATE service set active='f' where type='NF9132';
  UPDATE service set active='t' where name in (
    'STR, Intern #1',
    'STR, Intern #2',
    'GI A, Intern #1',
    'GI A, Intern #2',
    'GI A, Intern #3',
    'GI B, Intern #1',
    'GI B, Intern #2',
    'GI B, Intern #3',
    'Breast, Intern #1',
    'Breast, Intern #2',
    'Breast, APP');
END TRANSACTION;

-- NF 9133=Gen Med, Leukemia, Lymphoma
BEGIN TRANSACTION;
  UPDATE service set active='f' where type='NF9133';
  UPDATE service set active='t' where name in (
    'Lymphoma Green, Intern #3',
    'Lymphoma Green, Intern #2',
    'Lymphoma Green, Intern #1',
    'Leukemia B, Intern #2',
    'Leukemia B, Intern #1',
    'Leukemia A, Intern #3',
    'Leukemia A, Intern #2',
    'Leukemia A, Intern #1',
    'Gen Med, Intern #3',
    'Gen Med, Intern #2',
    'Gen Med, Intern #1');
END TRANSACTION;

-- Fix the fact that somehow there's two active Lymphoma Green #3s
BEGIN TRANSACTION;
  UPDATE service
  SET    active = 'f'
  WHERE  NAME = 'Lymphoma Green, Intern #3';

  UPDATE service
  SET    active = 't'
  WHERE  id IN
         (
                SELECT id
                FROM   service
                WHERE  NAME LIKE 'Lymphoma Green, Intern #3' limit 1);
END TRANSACTION;


