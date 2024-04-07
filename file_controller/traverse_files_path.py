import os


def traverse_files_path(file_path: str) -> []:
    res = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            path = os.path.join(root, file)
            # print(path[len(file_path) + 1::])
            res.append(path[len(file_path) + 1::])
    return res


if __name__ == '__main__':
    print(traverse_files_path('..\\files'))
