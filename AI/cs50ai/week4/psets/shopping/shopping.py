import csv
import sys
import calendar
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
    # """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []
        for row in reader:
            data = []
            pages = row[
                0:6
            ]  # pages the user visited and for how long(alternating duration and number)
            Ganalytics = row[6:10]  # info from google about page(floats)
            month = row[10]  # abbreviation for month user visited
            user_data = row[11:15]  # (integers)
            visitor_type = row[15]  # 0(not returning) 1 (returning)(int)
            weekend = row[16]  # 0(false) or 1(true)(int)
            label = row[17]  # 1(revenue is true) and 0 otherwise.

            for i in range(len(pages)):
                if i % 2 == 0:
                    data.append(int(pages[i]))

                else:
                    data.append(float(pages[i]))
            for cell in Ganalytics:
                data.append(float(cell))

            match month.lower().strip():
                case "jan":
                    data.append(0)
                case "feb":
                    data.append(1)
                case "mar":
                    data.append(2)
                case "apr":
                    data.append(3)
                case "may":
                    data.append(4)
                case "june":
                    data.append(5)
                case "jul":
                    data.append(6)
                case "aug":
                    data.append(7)
                case "sep":
                    data.append(8)
                case "oct":
                    data.append(9)
                case "nov":
                    data.append(10)
                case "dec":
                    data.append(11)

            for cell in user_data:
                data.append(int(cell))

            if visitor_type == "New_Visitor":
                data.append(0)
            else:
                data.append(1)
            if weekend == "FALSE":
                data.append(0)
            else:
                data.append(1)

            evidence.append(data)

            if label == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

    return (evidence, labels)
    # """
    # the follwoing would be a more efficient method of creating the above function.
    # consider the differences between my code an the ai code.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        evidence, labels = [], []

        month_index = {
            month: index for index, month in enumerate(calendar.month_abbr) if month
        }

        for row in reader:
            evidence.append(
                [int(row[i]) if i % 2 == 0 else float(row[i]) for i in range(6)]
                + [float(row[i]) for i in range(6, 10)]
                + [month_index.get(row[10].capitalize().strip(), -1)]
                + [int(row[i]) for i in range(11, 15)]
                + [1 if row[15] == "Returning_Visitor" else 0]
                + [1 if row[16].lower() == "true" else 0]
            )
            labels.append(1 if row[17].lower() == "true" else 0)
    return (evidence, labels)
     """


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    return model.fit(evidence, labels)


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
    sensitivity = 0
    true_count = 0
    specificity = 0
    false_count = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            true_count += 1
            if labels[i] == predictions[i]:
                sensitivity += 1
        elif labels[i] == 0:
            false_count += 1
            if labels[i] == predictions[i]:
                specificity += 1

    sensitivity = sensitivity / true_count
    specificity = specificity / false_count

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
