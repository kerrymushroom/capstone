from multiprocessing import Pool
from build import build_dict

# for running Pool() on windows jupyter notebook environment, it's recommended to import worker like build.py

dir_path = './nvBench_VegaLite' # this folder contains VIS_1.html to VIS_7247.html
file_table = sorted([os.path.join(dir_path,f) for f in os.listdir(dir_path)], key=len)

def main():
    with Pool() as pool:
        results = pool.map(build_dict, file_table)
    with open("newNVBench.json", "w") as outfile: # newNVBench json consists of html id, vega schema and more
        outfile.write(json.dumps(dict(results),indent=2))

if __name__ == '__main__':
	main()