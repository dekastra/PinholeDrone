import socket
import time
import threading

class Control:
    def __init__(self):
        self.local_ip = ''
        self.drone_ip = '192.168.10.1'
        self.port = 8889
        self.drone_add = (self.drone_ip, self.port)
        self.MAX_TIMEOUT = 15.0
        self.CLEAR = True
        self.resp = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.port))
        #send_command('command')
        #print('Activating SDK mode')

    def send_command(self, command, rc=False):
        if self.CLEAR is True:
            self.socket.sendto(command.encode('utf-8'), self.drone_add)
            print('Command: %s' % command)
            self.CLEAR = False
            if rc == False:
                try:
                    self.resp, ip = self.socket.recvfrom(1024)
                    print('Command response: %s' % self.resp)
                    self.CLEAR = True
                except socket.error as exc:
                    print('Caught exception socket.error: %s' % exc)
            else:
                self.CLEAR = True


    def take_off(self):
        self.send_command('takeoff')
        while not self.CLEAR:
            continue
        print('Drone is taking off')

    def land(self):
        self.send_command('land')
        while not self.CLEAR:
            continue
        print('Drone is landing')

    def emergency_stop(self):
        self.send_command('emergency')
        print('Emergency stop has been initiated!')

    def ascend(self, x):
        if x < 20.0 or x > 500.0:
            print('Value outside acceptable range')
            return
        command = 'up ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone ascends %d cm' % x)

    def descend(self, x):
        if x < 20.0 or x > 500.0:
            print('Value outside acceptable range')
            return
        command = 'down ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone descends %d cm' % x)

    def left_strafe(self, x):
        if x < 20.0 or x > 500.0:
            print('Value outside acceptable range')
            return
        command = 'left ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone strafe left %d cm' % x)

    def right_strafe(self, x):
        if x < 20.0 or x > 500.0:
            print('Value outside acceptable range')
            return
        command = 'right ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone strafe right %d cm' % x)

    def forward(self, x):
        if x < 20.0 or x > 500.0:
            print('Value outside acceptable range')
            return
        command = 'forward ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone move forward %d cm' % x)

    def backward(self, x):
        if x < 20.0 or x > 500.0:
            print('Value outside acceptable range')
            return
        command = 'back ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone move backward %d cm' % x)

    def rotate_right(self, x):
        if x < 1.0 or x > 360.0:
            print('Value outside acceptable range')
            return
        command = 'cw ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone rotate clockwise %d degree' % x)

    def rotate_left(self, x):
        if x < 1.0 or x > 360.0:
            print('Value outside acceptable range')
            return
        command = 'ccw ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone rotate counter clockwise %d degree' % x)

    def go_to(self, x, y, z, speed):
        if x < -500.0 or x > 500.0 or y < -500.0 or y > 500.0 or z < -500.0 or z > 500.0 or speed < 10.0 or speed > 100.0:
            print('Value outside acceptable range')
            return
        command = 'go ' + str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(speed)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Drone manouvers to x:%d cm, y: %d cm, z: %d cm' % (x, y, z))

    def rc_mode(self, a, b, c, d):
        if a < -100.0 or a > 100.0 or b < -100.0 or b > 100.0 or c < -100.0 or c > 100.0 or d < -100.0 or d > 100.0:
            print('Value outside acceptable range')
            return
        command = 'rc ' + str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d)
        self.send_command(command, rc=True)
        print('Drone uses rc mode')
        
    def set_speed(self, x):
        if x < 10.0 or x > 100.0:
            print('Value outside acceptable range')
            return
        command = 'speed ' + str(x)
        self.send_command(command)
        while not self.CLEAR:
            continue
        print('Setting drone speed to %d cm/s' % x)
