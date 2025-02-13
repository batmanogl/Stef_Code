import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def setup_browser_and_load_page(url, dropdown_xpath, item_xpath):
    """Sets up the browser, navigates to the page, and selects the required dropdown option."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)
        print(f"Opened URL: {url}")
        driver.maximize_window()
        print("Maximized the browser window.")
        time.sleep(3)

        # Close any pop-ups
        try:
            pop_up_close_button_xpath = '//*[@id="cdk-overlay-0"]/app-dialog/app-register-or-login/div/div[1]/cm-icon'
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pop_up_close_button_xpath))).click()
            print("Closed pop-up.")
        except:
            print("No pop-up to close or could not close it.")

        # Click on the dropdown toggle to open it
        dropdown_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        dropdown_element.click()
        print("Dropdown opened.")

        # Select the football option
        football_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Ποδόσφαιρο')]")))
        football_element.click()
        print("Successfully clicked the element 'Ποδόσφαιρο'.\n")

        # Wait for the page to load events
        time.sleep(3)
        return driver
    except Exception as e:
        print(f"An error occurred during setup: {e}")
        driver.quit()
        return None


def monitor_and_extract_matches(driver, event_xpaths, match_xpaths):
    """Monitors events and extracts match names, combining them into formatted strings."""
    combined_results = []

    for i, ((event_xpath, time_xpath), match_xpath) in enumerate(zip(event_xpaths, match_xpaths), start=1):
        try:
            # Wait for the event row to be present in the DOM
            event_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, event_xpath))
            )

            # Scroll to the element to ensure it is loaded into view
            driver.execute_script("arguments[0].scrollIntoView();", event_row)

            # Extract the event time text
            event_time_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, time_xpath))
            )
            event_time_text = event_time_element.text.strip()

            # Extract the match name
            match_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, match_xpath))
            )
            match_name = match_element.text

            # Parse the match name to extract team names
            lines = match_name.split("\n")
            if len(lines) >= 2:
                team1 = " ".join(lines[0].split()[:4])  # First four words of the first line
                team2 = " ".join(lines[1].split()[:4])  # First four words of the second line
                formatted_match = f"{team1} VS {team2}"

                # Handle "σε X'" format for remaining minutes
                if "σε" in event_time_text and "'" in event_time_text:
                    remaining_minutes = int(event_time_text.split()[1].replace("'", ""))
                    combined_results.append(f"{formatted_match}: Starts in {remaining_minutes} minutes.")
                else:
                    combined_results.append(f"{formatted_match}: Unrecognized time format ({event_time_text})")
            else:
                combined_results.append(f"Match {i}: Could not parse match name ({match_name})")
        except Exception as e:
            print(f"Error monitoring event {i}: {e}")

    # Extract and print only match names
    match_names = [result.split(":")[0].strip() for result in combined_results if ":" in result]
    return combined_results, match_names

def open_new_tab_and_click_element(driver, new_tab_url, new_tab_element_xpath, match_names):
    """Opens the source page and searches for match names.\n"""
    try:
        # Open a new tab
        driver.execute_script("window.open('');")
        print("\nOpened a new tab.")

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched to the new tab.")

        # Navigate to the URL
        driver.get(new_tab_url)
        print(f"Navigated to {new_tab_url}")

        # Maximize the browser window
        driver.maximize_window()
        print("Maximized the browser window.")
        time.sleep(3)

        # Wait for the element to be clickable and click it
        desired_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, new_tab_element_xpath))
        )
        ActionChains(driver).move_to_element(desired_element).click().perform()
        print("Clicked the desired element.")
        time.sleep(3)  #Adjust the sleep time based on how you are willing waiting for the search mechanism to find matches on the source page

        # Refresh the page before starting the search
        print("Refreshing the page...")
        driver.refresh()
        time.sleep(5)  # Allow the page to load completely after the refresh

        # Scroll to the bottom of the page to load all content
        print("\nScrolling through the page to load all content...")
        scroll_pause_time = 5
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

            # Check if the page height changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit the loop if no new content is loaded
            last_height = new_height

        print("Finished scrolling.")
    
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "eventRow_teams"))
)
        match_containers = driver.find_elements(By.CLASS_NAME, "eventRow_teams")

        page_source = driver.page_source.lower()  # Lowercase for case-insensitive search

        print(f"\nTotal match containers found: {len(match_containers)}\n")  #This print is useful only for debug purposes

        # Search for matches
        delayed_matches = []  # Store matches not found
        for match in match_names:
            teams = match.lower().split(" vs ")

            if len(teams) == 2:
                team1, team2 = map(str.strip, teams)
                match_found = False

                # Iterate through containers to find the match
                for container in match_containers:
                    try:
                       container_text = container.text.lower()

                       if team1 in container_text and team2 in container_text:
                           print(f"Match Found: {match}")
                           match_found = True
                           break
                    except AttributeError as e:
                        print(f"Error processing container (AttributeError): {e}")
                    except Exception as e:
                        print(f"Unexpected error processing container: {e}")

            if not match_found:
                print(f"Match Not Found: {match}")
                delayed_matches.append(match)                                        

        # Print delayed matches table
        if delayed_matches:
            print("\nDelayed Matches:")
            for delayed_match in delayed_matches:
                print(delayed_match)
        else:
            print("\nAll matches found.")

    except Exception as e:
        print(f"An error occurred in the new tab: {e}")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("\nClosed the new tab and returned to the original tab.")
    return delayed_matches

def create_xml_report(delayed_matches, file_name="delayed_matches_report.xml"):
    """Creates an XML report file with the delayed matches."""
    try:
        # Create the root element
        root = ET.Element("DelayedMatchesReport")

        # Add delayed matches as child elements
        for match in delayed_matches:
            match_element = ET.SubElement(root, "Match")
            match_element.text = match

        # Convert the tree to a byte string
        tree = ET.ElementTree(root)

        # Write the tree to an XML file
        with open(file_name, "wb") as xml_file:
            tree.write(xml_file, encoding="utf-8", xml_declaration=True)

        print(f"XML report created successfully: {file_name}")

    except Exception as e:
        print(f"An error occurred while creating the XML report: {e}")

if __name__ == "__main__":
    # Parameters
    url_to_visit = "https://www.novibet.gr/live-programma"
    dropdown_toggle_xpath = "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/app-live-schedule-filters/div[2]/div[2]/div[2]/cm-floating-container/div/cm-icon"  # Dropdown toggle button
    dropdown_item_xpath = '//*[@id="cdk-overlay-3"]/div/div/div[2]/span[1]'  # Desired item in the dropdown

    # Event and match XPaths
    event_xpaths = [
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[1]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[1]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[2]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[2]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[3]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[3]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[4]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[4]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[5]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[5]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[6]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[6]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[7]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[7]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[8]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[8]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[9]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[9]/sb-event-row/div/div/sb-event-row-time/div"
        ),
        (
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[10]/sb-event-row/div/div",
            "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[10]/sb-event-row/div/div/sb-event-row-time/div"
        )
    ]

    # List of match XPaths
    match_xpaths = [
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[1]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[2]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[3]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[4]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[5]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[6]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[7]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[8]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[9]/sb-event-row/div/div/a",
        "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-schedule/div/div[1]/div/div[1]/app-live-schedule-view/div/app-live-schedule-market-view/div/sb-event-row-flat[10]/sb-event-row/div/div/a"
    ]

    # Parameters for the new tab
    new_tab_url = "https://www.novibet.gr/stoixima-live"
    new_tab_element_xpath = "/html/body/app-root/app-layout/div/div[2]/app-sportsbook/div/app-in-play/div/div/div[1]/div/app-in-play-sports/div/div/div/sb-carousel/div/cm-swiper-carousel/div/swiper-container/swiper-slide[1]/div"
    
    # Setup browser and load page
    driver = setup_browser_and_load_page(url_to_visit, dropdown_toggle_xpath, dropdown_item_xpath)

    if driver:
        # Monitor events and extract matches
        results, match_names = monitor_and_extract_matches(driver, event_xpaths, match_xpaths)
        # Print the name of the matches and the starting times
        print("The next 10 matches that will start soon are:")
        for match in match_names:
            print(match)

        print("\nThe starting times for the aforementioned matches are:")
        for result in results:
            print(result)

        # Open a new tab, interact with the second page and search for matches in source page
        delayed_matches = open_new_tab_and_click_element(driver, new_tab_url, new_tab_element_xpath, match_names)

        # Generate the XML report
        create_xml_report(delayed_matches)

        # Close the browser
        driver.quit()
        print("Browser closed.")
