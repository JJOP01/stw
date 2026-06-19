import argparse

def _exit(code=0, *messages):
    for msg in messages:
        print(msg, file=sys.stderr)
    raise SystemExit(code)

def main():
    parser = argparse.ArgumentParser()
    print("Hello, this argparse works!")    

if __name__ == "__main__":
    main()
