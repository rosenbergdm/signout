-- For v0.3 upgrade
-- Set which services are currently active as of 2/26/21

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

