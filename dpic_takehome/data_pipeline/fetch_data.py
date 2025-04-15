import requests
from pathlib import Path

def main():
    url_1 = "https://raw.githubusercontent.com/cesarnunezh/dpic-takehome-assignment/refs/heads/main/data/raw/grievances.json?token=GHSAT0AAAAAAC44UUVR2BQOJL4PD6RA452CZ752J6Q"
    url_2 = "https://raw.githubusercontent.com/cesarnunezh/dpic-takehome-assignment/refs/heads/main/data/raw/iti_enrollments.csv?token=GHSAT0AAAAAAC44UUVRXVOEQJKSDTQERVTWZ752KLQ"

    path_1 = Path("data/raw/grievances.json")
    path_2 = Path("data/raw/iti_enrollments.csv")

    response1, response2 = requests.get(url_1) , requests.get(url_2)
    response1.raise_for_status()
    response2.raise_for_status()

    with open(path_1, "wb") as g:
        g.write(response1.content)
    
    with open(path_2, "wb") as i:
        i.write(response2.content)

if __name__ == "__main__":
    main()