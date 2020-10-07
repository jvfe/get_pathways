from selenium import webdriver
import os


def create_browser(download_path):

    profile = webdriver.FirefoxProfile()

    profile.set_preference("browser.download.folderList", 2)  # custom location
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference(
        "browser.download.dir",
        download_path,
    )
    # Don't ask permission to download
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/json")

    options = webdriver.FirefoxOptions()

    # Rodar em background
    options.add_argument("--headless")

    browser = webdriver.Firefox(firefox_profile=profile, options=options)

    return browser


def download_pathway(url, download_path):

    browser = create_browser(download_path)
    browser.get(url)
    browser.implicitly_wait(2)  # Tempo para carregar a pagina
    browser.find_element_by_css_selector("#ui-id-1").click()
    browser.find_element_by_css_selector("#savegraph").click()
    # browser.implicitly_wait(2)  # Tempo para baixar o arquivo
    browser.quit()


def main():

    # Tem que ser a full path, não sei por que.
    download_path = "/get_pathways/results"

    with open("data/codes.txt", "r") as codes:
        pathways = codes.read().splitlines()

    for pathway in pathways:
        url = (
            f"https://metacyc.org/cytoscape-js/ovsubset.html?orgid=META&pwys={pathway}"
        )
        try:
            download_pathway(url, download_path)
            os.rename("results/pwycollage.graph.json", f"results/{pathway}.json")
        except Exception:
            print(f"Nao consegui baixar {pathway}!")
            pass


if __name__ == "__main__":
    main()
