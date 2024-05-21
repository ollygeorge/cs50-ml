import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    print("Data Loading...")
    evidence = []
    labels = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = []
            data.append(int(row["Administrative"]))
            data.append(float(row["Administrative_Duration"]))
            data.append(int(row["Informational"]))
            data.append(float(row["Informational_Duration"]))
            data.append(int(row["ProductRelated"]))
            data.append(float(row["ProductRelated_Duration"]))
            data.append(float(row["BounceRates"]))
            data.append(float(row["ExitRates"]))
            data.append(float(row["PageValues"]))
            data.append(float(row["SpecialDay"]))
            data.append(int(month_to_index(row["Month"])))
            data.append(int(row["OperatingSystems"]))
            data.append(int(row["Browser"]))
            data.append(int(row["Region"]))
            data.append(int(row["TrafficType"]))
            data.append(int(row["VisitorType"] == "Returning_Visitor"))
            data.append(int(row["Weekend"] == "TRUE"))

            labels.append(int(row["Revenue"] == "TRUE"))

            evidence.append(data)

    print("Data Loaded!")
    return evidence, labels


def month_to_index(month_abbr):
    # Dictionary mapping month abbreviations to their respective indices
    month_dict = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "Jun": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }
    # Return the corresponding index or raise an error if the abbreviation is invalid
    return month_dict.get(month_abbr, -1)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    predictions = model.fit(evidence, labels)

    return predictions

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    predicted_positives = 0
    predicted_negatives = 0
    actual_positives = labels.count(1)
    actual_negatives = labels.count(0)

    print(actual_negatives)
    print(actual_positives)

    for prediction, label in zip(predictions, labels):
        if prediction == label:
            if prediction == 0:
                predicted_negatives += 1
            else:
                predicted_positives += 1
    sensitivity = predicted_positives / actual_positives
    specificity = predicted_negatives / actual_negatives

    return sensitivity, specificity




if __name__ == "__main__":
    main()
