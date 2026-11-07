import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:8084/RentalVehicleSystem"
OUTPUT_DIR = os.path.join(os.getcwd(), "project-documentation", "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_driver():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,920')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Edge(options=options)
    driver.set_window_size(1440, 920)
    return driver

def capture_all():
    driver = get_driver()
    try:
        # 1. Landing Page
        print("1. Capturing 01-home-page.png...")
        driver.get(f"{BASE_URL}/")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "01-home-page.png"))

        # 2. Browse Vehicles Catalog
        print("2. Capturing 02-browse-vehicles.png...")
        driver.get(f"{BASE_URL}/vehicles")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "02-browse-vehicles.png"))

        # 3. Vehicle Details Page
        print("3. Capturing 03-vehicle-details.png...")
        driver.get(f"{BASE_URL}/vehicle-details?id=2")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "03-vehicle-details.png"))

        # 4. Login Page
        print("4. Capturing 04-user-login.png...")
        driver.get(f"{BASE_URL}/login.jsp")
        time.sleep(1.0)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "04-user-login.png"))

        # 5. Registration Page
        print("5. Capturing 05-user-registration.png...")
        driver.get(f"{BASE_URL}/register.jsp")
        time.sleep(1.0)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "05-user-registration.png"))

        # 6. Log in as Customer
        print("6. Logging in as customer...")
        driver.get(f"{BASE_URL}/login.jsp")
        driver.find_element(By.ID, "email").send_keys("user@rental.com")
        driver.find_element(By.ID, "password").send_keys("user1234")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)

        # 7. Customer Booking Form (Vehicle 3 - Honda City)
        print("7. Capturing 06-booking-form.png...")
        today = datetime.date.today()
        st_date = today + datetime.timedelta(days=40)
        en_date = today + datetime.timedelta(days=43)
        driver.get(f"{BASE_URL}/booking?vehicleId=3")
        time.sleep(1.0)
        try:
            start_in = driver.find_element(By.ID, "startDate")
            end_in = driver.find_element(By.ID, "endDate")
            start_in.clear()
            start_in.send_keys(str(st_date))
            end_in.clear()
            end_in.send_keys(str(en_date))
            # Trigger calculation by calling oninput
            driver.execute_script("if (typeof calculatePrice === 'function') { calculatePrice(); }")
            time.sleep(0.5)
        except Exception as e:
            print("Date input exception:", e)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "06-booking-form.png"))

        # 8. Submit booking to get to Payment Sandbox
        print("8. Submitting booking to reach Payment Sandbox...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)

        # 9. Payment Gateway Sandbox
        print("9. Capturing 07-payment-gateway-sandbox.png...")
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "07-payment-gateway-sandbox.png"))

        # 10. Complete Payment to Confirm Booking
        print("10. Completing simulated payment...")
        try:
            pay_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            pay_btn.click()
            time.sleep(1.5)
        except Exception as e:
            print("Payment click exception:", e)

        # 11. Customer My Bookings Dashboard
        print("11. Capturing 08-my-bookings.png...")
        driver.get(f"{BASE_URL}/my-bookings")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "08-my-bookings.png"))

        # 12. Overlap Error Validation
        print("12. Triggering and capturing 09-booking-overlap-validation.png...")
        driver.get(f"{BASE_URL}/booking?vehicleId=3")
        time.sleep(1.0)
        start_in = driver.find_element(By.ID, "startDate")
        end_in = driver.find_element(By.ID, "endDate")
        start_in.clear()
        start_in.send_keys(str(st_date))
        end_in.clear()
        end_in.send_keys(str(en_date))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "09-booking-overlap-validation.png"))

        # 13. Log out customer
        print("13. Logging out customer...")
        driver.get(f"{BASE_URL}/logout")
        time.sleep(1.0)

        # 14. Log in as Admin
        print("14. Logging in as Administrator...")
        driver.get(f"{BASE_URL}/login.jsp")
        driver.find_element(By.ID, "email").send_keys("admin@rental.com")
        driver.find_element(By.ID, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)

        # 15. Admin Dashboard
        print("15. Capturing 10-admin-dashboard.png...")
        driver.get(f"{BASE_URL}/admin/dashboard")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "10-admin-dashboard.png"))

        # 16. Admin Fleet Inventory Management
        print("16. Capturing 11-admin-fleet-management.png...")
        driver.get(f"{BASE_URL}/admin/vehicles")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "11-admin-fleet-management.png"))

        # 17. Admin Add Vehicle Modal/Card
        print("17. Capturing 12-admin-add-vehicle-form.png...")
        try:
            driver.execute_script("toggleAddForm();")
            time.sleep(0.5)
        except Exception as e:
            print("Toggle form exception:", e)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "12-admin-add-vehicle-form.png"))

        # 18. Admin Customer Reservations Control
        print("18. Capturing 13-admin-reservations.png...")
        driver.get(f"{BASE_URL}/admin/bookings")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "13-admin-reservations.png"))

        print("\nAll 13 screenshots successfully captured and saved!")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_all()
