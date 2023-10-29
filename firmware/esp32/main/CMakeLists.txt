idf_component_register(
    SRCS "main.c" "handlers/taskHandler.c" "handlers/i2cHandler.c" "utils/byte_operator.c"
    INCLUDE_DIRS "." "./handlers" "./utils"
)
