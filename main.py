import json

import os

import hashlib

import secrets

from datetime import datetime

from getpass import getpass

class PersonalDiary:

    def __init__(self):

        self.data_file = "personal_diary_data.json"

        self.backup_folder = "diary_backups"

        self.data = {

            "users": {},

            "entries": []

        }

        self.current_user = None

        self.load_data()

    def load_data(self):

        try:

            if os.path.exists(self.data_file):

                with open(self.data_file, "r", encoding="utf-8") as file:

                    self.data = json.load(file)

                if "users" not in self.data:

                    self.data["users"] = {}

                if "entries" not in self.data:

                    self.data["entries"] = []

        except (json.JSONDecodeError, OSError):

            self.data = {

                "users": {},

                "entries": []

            }

    def save_data(self):

        try:

            temporary_file = self.data_file + ".tmp"

            with open(temporary_file, "w", encoding="utf-8") as file:

                json.dump(self.data, file, indent=4, ensure_ascii=False)

            os.replace(temporary_file, self.data_file)

            return True

        except OSError:

            return False

    def hash_password(self, password, salt=None):

        if salt is None:

            salt = secrets.token_hex(16)

        password_hash = hashlib.pbkdf2_hmac(

            "sha256",

            password.encode("utf-8"),

            salt.encode("utf-8"),

            100000

        ).hex()

        return salt, password_hash

    def verify_password(self, password, salt, stored_hash):

        _, password_hash = self.hash_password(password, salt)

        return secrets.compare_digest(password_hash, stored_hash)

    def clear_screen(self):

        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):

        input("\nPress Enter to continue...")

    def line(self, character="=", length=75):

        print(character * length)

    def header(self, title):

        self.clear_screen()

        self.line()

        print(title.center(75))

        self.line()

    def validate_username(self, username):

        if not username:

            return False

        if len(username) < 3:

            return False

        if " " in username:

            return False

        return True

    def register(self):

        self.header("PERSONAL DIARY - CREATE ACCOUNT")

        username = input("Enter username: ").strip().lower()

        if not self.validate_username(username):

            print("\nUsername must contain at least 3 characters and no spaces.")

            self.pause()

            return

        if username in self.data["users"]:

            print("\nUsername already exists.")

            self.pause()

            return

        password = getpass("Enter password: ")

        confirm_password = getpass("Confirm password: ")

        if len(password) < 6:

            print("\nPassword must contain at least 6 characters.")

            self.pause()

            return

        if password != confirm_password:

            print("\nPasswords do not match.")

            self.pause()

            return

        salt, password_hash = self.hash_password(password)

        self.data["users"][username] = {

            "salt": salt,

            "password_hash": password_hash,

            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        }

        if self.save_data():

            print("\nAccount created successfully.")

        else:

            print("\nUnable to save account.")

        self.pause()

    def login(self):

        self.header("PERSONAL DIARY - LOGIN")

        username = input("Username: ").strip().lower()

        password = getpass("Password: ")

        user = self.data["users"].get(username)

        if user is None:

            print("\nInvalid username or password.")

            self.pause()

            return False

        if not self.verify_password(

            password,

            user["salt"],

            user["password_hash"]

        ):

            print("\nInvalid username or password.")

            self.pause()

            return False

        self.current_user = username

        print("\nLogin successful.")

        self.pause()

        return True

    def generate_entry_id(self):

        existing_ids = []

        for entry in self.data["entries"]:

            try:

                existing_ids.append(int(entry["id"]))

            except (ValueError, KeyError):

                pass

        if not existing_ids:

            return 1

        return max(existing_ids) + 1

    def get_user_entries(self):

        return [

            entry for entry in self.data["entries"]

            if entry.get("username") == self.current_user

        ]

    def get_entry_by_id(self, entry_id):

        for entry in self.data["entries"]:

            if (

                entry.get("username") == self.current_user

                and str(entry.get("id")) == str(entry_id)

            ):

                return entry

        return None

    def add_entry(self):

        self.header("ADD NEW DIARY ENTRY")

        title = input("Title: ").strip()

        if not title:

            print("\nTitle cannot be empty.")

            self.pause()

            return

        print("\nWrite your diary entry.")

        print("Type END on a separate line when finished.\n")

        content_lines = []

        while True:

            line = input()

            if line == "END":

                break

            content_lines.append(line)

        content = "\n".join(content_lines).strip()

        if not content:

            print("\nDiary content cannot be empty.")

            self.pause()

            return

        print("\nAvailable moods:")

        print("1. Happy")

        print("2. Excited")

        print("3. Calm")

        print("4. Sad")

        print("5. Angry")

        print("6. Stressed")

        print("7. Neutral")

        mood_choice = input("\nSelect mood: ").strip()

        moods = {

            "1": "Happy",

            "2": "Excited",

            "3": "Calm",

            "4": "Sad",

            "5": "Angry",

            "6": "Stressed",

            "7": "Neutral"

        }

        mood = moods.get(mood_choice, "Neutral")

        tag_input = input(

            "\nEnter tags separated by commas: "

        ).strip()

        tags = []

        if tag_input:

            tags = [

                tag.strip().lower()

                for tag in tag_input.split(",")

                if tag.strip()

            ]

        now = datetime.now()

        entry = {

            "id": self.generate_entry_id(),

            "username": self.current_user,

            "title": title,

            "content": content,

            "mood": mood,

            "tags": tags,

            "favorite": False,

            "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),

            "updated_at": now.strftime("%Y-%m-%d %H:%M:%S")

        }

        self.data["entries"].append(entry)

        if self.save_data():

            print("\nDiary entry saved successfully.")

        else:

            print("\nUnable to save diary entry.")

        self.pause()

    def display_entry(self, entry):

        self.line("-")

        print(f"Entry ID     : {entry['id']}")

        print(f"Title        : {entry['title']}")

        print(f"Date Created : {entry['created_at']}")

        print(f"Last Updated : {entry['updated_at']}")

        print(f"Mood         : {entry['mood']}")

        tags = ", ".join(entry.get("tags", []))

        print(f"Tags         : {tags if tags else 'None'}")

        print(

            f"Favorite     : "

            f"{'Yes' if entry.get('favorite', False) else 'No'}"

        )

        print("\nContent:")

        print(entry["content"])

        self.line("-")

    def view_all_entries(self):

        self.header("MY DIARY ENTRIES")

        entries = self.get_user_entries()

        if not entries:

            print("No diary entries found.")

            self.pause()

            return

        entries.sort(

            key=lambda x: x.get("created_at", ""),

            reverse=True

        )

        for entry in entries:

            print(

                f"\nID: {entry['id']} | "

                f"{entry['title']} | "

                f"{entry['created_at']} | "

                f"Mood: {entry['mood']}"

            )

        print("\nEnter an Entry ID to read it.")

        print("Enter 0 to return.")

        choice = input("\nEntry ID: ").strip()

        if choice == "0":

            return

        entry = self.get_entry_by_id(choice)

        if entry is None:

            print("\nEntry not found.")

        else:

            self.header("DIARY ENTRY")

            self.display_entry(entry)

        self.pause()

    def edit_entry(self):

        self.header("EDIT DIARY ENTRY")

        entries = self.get_user_entries()

        if not entries:

            print("No diary entries available.")

            self.pause()

            return

        for entry in entries:

            print(

                f"{entry['id']}. "

                f"{entry['title']} "

                f"({entry['created_at']})"

            )

        entry_id = input("\nEnter Entry ID: ").strip()

        entry = self.get_entry_by_id(entry_id)

        if entry is None:

            print("\nEntry not found.")

            self.pause()

            return

        self.header("EDIT ENTRY")

        print(f"Current Title: {entry['title']}")

        new_title = input(

            "New title (press Enter to keep current): "

        ).strip()

        if new_title:

            entry["title"] = new_title

        print("\nCurrent content:")

        print(entry["content"])

        choice = input(

            "\nDo you want to replace the content? (y/n): "

        ).strip().lower()

        if choice == "y":

            print("\nEnter new content.")

            print("Type END on a separate line when finished.\n")

            content_lines = []

            while True:

                line = input()

                if line == "END":

                    break

                content_lines.append(line)

            new_content = "\n".join(content_lines).strip()

            if new_content:

                entry["content"] = new_content

        print(f"\nCurrent mood: {entry['mood']}")

        change_mood = input(

            "Change mood? (y/n): "

        ).strip().lower()

        if change_mood == "y":

            moods = {

                "1": "Happy",

                "2": "Excited",

                "3": "Calm",

                "4": "Sad",

                "5": "Angry",

                "6": "Stressed",

                "7": "Neutral"

            }

            print("\n1. Happy")

            print("2. Excited")

            print("3. Calm")

            print("4. Sad")

            print("5. Angry")

            print("6. Stressed")

            print("7. Neutral")

            mood_choice = input("Select mood: ").strip()

            if mood_choice in moods:

                entry["mood"] = moods[mood_choice]

        print(

            f"\nCurrent tags: "

            f"{', '.join(entry.get('tags', []))}"

        )

        change_tags = input(

            "Change tags? (y/n): "

        ).strip().lower()

        if change_tags == "y":

            tag_input = input(

                "Enter tags separated by commas: "

            ).strip()

            entry["tags"] = [

                tag.strip().lower()

                for tag in tag_input.split(",")

                if tag.strip()

            ]

        entry["updated_at"] = datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )

        if self.save_data():

            print("\nEntry updated successfully.")

        else:

            print("\nUnable to update entry.")

        self.pause()

    def delete_entry(self):

        self.header("DELETE DIARY ENTRY")

        entries = self.get_user_entries()

        if not entries:

            print("No diary entries available.")

            self.pause()

            return

        for entry in entries:

            print(

                f"{entry['id']}. "

                f"{entry['title']} "

                f"({entry['created_at']})"

            )

        entry_id = input("\nEnter Entry ID to delete: ").strip()

        entry = self.get_entry_by_id(entry_id)

        if entry is None:

            print("\nEntry not found.")

            self.pause()

            return

        print("\nSelected entry:")

        print(f"Title: {entry['title']}")

        confirmation = input(

            "\nAre you sure you want to delete it? (y/n): "

        ).strip().lower()

        if confirmation != "y":

            print("\nDeletion cancelled.")

            self.pause()

            return

        self.data["entries"].remove(entry)

        if self.save_data():

            print("\nEntry deleted successfully.")

        else:

            print("\nUnable to delete entry.")

        self.pause()

    def search_entries(self):

        self.header("SEARCH DIARY")

        keyword = input(

            "Enter keyword, title, content or tag: "

        ).strip().lower()

        if not keyword:

            print("\nSearch keyword cannot be empty.")

            self.pause()

            return

        results = []

        for entry in self.get_user_entries():

            title = entry.get("title", "").lower()

            content = entry.get("content", "").lower()

            mood = entry.get("mood", "").lower()

            tags = " ".join(entry.get("tags", [])).lower()

            if (

                keyword in title

                or keyword in content

                or keyword in mood

                or keyword in tags

            ):

                results.append(entry)

        self.header("SEARCH RESULTS")

        if not results:

            print("No matching entries found.")

        else:

            print(f"Found {len(results)} matching entries.\n")

            for entry in results:

                print(

                    f"ID: {entry['id']} | "

                    f"Title: {entry['title']} | "

                    f"Mood: {entry['mood']} | "

                    f"Date: {entry['created_at']}"

                )

        self.pause()

    def search_by_mood(self):

        self.header("SEARCH BY MOOD")

        mood = input(

            "Enter mood: "

        ).strip().lower()

        results = [

            entry

            for entry in self.get_user_entries()

            if entry.get("mood", "").lower() == mood

        ]

        if not results:

            print("\nNo entries found for this mood.")

        else:

            print(

                f"\nFound {len(results)} entries with mood "

                f"'{mood.title()}'.\n"

            )

            for entry in results:

                print(

                    f"ID: {entry['id']} | "

                    f"{entry['title']} | "

                    f"{entry['created_at']}"

                )

        self.pause()

    def search_by_date(self):

        self.header("SEARCH BY DATE")

        date_text = input(

            "Enter date in YYYY-MM-DD format: "

        ).strip()

        try:

            datetime.strptime(date_text, "%Y-%m-%d")

        except ValueError:

            print("\nInvalid date format.")

            self.pause()

            return

        results = [

            entry

            for entry in self.get_user_entries()

            if entry.get("created_at", "").startswith(date_text)

        ]

        if not results:

            print("\nNo entries found on this date.")

        else:

            print(f"\nEntries for {date_text}:\n")

            for entry in results:

                print(

                    f"ID: {entry['id']} | "

                    f"{entry['title']} | "

                    f"Mood: {entry['mood']}"

                )

        self.pause()

    def toggle_favorite(self):

        self.header("FAVORITE DIARY ENTRY")

        entries = self.get_user_entries()

        if not entries:

            print("No diary entries available.")

            self.pause()

            return

        for entry in entries:

            status = "★" if entry.get("favorite", False) else " "

            print(

                f"{entry['id']}. [{status}] {entry['title']}"

            )

        entry_id = input("\nEnter Entry ID: ").strip()

        entry = self.get_entry_by_id(entry_id)

        if entry is None:

            print("\nEntry not found.")

            self.pause()

            return

        entry["favorite"] = not entry.get("favorite", False)

        if self.save_data():

            if entry["favorite"]:

                print("\nEntry added to favorites.")

            else:

                print("\nEntry removed from favorites.")

        else:

            print("\nUnable to save changes.")

        self.pause()

    def view_favorites(self):

        self.header("FAVORITE ENTRIES")

        favorites = [

            entry

            for entry in self.get_user_entries()

            if entry.get("favorite", False)

        ]

        if not favorites:

            print("No favorite entries found.")

            self.pause()

            return

        for entry in favorites:

            print(

                f"ID: {entry['id']} | "

                f"{entry['title']} | "

                f"{entry['created_at']} | "

                f"Mood: {entry['mood']}"

            )

        self.pause()

    def statistics(self):

        self.header("DIARY STATISTICS")

        entries = self.get_user_entries()

        if not entries:

            print("No entries available for statistics.")

            self.pause()

            return

        total_entries = len(entries)

        favorite_entries = sum(

            1

            for entry in entries

            if entry.get("favorite", False)

        )

        mood_count = {}

        for entry in entries:

            mood = entry.get("mood", "Neutral")

            mood_count[mood] = mood_count.get(mood, 0) + 1

        tag_count = {}

        for entry in entries:

            for tag in entry.get("tags", []):

                tag_count[tag] = tag_count.get(tag, 0) + 1

        total_words = 0

        for entry in entries:

            total_words += len(

                entry.get("content", "").split()

            )

        average_words = total_words / total_entries

        print(f"Total diary entries : {total_entries}")

        print(f"Favorite entries    : {favorite_entries}")

        print(f"Total words         : {total_words}")

        print(f"Average words       : {average_words:.2f}")

        print("\nMood Statistics")

        for mood, count in sorted(

            mood_count.items(),

            key=lambda x: x[1],

            reverse=True

        ):

            percentage = (count / total_entries) * 100

            print(

                f"{mood:<12} : "

                f"{count:<5} "

                f"({percentage:.2f}%)"

            )

        print("\nMost Used Tags")

        if tag_count:

            sorted_tags = sorted(

                tag_count.items(),

                key=lambda x: x[1],

                reverse=True

            )

            for tag, count in sorted_tags[:10]:

                print(f"{tag:<20} : {count}")

        else:

            print("No tags available.")

        self.pause()

    def backup_data(self):

        self.header("BACKUP DIARY DATA")

        try:

            os.makedirs(self.backup_folder, exist_ok=True)

            timestamp = datetime.now().strftime(

                "%Y%m%d_%H%M%S"

            )

            backup_file = os.path.join(

                self.backup_folder,

                f"diary_backup_{timestamp}.json"

            )

            with open(

                backup_file,

                "w",

                encoding="utf-8"

            ) as file:

                json.dump(

                    self.data,

                    file,

                    indent=4,

                    ensure_ascii=False

                )

            print("\nBackup created successfully.")

            print(f"Backup file: {backup_file}")

        except OSError:

            print("\nUnable to create backup.")

        self.pause()

    def export_user_diary(self):

        self.header("EXPORT DIARY")

        entries = self.get_user_entries()

        if not entries:

            print("No diary entries available.")

            self.pause()

            return

        filename = input(

            "Enter export filename: "

        ).strip()

        if not filename:

            filename = "my_diary.txt"

        if not filename.lower().endswith(".txt"):

            filename += ".txt"

        try:

            with open(

                filename,

                "w",

                encoding="utf-8"

            ) as file:

                file.write(

                    "PERSONAL DIARY\n"

                )

                file.write(

                    "=" * 70 + "\n\n"

                )

                for entry in sorted(

                    entries,

                    key=lambda x: x.get("created_at", ""),

                    reverse=True

                ):

                    file.write(

                        f"Entry ID: {entry['id']}\n"

                    )

                    file.write(

                        f"Title: {entry['title']}\n"

                    )

                    file.write(

                        f"Date: {entry['created_at']}\n"

                    )

                    file.write(

                        f"Mood: {entry['mood']}\n"

                    )

                    file.write(

                        f"Tags: "

                        f"{', '.join(entry.get('tags', []))}\n"

                    )

                    file.write(

                        "\nContent:\n"

                    )

                    file.write(

                        entry["content"]

                    )

                    file.write(

                        "\n\n" + "-" * 70 + "\n\n"

                    )

            print(

                f"\nDiary exported successfully to {filename}"

            )

        except OSError:

            print("\nUnable to export diary.")

        self.pause()

    def profile(self):

        self.header("MY PROFILE")

        user = self.data["users"].get(

            self.current_user

        )

        entries = self.get_user_entries()

        print(f"Username       : {self.current_user}")

        print(

            f"Account Created: "

            f"{user.get('created_at', 'Unknown')}"

        )

        print(

            f"Total Entries  : "

            f"{len(entries)}"

        )

        self.pause()

    def diary_menu(self):

        while self.current_user is not None:

            self.header(

                f"PERSONAL DIARY | "

                f"Welcome {self.current_user}"

            )

            print("1. Add New Diary Entry")

            print("2. View Diary Entries")

            print("3. Edit Diary Entry")

            print("4. Delete Diary Entry")

            print("5. Search Diary")

            print("6. Search by Mood")

            print("7. Search by Date")

            print("8. Add/Remove Favorite")

            print("9. View Favorite Entries")

            print("10. Diary Statistics")

            print("11. Backup Diary Data")

            print("12. Export Diary")

            print("13. My Profile")

            print("14. Logout")

            print("15. Exit")

            choice = input(

                "\nEnter your choice: "

            ).strip()

            if choice == "1":

                self.add_entry()

            elif choice == "2":

                self.view_all_entries()

            elif choice == "3":

                self.edit_entry()

            elif choice == "4":

                self.delete_entry()

            elif choice == "5":

                self.search_entries()

            elif choice == "6":

                self.search_by_mood()

            elif choice == "7":

                self.search_by_date()

            elif choice == "8":

                self.toggle_favorite()

            elif choice == "9":

                self.view_favorites()

            elif choice == "10":

                self.statistics()

            elif choice == "11":

                self.backup_data()

            elif choice == "12":

                self.export_user_diary()

            elif choice == "13":

                self.profile()

            elif choice == "14":

                self.current_user = None

                print("\nLogged out successfully.")

                self.pause()

            elif choice == "15":

                self.current_user = None

                return False

            else:

                print("\nInvalid choice.")

                self.pause()

        return True

    def main_menu(self):

        while True:

            self.header("PERSONAL DIARY MANAGEMENT SYSTEM")

            print("1. Create Account")

            print("2. Login")

            print("3. Exit")

            choice = input(

                "\nEnter your choice: "

            ).strip()

            if choice == "1":

                self.register()

            elif choice == "2":

                if self.login():

                    continue_program = self.diary_menu()

                    if not continue_program:

                        break

            elif choice == "3":

                print("\nThank you for using Personal Diary.")

                break

            else:

                print("\nInvalid choice.")

                self.pause()

def main():

    application = PersonalDiary()

    application.main_menu()

if __name__ == "__main__":

    main()