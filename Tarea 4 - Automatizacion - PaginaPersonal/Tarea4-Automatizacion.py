import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función para capturar la pantalla
def capture_screenshot(driver, screenshot_name):
    try:
        screenshots_dir = os.path.join(os.getcwd(), 'Screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)  
        screenshot_path = os.path.join(screenshots_dir, f"{screenshot_name}_{time.strftime('%Y%m%d_%H%M%S')}.png")
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    except Exception as ex:
        print(f"Error al capturar la pantalla: {ex}")
        return None

# Configuración del WebDriver
@pytest.fixture(scope="function")
def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(executable_path=r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\Driver\\msedgedriver.exe")
    
    driver = webdriver.Edge(service=service, options=options)
    yield driver
    driver.quit()

# Test de Login exitoso
def test_successful_login(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Login - Caso de Éxito"
    print(f"Prueba: {test_name}")
    
    try:
        driver.get("https://webautomatizacion.netlify.app/login.html")  
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        screenshot_path = capture_screenshot(driver, "LoginPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("123")
        
        login_button = driver.find_element(By.XPATH, "//button[@class='button1']")
        login_button.click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
        
        screenshot_path = capture_screenshot(driver, "LoggedInPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        assert "index.html" in driver.current_url, "No se redirigió correctamente a la página principal."
        
        print(f"Prueba exitosa: Login realizado y redirigido a la página principal.")
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"

# Test de Login fallido
def test_failed_login(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Login - Caso de Fracaso"
    print(f"Prueba: {test_name}")
    
    try:
        driver.get("https://webautomatizacion.netlify.app/login.html")  
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        screenshot_path = capture_screenshot(driver, "LoginPage_Failure")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        driver.find_element(By.ID, "username").send_keys("Popoloperez")
        driver.find_element(By.ID, "password").send_keys("156")
        driver.find_element(By.XPATH, "//button[@class='button1']").click()
        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "errorAlert")))
        
        screenshot_path = capture_screenshot(driver, "FailedLoginAttempt")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        error_alert = driver.find_element(By.ID, "errorAlert")
        assert error_alert.is_displayed(), "La alerta de error no apareció como se esperaba."
        
        print(f"Prueba fallida completada con el mensaje de error.")
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"

# Test de Logout exitoso
def test_successful_logout(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Logout - Caso de Éxito"
    print(f"Prueba: {test_name}")
    
    try:
        driver.get("https://webautomatizacion.netlify.app/login.html") 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.XPATH, "//button[@class='button1']").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
        
        assert "index.html" in driver.current_url, "No se redirigió correctamente a la página principal."
        
        screenshot_path = capture_screenshot(driver, "LoggedInPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        logout_button = driver.find_element(By.ID, "logoutButton")
        logout_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("login.html"))
        assert "login.html" in driver.current_url, "No se redirigió correctamente a la página de inicio de sesión."

        is_logged_in = driver.execute_script("return localStorage.getItem('isLoggedIn')")
        assert is_logged_in is None, "La sesión no fue eliminada correctamente."

        screenshot_path = capture_screenshot(driver, "LoggedOutPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        print("Prueba de logout exitosa.")
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"

# Test de Blog

def test_navigate_to_blog(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Navegación a Blog"
    print(f"Prueba comenzando: {test_name}")  
    
    try:
        print("Accediendo a la página de login...")  
        driver.get("https://webautomatizacion.netlify.app/login.html")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

        print("Rellenando credenciales...")  
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.XPATH, "//button[@class='button1']").click()

        print("Esperando redirección a la página principal...")  
        WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
        assert "index.html" in driver.current_url, "No se redirigió correctamente a la página principal."

        print("Redirigido a la página principal. Procediendo a navegar a Blog...")  
        blog_link = driver.find_element(By.LINK_TEXT, "BLOG")
        blog_link.click()

        WebDriverWait(driver, 10).until(EC.url_to_be("https://webautomatizacion.netlify.app/blog"))

        print("Redirigido a la página del blog. Verificando URL...")  
        assert driver.current_url == "https://webautomatizacion.netlify.app/blog", f"Se esperaban redirigir a la URL correcta del blog. Se obtuvo: {driver.current_url}"

        screenshot_path = capture_screenshot(driver, "BlogPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")

        print("Prueba de navegación a Blog exitosa.")
    
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"  

# Test de navegación a la página de Blog
def test_navigate_to_blog(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Navegación a Blog"
    print(f"Prueba: {test_name}")
    
    try:
        driver.get("https://webautomatizacion.netlify.app/login.html")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.XPATH, "//button[@class='button1']").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
        assert "index.html" in driver.current_url, "No se redirigió correctamente a la página principal."

        blog_link = driver.find_element(By.LINK_TEXT, "BLOG")
        blog_link.click()
        time.sleep(5)  
        WebDriverWait(driver, 10).until(EC.url_to_be("https://webautomatizacion.netlify.app/blog"))
        
        assert driver.current_url == "https://webautomatizacion.netlify.app/blog", f"Se esperaban redirigir a la URL correcta del blog. Se obtuvo: {driver.current_url}"

        screenshot_path = capture_screenshot(driver, "BlogPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        print("Prueba de navegación a Blog exitosa.")
    
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"

# Test de navegación a la página de Temas
def test_navigate_to_themes(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Navegación a Temas"
    print(f"Prueba: {test_name}")
    
    try:
        driver.get("https://webautomatizacion.netlify.app/login.html")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.XPATH, "//button[@class='button1']").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
        assert "index.html" in driver.current_url, "No se redirigió correctamente a la página principal."

        themes_link = driver.find_element(By.LINK_TEXT, "TEMAS")
        themes_link.click()  
        time.sleep(5)  

        WebDriverWait(driver, 10).until(EC.url_to_be("https://webautomatizacion.netlify.app/cursos"))
        
        assert driver.current_url == "https://webautomatizacion.netlify.app/cursos", f"Se esperaban redirigir a la URL correcta de Temas. Se obtuvo: {driver.current_url}"

        screenshot_path = capture_screenshot(driver, "ThemesPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        print("Prueba de navegación a Temas exitosa.")
    
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"

#Test De Contactos
def test_navigate_to_contacts(setup_driver):
    driver = setup_driver
    test_name = "Prueba de Navegación a Contactos"
    print(f"Prueba: {test_name}")
    
    try:

        driver.get("https://webautomatizacion.netlify.app/login.html")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.XPATH, "//button[@class='button1']").click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("index.html"))
        assert "index.html" in driver.current_url, "No se redirigió correctamente a la página principal."

        contacts_link = driver.find_element(By.LINK_TEXT, "CONTACTOS")
        contacts_link.click()
        time.sleep(5)  

        WebDriverWait(driver, 10).until(EC.url_to_be("https://webautomatizacion.netlify.app/contactos"))
        
        assert driver.current_url == "https://webautomatizacion.netlify.app/contactos", f"Se esperaban redirigir a la URL correcta de Contactos. Se obtuvo: {driver.current_url}"

        screenshot_path = capture_screenshot(driver, "ContactsPage")
        print(f"Captura de pantalla guardada en: {screenshot_path}")
        
        print("Prueba de navegación a Contactos exitosa.")
    
    except Exception as ex:
        print(f"Error durante la prueba: {ex}")
        assert False, f"Error durante la prueba: {ex}"

if __name__ == "__main__":
    pytest.main(["--html=report.html"])


"""
COMANDO QUE SI O SI SE DEBE USAR PARA LA EJECUCION: pytest Tarea4-Automatizacion.py --html=report.html
"""