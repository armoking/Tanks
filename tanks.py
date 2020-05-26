from tkinter import *
from random import randrange
import time

DIM = 20

field = [['.' for y in range(DIM)] for x in range(DIM)]
directions = [(32, 0), (0, 32), (-32, 0), (0, -32)]
bullets = []
tanks = []

tk = Tk()
tk.title('tanks')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=DIM * 32, height=DIM * 32, highlightthickness=0)
canvas.pack()


class Bullet:
    def __init__(self, x, y, dir, color):
        self.x = x
        self.y = y
        self.dir = dir
        self.damage = 30
        self.color = color
        self.id = canvas.create_oval(8, 8, 24, 24, fill=color)
        canvas.move(self.id, self.x, self.y)

    def move(self):
        dx, dy = directions[self.dir]
        nx = self.x + dx
        ny = self.y + dy
        if nx < 0 or ny < 0 or nx >= DIM * 32 or ny >= DIM * 32:
            self.damage = 0
            return
        self.x = nx
        self.y = ny
        self.damage = self.damage - 1
        canvas.move(self.id, dx, dy)


class Tank:
    def __init__(self, x, y, dir, index, color):
        self.x = x
        self.y = y
        self.dir = dir
        self.hp = 1
        self.index = index
        self.color = color
        self.id = canvas.create_rectangle(0, 0, 32, 32, fill=color)
        canvas.move(self.id, self.x, self.y)

    def move(self):
        dx, dy = directions[self.dir]
        nx = self.x + dx
        ny = self.y + dy
        if nx < 0 or ny < 0 or nx >= DIM * 32 or ny >= DIM * 32:
            return
        for tank in tanks:
            if tank.x == nx and tank.y == ny:
                return
        self.x = nx
        self.y = ny
        canvas.move(self.id, dx, dy)

    def change_dir(self, next_dir):
        self.dir = next_dir % len(directions)

    def fire(self):
        bullet = Bullet(self.x, self.y, self.dir, self.color)
        bullet.move()
        bullets.append(bullet)


def move_bullets():
    remove_bullets = []
    for bullet in bullets:
        if bullet.damage <= 0:
            remove_bullets.append(bullet)
        else:
            for tank in tanks:
                if tank.x == bullet.x and tank.y == bullet.y:
                    tank.hp -= bullet.damage
                    remove_bullets.append(bullet)
                    break
            if bullet not in remove_bullets:
                bullet.move()
    for bullet in remove_bullets:
        if bullet in bullets:
            canvas.delete(bullet.id)
            bullets.remove(bullet)


def move_tanks():
    remove_tanks = []
    for tank in tanks:
        if tank.hp <= 0:
            remove_tanks.append(tank)
            continue
        action = randrange(6)
        if action < 4:
            if tank.dir == action:
                tank.move()
            else:
                tank.change_dir(action)
        elif action == 4:
            tank.fire()
    for tank in remove_tanks:
        if tank in tanks:
            canvas.delete(tank.id)
            print('tank ' + str(tank.index) + ' is dead now')
            tanks.remove(tank)


tk.update()


def get_rand_color():
    colors = list('0123456789abcdef')
    ans = '#'
    for i in range(6):
        ans += colors[randrange(16)]
    return ans


def spawn_tank(index):
    x, y = randrange(DIM) * 32, randrange(DIM) * 32
    dir = randrange(4)
    tank = Tank(x, y, dir, index, get_rand_color())
    tanks.append(tank)


def game():
    tanks.clear()
    bullets.clear()
    tanks_count = randrange(4, 6)
    for i in range(tanks_count):
        spawn_tank(i + 1)

    while len(tanks) > 1:
        print([tank.id for tank in tanks])
        move_tanks()
        move_bullets()
        move_bullets()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.04)

    time.sleep(1)
    print(str(tanks[0].index) + ' won the game!!!')
    print('------------')


game()
