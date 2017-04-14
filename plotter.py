import matplotlib.pyplot as plt


def display_results(results):
    poor = [results["poor"][a] for a in results["poor"]]
    fair = [results["fair"][a] for a in results["fair"]]
    good = [results["good"][a] for a in results["good"]]
    great = [results["great"][a] for a in results["great"]]
    excellent = [results["excellent"][a] for a in results["excellent"]]

    print("poor: {}".format(poor))
    print("fair: {}".format(fair))
    print("good: {}".format(good))
    print("great: {}".format(great))
    print("excellent: {}".format(excellent))

    total = poor + fair + good + great + excellent
    print("total: {}".format(total))

    fig, ax = plt.subplots()
    ax.set_title("Number of guitars in each category.")

    plt.pie([len(poor), len(fair), len(good), len(great), len(excellent)], labels=("Poor", "Fair", "Good", "Great", "Excellent"), autopct='%.0f%%')
    plt.show()

    fig, ax = plt.subplots()
    ax.set_title("Number of guitars in each category.")

    min = 1100
    max = 1200
    cheap = len([a for a in total if a < min])
    good = len([a for a in total if min <= a < max])
    expensive = len([a for a in total if a >= max])

    plt.bar([1, 2, 3], [cheap, good, expensive], 0.5, color="green")

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["a < {}".format(min), "{} <= a < {}".format(min, max), "a >= {}".format(max)])

    plt.show()
