from .types import Pod, Subpod


def extract_usefull_subpods(pod: Pod) -> list[Subpod]:
    # remove step-by-step if not available
    subpods = [subpod for subpod in pod.subpods if subpod.plaintext != '(step-by-step solution unavailable)']

    # firstly try to extract subpods with titles
    if with_titles := [subpod for subpod in subpods if subpod.title]:
        return with_titles

    # if no one has a title then return all of them
    return subpods
