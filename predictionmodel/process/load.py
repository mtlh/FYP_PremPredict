import joblib as jb

def load(filename):
    model = jb.load(filename)
    return model