from . import helper


class Person:
    def walk(self):
        print("i started walking...")
        print("i stopped walking.")
        helper.export_to_csv()

    def swim(self):
        print("i started swimming...")
        print("i stopped swimming.")
        helper.export_to_csv()


if __name__ == "__main__":
    pass
