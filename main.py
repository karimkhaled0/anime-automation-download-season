from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Provide the actual path
edge_driver_path = "edgedriver_linux64/msedgedriver"

extension_path = "/home/karim/.config/microsoft-edge/Default/Extensions/ndcileolkflehcjpmjnfbnaibdcgglog/5.13.0_0"

# Initialize the Edge web driver with the configured options
service = webdriver.EdgeService(
    executable_path=edge_driver_path,
)

options = webdriver.EdgeOptions()
options.add_argument(f"--load-extension={extension_path}")
driver = webdriver.Edge(service=service, keep_alive=True, options=options)

# Create an array to store download links
download_links = []

# Wait for 10 seconds after opening the browser
time.sleep(5)

# Iterate through episode numbers from 1 to 28
for episode_number in range(1, 29):
    # Construct the URL for the current episode
    episode_url = f"https://animerco.org/episodes/shingeki-no-kyojin-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%b1%d8%a7%d8%a8%d8%b9-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-{episode_number}/#play"

    # Open the website for the current episode
    driver.get(episode_url)

    # Get the title of the page
    title = driver.title

    driver.implicitly_wait(0.5)

    # Find and click the button with explicit wait
    try:
        xpath = '/html/body/div[6]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/a'
        button_xpath = '/html/body/div[6]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/a'
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, button_xpath))
        )
        button.click()
    except Exception as e:
        print(
            f"Episode {episode_number}: Button not found or unable to click.")
        continue

    time.sleep(3)

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Find and get the download link from the second website
    link_xpath = '//*[@id="downloadButton"]'
    try:
        link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, link_xpath))
        )
        link = link_element.get_attribute("href")
    except Exception as e:
        print(f"Episode {episode_number}: Download link not found.")
        link = "N/A"

    # Append the link to the download_links array
    download_links.append(link)

    # Close the new tab
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])

# Close the web browser
driver.quit()

# Print all the download links
for i, download_link in enumerate(download_links, start=1):
    print(f"{download_link}")
