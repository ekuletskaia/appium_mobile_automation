from appium import webdriver
from appium.options.android import UiAutomator2Options

from app.application import Application


def mobile_driver_init(context, scenario_name):
    """
    :param context: Behave context
    """
    desired_capabilities = {
        "platformName": "Android",
        "automationName": 'uiautomator2',
        "platformVersion": "13.0",
        "deviceName": "emulator-5554",
        "appActivity": "com.hotake.hotake.MainActivity",
        "appPackage": "com.stunt.dev.application",
        "app": r"C:\Users\elena.kuletsky\Desktop\mobile_automation\mobile_app\app-dev-release.apk"
    }

    appium_server_url = 'http://localhost:4723'
    capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)

    context.driver = webdriver.Remote(appium_server_url, options=capabilities_options)
    context.driver.implicitly_wait(5)

    context.app = Application(context.driver)


def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    mobile_driver_init(context, scenario.name)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        context.driver.save_screenshot(f'{step}.png')
        print('\nStep failed: ', step)


def after_scenario(context, feature):
    context.driver.quit()
