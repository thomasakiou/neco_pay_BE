try:
    from app import main
    print("Import successful")
except Exception as e:
    import traceback
    with open("error.log", "w") as f:
        traceback.print_exc(file=f)
    traceback.print_exc()
