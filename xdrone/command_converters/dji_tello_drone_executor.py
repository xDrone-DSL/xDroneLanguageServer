import socket
import threading
import time
from logging import info, error
from typing import List

from xdrone.shared.command import Command


class DJITelloExecutor:
    TELLO_IP = "192.168.10.1"
    COMMAND_PORT = 8889
    HOST_IP = "0.0.0.0"
    RESPONSE_PORT = 9000

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((DJITelloExecutor.HOST_IP, DJITelloExecutor.RESPONSE_PORT))
        self.recv_thread = threading.Thread(name="Thread-Receive", target=self._recv)
        self.recv_thread.daemon = True
        self.running = True
        self.waiting_for_resp = False

    def _terminate(self):
        while self.waiting_for_resp:
            pass
        self.running = False
        self.sock.close()

    def _recv(self):
        while True:
            while not self.waiting_for_resp:
                if not self.running:
                    return
            try:
                msg, _ = self.sock.recvfrom(1024)
                info("received response: {}".format(msg.decode(encoding="utf-8")))
            except Exception as err:
                if self.running:
                    error("Error met when receiving response: " + str(err))
            self.waiting_for_resp = False

    def _send(self, msg):
        while self.waiting_for_resp:
            pass
        msg = msg.encode(encoding="utf-8")
        self.sock.sendto(msg, (DJITelloExecutor.TELLO_IP, DJITelloExecutor.COMMAND_PORT))
        info("sent message: {}".format(msg))
        self.waiting_for_resp = True

    def _emergency(self):
        msg = "emergency".encode(encoding="utf-8")
        self.sock.sendto(msg, (DJITelloExecutor.TELLO_IP, DJITelloExecutor.COMMAND_PORT))
        self.waiting_for_resp = False

    def execute_commands(self, commands: List[Command]):
        try:
            self.recv_thread.start()

            self._send("command")
            for command in commands:
                if command.opcode == "takeoff":
                    self._send("takeoff")
                if command.opcode == "land":
                    self._send("land")
                if command.opcode == "up":
                    self._send("up" + " " + str(int(command.operands[0] * 100)))
                if command.opcode == "down":
                    self._send("down" + " " + str(int(command.operands[0] * 100)))
                if command.opcode == "left":
                    self._send("left" + " " + str(int(command.operands[0] * 100)))
                if command.opcode == "right":
                    self._send("right" + " " + str(int(command.operands[0] * 100)))
                if command.opcode == "forward":
                    self._send("forward" + " " + str(int(command.operands[0] * 100)))
                if command.opcode == "backward":
                    self._send("back" + " " + str(int(command.operands[0] * 100)))
                if command.opcode == "rotate_left":
                    self._send("ccw" + " " + str(int(command.operands[0])))
                if command.opcode == "rotate_right":
                    self._send("cw" + " " + str(int(command.operands[0])))
                if command.opcode == "wait":
                    time.sleep(command.operands[0])
        except KeyboardInterrupt:
            self._emergency()
            info("KeyboardInterrupt received. Forced stop.")
        finally:
            self._terminate()
            if self.recv_thread.is_alive():
                self.recv_thread.join()
