class Node():
    def __init__(self, name = None , next = None):
        self.name = name
        self.next = next

class MyQueue():
    def __init__(self):
        self.head = None

    def clear(self):
        self.__init__()

    #добавляет в конец списка
    def add(self, new_obj):
        newnode = Node(new_obj)
        if self.head is None:
            self.head = newnode
            return
        lastnode = self.head
        while (lastnode.next):
            lastnode = lastnode.next
        lastnode.next = newnode

    #удаляет элемент по значению
    def remove(self, rm):
        headnode = self.head
        if headnode is not None:
            if headnode.name == rm:
                self.head = headnode.next
                headnode = None
                return
        while headnode is not None:
            if headnode.name == rm:
                 break
            prev = headnode
            headnode = headnode.next
        if headnode == None:
            return

        prev.next = headnode.next
        headnode = None

    def make_arr(self):
        self.arr = []
        if self.head is not None:
            elem = self.head
            while (elem.next):
                self.arr.append(elem.name)
                elem = elem.next
            self.arr.append(elem.name)
        return self.arr

class Country():
    def __init__(self, name=None, population=0, capital=None):
        self.name = name
        self.population = population
        self.capital = capital

    def __str__(self):
        return f"{self.name} - {self.capital}: {self.population}"



integers = MyQueue()
for i in range(1,10):
    MyQueue.add(integers, i)

Russia = Country('Russia', 145000000, 'Moscow')
Italy = Country('Italy', 60000000, 'Milan')
GB = Country('Great Britain', 66650000, 'London')


countries = MyQueue()
MyQueue.add(countries, Russia)
MyQueue.add(countries, Italy)
MyQueue.add(countries, GB)

for country in MyQueue.make_arr(countries):
    print(country)


print(MyQueue.make_arr(integers))