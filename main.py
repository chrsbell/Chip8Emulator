from window import Window


def main():

    window = Window()
    with window.init_opengl():
        try:
            while not window.quit:
                window.update()
        finally:
            if not window.quit:
                window.close()


if __name__ == '__main__':
    main()
