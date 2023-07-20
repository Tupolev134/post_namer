import os

from core.data.PDF_wrapper import PDF_wrapper


class NamingController:
    def __init__(self, path_to_pdf_folder):
        self.files = [f for f in os.listdir(path_to_pdf_folder) if f.endswith('.pdf')]
        self.index_current_file = 0
        self.current_file = None

        self.update_current_file()

    def update_current_file(self):
        self.current_file = PDF_wrapper(self.files[self.index_current_file])

    def load_index(self, index):
        if 0 < index < len(self.files) -1:
            self.index_current_file = index
            self.update_current_file()

    def load_next_file(self):
        if self.index_current_file < len(self.files) - 1:
            self.index_current_file += 1
            self.update_current_file()

    def load_previous_file(self):
        if self.index_current_file > 0:
            self.index_current_file -= 1
            self.update_current_file()

if __name__ == '__main__':
    nc = NamingController("/Users/tupolev/Desktop/Arbeit/MRP/Fasanenstraße/2023/05_May/22.05.2023/ALLGEMEIN")
    for file in nc.files:
        print(file)
        print(nc.current_file.identification)
        print("\n")
        nc.load_next_file()