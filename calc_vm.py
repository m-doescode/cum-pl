
def func_print(str):
    print(str)

def func_sqrt(sq):
    return sq**0.5

# Standard library
stdlib = { 'print': func_print, 'sqrt': func_sqrt }

# For the sake of ease
binops = {
    'sum':  lambda x, y: x + y,
    'sub':  lambda x, y: x - y,
    'mult': lambda x, y: x * y,
    'div':  lambda x, y: x / y
}

def to_list(map):
    list = [None] * (max(map.keys())+1)
    for i, v in map.items():
        list[i] = v
    return list

def run(constants, instructions):
    print("Running VM...")
    registers = {}

    for inst in instructions:
        match inst[0]:
            case 'loadk':
                registers[inst[1]] = constants[inst[2]]
            case 'mov':
                registers[inst[1]] = registers[inst[2]]
            case 'call':
                fname = registers[inst[2]]
                try:
                    func = stdlib[fname]
                except KeyError:
                    raise NameError(f"Unknown function '{fname}'")
                registers[inst[1]] = func(*to_list(registers)[inst[3]:inst[3]+inst[4]])
            case "sum"|"sub"|"mult"|"div":
                registers[inst[1]] = binops[inst[0]](registers[inst[2]],registers[inst[3]])
