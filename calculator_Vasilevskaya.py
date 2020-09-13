import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# set Desired Capabilities
# set [udid] to your android device id, it can be found by "adb devices" command
desired_caps = {
  "deviceName": "my",
  "platformName": "android",
  "platformVersion": "10",
  "udid": "3173a32",
  "appPackage": "com.vbanthia.androidsampleapp",
  "appActivity": "com.vbanthia.androidsampleapp.MainActivity"
  }

driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

# app view id
idInputFieldLeft = "com.vbanthia.androidsampleapp:id/inputFieldLeft"
idInputFieldRight = "com.vbanthia.androidsampleapp:id/inputFieldRight"
idAdditionButton = "com.vbanthia.androidsampleapp:id/additionButton"
idSubtractButton = "com.vbanthia.androidsampleapp:id/subtractButton"
idMultiplicationButton = "com.vbanthia.androidsampleapp:id/multiplicationButton"
idDivisionButton = "com.vbanthia.androidsampleapp:id/divisionButton"
idResetButton = "com.vbanthia.androidsampleapp:id/resetButton"
idResultTextView = "com.vbanthia.androidsampleapp:id/resultTextView"
idErrorMessageUpdate = "android:id/alertTitle"
idErrorButtonOK = "android:id/button1"

# input, expected datas and expected result data for tests
# each line consists of input left field value, input right field value, expected left value, expected right value,
# expected result for each test
# e.g. "5" will be entered into left field, "5" in right field, "5.00" and "5.00" will be expected in result string
# expected result for addition "10.00", substraction "0.00", multiply "25.00", divide "1.00"
# expected addition result "5.00 + 5.00 = 10.00" 
testSets = [
    [["5","5"],["5.00","5.00"],["10.00","0.00","25.00","1.00"]],
    [["0","5"],["0.00","5.00"],["5.00","-5.00","0.00","0.00"]],
    [["5","0"],["5.00","0.00"],["5.00","5.00","0.00","Делить на \"0\" нельзя"]],
    [["99999999999999999","99999999999999999"],["99999999999999999.00","99999999999999999.00"],["199999999999999998.00","0.00","1Е+34","1.00"]],
    [["99999999","99999999"],["99999999.00","99999999.00"],[ "199999998.00","0.00","9999999800000001","1.00"]],
    [["100000000000000000001","1"],["1Е+20","1.00"],["1Е+20","1Е+20","1Е+20","1Е+20"]],
    [["1","100000000000000000001"],["1.00","1Е+20"],["1Е+20","-1Е+20","1Е+20","1Е-20"]],
    [["-100000000000000000001","1"],["-1Е+20","1.00"],["-1Е+20","-1Е+20","-1Е+20","-1Е+20"]],
    [["1","-100000000000000000001"],["1.00","-1Е+20"],["-1Е+20","1Е+20","-1Е+20","0.00"]],
    [["-4","1"],["-4.00","1.00"],["-3.00","-5.00","-4.00","-4.00"]],
    [["-4","-4"],["-4.00","-4.00"],["-8.00","0.00","16.00","1.00"]],
    [["1","-4"],["1.00","-4.00"],["-3.00","5.00","-4.00","-0.25"]],
    [["0.1","0.0"],["0.10","0.00"],["0.10","0.10","0.00","Делить на \"0\" нельзя"]],
    [["0.1","0.1"],["0.10","0.10"],["0.20","0.00","0.01","1.00"]],
    [["0.0","0.1"],["0.00","0.10"],["0.10","-0.10","0.00","0.00"]],
    [["0.0","0.0"],["0.00","0.00"],["0.00","0.00","0.00","Делить на \"0\" нельзя"]],
    [["-0.1","-0.1"],["-0.10","-0.10"],[ "-0.20","0.00","0.01","1.00"]],
    [["0.14","0.14"],["0.14","0.14"],["0.28","0.00","0.02","1.00"]],
    [["0","0.145"],["0.00","0.14"],["0.14","-0.14","0.00","0.00"]],
    [["0.148","0.141"],["0.15","0.14"],["0.29","0.01","0.02","1.05"]],
    [[".2","0.1"],["0.20","0.10"],["0.30","0.10","0.02","2.00"]],
    [["0.1",".2"],["0.10","0.20"],["0.30","-0.10","0.02","0.50"]]
]

# find elements for each view id
def findElementsById():
    global leftField
    leftField = driver.find_element_by_id(idInputFieldLeft)
    global rightField
    rightField = driver.find_element_by_id(idInputFieldRight)
    global additionButton
    additionButton = driver.find_element_by_id(idAdditionButton)
    global subtractButton
    subtractButton = driver.find_element_by_id(idSubtractButton)
    global multiplicationButton
    multiplicationButton = driver.find_element_by_id(idMultiplicationButton)
    global divisionButton
    divisionButton = driver.find_element_by_id(idDivisionButton)
    global resetButton
    resetButton = driver.find_element_by_id(idResetButton)
    global actualResultField
    actualResultField = driver.find_element_by_id(idResultTextView)

countTests = len(testSets)

#test checks "Addition", "Subtract", "Multiplication" and "Division" functions
def test(testSets, button, buttonSign, count):
    # going through the values of testSets list and getting needed elements
    for i in range (len(testSets[0][2])):
        countSuccess = count
        countFaild = 0
        for j in range (len(testSets)):
            leftField.set_text(testSets[j][0][0])
            rightField.set_text(testSets[j][0][1])
            button[i].click()

            # getting of actual result string
            actualResultString = actualResultField.text

            # setting of expected result string
            expectedResultString = testSets[j][1][0] + " " + buttonSign[i] + " " + testSets[j][1][1] + " = " + testSets[j][2][i]

            # comparison of results
            # if actual and expected results are different
            # print failed element
            if expectedResultString != actualResultString:
                aResult = actualResultString.split()
                actFirstNum = aResult[0]
                actSecondNum = aResult[2]
                actResultNum = aResult[4]
                print ("Error. Operation: " + buttonSign[i])
                print("Entered left number: " + testSets[j][0][0] + "\tEntered right number: " + testSets[j][0][1] + 
                "\nExpected left number:" + testSets[j][1][0] + "\tExpected right number: " + testSets[j][1][1] + "\tExpected result: " + testSets[j][2][i] +
                "\nActual left number: " + actFirstNum + "\tActual right number: " + actSecondNum + "\tActual result: " +actResultNum)
                print()

                # count failed and successful tests
                countFaild = countFaild + 1
                countSuccess = countSuccess - 1
        
        # print test results
        print ("Test operation \"" + buttonSign[i] + "\" completed\n")
        print ("Total test count for operation \"" + buttonSign[i] + "\" is " + str(count))
        print ("Successful tests: " + str(countSuccess))
        print ("Failed tests: " + str(countFaild))
        print()
        leftField.set_text("")
        rightField.set_text("")


#test checks that data in fields are saved after rotation
def rotateTest (button):
    # save old orientation
    oldOrientation = driver.orientation

    # set test orientation and find elements
    driver.orientation = "PORTRAIT"
    findElementsById()

    # set test data
    leftFieldPortraitText = "5.00"
    rightFieldPortraitText = "6.00"
    leftField.set_text(leftFieldPortraitText)
    rightField.set_text(rightFieldPortraitText)
    button.click()
    resultPortraitText = actualResultField.text
   
    #change orientation and get values
    driver.orientation = "LANDSCAPE"
    findElementsById()
    leftFieldLandscape = leftField.text
    rightFieldLandscape = rightField.text
    actualResultLandscape = actualResultField.text

    #check values after rotation
    if (leftFieldPortraitText != leftFieldLandscape):
        print ("Error. Operation - check left number after rotation" )
        print ("Left number before rotation: " + leftFieldPortraitText)
        print ("Left number after rotation: " + leftFieldLandscape)
    if (rightFieldPortraitText != rightFieldLandscape):
        print ("Error. Operation - check right number after rotation" )
        print ("Right number before rotation: " + rightFieldPortraitText)
        print ("Right number after rotation: " + rightFieldLandscape)
    if (resultPortraitText != actualResultLandscape):
        print ("Error. Operation - check result number after rotation" )
        print ("Result before rotation: " + resultPortraitText)
        print ("Result after rotation: " + actualResultLandscape)
    
    #reset values and restore orientation
    resetButton.click()
    driver.orientation = oldOrientation
    findElementsById()
    print("Screen rotation test completed\n")

#test checks reset button
def resetTest (opButton, resButton):
    # set test data
    leftFieldText = "5.00"
    rightFieldText = "6.00"
    leftField.set_text(leftFieldText)
    rightField.set_text(rightFieldText)
    opButton.click()
    leftFieldBeforeReset = leftField.text
    rightFieldBeforeReset = rightField.text

    # getting of actual result string before pushing Reset
    actualResultBeforeReset = actualResultField.text

    # click reset button and get the values of the fields
    resButton.click()
    leftFieldAfterReset = leftField.text
    rightFieldAfterReset = rightField.text
    actualResultAfterReset = actualResultField.text
    
    # check values after clicking reset button
    if (leftFieldAfterReset != ""):
        print ("Error. Operation - Reset button" )
        print ("Left number before reset: " + leftFieldBeforeReset)
        print ("Left number after reset: " + leftFieldAfterReset)
    if (rightFieldAfterReset != ""):
        print ("Error. Operation - Reset button" )
        print ("Right number before reset: " + rightFieldBeforeReset)
        print ("Right number after reset: " + rightFieldAfterReset)
    if (actualResultAfterReset != ""):
        print ("Error. Operation - Reset button" )
        print ("Result before reset: " + actualResultBeforeReset)
        print ("Result after reset: " + actualResultAfterReset )
    print("Reset button test completed\n")

#test checks that empty field is not valid for input
def testEmpty(button):
    # set test data
    inputData = [["", "5"], ["5", ""], ["",""]]
    outputData = "Please, fill the input fields correctly"
    #check result after set empty data
    for i in range(len(inputData)):
        leftField.set_text(inputData[i][0])
        rightField.set_text(inputData[i][1])
        button.click()
        if actualResultField.text != outputData:
            print("Error. Operation - Empty values in fields test")
    print("Empty values in fields test completed\n")

# wait application start, then close error message
try:
  wait = WebDriverWait(driver, 3)
  errorMessage = wait.until(EC.element_to_be_clickable((By.ID,idErrorMessageUpdate)))
  errorButton = driver.find_element_by_id(idErrorButtonOK)
  errorButton.click()
finally:
  wait = WebDriverWait(driver, 3)
  element = wait.until(EC.element_to_be_clickable((By.ID,idAdditionButton)))
  print("Application started")

# finding of elements
findElementsById()
buttons = [additionButton, subtractButton, multiplicationButton, divisionButton]
buttunsSign = ["+", "-", "*", "/"]

#start autotests
test(testSets, buttons, buttunsSign, countTests)
rotateTest(additionButton)
testEmpty(additionButton)
resetTest(additionButton, resetButton)
print ("All tests completed")