import argparse

def _exit(code=0, *messages):
    for msg in messages:
        print(msg, file=sys.stderr)
    raise SystemExit(code)


def _real_main():
    parser = argparse.ArgumentParser()
    assert False, "do this!"

def main(): # for clear error handling
    try:
        _exit(_real_main())
    except Error as e:
        _exit(1)

if __name__ == "__main__":
    main()
