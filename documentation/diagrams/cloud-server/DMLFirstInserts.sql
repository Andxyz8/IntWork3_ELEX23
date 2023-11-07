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