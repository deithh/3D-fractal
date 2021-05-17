class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0

    def dequeue(self):
        if self.head is None:
            return None
        temp = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None
        self.len -= 1
        return temp

    def enqueue(self, data):
        if self.tail is None:
            self.head = Node(data)
            self.tail = self.head
        else:
            self.tail.next = Node(data)
            self.tail.next.prev = self.tail
            self.tail = self.tail.next
        self.len += 1

    def is_empty(self):
        if not self.len:
            return True
        return False
    def __len__(self):
        return self.len
    def clear(self):
        self.head = None
        self.tail = None
        self.len = 0

class Camera:
    def __init__(self):
        self.__Rx = width/2
        self.__Ry = height/2
        self.__Rz = 0
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__step = 5
        self.__Rstep = .01
        
    def rotateX(self, sign):
        if sign:
            self.__Rx += self.__step
        else:
            self.__Rx -= self.__step
        
    def rotateY(self, sign):
        if sign:
            self.__Ry += self.__step
        else:
            self.__Ry -= self.__step
            
    def moveX(self, sign):
        if sign:
            self.__x += self.__step
        else:
            self.__x -= self.__step
            
    def moveZ(self, sign):
        if sign:
            self.__z += self.__step
        else:
            self.__z -= self.__step
        
        
    def process_events(self):
        
        while not events.is_empty():
            
            event = events.dequeue()

            if event == RIGHT:
                self.rotateY(1)
            elif event == LEFT:
                self.rotateY(0)
            elif event == UP:
                self.rotateX(1)
            elif event == DOWN:
                self.rotateX(0)
            elif event == 68: #d
                self.moveX(0)
            elif event == 65: #a
                self.moveX(1)
            elif event == 87: #w
                self.moveZ(0)
            elif event == 83: #s
                self.moveZ(1)
            
                
            
    def update(self):
        self.process_events()
        look = PVector(self.__Rx, self.__Ry, self.__Rz)
        camera(self.__x, self.__y, self.__z,
               self.__Rx, self.__Ry, self.__Rz,
               0,-1,0)
        pushMatrix()


    
class Objects:
    def __init__(self):
        self.__objects = []
        self.__len = 0
        
    def add(self, object):
        self.__objects.append(object)
        self.__len += 1
        
        
    def draw(self):
        for object in self.__objects:
            object.draw()
    
    def __len__(self):
        return self.__len
    
class Object:
    def __init__(self, func, size, x, y, z):
        self.__func = func
        self.__size = size
        self.__x = x
        self.__y = y
        self.__z = z
        
    def draw(self):
        translate(self.__x, self.__y, self.__z)
        fill(*self.calc_color())
        self.__func(self.__size)
        translate(-self.__x, -self.__y, -self.__z)
        
    def calc_color(self):
        return self.hsv2rgb(self.__size / max_size * 255)
    
    @staticmethod
    def hsv2rgb(hue, sat = 1, val = 1):

        c = sat * val
        x = c * (1 - abs((hue/60) % 2 - 1))
        m = val - c
        if 60 > hue:
            rgb = (c,x,0)
        elif 120 > hue:
            rgb = (x,c,0)
        elif 180 > hue:
            rgb = (0,c,x)
        elif 240 > hue:
            rgb = (0,x,c)
        elif 300 > hue:
            rgb = (x,0,c)
        elif 360 > hue:
            rgb = (c,0,x)
        else:
            return -1
    
    
        rgb = [int((i+m)*255) for i in rgb]
        return rgb


    
def fractal(func, size, x, y, z):
    objects.add(Object(func, size, x, y, z))
    dis = size     
    nsize = size//2.3
    if nsize > 0:
        fractal(func, nsize, x + dis, y, z)
        fractal(func, nsize, x - dis, y, z)
        
        fractal(func, nsize, x, y + dis, z)
        fractal(func, nsize, x, y - dis, z)
        
        fractal(func, nsize, x, y, z + dis)
        fractal(func, nsize, x, y, z - dis)
        

def keyPressed():
    events.enqueue(keyCode)


def setup():
    global cam, events, objects, max_size 
    hint(ENABLE_KEY_REPEAT)
    max_size = 200
    cam = Camera()
    events = Queue()
    objects = Objects()
    fractal(box, max_size, 500, 500, 0)
    print(len(objects))
    size(1000, 1000, P3D)
    fill(50)


            
                                    
def draw():
    
    background(255);
    cam.update()
    lights()
    objects.draw() 
    popMatrix()

    events.clear()

    

    
    
