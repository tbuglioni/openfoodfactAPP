from interface.choice import Choice


def main():
    my_app = Choice()
    my_app._choose_in_db_menu()
    my_app.loop_app()


if __name__ == "__main__":
    main()