import rov_comm
import ports

server = rov_comm.ZMQ_Server(data_template=0,
driver_port = ports.HYDRO_DRIVER_PORT,
client_port = ports.HYDRO_CLIENT_PORT)

server.run()
