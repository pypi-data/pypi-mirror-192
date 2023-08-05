import sys
from .dataset_ingestion import ingest
from .dataset_split import split
from .training import train
from .serialization import save
from .evaluation import evaluate


def main():
    test_size = 0.2
    seed = 0
    target = "price"
    dataset_path = sys.argv[1]
    categorical_features = ["cut", "color", "clarity"]

    dataset = ingest(dataset_path, categorical_features)

    samples_train, targets_train, samples_test, targets_test = split(
        dataset, target, test_size, seed
    )

    model = train(samples_train, targets_train, seed)

    score = evaluate(model, samples_test, targets_test)

    print("Model score: " + str(score))
    save(model, "./model.json")
