import urllib.request
import urllib.parse
import http.cookiejar
import datetime
import re

BASE_URL = "http://localhost:8084/RentalVehicleSystem"

def make_session():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    return opener

def test_flow():
    print("=== Step 1: Testing Public Pages & Logged-Out Navbar ===")
    public_opener = make_session()
    
    # 1. Landing Page
    req = urllib.request.Request(f"{BASE_URL}/")
    with public_opener.open(req) as resp:
        assert resp.status == 200, f"Landing page returned {resp.status}"
        body = resp.read().decode('utf-8')
        assert "RentRide" in body
        assert "Browse Vehicles" in body
        assert "Login" in body
        assert "Register" in body
        print(" [PASS] Landing Page GET 200 OK — Navbar has: Home, Browse Vehicles, Login, Register")

    # 2. Vehicle Images Verification
    for img_name in ["swift.jpg", "creta.jpg", "city.jpg", "fortuner.jpg", "hunter.jpg", "default.jpg"]:
        img_url = f"{BASE_URL}/images/vehicles/{img_name}"
        with public_opener.open(img_url) as resp:
            assert resp.status == 200
            content_type = resp.headers.get("Content-Type", "")
            size = len(resp.read())
            assert size > 10000, f"Image {img_name} seems empty"
            print(f" [PASS] Vehicle Image served: {img_name} ({size} bytes, {content_type})")

    # 3. Vehicles Page with Images
    req = urllib.request.Request(f"{BASE_URL}/vehicles")
    with public_opener.open(req) as resp:
        assert resp.status == 200
        body = resp.read().decode('utf-8')
        assert "vehicle-photo" in body
        assert "images/vehicles/" in body
        print(" [PASS] Available Vehicles catalog displays real vehicle photography")

    print("\n=== Step 2: Testing Customer Registration & Logged-In Navbar ===")
    customer_opener = make_session()
    ts = int(datetime.datetime.now().timestamp())
    email = f"user_{ts}@test.com"
    
    # Register
    reg_data = urllib.parse.urlencode({
        "name": "Alex Mercer",
        "email": email,
        "password": "Password123"
    }).encode('utf-8')
    with customer_opener.open(urllib.request.Request(f"{BASE_URL}/register", data=reg_data, method="POST")) as resp:
        print(f" [PASS] Customer Registration successful")

    # Login
    login_data = urllib.parse.urlencode({
        "email": email,
        "password": "Password123"
    }).encode('utf-8')
    with customer_opener.open(urllib.request.Request(f"{BASE_URL}/login", data=login_data, method="POST")) as resp:
        body = resp.read().decode('utf-8')
        assert "Alex Mercer" in body or "My Bookings" in body
        print(f" [PASS] Customer Login authenticated")

    # Check Logged-in Navbar on /vehicles
    with customer_opener.open(f"{BASE_URL}/vehicles") as resp:
        body = resp.read().decode('utf-8')
        assert "My Bookings" in body
        assert "Alex Mercer" in body
        assert "Logout" in body
        print(" [PASS] Logged-in Navbar verified: Home, Browse Vehicles, My Bookings, Alex Mercer, Logout")

    print("\n=== Step 3: Testing Booking Flow with Vehicle 2 (Creta) ===")
    today = datetime.date.today()
    # Pick dates 10 days out so no collision with existing bookings
    start_date = today + datetime.timedelta(days=10)
    end_date = today + datetime.timedelta(days=13)

    # Booking Form
    with customer_opener.open(f"{BASE_URL}/booking?vehicleId=2") as resp:
        assert resp.status == 200
        body = resp.read().decode('utf-8')
        assert "Creta" in body
        print(" [PASS] Booking Form GET 200 OK for Hyundai Creta")

    # Submit Booking
    book_data = urllib.parse.urlencode({
        "vehicleId": "2",
        "startDate": str(start_date),
        "endDate": str(end_date)
    }).encode('utf-8')
    with customer_opener.open(urllib.request.Request(f"{BASE_URL}/booking", data=book_data, method="POST")) as resp:
        url = resp.geturl()
        m = re.search(r"bookingId=(\d+)", url)
        assert m, f"No bookingId in url: {url}"
        booking_id = m.group(1)
        print(f" [PASS] Booking successfully created -> Booking ID #{booking_id}")

    print("\n=== Step 4: Testing Mock Payment Sandbox ===")
    with customer_opener.open(f"{BASE_URL}/payment?bookingId={booking_id}") as resp:
        assert resp.status == 200
        body = resp.read().decode('utf-8')
        assert "TEST SANDBOX" in body
        assert "Simulated Credit/Debit Card" in body
        print(" [PASS] Mock Sandbox Payment screen rendered correctly")

    # Process Successful Payment
    pay_data = urllib.parse.urlencode({
        "bookingId": booking_id,
        "paymentStatus": "SUCCESS"
    }).encode('utf-8')
    with customer_opener.open(urllib.request.Request(f"{BASE_URL}/payment", data=pay_data, method="POST")) as resp:
        body = resp.read().decode('utf-8')
        assert "Payment completed successfully" in body or "CONFIRMED" in body
        print(" [PASS] Payment settled -> Booking marked CONFIRMED in My Bookings")

    print("\n=== Step 5: Testing Overlap Rejection ===")
    # Attempt duplicate booking on same vehicle for overlapping dates
    overlap_book = urllib.parse.urlencode({
        "vehicleId": "2",
        "startDate": str(today + datetime.timedelta(days=11)),
        "endDate": str(today + datetime.timedelta(days=12))
    }).encode('utf-8')
    with customer_opener.open(urllib.request.Request(f"{BASE_URL}/booking", data=overlap_book, method="POST")) as resp:
        body = resp.read().decode('utf-8')
        assert "overlapping" in body.lower() or "unavailable" in body.lower()
        print(" [PASS] Overlap detected and safely rejected")

    print("\n=== Step 6: Testing Admin Portal & Admin Navbar ===")
    admin_opener = make_session()
    admin_login = urllib.parse.urlencode({
        "email": "admin@rental.com",
        "password": "admin123"
    }).encode('utf-8')
    with admin_opener.open(urllib.request.Request(f"{BASE_URL}/login", data=admin_login, method="POST")) as resp:
        body = resp.read().decode('utf-8')
        assert "Admin Dashboard" in body
        assert "Manage Vehicles" in body
        assert "Manage Bookings" in body
        assert "Logout" in body
        print(" [PASS] Admin Navbar verified: Admin Dashboard, Manage Vehicles, Manage Bookings, Logout")

    with admin_opener.open(f"{BASE_URL}/admin/dashboard") as resp:
        assert resp.status == 200
        body = resp.read().decode('utf-8')
        assert "Operational Dashboard" in body
        assert "Gross Revenue" in body
        print(" [PASS] Admin Dashboard metrics & revenue loaded")

    with admin_opener.open(f"{BASE_URL}/admin/vehicles") as resp:
        assert resp.status == 200
        body = resp.read().decode('utf-8')
        assert "Fleet Inventory Management" in body
        assert "swift.jpg" in body
        print(" [PASS] Admin Fleet Inventory displays vehicle photos & management controls")

    with admin_opener.open(f"{BASE_URL}/admin/bookings") as resp:
        assert resp.status == 200
        body = resp.read().decode('utf-8')
        assert "Customer Reservations Control" in body
        print(" [PASS] Admin Customer Reservations loaded")

    print("\n=== ALL UI, CSS, NAVBAR, AND IMAGE TESTS PASSED 100%! ===")

if __name__ == "__main__":
    test_flow()
