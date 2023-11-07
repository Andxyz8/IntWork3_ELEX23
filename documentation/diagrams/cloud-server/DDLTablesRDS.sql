CREATE TABLE IF NOT EXISTS user_patrole(
    id_user SERIAL PRIMARY KEY NOT NULL,
    username VARCHAR,
    password VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS route(
    id_route SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR,
    description VARCHAR,
    status VARCHAR,
    number_repeats INTEGER,
    interval_between_repeats TIMESTAMP,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_has_route(
  id_user_has_route SERIAL PRIMARY KEY NOT NULL,
  id_user INTEGER,
  id_route INTEGER,
  relation VARCHAR,
  CONSTRAINT fk_tb_user_patrole_column_id_user_user_has_route FOREIGN KEY (id_user) REFERENCES user_patrole (id_user),
  CONSTRAINT fk_tb_route_column_id_route_user_has_route FOREIGN KEY (id_route) REFERENCES route (id_route)
);

CREATE TABLE IF NOT EXISTS route_steps(
    id_route_step SERIAL PRIMARY KEY NOT NULL,
    id_route INTEGER,
    step_sequence VARCHAR,
    start_aruco_marker INTEGER,
    next_aruco_marker INTEGER,
    number_rotations_left_encoder DECIMAL,
    number_rotations_right_encoder DECIMAL,
    right_pwm_intensity DECIMAL,
    left_pwm_intensity DECIMAL,
    compass_module_degrees DECIMAL,
    CONSTRAINT fk_tb_route_column_id_route_route_steps FOREIGN KEY (id_route) REFERENCES route (id_route)
);

CREATE TABLE IF NOT EXISTS robot(
    id_robot SERIAL PRIMARY KEY NOT NULL,
    id_user_owner INTEGER,
    qr_code_info VARCHAR,
    has_ultrassonic_sensor BOOL,
    has_compass_module BOOL,
    has_smoke_sensor BOOL,
    created_at TIMESTAMP,
    CONSTRAINT fk_tb_user_patrole_column_id_user_robot FOREIGN KEY (id_user_owner) REFERENCES user_patrole (id_user)
);

CREATE TABLE IF NOT EXISTS route_execution(
  id_route_execution SERIAL PRIMARY KEY NOT NULL,
  id_robot INTEGER,
  id_route INTEGER,
  moment_start TIMESTAMP,
  moment_end TIMESTAMP,
  CONSTRAINT fk_tb_route_column_id_route_route_execution FOREIGN KEY (id_route) REFERENCES route (id_route),
  CONSTRAINT fk_tb_robot_column_id_robot_route_execution FOREIGN KEY (id_robot) REFERENCES robot (id_robot)
);

CREATE TABLE IF NOT EXISTS sensor_reading(
  id_sensor_reading SERIAL PRIMARY KEY NOT NULL,
  id_route_execution INTEGER,
  sensor VARCHAR,
  value VARCHAR,
  moment TIMESTAMP,
  CONSTRAINT fk_tb_route_execution_column_id_route_execution_sensor_reading FOREIGN KEY (id_route_execution) REFERENCES route_execution (id_route_execution)
);

CREATE TABLE IF NOT EXISTS alarm_triggering(
  id_alarm_triggering SERIAL PRIMARY KEY NOT NULL,
  id_route_execution INTEGER,
  reason VARCHAR,
  moment TIMESTAMP,
  CONSTRAINT fk_tb_route_execution_column_id_route_execution_alarm_triggering FOREIGN KEY (id_route_execution) REFERENCES route_execution (id_route_execution)
);

CREATE TABLE IF NOT EXISTS camera_triggering(
  id_camera_triggering SERIAL PRIMARY KEY NOT NULL,
  id_route_execution INTEGER,
  reason VARCHAR,
  image_url VARCHAR,
  moment TIMESTAMP,
  CONSTRAINT fk_tb_route_execution_column_id_route_execution_camera_triggeri FOREIGN KEY (id_route_execution) REFERENCES route_execution (id_route_execution)
);

CREATE TABLE IF NOT EXISTS notification(
  id_notification SERIAL PRIMARY KEY NOT NULL,
  id_route_execution INTEGER,
  message VARCHAR,
  value VARCHAR,
  moment TIMESTAMP,
  CONSTRAINT fk_tb_route_execution_column_id_route_execution_notification FOREIGN KEY (id_route_execution) REFERENCES route_execution (id_route_execution)
);
