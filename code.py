import os.path
import glob

mtl_file = os.path.isfile("object.mtl")
obj_file = os.path.isfile("object.obj")

file_list = glob.glob('v_file*.txt')

if mtl_file:
    def num_gen():
        num = 1
        while True:
            yield num
            num += 1
    counter = num_gen()

    with open('object.mtl') as sf:
        lines = sf.readlines()
    kd_list = []
    is_collecting_kd = False

    for line in lines:
        if line.startswith('newmtl '):
            if kd_list:
                with open(f'color{next(counter)}.txt', 'w') as file:
                    for v_line in kd_list:
                        file.write(v_line)
                kd_list.clear()
            is_collecting_kd = True

        elif line.startswith('Kd ') and is_collecting_kd:
            kd_list.append(line)

        elif line.startswith('Ks '):
            is_collecting_kd = False

    if kd_list:
        with open(f'color{next(counter)}.txt', 'w') as file:
            for v_line in kd_list:
                file.write(v_line)

if obj_file:
    def num_gen(num):
        while True:
            yield num
            num += 1
    counter = num_gen(1)
with open('object.obj') as sf:
    lines = sf.readlines()
    v_list = list()
for line in lines:
    if line.startswith('v '):
        v_list.append(line)

    elif line.startswith('f '):
        if v_list:
            with open(f'v_file{next(counter)}.txt', 'w') as file:
                for v_line in v_list:
                    file.write(v_line)
            v_list.clear()

for color_file, v_file_file in zip(sorted(glob.glob('color*.txt')), sorted(glob.glob('v_file*.txt'))):
    num = color_file.split('color')[1].split('.txt')[0]
    with open(f'out{num}.txt', 'w') as out_file:
        with open(color_file, 'r') as cf, open(v_file_file, 'r') as mf:
            color_line = cf.readline().strip()
            color1, color2, color3 = color_line.split('Kd ')[1].split()

            for line in mf:
                cline = line.replace("v ", "^").replace(" ", " ^").strip()
                result = f"particle dust {color1} {color2} {color3} 1 {cline} 0 0 0 0 1 force"
                out_file.write(result + "\n")

with open('output.mcfunction', 'w') as final_file:
    for out_file in sorted(glob.glob('out*.txt')):
        with open(out_file, 'r') as of:
            final_file.write(of.read())

for file_path in glob.glob('*.txt'):
    if file_path != 'output.mcfunction':
        os.remove(file_path)