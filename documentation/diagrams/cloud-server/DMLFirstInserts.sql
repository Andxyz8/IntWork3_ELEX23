-- TABLE: user_patrole
INSERT INTO user_patrole(
  username,
  password,
  created_at
) VALUES(
  'admin',
  'admin',
  TIMESTAMP '2023-11-07 16:43:21'
);


-- TABLE: robot
INSERT INTO robot(
  id_user_owner,
  has_ultrassonic_sensor,
  has_compass_module,
  has_smoke_sensor,
  created_at
) VALUES(
  1,
  FALSE,
  FALSE,
  FALSE,
  TIMESTAMP '2023-11-07 16:45:37'
);

INSERT INTO route(
  title,
  description,
  status,
  number_repeats,
  interval_between_repeats,
  created_at
) VALUES(
  'Test Route',
  'Testing functionalities',
  'Active',
  3,
  TIMESTAMP '2023-11-07 00:15:00',
  TIMESTAMP '2023-11-07 20:23:05'
);
