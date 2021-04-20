import logging
import unittest
from unittest.mock import Mock, call

from xdrone.command_converters.dji_tello_drone_executor import DJITelloExecutor
from xdrone.shared.command import Command


class TestDJITelloExecutor(unittest.TestCase):

    def test_dji_tello_executor_should_send_correct_message(self) -> None:
        mocked_socket = Mock()
        mocked_socket.recvfrom = Mock(return_value=(b'ok', ('192.168.10.1', 8889)))
        mocked_socket.sendto = Mock()
        commands = [Command.takeoff(),
                    Command.up(1),
                    Command.down(1),
                    Command.left(1),
                    Command.right(1),
                    Command.forward(1),
                    Command.backward(1),
                    Command.rotate_left(90),
                    Command.rotate_right(90),
                    Command.wait(0),
                    Command.land()]
        executor = DJITelloExecutor()
        executor.sock.close()
        executor.sock = mocked_socket
        with self.assertLogs(logging.getLogger()) as log:
            executor.execute_commands(commands)
        calls = [call(b"command", ('192.168.10.1', 8889)),
                 call(b"takeoff", ('192.168.10.1', 8889)),
                 call(b"up 100", ('192.168.10.1', 8889)),
                 call(b"down 100", ('192.168.10.1', 8889)),
                 call(b"left 100", ('192.168.10.1', 8889)),
                 call(b"right 100", ('192.168.10.1', 8889)),
                 call(b"forward 100", ('192.168.10.1', 8889)),
                 call(b"back 100", ('192.168.10.1', 8889)),
                 call(b"ccw 90", ('192.168.10.1', 8889)),
                 call(b"cw 90", ('192.168.10.1', 8889)),
                 call(b"land", ('192.168.10.1', 8889))]
        mocked_socket.sendto.assert_has_calls(calls)
        expected_log = ["INFO:root:sent message: b'command'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'takeoff'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'up 100'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'down 100'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'left 100'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'right 100'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'forward 100'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'back 100'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'ccw 90'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'cw 90'",
                        "INFO:root:received response: ok",
                        "INFO:root:sent message: b'land'",
                        "INFO:root:received response: ok"]
        self.assertEqual(expected_log, log.output)

    def test_dji_tello_executor_if_receive_error_should_print(self) -> None:
        mocked_socket = Mock()
        mocked_socket.recvfrom = Mock(side_effect=Exception('exception'))
        mocked_socket.sendto = Mock()
        commands = [Command.takeoff(),
                    Command.land()]
        executor = DJITelloExecutor()
        executor.sock.close()
        executor.sock = mocked_socket
        with self.assertLogs(logging.getLogger()) as log:
            executor.execute_commands(commands)
        calls = [call(b"command", ('192.168.10.1', 8889)),
                 call(b"takeoff", ('192.168.10.1', 8889)),
                 call(b"land", ('192.168.10.1', 8889))]
        mocked_socket.sendto.assert_has_calls(calls)
        expected_log = ["INFO:root:sent message: b'command'",
                        "ERROR:root:exception",
                        "INFO:root:sent message: b'takeoff'",
                        "ERROR:root:exception",
                        "INFO:root:sent message: b'land'",
                        "ERROR:root:exception"]
        self.assertEqual(expected_log, log.output)
