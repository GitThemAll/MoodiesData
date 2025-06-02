import os
import requests
import csv
from dotenv import load_dotenv

class KlaviyoClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("klaviyo_api_key")
        self.base_url = "https://a.klaviyo.com/api/profiles/"
        self.headers = {
            "Authorization": f"Klaviyo-API-Key {self.api_key}",
            "Accept": "application/json",
            "revision": "2023-10-15"
        }

    def fetch_all_profiles(self):
        """Fetch all Klaviyo profiles with pagination."""
        all_profiles = []
        params = {
            "page[size]": 100  # max per page
        }
        url = self.base_url

        while url:
            print(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_profiles.extend(data.get("data", []))

            # Handle pagination
            url = data.get("links", {}).get("next", None)
            params = None  # Next link contains all needed

        return all_profiles

    def save_profiles_to_csv(self, profiles, filename="klaviyo_customers.csv"):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                'Email', 'Email Marketing Consent',
                'First Active', 'Last Active', 'Profile Created On', 'Date Added',
                'Last Open', 'Last Click',
                'Initial Source', 'Last Source',
                'Historic Customer Lifetime Value', 'Accepts Marketing', 'Last Purchase Date'
            ])

            for profile in profiles:
                attr = profile.get("attributes", {})
                writer.writerow([
                    attr.get("email"),
                    attr.get("email_marketing_consent", {}).get("consent"),
                    attr.get("first_active"),
                    attr.get("last_active"),
                    attr.get("created"),
                    attr.get("updated"),
                    attr.get("last_open"),
                    attr.get("last_click"),
                    attr.get("initial_source"),
                    attr.get("last_source"),
                    attr.get("historic_customer_lifetime_value"),
                    attr.get("accepts_marketing"),
                    attr.get("last_purchase_date")
                ])

        print(f"✅ Saved {len(profiles)} profiles to {filename}")