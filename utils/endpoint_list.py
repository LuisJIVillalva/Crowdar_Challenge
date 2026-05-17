from core.envs import read_config_file
HOST = read_config_file("BACKEND", "host")

GET_DEPARTMENTS = HOST + "menu/departments"