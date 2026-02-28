-- ============================================================
-- saasmetrics.ai  |  BigQuery Setup Script v2
-- Dataset: saasmetrics
--
-- DISAMBIGUATION COLUMNS INTENTIONALLY INCLUDED:
--   list_price_unit  = price per seat per year (P)
--   list_price_total = list_price_unit x seats_contracted (P x Q, undiscounted line total)
--   seats_contracted = seats on signed order form
--   seats_active     = seats with login in last 30 days
--   arr_usd          = recognized ARR (current billing period)
--   arr_bookings_usd = booked ARR (signed TCV/term, can differ pre-start)
--   csm_owner        = Customer Success Manager (retention, renewals)
--   ae_owner         = Account Executive (new business, closed the deal)
--
-- These pairs are resolved by the data dictionary injected into
-- the system prompt. The model never guesses; it uses definitions.
--
-- Run:
--   bq mk --dataset --location=US YOUR_PROJECT:saasmetrics
--   bq query --project_id=YOUR_PROJECT --use_legacy_sql=false < bq_setup.sql
-- ============================================================

CREATE OR REPLACE TABLE `saasmetrics.customers` (
  customer_id        STRING    NOT NULL,
  name               STRING,
  industry           STRING,
  tier               STRING,
  region             STRING,
  country            STRING,
  arr_usd            INT64,
  arr_bookings_usd   INT64,
  seats_contracted   INT64,
  seats_active       INT64,
  contract_start     DATE,
  contract_end       DATE,
  csm_owner          STRING,
  ae_owner           STRING,
  status             STRING,
  health_score       INT64,
  nps_score          INT64,
  products           STRING,
  created_at         TIMESTAMP
);

INSERT INTO `saasmetrics.customers` VALUES
('C001','Apex Financial',        'Banking',    'Enterprise','US-East','USA', 480000,480000, 850,848,'2022-01-15','2025-01-14','Priya Nair',    'James Okoye',   'Active',  82, 42,'ThreatShield Enterprise, TI Add-on',TIMESTAMP '2022-01-10 09:00:00'),
('C002','Vantage Capital',       'Hedge Fund', 'Enterprise','US-West','USA', 360000,360000, 620,595,'2023-03-01','2025-02-28','James Okoye',   'James Okoye',   'Active',  77, 38,'ThreatShield Enterprise',           TIMESTAMP '2023-02-22 10:30:00'),
('C003','NordBank AG',           'Banking',    'Mid-Market','EMEA',  'DEU', 144000,144000, 200,  0,'2023-06-10','2024-06-09','Sophie Laurent','Sophie Laurent','Churned',  0,-20,'ThreatShield Mid-Market',           TIMESTAMP '2023-06-05 08:15:00'),
('C004','Castlepoint Insurance', 'Insurance',  'Mid-Market','US-East','USA',  96000, 96000, 150,135,'2024-01-01','2025-12-31','Priya Nair',    'Priya Nair',    'Active',  88, 55,'ThreatShield Mid-Market',           TIMESTAMP '2023-12-18 14:00:00'),
('C005','Pinnacle Wealth',       'Wealth Mgmt','SMB',       'US-West','USA',  36000, 36000,  45, 22,'2024-04-01','2025-03-31','James Okoye',   'Wei Zhang',     'Active',  55, 20,'ThreatShield SMB',                  TIMESTAMP '2024-03-25 11:45:00'),
('C006','Meridian Trading',      'Trading',    'Enterprise','APAC',  'SGP', 540000,540000,1100,890,'2021-07-01','2024-06-30','Wei Zhang',     'Wei Zhang',     'At-Risk', 31,-15,'ThreatShield Enterprise, TI Add-on',TIMESTAMP '2021-06-22 07:30:00'),
('C007','BlueSky Fintech',       'Fintech',    'SMB',       'US-East','USA',  24000, 24000,  30, 30,'2024-08-01','2025-07-31','Sophie Laurent','Sophie Laurent','Active',  72, 35,'ThreatShield SMB',                  TIMESTAMP '2024-07-28 16:00:00'),
('C008','GoldLeaf Advisors',     'Wealth Mgmt','Mid-Market','US-West','USA',  96000, 96000, 175,155,'2024-10-01','2025-09-30','Sophie Laurent','Sophie Laurent','Active',  91, 60,'ThreatShield Mid-Market',           TIMESTAMP '2024-09-25 13:00:00'),
('C009','Fortress Bank NA',      'Banking',    'Enterprise','US-East','USA',      0,     0,NULL,NULL,NULL,       NULL,        'James Okoye',   'James Okoye',   'Prospect',NULL,NULL,'',                              TIMESTAMP '2024-09-01 09:00:00'),
('C010','EuroCredit AG',         'Banking',    'Enterprise','EMEA',  'CHE',      0,     0,NULL,NULL,NULL,       NULL,        'James Okoye',   'James Okoye',   'Prospect',NULL,NULL,'',                              TIMESTAMP '2024-09-10 10:00:00'),
('C011','DataVault Reinsurance', 'Insurance',  'Enterprise','US-East','USA',      0,     0,NULL,NULL,NULL,       NULL,        'Priya Nair',    'Priya Nair',    'Prospect',NULL,NULL,'',                              TIMESTAMP '2024-09-20 11:00:00'),
('C012','SwiftTrade LLC',        'Trading',    'Mid-Market','APAC',  'AUS',      0,     0,NULL,NULL,NULL,       NULL,        'Wei Zhang',     'Wei Zhang',     'Prospect',NULL,NULL,'',                              TIMESTAMP '2024-08-15 08:00:00'),
('C013','NexGen Insurance',      'Insurance',  'Mid-Market','US-West','USA',      0,     0,NULL,NULL,NULL,       NULL,        'Wei Zhang',     'Wei Zhang',     'Prospect',NULL,NULL,'',                              TIMESTAMP '2024-09-05 14:00:00'),
('C015','Brightpath Credit',     'Fin Services','Mid-Market','US-East','USA', 72000, 72000, 110,  0,'2023-08-01','2024-07-31','Priya Nair',    'Priya Nair',    'Churned',  0,-30,'ThreatShield Mid-Market',           TIMESTAMP '2023-07-25 10:00:00'),
('C016','Ironclad Payments',     'Fintech',    'SMB',       'US-West','USA',  18000, 18000,  25, 20,'2023-11-01','2024-10-31','Wei Zhang',     'Sophie Laurent','Active',  68, 15,'ThreatShield SMB',                  TIMESTAMP '2023-10-28 15:00:00'),
('C017','Redstone Capital',      'Hedge Fund', 'SMB',       'US-East','USA',  21600, 21600,  30, 28,'2024-02-01','2025-01-31','Priya Nair',    'Priya Nair',    'Active',  74, 30,'ThreatShield SMB',                  TIMESTAMP '2024-01-28 09:00:00'),
('C018','Pacific Mutual Bank',   'Banking',    'Mid-Market','US-West','USA', 108000,108000, 190,174,'2022-10-01','2024-09-30','Wei Zhang',     'Wei Zhang',     'Active',  80, 45,'ThreatShield Mid-Market',           TIMESTAMP '2022-09-20 11:00:00'),
('C019','Clearfund LP',          'Wealth Mgmt','SMB',       'EMEA',  'GBR',  19200, 19200,  27, 25,'2024-05-01','2025-04-30','Sophie Laurent','Sophie Laurent','Active',  65, 25,'ThreatShield SMB',                  TIMESTAMP '2024-04-25 14:00:00'),
('C020','AxisBank Financial',    'Banking',    'Mid-Market','APAC',  'IND',  84000, 84000, 145,125,'2023-12-01','2024-11-30','Wei Zhang',     'Wei Zhang',     'Active',  79, 40,'ThreatShield Mid-Market',           TIMESTAMP '2023-11-22 08:30:00'),
('C021','NexPoint Securities',   'Fin Services','SMB',      'US-East','USA',  16800, 16800,  23, 18,'2024-06-01','2025-05-31','Priya Nair',    'Priya Nair',    'Active',  61, 10,'ThreatShield SMB',                  TIMESTAMP '2024-05-28 10:00:00');


CREATE OR REPLACE TABLE `saasmetrics.subscriptions` (
  sub_id             STRING    NOT NULL,
  customer_id        STRING,
  product            STRING,
  seats_contracted   INT64,
  seats_active       INT64,
  list_price_unit    INT64,
  list_price_total   INT64,
  discount_pct       FLOAT64,
  mrr_usd            INT64,
  arr_usd            INT64,
  status             STRING,
  start_date         DATE,
  end_date           DATE,
  auto_renew         BOOL,
  tier               STRING
);

INSERT INTO `saasmetrics.subscriptions` VALUES
('S001','C001','ThreatShield Enterprise',    850,848,420,357000,0.00,33333,400000,'Active',   '2022-01-15','2025-01-14',TRUE, 'Enterprise'),
('S002','C001','Threat Intelligence Add-on',   0,  0,  0, 45000,0.00, 6667, 80000,'Active',   '2022-01-15','2025-01-14',TRUE, 'Enterprise'),
('S003','C002','ThreatShield Enterprise',    620,595,420,260400,0.00,30000,360000,'Active',   '2023-03-01','2025-02-28',TRUE, 'Enterprise'),
('S004','C003','ThreatShield Mid-Market',    200,  0,480, 96000,0.00,12000,144000,'Cancelled','2023-06-10','2024-06-09',FALSE,'Mid-Market'),
('S005','C004','ThreatShield Mid-Market',    150,135,480, 72000,0.00, 8000, 96000,'Active',   '2024-01-01','2025-12-31',TRUE, 'Mid-Market'),
('S006','C005','ThreatShield SMB',            45, 22,540, 24300,0.00, 3000, 36000,'Active',   '2024-04-01','2025-03-31',TRUE, 'SMB'),
('S007','C006','ThreatShield Enterprise',   1100,890,420,462000,0.00,37500,450000,'Active',   '2021-07-01','2024-06-30',FALSE,'Enterprise'),
('S008','C006','Threat Intelligence Add-on',   0,  0,  0, 45000,0.00, 7500, 90000,'Active',   '2021-07-01','2024-06-30',FALSE,'Enterprise'),
('S009','C007','ThreatShield SMB',            30, 30,540, 16200,0.00, 2000, 24000,'Active',   '2024-08-01','2025-07-31',TRUE, 'SMB'),
('S010','C008','ThreatShield Mid-Market',    175,155,480, 84000,0.00, 8000, 96000,'Active',   '2024-10-01','2025-09-30',TRUE, 'Mid-Market'),
('S011','C015','ThreatShield Mid-Market',    110,  0,480, 52800,0.00, 6000, 72000,'Cancelled','2023-08-01','2024-07-31',FALSE,'Mid-Market'),
('S012','C016','ThreatShield SMB',            25, 20,540, 13500,0.00, 1500, 18000,'Active',   '2023-11-01','2024-10-31',TRUE, 'SMB'),
('S013','C017','ThreatShield SMB',            30, 28,540, 16200,0.00, 1800, 21600,'Active',   '2024-02-01','2025-01-31',TRUE, 'SMB'),
('S014','C018','ThreatShield Mid-Market',    190,174,480, 91200,0.00, 9000,108000,'Active',   '2022-10-01','2024-09-30',TRUE, 'Mid-Market'),
('S015','C019','ThreatShield SMB',            27, 25,540, 14580,0.00, 1600, 19200,'Active',   '2024-05-01','2025-04-30',TRUE, 'SMB'),
('S016','C020','ThreatShield Mid-Market',    145,125,480, 69600,0.00, 7000, 84000,'Active',   '2023-12-01','2024-11-30',TRUE, 'Mid-Market'),
('S017','C021','ThreatShield SMB',            23, 18,540, 12420,0.00, 1400, 16800,'Active',   '2024-06-01','2025-05-31',TRUE, 'SMB');


CREATE OR REPLACE TABLE `saasmetrics.revenue_monthly` (
  month           STRING,
  arr_usd         INT64,
  mrr_usd         INT64,
  new_arr         INT64,
  expansion_arr   INT64,
  churned_arr     INT64,
  net_new_arr     INT64,
  nrr_pct         FLOAT64,
  customers_count INT64,
  new_logos       INT64,
  churned_logos   INT64
);

INSERT INTO `saasmetrics.revenue_monthly` VALUES
('2023-01', 980000, 81667, 90000,15000,-10000, 95000,105.2,28,2,0),
('2023-02',1060000, 88333, 85000,20000,-25000, 80000,104.8,29,2,1),
('2023-03',1150000, 95833,110000,25000,-25000,110000,106.1,31,3,0),
('2023-04',1220000,101667, 85000,18000,-33000, 70000,104.5,32,2,1),
('2023-05',1300000,108333, 95000,22000,-17000,100000,105.7,34,2,0),
('2023-06',1390000,115833,105000,28000,-43000, 90000,105.2,36,3,1),
('2023-07',1450000,120833, 78000,20000,-38000, 60000,104.1,37,2,1),
('2023-08',1520000,126667, 90000,32000,-52000, 70000,103.9,38,2,2),
('2023-09',1540000,128333, 55000,18000,-53000, 20000,104.5,38,1,1),
('2023-10',1580000,131667, 62000,24000,-46000, 40000,105.1,39,2,1),
('2023-11',1640000,136667, 85000,30000,-25000, 90000,106.0,41,2,0),
('2023-12',1680000,140000, 70000,22000,-52000, 40000,105.5,41,2,1),
('2024-01',1720000,143333,120000,45000,-30000,135000,109.8,42,3,0),
('2024-02',1800000,150000, 95000,38000,-53000, 80000,109.1,43,2,1),
('2024-03',1900000,158333,180000,52000,-32000,200000,112.7,46,4,0),
('2024-04',1970000,164167,110000,29000,-69000, 70000,107.9,47,2,1),
('2024-05',2050000,170833,140000,61000,-21000,180000,113.6,49,3,0),
('2024-06',2120000,176667,160000,44000,-134000,70000,107.2,50,3,2),
('2024-07',2230000,185833,210000,55000,-25000,240000,114.8,53,4,0),
('2024-08',2310000,192500,130000,48000,-28000,150000,112.4,54,2,0),
('2024-09',2220000,185000,155000,62000,-27000,190000,112.1,56,2,1);


CREATE OR REPLACE TABLE `saasmetrics.support_tickets` (
  ticket_id      STRING NOT NULL,
  customer_id    STRING,
  created_date   DATE,
  resolved_date  DATE,
  severity       STRING,
  category       STRING,
  subject        STRING,
  status         STRING,
  csat_score     INT64,
  resolution_hrs INT64
);

INSERT INTO `saasmetrics.support_tickets` VALUES
('T001','C001','2024-07-03','2024-07-03','P2','Integration','SIEM connector dropping events',       'Resolved', 5,  4),
('T002','C001','2024-08-14','2024-08-15','P1','Outage',     'Dashboard unavailable 45 minutes',     'Resolved', 4, 18),
('T003','C002','2024-06-22','2024-06-23','P2','Feature',    'API rate limit increase request',       'Resolved', 5,  8),
('T004','C003','2024-04-10','2024-04-11','P3','Billing',    'Invoice discrepancy Q1 2024',           'Resolved', 3, 24),
('T005','C004','2024-09-01','2024-09-02','P2','Integration','SSO config issue post-upgrade',         'Resolved', 5, 10),
('T006','C005','2024-07-18',NULL,         'P3','Feature',   'Request: mobile app support',           'Open',    NULL,NULL),
('T007','C006','2024-05-20','2024-05-21','P1','Outage',     'API 500 errors APAC region',            'Resolved', 2, 14),
('T008','C006','2024-07-09','2024-07-10','P2','Performance','Dashboard queries over 30 seconds',     'Resolved', 3, 16),
('T009','C006','2024-08-30',NULL,         'P2','Contract',  'Renewal terms clarification',           'Escalated',NULL,NULL),
('T010','C007','2024-09-05','2024-09-05','P3','Onboarding', 'User provisioning walkthrough',         'Resolved', 5,  2),
('T011','C008','2024-10-02','2024-10-02','P3','Onboarding', 'Admin role setup assistance',           'Resolved', 5,  3),
('T012','C016','2024-08-22','2024-08-23','P3','Billing',    'Seat count overage billing query',      'Resolved', 4,  6),
('T013','C018','2024-09-15','2024-09-16','P2','Integration','Active Directory sync failing',         'Resolved', 5, 12),
('T014','C020','2024-08-10','2024-08-11','P2','Performance','Report generation timeout',             'Resolved', 4,  9),
('T015','C001','2024-09-20','2024-09-20','P3','Feature',    'Custom alert threshold configuration',  'Resolved', 5,  1),
('T016','C005','2024-09-10',NULL,         'P3','General',   'No CSM response after 2 follow-ups',   'Escalated',NULL,NULL),
('T017','C006','2024-09-25',NULL,         'P1','Contract',  'Acquisition-related contract hold',     'Escalated',NULL,NULL);


CREATE OR REPLACE TABLE `saasmetrics.usage_metrics` (
  customer_id      STRING,
  month            STRING,
  active_users     INT64,
  seats_contracted INT64,
  seat_utilization FLOAT64,
  api_calls        INT64,
  alerts_triggered INT64,
  alerts_actioned  INT64,
  logins_per_user  FLOAT64,
  feature_adoption FLOAT64
);

INSERT INTO `saasmetrics.usage_metrics` VALUES
('C001','2024-07',812, 850,0.955,482000,1240,1180,18.2,0.78),
('C001','2024-08',851, 850,1.001,531000,1380,1320,19.1,0.81),
('C001','2024-09',848, 970,0.874,510000,1290,1255,18.7,0.82),
('C002','2024-07',589, 620,0.950,290000, 880, 820,15.4,0.70),
('C002','2024-08',601, 620,0.969,310000, 910, 860,16.0,0.72),
('C002','2024-09',595, 620,0.960,295000, 895, 840,15.7,0.71),
('C004','2024-07',128, 150,0.853,145000, 320, 290,12.1,0.55),
('C004','2024-08',131, 150,0.873,152000, 335, 308,12.5,0.57),
('C004','2024-09',135, 150,0.900,158000, 341, 318,12.9,0.58),
('C005','2024-07', 28,  45,0.622, 22000,  48,  32, 8.1,0.38),
('C005','2024-08', 25,  45,0.556, 19000,  41,  27, 7.2,0.35),
('C005','2024-09', 22,  45,0.489, 17000,  38,  22, 6.5,0.31),
('C006','2024-07',980,1100,0.891,620000,2100,1980,14.2,0.65),
('C006','2024-08',960,1100,0.873,590000,2050,1920,13.8,0.63),
('C006','2024-09',890,1100,0.809,540000,1880,1720,12.5,0.58),
('C007','2024-08', 28,  30,0.933, 18000,  55,  45,10.2,0.45),
('C007','2024-09', 30,  30,1.000, 21000,  62,  55,11.1,0.50),
('C008','2024-10',155, 175,0.886, 98000, 210, 195,13.5,0.52),
('C018','2024-07',162, 190,0.853,182000, 420, 390,13.2,0.60),
('C018','2024-08',168, 190,0.884,191000, 435, 405,13.8,0.62),
('C018','2024-09',174, 190,0.916,198000, 448, 420,14.1,0.64),
('C020','2024-07',118, 145,0.814,142000, 330, 295,11.5,0.53),
('C020','2024-08',122, 145,0.841,148000, 345, 310,12.0,0.55),
('C020','2024-09',125, 145,0.862,153000, 358, 322,12.3,0.56);
