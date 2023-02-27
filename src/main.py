from afn import AFN


def run():
    thompson = AFN()
    regex = input("Please enter a regular expression: ")
    s = input("Please enter a string to match: ")

    while s != "q":
        print(thompson.match(regex, s))
        regex = input("\n(q - quit) Please enter a regular expression to match: ")
        s = input("\n(q - quit) Please enter a string to match: ")


if __name__ == "__main__":
    run()
