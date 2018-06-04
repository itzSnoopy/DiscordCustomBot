<<<<<<< HEAD
from bs4 import BeautifulSoup
import selenium
from selenium.webdriver.common.keys import Keys
from time import sleep
from decimal import *

root_url = "https://intranet.cibertec.edu.pe/LoginIntranet/LoginCIB.aspx"
driver = None
getcontext().prec = 2

# Test user login


def testUser(args):
    # Open global variables
    global root_url
    global driver

    # 0: validation result(T/F), 1: Names or login error message
    results = ["ERROR"]
    driver = selenium.webdriver.Firefox(executable_path="geckodriver.exe")

    # Read site
    driver.get(root_url)

    login(args[0], args[1])

    waitUntilLoad()

    if driver.current_url == "https://intranet.cibertec.edu.pe/Programas/Tipo_Modalidad.asp":
        # seleccionar modalidad
        modalidad("regular")

        waitUntilLoad()

        # validate and get name
        results = ["Validated", getName()]

    else:
        html = driver.page_source
        page_soup = BeautifulSoup(html, "lxml")

        try:
            message = page_soup.find(
                "span", attrs={"class": "MensajeError"}).getText()
        except err:
            message = "Error al cargar la pagina, vuelva a intentarlo"

        results = ["Error", message]

    # print(str(results))

    driver.quit()

    return results

# Check Horario


def checkHorario(args):
    # Open global variables
    global root_url
    global driver

    driver = selenium.webdriver.Firefox()

    # Read site
    driver.get(root_url)

    login(args[0], args[1])

    waitUntilLoad()

    modalidad("regular")

    waitUntilLoad()

    aplicacion("horario")

    waitUntilLoad()

    manageTabs(1)

    waitUntilLoad()

    modalidad("regular")

    waitUntilLoad()

    data = filterHorarioTable()

    writeOutput(data)

    driver.quit()

    print("finished horario module")

    return


def checkPromedio(args):
    # Open global variables
    global root_url
    global driver

    driver = selenium.webdriver.Firefox()

    # Read site
    driver.get(root_url)

    login(args[0], args[1])

    waitUntilLoad()

    modalidad("regular")

    waitUntilLoad()

    aplicacion("promedio")

    waitUntilLoad()

    manageTabs(1)

    waitUntilLoad()

    modalidad("promedio")

    waitUntilLoad()

    manageTabs(1)

    waitUntilLoad()

    modalidad("regular")

    waitUntilLoad()

    if len(args) == 2:
        data = filterPromedioTable()
    elif len(args) == 3:
        data = filterCursoTable(args[2])

    driver.quit()

    print("finished horario module")

    return data


def filterHorarioTable():
    data = getHorarioTable()
    finalTable = []

    # page_soup = BeautifulSoup(data, "lxml")
    table = data.findAll("tr")

    for i in range(len(table)):
        if i == 0:  # add days of week
            finalTable.append(table[i])
            continue

        row = table[i].findAll("td")

        for j in range(len(row)):
            if j == 0:  # add hora
                continue

            cell = row[j]

            # .decode('unicode_escape').encode('ascii', ignore)
            # text = cell.getText().strip("\n").replace("b''", "").encode('ascii', 'ignore').decode('unicode_escape').encode("ascii", "ignore")

            # text = cell.getText().encode("ascii", "ignore").decode("unicode_escape").encode("ascii", "ignore")

            # text = cell.getText().strip("b'\n'")
            text = "" + cell.getText().encode("ascii", "ignore").decode("unicode_escape")

            if len(text) > 1:
                finalTable.append(row)
                break

    return finalTable


def filterPromedioTable():
    data = getPromedioTable()
    finalTable = []

    table = data.findAll("tr")

    for i in range(len(table)):
        # ignore headers and footer
        if i == 0 or i == (len(table) - 1):
            continue

        row = table[i].findAll("td")

        finalTable.append([
            row[1].getText().encode("ascii", "ignore").decode(
                "unicode_escape").replace("\t", "").replace("\n", ""),
            row[2].getText().encode("ascii", "ignore").decode("unicode_escape"),
            row[3].getText().encode("ascii", "ignore").decode("unicode_escape"),
            row[7].getText().encode("ascii", "ignore").decode("unicode_escape"),
            row[8].getText().encode("ascii", "ignore").decode("unicode_escape")]
        )

    return finalTable


def filterCursoTable(code):
    data = getCursoTable(code)
    finalTable = []

    table = data.findAll("tr")

    total = Decimal(0)
    avance = Decimal(0)
    suma = Decimal(0)

    for i in range(len(table)):
        if i <= 3 or i == (len(table) - 1):  # ignore headers
            continue

        row = table[i].findAll("td")

        value = row[3].getText().encode(
            "ascii", "ignore").decode("unicode_escape")[:-1]
        score = row[4].getText().encode(
            "ascii", "ignore").decode("unicode_escape")

        calc = ""

        if not score == "":
            value = Decimal(value)
            score = Decimal(score)

            total += score * value / 50
            avance += value
            suma += score

            calc = str(score * value / 50)
        else:
            continue

        finalTable.append([
            row[0].getText().encode("ascii", "ignore").decode("unicode_escape") +
            row[2].getText().encode("ascii", "ignore").decode("unicode_escape"),
            row[3].getText().encode("ascii", "ignore").decode(
                "unicode_escape").encode("ascii", "ignore").decode("unicode_escape"),
            row[4].getText().encode("ascii", "ignore").decode("unicode_escape"),
            calc
        ])

    finalTable.append([
        "Total", str(avance) + "%", str(suma), str(total)
    ])

    for item in finalTable:
        print(item)

    return finalTable


def getHorarioTable():
    global driver

    # Get the iFrame
    iframe = driver.find_element_by_name("F1")
    driver.switch_to.frame(iframe)

    # soup it
    page_soup = BeautifulSoup(driver.page_source, "lxml")

    data = page_soup.findAll(lambda tag: tag.name == "table", attrs={
        "bgcolor": "000080"})[0]  # findchildren.findchildren

    return data


def getPromedioTable():
    global driver

    # Get the iFrame
    iframe = driver.find_element_by_name("F1")
    driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_name("z1")
    driver.switch_to.frame(iframe)

    # soup it
    page_soup = BeautifulSoup(driver.page_source, "lxml")

    data = page_soup.find(lambda tag: tag.name == "table",
                          attrs={"bgcolor": "000080"}).find("table")

    return data


def getCursoTable(code):
    global driver
    data = []

    # Get the iFrame
    iframe = driver.find_element_by_name("F1")
    driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_name("z1")
    driver.switch_to.frame(iframe)

    driver.execute_script("Todas()")

    waitUntilLoad()
    waitUntilLoad()
    waitUntilLoad()
    waitUntilLoad()

    # soup it
    page_soup = BeautifulSoup(driver.page_source, "lxml")

    data = ["None found"]

    for table in page_soup.findAll("table", attrs={"bgcolor": "000080"}):
        if not table.findChildren("tbody"):
            continue

        if table.find("td").findNext("td").getText()[1:] == code:
            data = table
            break

    return data

# Re-usable commands


def modalidad(tipo):
    global driver

    if tipo == "regular":
        modalidad = driver.find_element_by_xpath("//input[@name='radReg']")
        modalidad.click()

        driver.execute_script("JavaScript:validar();")

    return


def manageTabs(tabIndex):
    global driver

    driver.switch_to.window(driver.window_handles[tabIndex])


def getName():
    global driver

    result = "NAME NOT FOUND"

    waitUntilLoad()

    iframe = driver.find_element_by_name("bienvenida")
    driver.switch_to.frame(iframe)

    page_soup = BeautifulSoup(driver.page_source, "lxml")

    data = page_soup.find("font").getText()
    result = str(data[:-35]).strip("\n")

    # print(result)

    driver.switch_to.default_content()

    return result


def select(index):  # dictionary for selecting in application
    return{
        "promedio": "Consulta tus notas del período actual",
        "horario": "Utiliza esta opción para conocer tus horarios de clases y recuperaciones"
    }.get(index, "notas")


def aplicacion(module):
    global driver

    iframe = driver.find_element_by_name("principal")
    driver.switch_to.frame(iframe)
    driver.execute_script("OpenSubmenu(sec3)")

    waitUntilLoad()

    app = driver.find_element_by_xpath("//a[@title='" + select(module) + "']")
    app.click()

    driver.switch_to.default_content()

    return


def login(idLogin, idPassword):
    global driver

    # Get login box
    username = driver.find_element_by_xpath(
        "//input[@class='WEB_cajaLogin'][1]")
    password = driver.find_element_by_xpath("//input[@type='password']")
    submit = driver.find_element_by_xpath(
        "//a[@href='javascript:InvocarForm();']")

    username.send_keys(str(idLogin))
    password.send_keys(str(idPassword))
    driver.execute_script("javascript:InvocarForm();")

    return


def writeOutput(output):
    with open("output.html", "w") as text:
        text.write("<html><body>")
        text.write(
            "<table width='650' cellspacing='1' cellpadding='0' border='0' bgcolor='000080' alignt='left'>")

        for row in output:
            text.write("<tr>")
            for cell in row:
                text.write(str(cell) + "\n")

            text.write("</tr>")
        text.write("</table></html></body>")

    return

# Wait until load


def waitUntilLoad():
    global driver

    while True:
        sleep(0.4)

        if(str(driver.execute_script("return document.readyState")) == "complete"):
            break


if __name__ == "__main__":
    #testUser(["i201812345", "P4$$W0RD"])
    #checkPromedio(["i201812345", "P4$$W0RD", "1922"])
    print("packCibertec.py: testing!")
=======
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
>>>>>>> 38ed5d55e9909f4d0014ab75a2d99683387cc514
