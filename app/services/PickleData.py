import pickle


def save_data(filename, data):
    file = open(filename, 'ab')
    pickle.dump(data, file)
    file.close()


def load_data(filename):
    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()

    return data
