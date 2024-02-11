import progressbar


def get_progress_bar(description: str, collection: list[any], descriptor: str):
    return progressbar.ProgressBar(
        widgets=[
            description,
            progressbar.Percentage(),
            " ",
            progressbar.Bar(),
            " ",
            progressbar.ETA(),
            " ",
            progressbar.Counter(format="%(value)d/%(max_value)d " + descriptor),
        ],
        max_value=len(collection),
    )
