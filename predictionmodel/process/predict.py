def predict(model, xtest):
    # Make predictions on new data
    y_pred = model.predict(xtest)
    return y_pred