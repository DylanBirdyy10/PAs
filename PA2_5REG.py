import random
from Queue_for_ALGO import Queue


SECONDS_PER_ITEM = 4
OVERHEAD_SECONDS = 45
AVERAGE_ARRIVAL_INTERVAL = 30
SIMULATION_DURATION = 7200
CUSTOMER_ITEM_RANGE = (6, 20)
UPDATE_INTERVAL = 50
queue = Queue()


class Customer:
    def __init__(self, item):
        self.item = item

    def checkout_time(self):
        return self.item * 4 + 45


class Register:
    def __init__(self, is_express=False):
        self.is_express = is_express
        self.queue = Queue()
        self.total_customers_served = 0
        self.total_items_processed = 0
        self.total_idle_time = 0
        self.total_wait_time = 0
        self.current_customer_end_time = None
        self.idle_start_time = None

    def add_customer(self, customer, current_time):
        was_idle = self.queue.isEmpty()
        customer.enqueue_time = current_time
        self.queue.enqueue(customer)

        if was_idle and self.idle_start_time is not None:

            self.total_idle_time += current_time - self.idle_start_time
            self.idle_start_time = None

        if self.queue.size() == 1:
            self.current_customer_end_time = current_time + customer.checkout_time()

    def process_next_customer(self, current_time):
        if not self.queue.isEmpty():
            customer = self.queue.dequeue()
            self.total_customers_served += 1
            self.total_items_processed += customer.item
            wait_time = current_time - customer.enqueue_time
            self.total_wait_time += wait_time
            if self.queue.isEmpty():
                self.idle_start_time = current_time

    def next_customer_checkout_time(self):
        if not self.queue.isEmpty():
            return self.queue.items[-1].checkout_time()
        else:
            return 0

    def is_busy(self):
        return not self.queue.isEmpty()

    def queue_length(self):
        return self.queue.size()


def generate_customer():
    item = random.randint(*CUSTOMER_ITEM_RANGE)
    return Customer(item)


def choose_register(customer, registers):
    if customer.item < 10:
        express_registers = [r for r in registers if r.is_express]
        non_express_registers = [r for r in registers if not r.is_express]

        if express_registers and express_registers[0].queue_length() == 0:
            return express_registers[0]

        all_registers = express_registers + non_express_registers
    else:
        all_registers = [r for r in registers if not r.is_express]

    min_queue_length = min(r.queue_length() for r in all_registers)
    registers_with_min_queue = [
        r for r in all_registers if r.queue_length() == min_queue_length
    ]

    chosen_register = random.choice(registers_with_min_queue)
    return chosen_register


def simulate_shift(registers):
    simulation_time = 0
    next_customer_arrival = simulation_time + random.randint(20, 40)

    while simulation_time < SIMULATION_DURATION:
        if simulation_time >= next_customer_arrival:
            customer = generate_customer()
            chosen_register = choose_register(customer, registers)
            chosen_register.add_customer(customer, simulation_time)
            next_customer_arrival = simulation_time + random.randint(20, 40)

        for register in registers:
            if register.is_busy() and (
                register.current_customer_end_time is None
                or simulation_time >= register.current_customer_end_time
            ):
                register.process_next_customer(simulation_time)

        simulation_time += 1

        if simulation_time % UPDATE_INTERVAL == 0:
            display_status(registers, simulation_time)

    display_status(registers, simulation_time)


def display_status(registers, elapsed_time):
    print(f"\nStatus at {elapsed_time} seconds:")
    print(f"{'Register':<10}{'Serving':<10}{'Queue':<30}")
    print("-" * 50)

    for i, register in enumerate(registers, start=1):
        serving = "--"

        if register.is_busy():

            serving = (
                f"{register.queue.items[0].item} items"
                if not register.queue.isEmpty()
                else "--"
            )

        queue_display = (
            "| "
            + ", ".join(
                f"{customer.item} items" for customer in register.queue.items[1:]
            )
            if not register.queue.isEmpty()
            else ""
        )

        register_type = "Express" if register.is_express else "Regular"
        print(f"{register_type} {i:<5} {serving:<10} {queue_display:<30}")


def display_final_statistics(registers):
    print("\n")
    print(
        f"{'Register':<10} {'Total Customers':<16} {'Total Items':<12} {'Total Idle Time (min)':<22} {'Average Wait Time (sec)':<22}"
    )
    total_customers = 0
    total_items = 0
    total_idle_time = 0
    total_wait_time = 0

    for i, register in enumerate(registers, start=1):
        register_name = "Express" if register.is_express else f"Regular {i}"
        avg_wait_time = (
            register.total_wait_time / register.total_customers_served
            if register.total_customers_served > 0
            else 0
        )
        print(
            f"{register_name:<10} {register.total_customers_served:<16} {register.total_items_processed:<12} {register.total_idle_time/60:<22.2f} {avg_wait_time:<22.2f}"
        )

        total_customers += register.total_customers_served
        total_items += register.total_items_processed
        total_idle_time += register.total_idle_time
        total_wait_time += register.total_wait_time

    overall_avg_wait_time = (
        total_wait_time / total_customers if total_customers > 0 else 0
    )

    print("-" * 100)
    print(
        f"{'TOTAL:':<10} {total_customers:<16} {total_items:<12} {total_idle_time/60:<22.2f} {overall_avg_wait_time:<22.2f}"
    )


def run_simulation():
    registers = [Register() for _ in range(5)]
    registers.append(Register(is_express=True))

    simulate_shift(registers)

    display_final_statistics(registers)


def main():
    for i in range(12):
        run_simulation()


main()
