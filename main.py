from run import run
from init import init_data_collection

K = 5

def main():

    # offline
    data_collection, files_dict = init_data_collection('source')

    # online
    run(data_collection, files_dict, K)


if __name__ == "__main__":
    main()
