"""ServerSide mode

Creates mock server which sends all the data to main server,
main part of application.
"""

__author__ = 'Ales Lerch'

import threading
import multiprocessing
import socket
import signal
import logging
import sys
import ssl
import http_parser as hp
import exploit_checker as ec
import multiprocessing
import exploit_manager as em

class ServerSide:

    TIMEOUT = 0.1

    def __init__(self,host = '',port = 80,genFD = False):
        self.host = host
        self.port = port
        self.log = logging.getLogger('mainLogger')
        self.exCh = ec.ExploitChecker(genFD)
        self.emanager = em.ExploitManager(self.exCh)
        self.genFakeData = genFD

    def activate_mock_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.log.info('Activating fake server on adress %s and on port %s' % (self.host,self.port))
            self.sock.bind((self.host, self.port))
        except:
            self.log.error('Unable to set fake server on port %s' % self.port)
            broken_port = self.port
            self.port = 8080

            try:
                self.sock.bind((self.host,self.port))
            except:
                self.log.error('Failed to set fake server on 8080 and %s' % broken_port)
                self.shutdown()
        self.log.info('Fake server is set on port %s' % self.port)
        self.listen()

    def shut_down(self):
        try:
            self.emanager.exploit_queue.close()
            self.emanager.exploit_queue.join_thread()
            for process in multiprocessing.active_children():
                self.log.info("Shutting down process %r", process)
                process.terminate()
                process.join()
            self.log.info('Shutting down fake server')
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        except Exception as e:
            self.log.warning('Failed to shutdown, reason: %s' % e)

    def connect_to_server(self,server_host = '', server_port = 8888,
            ssl_option = False, server_timeout = 0.1):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ssl_option:
            ssl_sock = ssl.wrap_socket(server_socket,
                    ca_certs="server.crt",
                    cert_reqs=ssl.CERT_REQUIRED)
        server_socket.settimeout(server_timeout)
        try:
            self.log.info('Trying to create connection to server on port %s' % server_port)
            if ssl_option:
                ssl_sock.connect((server_host,server_port))
                #print(repr(ssl_sock.getpeername()))
                #print(ssl_sock.cipher())
                #print(pprint.pformat(ssl_sock.getpeercert()))
            else:
                server_socket.connect((server_host,server_port))
        except Exception as e:
            self.log.error('Failed to connect to server, reason:%s' % e)

        self.log.info('Connection success')
        return server_socket

    def listen(self,ssl_option = False, client_timeout = 0.1):
        self.log.info('Fake server is listening on port %s' % self.port)
        #core_num = multiprocessing.cpu_count()
        process = multiprocessing.Process(target=self.emanager.que_checking)
        process.daemon = True
        process.start()

        self.sock.listen(5)

        while True:
            client, client_address = self.sock.accept()
            client.settimeout(client_timeout)
            if ssl_option:
                ssl_sock = ssl.wrap_socket(client,
                        ca_certs="/etc/ssl/certs/ca-certificates.crt",
                        cert_reqs=ssl.CERT_REQUIRED)
                client = ssl_sock
            try:
                self.log.info('Creating new thread: %s' % threading.current_thread())
                process = multiprocessing.Process(target=self.socket_handler, args=(client, client_address))
                process.daemon = True
                process.start()
            except Exception as e:
                self.log.error('Failed to create new thread, reason %s' % e)
                executor.shutdown()
                client.send(b"""HTTP/1.0 500 Internal Server
                                Error\r\nContent-Type:text/html\r\n\r\n<head>\n<title>Error
                                500</title>\n</head>\n<body>\n<h1>Error 500 internal
                                Error</h1>\n""")
                client.close()
                #save the thread somehow?

    def socket_handler(self,client_handler,client_address):
        while True:
            server_handler = self.connect_to_server()
            try:
                client_data = self.get_data_from(client_handler)
                if client_data:
                    try:
                        hparser = hp.HTTPRequest(client_data,client_handler,
                                client_address,self.genFakeData)
                        #self.emanager.add_to_que(hparser.get_info_data())
                        self.emanager.exploit_queue.put(hparser.get_data())
                        #self.exCh.checkThisData(hparser.get_info_data())
                    except AttributeError as a:
                        self.log.warning('Could not parse input data:%s' % a)

                    server_handler.sendall(client_data)
                    server_data = self.get_data_from(server_handler)

                    if server_data:
                        client_handler.send(server_data)
                    else:
                        raise TimeoutError('[Warning] Server connection lost')
                else:
                    raise TimeoutError('[Warning] Client connection %s on adress %s lost' % (client_handler,client_address))
            except Exception as e:
                self.log.error('Socket handler failed to link data between client and server,reason: %s' % e)

                try:
                    self.log.info('Closing server connection')
                    server_handler.close()
                except Exception as e:
                    self.log.warning('Failed to close server side connection, reason: %s' % e)

                try:
                    client_handler.close()
                except Exception as e:
                    self.log.warning('Failed to close client side connection, reason %s' % e)
            finally:
                break

    def get_data_from(self,specific_socket):
        """Get data from client or server. Return sum of byte string or empty
        byte string 
        >>> get_data_from('')
        b''
        """
        totall_data = b''
        while True:
            buffer_data = b''
            try:
                buffer_data = specific_socket.recv(1024)
                #self.save_data.append(bytes.decode(buffer_data))
                if not buffer_data:
                    break
            except socket.timeout:
                break
            except Exception as e:
                self.log.error('Failed to recive data from specific socket: %s' % e)
            totall_data = totall_data + buffer_data
        return totall_data

if __name__ == "__main__":
    try:
        s = ServerSide('localhost',8887)
        s.activate_mock_server()
    except KeyboardInterrupt:
        pass
    finally:
        s.shut_down()
