from threading import Thread
from time import sleep
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()
        self.customer_count = 0

    def customer_arrival(self):
        for _ in range(20):  # Ограничение на 20 посетителей
            self.customer_count += 1
            print(f"Посетитель номер {self.customer_count} прибыл")
            self.serve_customer(self.customer_count)
            sleep(1)

    def serve_customer(self, customer_number):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                customer = Customer(customer_number, table, self)
                customer.start()
                return

        print(f"Посетитель номер {customer_number} ожидает свободный стол")
        self.queue.put(customer_number)

    def table_ready(self, table):
        if not self.queue.empty():
            next_customer = self.queue.get()
            customer = Customer(next_customer, table, self)
            customer.start()
        else:
            table.is_busy = False

class Customer(Thread):
    def __init__(self, customer_number, table, cafe):
        Thread.__init__(self)
        self.customer_number = customer_number
        self.table = table
        self.cafe = cafe

    def run(self):
        print(f"Посетитель номер {self.customer_number} сел за стол {self.table.number}")
        sleep(5)  # Время обслуживания 5 секунд
        print(f"Посетитель номер {self.customer_number} покушал и ушёл")
        self.cafe.table_ready(self.table)

# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()