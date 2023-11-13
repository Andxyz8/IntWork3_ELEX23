#include "compass_module.h"

void init_i2c_config_compass_module(){
    i2c_config_t i2c_config_master_compass = {
        .mode = I2C_ESP_MODE_WITH_COMPASS_MODULE,
        .sda_io_num = GPIO_23_I2C_SDA_CMD,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = GPIO_19_I2C_SCL_CMD,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_MAX_SPEED,
        .clk_flags = 0
    };

    i2c_param_config(
        I2C_ESP_NUM_FOR_COMPASS_MODULE,
        &i2c_config_master_compass
    );

    i2c_driver_install(
        I2C_ESP_NUM_FOR_COMPASS_MODULE,
        I2C_ESP_MODE_WITH_COMPASS_MODULE,
        0, // As we are the master, we don't need the buffer
        0, // As we are the master, we don't need the buffer
        0  // Use of flags for interruptions
    );
}

void destroy_i2c_config_compass_module(){
    i2c_driver_delete(I2C_ESP_NUM_FOR_COMPASS_MODULE);
}

void start_command_sequece_write(){
    // Start command link
    i2c_cmd_compass_module = i2c_cmd_link_create();

    // Start command sequence
    i2c_master_start(i2c_cmd_compass_module);

    // Define which slave to write as a WRITE operation
    i2c_master_write_byte(
        i2c_cmd_compass_module,
        (I2C_COMPASS_MODULE_ADDRESS << 1) | I2C_MASTER_WRITE,
        1 // Enable ACK signal
    );
}

void start_command_sequence_read(){
    // Start command link
    i2c_cmd_compass_module = i2c_cmd_link_create();

    // Start command sequence
    i2c_master_start(i2c_cmd_compass_module);

    // Define which slave to write as a READ operation
    i2c_master_write_byte(
        i2c_cmd_compass_module,
        (I2C_COMPASS_MODULE_ADDRESS << 1) | I2C_MASTER_READ,
        1 // Enable ACK signal
    );
}

void set_compass_module(){
    // Select register SET/RESET from compass module to write
    i2c_master_write_byte(i2c_cmd_compass_module, 0x0B, 1);

    // Write into SET/REGISTER the value 0x01 (SET)
    i2c_master_write_byte(i2c_cmd_compass_module, 0x01, 1);
}

void set_compass_module_config(){
    // Select Control Register to write
    i2c_master_write_byte(i2c_cmd_compass_module, 0x09, 1);

    // Write into Control Register the value 
    i2c_master_write_byte(i2c_cmd_compass_module, 0x5D, 1);
}

void end_command_sequence(){
    // End command sequence
    i2c_master_stop(i2c_cmd_compass_module);

    // Send all the queued commands on the I2C bus
    i2c_master_cmd_begin(
        I2C_ESP_NUM_FOR_COMPASS_MODULE,
        i2c_cmd_compass_module,
        pdMS_TO_TICKS(1000)
    );
    // Free the I2C commands list
    i2c_cmd_link_delete(i2c_cmd_compass_module);
}

void initialize_compass_module(){
    start_command_sequece_write();
    set_compass_module();
    end_command_sequence();

    start_command_sequece_write();
    set_compass_module_config();
    end_command_sequence();

    start_command_sequece_write();
    // Point the register to read raw data
    i2c_master_write_byte(i2c_cmd_compass_module, 0x00, 1);
    end_command_sequence();
}

void read_compass_module_raw_data(uint8_t* raw_data){
    start_command_sequence_read();

    // Read bytes from compass module
    i2c_master_read_byte(i2c_cmd_compass_module, raw_data,   0); //"Data Output X MSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, raw_data+1, 0); //"Data Output X LSB Register"

    // Even if we don't use later, we must read to move the read pointer to the next registers
    i2c_master_read_byte(i2c_cmd_compass_module, raw_data+2, 0); //"Data Output Z MSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, raw_data+3, 0); //"Data Output Z LSB Register"

    i2c_master_read_byte(i2c_cmd_compass_module, raw_data+4, 0); //"Data Output Y MSB Register"
    i2c_master_read_byte(i2c_cmd_compass_module, raw_data+5, 1); //"Data Output Y LSB Register "

    end_command_sequence();
}

int proccess_compass_module_raw_data(uint8_t* raw_data){
    // Must combine raw data to get the raw components value
    short x = raw_data[0] << 8 | raw_data[1];
    // As we don't use, there's no need to calculate
    short z = raw_data[2] << 8 | raw_data[3];
    short y = raw_data[4] << 8 | raw_data[5];

    printf("%d\t %d\t %d\n", x, y, z);

    // Convert componentes into angle in degrees
    int angle = atan2((double) y, (double) x) * (180 / 3.14159265) + 180;

    return angle;
}

int get_compass_module_degrees(){
    initialize_compass_module();

    // Instantiate raw data array
    uint8_t* raw_data = (uint8_t*) malloc(6 * sizeof(uint8_t));
    
    read_compass_module_raw_data(raw_data);

    // printf("DATA0: %d\n", raw_data[0]);
    // printf("DATA1: %d\n", raw_data[1]);
    // printf("DATA2: %d\n", raw_data[2]);
    // printf("DATA3: %d\n", raw_data[3]);
    // printf("DATA4: %d\n", raw_data[4]);
    // printf("DATA5: %d\n", raw_data[5]);

    int var = proccess_compass_module_raw_data(raw_data);

    free(raw_data);
    // printf("%f\n", angle);
    return var;
}
