from dotenv import load_dotenv
from ceetsii.Entrypoint import Entrypoint

def main():
    load_dotenv()
    entry = Entrypoint()
    entry.run()

if __name__ == '__main__':
    main()
