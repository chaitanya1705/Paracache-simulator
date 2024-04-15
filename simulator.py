import math
from tabulate import tabulate

class CacheSimulator:
    def __init__(self, cache_size, block_size, memory_size):
        self.cache_size = cache_size
        self.block_size = block_size
        self.memory_size = memory_size
        self.num_blocks = self.cache_size // self.block_size
        self.cache = {}
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.steps = []

    def access_memory(self, address):
        block_number = address // self.block_size
        index = block_number % self.num_blocks
        tag = block_number // self.num_blocks
        step = {"Address": address, "Block Number": block_number, "Index": index, "Tag": tag}
        if index in self.cache:
            if self.cache[index]['tag'] == tag:
                self.hits += 1
                step["Result"] = "Hit"
                self.steps.append(step)
                return "hit"
            else:
                self.evictions += 1
                self.misses += 1
                self.cache[index] = {'tag': tag, 'data': 'some_data'}
                step["Result"] = "Miss (Eviction)"
                self.steps.append(step)
                return "miss"
        else:
            self.misses += 1
            self.cache[index] = {'tag': tag, 'data': 'some_data'}
            step["Result"] = "Miss (New Block)"
            self.steps.append(step)
            return "miss"

    def get_stats(self):
        total_accesses = self.hits + self.misses
        if total_accesses == 0:
            return "No accesses performed"
        hit_ratio = self.hits / total_accesses
        miss_ratio = self.misses / total_accesses
        stats = [
            ["Total accesses", total_accesses],
            ["Hit ratio", f"{hit_ratio:.2f}"],
            ["Miss ratio", f"{miss_ratio:.2f}"]
        ]
        return tabulate(stats, headers=["Metric", "Value"])

    @staticmethod
    def main():
        print("Cache Simulator Configuration")
        cache_size = int(input("Enter Cache Size: "))
        memory_size = int(input("Enter Memory Size: "))
        offset_bits = int(input("Enter Offset Bits: "))
        block_size = 2 ** offset_bits

        index_bits = int(math.log2(cache_size // block_size))
        total_address_bits = int(math.log2(memory_size))
        tag_bits = total_address_bits - index_bits - offset_bits
        print("\nCache Configuration")
        print(f"Offset = {offset_bits} bits")
        print(f"Index = {index_bits} bits")
        print(f"Instruction Length = {total_address_bits} bits")
        print(f"Tag = {tag_bits} bits")
        print(f"Block = {tag_bits + offset_bits} bits")

        simulator = CacheSimulator(cache_size, block_size, memory_size)
        while True:
            address_input = input("Enter a memory address (or type exit to finish): ")
            if address_input.lower() == "exit":
                break
            if address_input.isdigit():
                simulator.access_memory(int(address_input))
                print(tabulate(simulator.steps,
                               headers="keys", tablefmt="grid", numalign="center"))
            else:
                print("Invalid input")
        print(simulator.get_stats())


if __name__ == "__main__":
    CacheSimulator.main()
