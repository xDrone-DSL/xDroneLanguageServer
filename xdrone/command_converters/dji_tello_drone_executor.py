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
        self._running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((DJITelloExecutor.HOST_IP, DJITelloExecutor.RESPONSE_PORT))  # Bind for receiving
        self.waiting_for_resp = False

    def terminate(self):
        self._running = False
        self.sock.close()

    def recv(self):
        while self._running:
            while not self.waiting_for_resp:
                pass
            try:
                msg, _ = self.sock.recvfrom(1024)  # Read 1024-bytes from UDP socket
                info("received response: {}".format(msg.decode(encoding="utf-8")))
            except Exception as err:
                error(err)
            self.waiting_for_resp = False

    def send(self, msg):
        while self.waiting_for_resp:
            pass
        msg = msg.encode(encoding="utf-8")
        self.sock.sendto(msg, (DJITelloExecutor.TELLO_IP, DJITelloExecutor.COMMAND_PORT))
        info("sent message: {}".format(msg))  # Print message
        self.waiting_for_resp = True

    def execute_commands(self, commands: List[Command]):
        recvThread = threading.Thread(target=self.recv)
        recvThread.start()

        self.send("command")
        for command in commands:
            if command.opcode == "takeoff":
                self.send("takeoff")
            if command.opcode == "land":
                self.send("land")
            if command.opcode == "up":
                self.send("up" + " " + str(int(command.operands[0] * 100)))
            if command.opcode == "down":
                self.send("down" + " " + str(int(command.operands[0] * 100)))
            if command.opcode == "left":
                self.send("left" + " " + str(int(command.operands[0] * 100)))
            if command.opcode == "right":
                self.send("right" + " " + str(int(command.operands[0] * 100)))
            if command.opcode == "forward":
                self.send("forward" + " " + str(int(command.operands[0] * 100)))
            if command.opcode == "backward":
                self.send("back" + " " + str(int(command.operands[0] * 100)))
            if command.opcode == "rotate_left":
                self.send("ccw" + " " + str(int(command.operands[0])))
            if command.opcode == "rotate_right":
                self.send("cw" + " " + str(int(command.operands[0])))
            if command.opcode == "wait":
                time.sleep(command.operands[0])

        self.terminate()
        recvThread.join()
