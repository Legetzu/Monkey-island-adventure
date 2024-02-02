import tkinter as tk
import random
import time
import threading
import winsound


monkey = None
monkey_coords = None
monkeys = []
monkey_canvas = []
aware_monkeys = []
in_water = []
island_count = 0
stop = False

class Monkey:
    def __init__(self, aware, swimming, on_island, x, y, canvas):
        self.aware = aware
        self.swimming = swimming
        self.on_island = on_island
        self.x = x
        self.y = y
        self.canvas = canvas
    
    def is_aware(self):
        if self.aware is True:
            return True
        else: return False

class Island:
    def __init__(self, dock, x, y, canvas, text):
        self.dock = dock
        self.name = f'S{island_count}'
        self.x = x
        self.y = y
        self.canvas = canvas
        self.text = text



def create_new_island():
    global island_count
    global stop
    stop = False
    while True:
        x = random.randint(50, 750)
        y = random.randint(50, 450)
        overlapping = False
        for island in islands:
            coords = canvas.coords(island.canvas)
            if coords and abs(coords[0] - x) < 100 and abs(coords[1] - y) < 100:
                overlapping = True
                break
        if not overlapping:
            break
        
    island_count = len(islands) + 1
    island = Island(False,x,y,canvas.create_rectangle(x, y, x + 100, y + 100, fill="green"), canvas.create_text((x + 50, y + 65), text="10", fill="white"))
    islands.append(island)
    canvas.create_text((x + 50, y + 50), text=island.name, fill="white")

    if island.name == "S1":
        add_dock(island)
        island.dock = True
        add_aware_monkeys(island)
    
    else:
        add_monkeys(island)

    canvas.tag_raise("monkey")

def add_monkeys(island):
    
    if island:
        for _ in range(10):
            add_monkey(island)
            canvas.update()
            
def add_aware_monkeys(island):
    if island:
        for _ in range(10):
            add_aware_monkey(island)
            canvas.update()

def move_to_sea():
    if monkeys:
        for i in range(len(monkeys)):
                if monkeys[i].aware is True and monkeys[i].swimming is False:
                    monkey = monkeys[i]
                    for island in islands:
                        if monkey.on_island is island.name:
                            chosen_island = island
                    x, y, _, _ = canvas.coords(chosen_island.canvas)
                    monkeys[i].swimming = True
                    t = threading.Thread(target=monkey_swim, args=(chosen_island, monkey))
                    t.start()
                    return
                
def move_to_sea_auto():
    if monkeys:
        for island in islands:
            for i in range(len(monkeys)):
                if monkeys[i].aware is True and monkeys[i].swimming is False:
                    monkey = monkeys[i]
                    if monkey.on_island is island.name:
                        x, y, _, _ = canvas.coords(island.canvas)
                        monkeys[i].swimming = True
                        t = threading.Thread(target=monkey_swim, args=(island, monkey))
                        t.start()
                        break


def monkey_swim(island, monkey):
    global stop
    x, y, _, _ = canvas.coords(island.canvas)
    dest_x, dest_y = random.choice([(x - 1000, y + 50), (x + 1000, y + 50), (x + 50, y + 1000), (x + 50, y - 1000)])

    coords = []
    coords.append(monkey.x)
    coords.append(monkey.y)

    while coords != (dest_x, dest_y):
        if stop is True:
            return
        if (monkey.swimming) is False:
            break

        if coords[0] < dest_x:
            monkey.x = coords[0] + 1
        elif coords[0] > dest_x:
            monkey.x = coords[0] - 1
        if coords[1] < dest_y:
            monkey.y = coords[1] + 1
        elif coords[1] > dest_y:
            monkey.y = coords[1] - 1

        canvas.move(monkey.canvas, monkey.x - coords[0], monkey.y - coords[1])
        coords = (monkey.x, monkey.y)
        canvas.update()
        winsound.Beep(100, 30)
        time.sleep(0.1)        


def add_dock(island):
    x, y, _, _ = canvas.coords(island.canvas)
    canvas.create_line(x, y + 50, x - 20, y + 50, fill="brown", width=2)
    canvas.create_line(x + 50, y, x + 50, y - 20, fill="brown", width=2)
    canvas.create_line(x + 100, y + 50, x + 120, y + 50, fill="brown", width=2)
    canvas.create_line(x + 50, y + 100, x + 50, y + 120, fill="brown", width=2) 

    for monkey in monkeys:
        if monkey.on_island is island.name:
            monkey.aware = True

def add_monkey(island):
    x, y, _, _ = canvas.coords(island.canvas)
    monkey_x = random.randint(int(x), int(x + 100))
    monkey_y = random.randint(int(y), int(y + 100))
    monkeys.append(Monkey(False,False,island.name,monkey_x,monkey_y, canvas.create_oval(monkey_x, monkey_y, monkey_x + 5, monkey_y + 5, fill="brown",tags="monkey")))

def add_aware_monkey(island):
    x, y, _, _ = canvas.coords(island.canvas)
    monkey_x = random.randint(int(x), int(x + 100))
    monkey_y = random.randint(int(y), int(y + 100))
    monkeys.append(Monkey(True,False,island.name,monkey_x,monkey_y,canvas.create_oval(monkey_x, monkey_y, monkey_x + 5, monkey_y + 5, fill="brown", tags="monkey")))

def ten_second_thread():
    while True:
        for monkey in monkeys:
            if monkey.swimming is False:
                if random.random() < 0.01:
                    monkeys.remove(monkey)
                    canvas.delete(monkey.canvas)
                    play_laughter_death_sound()
        move_to_sea_auto()
        time.sleep(10)

def monkey_sound():
    while True:
        for monkey in monkeys:
            laugh = random.randint(200, 1000)
            winsound.Beep(laugh, 30)
        time.sleep(10)



def check_shark_attack():
    while True:
        for monkey in monkeys:
            if monkey.swimming is True:
                if random.random() < 0.01:
                    monkeys.remove(monkey)
                    canvas.delete(monkey.canvas)
                    play_shark_attack_sound()
        time.sleep(1)

def play_laughter_death_sound():
    winsound.Beep(1000, 200)
    print("Monkey died of laughter")

def play_shark_attack_sound():
    winsound.Beep(600, 200)
    time.sleep(0.3)
    winsound.Beep(300, 200)
    print("Monkey was eaten by shark")

def clear_sea():
    global island_count
    global stop
    canvas.delete("all")
    islands.clear()
    monkeys.clear()
    island_count = 0
    stop = True

def island_collision():
    while True:
        if monkeys:
            for monkey in monkeys:
                if monkey.swimming is True:
                    for island in islands:
                        x, y, x2, y2 = canvas.coords(island.canvas)
                        if monkey.x >= x and monkey.x <= x2:
                            if monkey.y >= y and monkey.y <= y2:
                                if island.dock is False:
                                    island.dock = True
                                    monkey.on_island = island.name
                                    monkey.swimming = False
                                    add_dock(island)
                                else:
                                    if monkey.on_island != island.name:
                                        monkey.on_island = island.name
                                        monkey.swimming = False
        time.sleep(0.5)

def amount_counter():
    while True:
        try:
            for island in islands:
                counter = 0
                for monkey in monkeys:
                    if monkey.swimming is False and monkey.on_island is island.name:
                        counter+=1
                canvas.itemconfig(island.text, text=counter)
            time.sleep(0.5)
        except:
            time.sleep(0.5)


def start_threads():
    t1 = threading.Thread(target=ten_second_thread)
    t2 = threading.Thread(target=check_shark_attack)
    t3 = threading.Thread(target=island_collision)
    t4 = threading.Thread(target=amount_counter)
    t5 = threading.Thread(target=monkey_sound)
    t3.start()
    t1.start()
    t2.start()
    t4.start()
    t5.start()

# Luo pääikkuna
root = tk.Tk()
root.title("Monkey island adventure")

point_button=[]
def i_suppose_i_have_earned_so_much_points(amount_of_points):
    for i in range(4):
        point_button[i].configure(bg='gray')
    time.sleep(1)    
    for i in range(amount_of_points):
        point_button[i].configure(bg='green')
        winsound.Beep(440 + i * 100, 500)
button_frame = tk.Frame(root)
button_frame.pack()
point_button = []
numero = 0
for i in range(4):
    numero +=5
    button_temp = tk.Button(button_frame, text="Points: " + str(numero), padx=40)
    button_temp.pack(side=tk.LEFT)
    point_button.append(button_temp)


i_suppose_i_have_earned_so_much_points(4)

canvas = tk.Canvas(root, width=800, height=500, bg="blue")
canvas.pack()

new_island_button = tk.Button(root, text="NEW ISLAND", command=create_new_island)
new_island_button.pack()

clear_sea_button = tk.Button(root, text="CLEAR SEA", command=clear_sea)
clear_sea_button.pack()

move_to_sea_button = tk.Button(root, text="MOVE TO SEA", command=move_to_sea)
move_to_sea_button.pack()

start_threads()

islands = []

root.mainloop()