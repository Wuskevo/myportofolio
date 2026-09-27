import os
import sys
import uuid
from datetime import date

import django
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

USER_PASSWORD = os.getenv("E2E_USER_PASSWORD")
ADMIN_PASSWORD = os.getenv("E2E_ADMIN_PASSWORD")

if not USER_PASSWORD or not ADMIN_PASSWORD:
    sys.exit("E2E_USER_PASSWORD and E2E_ADMIN_PASSWORD are not set in your .env file.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portofolio.settings")
django.setup()
from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse

from main.models import Credential, Experience, Project


def setup_users():
    user, _ = User.objects.get_or_create(username="burhan_test")
    user.set_password(USER_PASSWORD)
    user.is_superuser = False
    user.is_staff = False
    user.is_active = True
    user.groups.clear()
    user.user_permissions.clear()
    user.save()

    editor, _ = User.objects.get_or_create(username="editor_test")
    editor.set_password(USER_PASSWORD)
    editor.is_superuser = False
    editor.is_staff = False
    editor.is_active = True
    editor.user_permissions.clear()
    editor.save()

    editor_group, _ = Group.objects.get_or_create(name="Editor")
    editor_permissions = Permission.objects.filter(
        content_type__app_label="main",
        codename__in=(
            "change_experience",
            "change_credential",
            "change_project",
        ),
    )
    if editor_permissions.count() != 3:
        raise RuntimeError("Run migrations before setting up E2E editor permissions.")
    editor_group.permissions.set(editor_permissions)
    editor.groups.set([editor_group])

    admin, _ = User.objects.get_or_create(username="admin_test")
    admin.set_password(ADMIN_PASSWORD)
    admin.is_superuser = True
    admin.is_staff = True
    admin.is_active = True
    admin.save()


def create_test_records():
    token = uuid.uuid4().hex
    return {
        "experience": Experience.objects.create(
            title=f"E2E Experience {token}",
            description="Temporary authorization test record.",
            category="full-time",
        ),
        "credential": Credential.objects.create(
            title=f"E2E Credential {token}",
            description="Temporary authorization test record.",
            category="certification",
            issuer="E2E Test",
            date_received=date.today(),
        ),
        "project": Project.objects.create(
            title=f"E2E Project {token}",
            description="Temporary authorization test record.",
            tech_stack="Django",
        ),
    }


def crud_routes(records):
    return {
        "experiences": {
            "create": reverse("main:create_experience"),
            "update": reverse("main:update_experience", args=[records["experience"].id]),
            "delete": reverse("main:delete_experience", args=[records["experience"].id]),
            "list": reverse("main:show_experiences"),
        },
        "credentials": {
            "create": reverse("main:create_credential"),
            "update": reverse("main:update_credential", args=[records["credential"].id]),
            "delete": reverse("main:delete_credential", args=[records["credential"].id]),
            "list": reverse("main:show_credentials"),
        },
        "projects": {
            "create": reverse("main:create_project"),
            "update": reverse("main:update_project", args=[records["project"].id]),
            "delete": reverse("main:delete_project", args=[records["project"].id]),
            "list": reverse("main:show_projects"),
        },
    }


def login_as(driver, wait, base_url, username, password):
    driver.get(f"{base_url}/login/")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    wait.until(EC.url_to_be(f"{base_url}/"))
    wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "nav-user"), username))


def logout_from_site(driver, wait, base_url):
    driver.get(f"{base_url}/logout/")
    wait.until(EC.url_to_be(f"{base_url}/"))


def check_crud_authorization(driver, wait, base_url, records, role, allowed_operations):
    for section, routes in crud_routes(records).items():
        for operation in ("create", "update", "delete"):
            driver.get(f"{base_url}{routes[operation]}")

            if operation not in allowed_operations:
                assert "403" in driver.title or "Forbidden" in driver.page_source, (
                    f"{role} unexpectedly accessed {section} {operation}"
                )
                continue

            if operation == "delete":
                wait.until(EC.url_to_be(f"{base_url}{routes['list']}"))
            else:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-form")))

        print(f"[PASS] {role} {section} CRUD authorization verified")


def main():
    setup_users()

    options = webdriver.ChromeOptions()
    if "--headless" in sys.argv:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    base_url = "http://127.0.0.1:8000"
    records = {}

    try:
        records = create_test_records()

        # 1. Verify CSRF token on login form
        try:
            driver.get(f"{base_url}/login/")
        except Exception:
            print(f"Server is not running at {base_url}. Run 'python manage.py runserver' first.")
            return
        csrf = wait.until(
            EC.presence_of_element_located((By.NAME, "csrfmiddlewaretoken"))
        )
        assert csrf.get_attribute("value")
        assert driver.get_cookie("csrftoken")
        print("[PASS] CSRF token and cookie verified")

        # 2. Verify regular user login and CRUD authorization
        login_as(driver, wait, base_url, "burhan_test", USER_PASSWORD)
        assert driver.get_cookie("sessionid")
        assert driver.get_cookie("last_login")
        assert "Sesi Terakhir Login" in driver.page_source or "Last Login" in driver.page_source
        print("[PASS] Regular user login and session cookies verified")
        check_crud_authorization(driver, wait, base_url, records, "Regular user", set())

        # 3. Editors may update, but cannot create or delete portfolio data.
        logout_from_site(driver, wait, base_url)
        login_as(driver, wait, base_url, "editor_test", USER_PASSWORD)
        check_crud_authorization(
            driver,
            wait,
            base_url,
            records,
            "Editor",
            {"update"},
        )

        # 4. Superusers may create, update, and delete all portfolio data.
        logout_from_site(driver, wait, base_url)
        login_as(driver, wait, base_url, "admin_test", ADMIN_PASSWORD)
        check_crud_authorization(
            driver,
            wait,
            base_url,
            records,
            "Superuser",
            {"create", "update", "delete"},
        )

        # 5. Verify logout and cookie cleanup
        driver.get(f"{base_url}/logout/")
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/login/')]")))
        cookie_last_login = driver.get_cookie("last_login")
        assert cookie_last_login is None or cookie_last_login["value"] == ""
        print("[PASS] Logout and cookie cleanup verified")

        print("\nAll E2E tests passed successfully!")

    finally:
        driver.quit()
        for record in records.values():
            record.delete()


if __name__ == "__main__":
    main()