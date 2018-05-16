from bs4 import BeautifulSoup
import selenium
from selenium.webdriver.common.keys import Keys
import STATICS as st
from time import sleep

root_url = "https://intranet.cibertec.edu.pe/LoginIntranet/LoginCIB.aspx"
driver = None

def checkHorario(*args):
    # Open global variables
    global root_url
    global driver

    results = []
    driver = selenium.webdriver.Firefox()

    # Read site
    driver.get(root_url)

    loginWithID(args[0], args[1])
    sleep(2)

    modalidad()
    sleep(2)

    aplicacion("horario")
    sleep(2)

    manageTabs(1)
    sleep(0.5)

    modalidad()
    sleep(2)

    # assign result
    results = horario()

    # Close driver
    driver.quit()

    return results

def checkNotas():
    # Open global variables
    global root_url
    global driver

    results = []
    driver = selenium.webdriver.Firefox()

    # Read site
    driver.get(root_url)

    login()
    sleep(2)

    modalidad()
    sleep(2)

    aplicacion("notas")
    sleep(2)

    manageTabs(1)#switch to recently opened tab
    sleep(2)

    modalidad()
    sleep(2)

    #Assign result
    results = notas()

    #Close driver
    driver.quit()

    return results


def login():
    global driver

    # Get login box
    username = driver.find_element_by_xpath(
        "//input[@class='WEB_cajaLogin'][1]")
    password = driver.find_element_by_xpath("//input[@type='password']")
    submit = driver.find_element_by_xpath(
        "//a[@href='javascript:InvocarForm();']")

    username.send_keys(st.getUser())
    password.send_keys(st.getPass())
    # submit.click()
    driver.execute_script("javascript:InvocarForm();")

    return

def loginWithID(idLogin, idPassword):
    global driver

    # Get login box
    username = driver.find_element_by_xpath(
        "//input[@class='WEB_cajaLogin'][1]")
    password = driver.find_element_by_xpath("//input[@type='password']")
    submit = driver.find_element_by_xpath(
        "//a[@href='javascript:InvocarForm();']")

    username.send_keys(str(idLogin))
    password.send_keys(str(idPassword))
    # submit.click()
    driver.execute_script("javascript:InvocarForm();")

    return

def modalidad():
    global driver

    modalidad = driver.find_element_by_xpath("//input[@name='radReg']")
    modalidad.click()

    driver.execute_script("JavaScript:validar();")

    return

def aplicacion(required):#gonna be modular using dictionary to search for tags
    global driver

    iframe = driver.find_element_by_name("principal")
    driver.switch_to.frame(iframe)
    driver.execute_script("OpenSubmenu(sec3)")

    sleep(0.5)

    app = driver.find_element_by_xpath("//a[@title='"+select(required)+"']")
    app.click()

    driver.switch_to.default_content()

    return

def manageTabs(tabIndex):
    global driver

    driver.switch_to.window(driver.window_handles[tabIndex])
    return

# Parse the data


def horario():
    global driver

    # Get the iFrame
    iframe = driver.find_element_by_name("F1")
    driver.switch_to.frame(iframe)

    # Soup it!
    html = driver.page_source
    page_soup = BeautifulSoup(html, "lxml")

    data = page_soup.findAll("table", attrs={"bgcolor": "000080"})

    data = filterData(page_soup)

    # print(data)
    text = open("output.html", "w")
    text.write("<html><body>")
    text.write(str(data[0]))
    text.write("</body></html>")
    text.close()

    return data

def notas():
    global driver
    driver

    # Get the iFrame
    iframe = driver.find_element_by_name("F1")
    driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_name("z1")
    driver.switch_to.frame(iframe)

    # Soup it!
    html = driver.page_source
    page_soup = BeautifulSoup(html, "lxml")

    data = page_soup.findAll("table", attrs={"bgcolor": "000080"})

    data = filterData(page_soup)

    text = open("output.html", "w")
    text.write("<html><body>")
    text.write(str(data[0]))
    text.write("</body></html>")
    text.close()

    return data

# Filter table


def filterData(raw):
    result = raw.findAll(lambda tag: tag.name == "table", attrs={
                         "bgcolor": "000080"})  # findchildren.findchildren

    return result

#Diccionario de datos
def select(index):
    return{
        "notas":"Consulta tus notas del período actual",
        "horario":"Utiliza esta opción para conocer tus horarios de clases y recuperaciones"
    }.get(index, "notas")


if __name__ == "__main__":
    checkNotas()
