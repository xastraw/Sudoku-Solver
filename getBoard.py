from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


#opens up and scrapes the board
def scrapeBoard(difficulty):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    driver.get("https://www.nytimes.com/puzzles/sudoku/" + difficulty)
    driver.maximize_window()
    

    #close popup
    close_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.fam-close-x'))
    )
    close_btn.click()

    cells = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid^="sudoku-cell-"]')

    board = [[0 for _ in range(9)] for _ in range(9)]
    for cell in cells:
        index = int(cell.get_attribute("data-cell"))  # values from 0 to 80 for 81 sudoku squares
        row, col = divmod(index, 9)

        number_svg = cell.find_elements(By.CSS_SELECTOR, '[data-number]')

        if number_svg:
            number = number_svg[0].get_attribute("data-number")
            board[row][col] = int(number)


    return board, driver


def fillBoard(filledBoard, cDriver):
    driver = cDriver

    #flatten the board for a 1 to 1 pairing of the cells
    flattenedBoard = [cell for row in filledBoard for cell in row]

    for i in range(len(flattenedBoard)):
        driver.find_element(By.CSS_SELECTOR, f'[data-testid="sudoku-cell-{i}"]').click()
        driver.switch_to.active_element.send_keys(flattenedBoard[i])

    time.sleep(3)
    #close popup
    close_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="modal-close"]'))
    )
    close_btn.click()