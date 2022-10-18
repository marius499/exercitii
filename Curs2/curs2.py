import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class Login(unittest.TestCase):

    # elemente din pagina
    FORM_AUTH= (By.XPATH, '//a[@href="/login"]')
    LOGIN_PAGE_MSG = (By.XPATH, '//div/h2')
    LOGIN_BUTTON = (By.XPATH, '//button[@type="submit"]')
    ELEM_SELENIUM = (By.XPATH, '//a[@href="http://elementalselenium.com/"]')
    ERROR_MESSAGE = (By.XPATH, '//*[@id="flash"]')
    USERNAME_LOGIN = (By.XPATH, '//input[@id="username"]')
    PASSWORD_LOGIN = (By.XPATH, '//input[@id="password"]')
    CLOSE_ERROR_MESSAGE = (By.XPATH, '//a[@href="#"]')
    LABELS = (By.XPATH, '//label')
    CORRECT_LOGIN_MESSAGE = (By.XPATH, '//div[@class="flash success"]')
    CORRECT_LOGIN_MESSAGE2 = (By.XPATH, '//div[@id="flash"]/text()')
    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')

    # se ruleaza inainte de fiecare testare

    def setUp(self):
        s = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=s)
        self.chrome.maximize_window()
        self.chrome.get('https://the-internet.herokuapp.com/')  # url de start
        self.chrome.implicitly_wait(5)
        self.chrome.find_element(*self.FORM_AUTH).click()

    # se ruleaza dupa fiecare test
    def tearDown(self):
        self.chrome.quit()

    # Test1 - Verificati ca noul url e corect
    def test_url(self):
        actual = self.chrome.current_url
        expected = 'https://the-internet.herokuapp.com/login'
        self.assertEqual(expected, actual, ' Site-ul nu e corect')

    #Test2 - Verificati ca page title e corect
    def test_page_title(self):
        actual = self.chrome.title
        expected = 'The Internet'
        self.assertEqual(expected, actual, 'Title is not correct')

    #Test3 - Verificati textul de pe elementul xpath=//h2 e corect
    def test_elem_vizibil(self):
        elem = self.chrome.find_element(*self.LOGIN_PAGE_MSG)
        self.assertTrue(elem.is_displayed(), 'Message is not displayed')

    #Test4 - Verificati ca butonul de login este displayed
    def test_login_button(self):
        elem = self.chrome.find_element(*self.LOGIN_BUTTON)
        self.assertTrue(elem.is_displayed(), 'Button is not there')

    #Test4' - Verificati textul de pe butonul login  ??? not sure is correct ar fi trebuit poate un alt path //button[@type="submit"]/i
    def test_login_button_text(self):
        actual = self.chrome.find_element(*self.LOGIN_BUTTON).text
        expected = 'Login'
        self.assertEqual(expected, actual, 'the text is not correct')

    #Test5 - Verificati ca atributul href al linkului ‘Elemental Selenium’ e corect
    def test_attribute_elem_selenium(self):
        actual = self.chrome.find_element(*self.ELEM_SELENIUM).text
        expected = 'Elemental Selenium'
        self.assertEqual(expected, actual, 'Attribute is different')

    #Test6 - Lasati goale user si pass  /Click login / Verifica ca eroarea e displayed

    def test_error_login_check(self):
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        error = self.chrome.find_element(*self.ERROR_MESSAGE)  # salvam eroare in error
        self.assertTrue(error.is_displayed(), 'Eroarea nu e vizibila')

    #Test7 - Completeaza cu user si pass invalide/Click login / Verifica ca eroarea e displayed
    def test_login_invalid(self):
        self.chrome.find_element(*self.USERNAME_LOGIN).send_keys('marius')
        self.chrome.find_element(*self.PASSWORD_LOGIN).send_keys('Test123')
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        #sleep(5)
        actual = self.chrome.find_element(*self.ERROR_MESSAGE).text
        expected = 'Your username is invalid!'
        self.assertTrue(expected in actual, 'Error message text is incorrect')

    #Test8 - Lasati goale user si pass  /Click login / Apasa x la eroare/ Verifica ca eroarea a disparut
    def test_error_login_check_errorIsGone(self):
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        self.chrome.find_element(*self.CLOSE_ERROR_MESSAGE).click()
        error = self.chrome.find_elements() # salvam eroare in error
        self.assertTrue(len(error) == 0, 'eroarea e vizibila')
        # merge, dar nu stiu de ce :(  /// nu inteleg ce cauta acum rand 90 ... teoretic erooori pe care nu la gaseste, darr...

    #Test9 - Ia ca o lista toate //label  /  Verifica textul ca textul de pe ele sa fie cel asteptat (Username si Password)
    #         Aici e ok sa avem 2 asserturi
    def test_labels(self):
        actual = self.chrome.find_elements(*self.LABELS)[0].text
        expected = 'Username'
        self.assertEqual(expected, actual, 'label1 text  is wrong')
        actual = self.chrome.find_elements(*self.LABELS)[1].text
        expected = 'Password'
        self.assertEqual(expected, actual, 'label2 text  is wrong')

    #Test10 - Completeaza cu user si pass valide  /  Click login  /  Verifica ca noul url CONTINE /secure
    #         Verifica ca elementul cu clasa=’flash succes’ este displayed
    #         Verifica ca mesajul de pe acest element CONTINE textul ‘secure area!’
    def test_login_pass(self):
        self.chrome.find_element(*self.USERNAME_LOGIN).send_keys('tomsmith')
        self.chrome.find_element(*self.PASSWORD_LOGIN).send_keys('SuperSecretPassword!')
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        #sleep(5)
        actual = self.chrome.current_url
        expected = 'https://the-internet.herokuapp.com/secure'
        self.assertEqual(expected, actual, 'URL nu e corect')
        #self.chrome.find_elements(By.PARTIAL_LINK_TEXT, '/secure')[1].click()  # V2 Verifica ca noul url CONTINE /secure
        # clasa flash success e displayed
       # WebDriverWait(self.chrome, 10).until(EC.presence_of_element_located(By.XPATH, '//*[@id="flash"]/text()'))  nu merge ????
        sucessMessage = self.chrome.find_element(*self.CORRECT_LOGIN_MESSAGE)  # salvam eroare in error
        self.assertTrue(sucessMessage.is_displayed(), 'Mesajul de succes nu s-a afisat')
        # partial text message is displayed
        actual = self.chrome.find_element(*self.CORRECT_LOGIN_MESSAGE).text
        expected = 'You logged into a secure area!'
        self.assertTrue(expected in actual, 'Error message text is incorrect')

    #Test11  - Completeaza cu user si pass valide / Click login  / Click logout
    #          Verifica ca ai ajuns pe https://the-internet.herokuapp.com/login
    def test_login_pass_exit(self):
        self.chrome.find_element(*self.USERNAME_LOGIN).send_keys('tomsmith')
        self.chrome.find_element(*self.PASSWORD_LOGIN).send_keys('SuperSecretPassword!')
        self.chrome.find_element(*self.LOGIN_BUTTON).click()
        sleep(3)
        self.chrome.find_element(*self.LOGOUT_BUTTON).click()
        sleep(3)
        actual = self.chrome.current_url
        expected = 'https://the-internet.herokuapp.com/login'
        self.assertEqual(expected, actual, ' Site-ul nu e corect')