import requests


def select_operating_mode():
    '''Mode selection and menu draw'''

    draw_menu = u"""
    ╭────────────────────────────────────╮
    │\u001b[4m\u001b[44m Please select one of the two modes \u001b[0m│
    │       \u001b[31m1.\u001b[0m Generate random data      │
    │       \u001b[31m2.\u001b[0m Import data from json     │
    ╰────────────────────────────────────╯"""
    draw_question = u"\nType the \u001b[31mnumber\u001b[0m of the mode you want (1/2): "

    print(draw_menu)
    while True:
        ans = input(draw_question)
        if ans == "1":
            return 0
        elif ans == "2":
            return 1
        print("ERROR")


def server_ip_address():
    '''Server ip user input and menu draw'''

    print("Please enter the server ip")
    while True:
        url = "http://" + input("IP: ") + ":" + "5000"

        print("Using "+url)
        timeout = 5
        try:
            requests.get(url, timeout=timeout)
            print("Connected to the url")
            return url+"/api/send"
        except:
            print("No internet connection.")
