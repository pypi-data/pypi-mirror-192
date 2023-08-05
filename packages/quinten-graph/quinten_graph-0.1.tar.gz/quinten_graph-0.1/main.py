from src.quinten_graph.settings import QuintenSettings

def main():
    QS = QuintenSettings("finance")
    QS.set_style_quinten()
    print("class intialized")

if __name__ == "__main__":
    main()