import json
import os
from datetime import datetime

class Contact:
    def __init__(self, name, phone, email="", address=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at
    
    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        contact = Contact(
            data['name'],
            data['phone'],
            data.get('email', ''),
            data.get('address', '')
        )
        contact.created_at = data.get('created_at', contact.created_at)
        contact.updated_at = data.get('updated_at', contact.updated_at)
        return contact
    
    def display_summary(self, index=None):
        """Display contact in list format"""
        prefix = f"{index}. " if index is not None else ""
        print(f"{prefix}{self.name:<30} | 📱 {self.phone:<15}")
    
    def display_details(self):
        """Display full contact details"""
        print("\n" + "="*60)
        print(f"👤 CONTACT DETAILS")
        print("="*60)
        print(f"Name:    {self.name}")
        print(f"Phone:   {self.phone}")
        print(f"Email:   {self.email if self.email else 'Not provided'}")
        print(f"Address: {self.address if self.address else 'Not provided'}")
        print(f"Created: {self.created_at}")
        print(f"Updated: {self.updated_at}")
        print("="*60)

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title):
    """Display a formatted header"""
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)

def load_contacts():
    """Load contacts from JSON file with error handling"""
    if not os.path.exists('contacts.json'):
        return []
    
    try:
        with open('contacts.json', 'r') as f:
            data = json.load(f)
            return [Contact.from_dict(item) for item in data]
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Warning: Could not load contacts. Starting fresh. Error: {e}")
        return []

def save_contacts(contacts):
    """Save contacts to JSON file with error handling"""
    try:
        with open('contacts.json', 'w') as f:
            json.dump([contact.to_dict() for contact in contacts], f, indent=4)
        return True
    except IOError as e:
        print(f"❌ Error: Could not save contacts. Error: {e}")
        return False

def validate_phone(phone):
    """Basic phone number validation"""
    # Remove common separators
    clean_phone = ''.join(filter(str.isdigit, phone))
    return len(clean_phone) >= 10

def validate_email(email):
    """Basic email validation"""
    if not email:  # Email is optional
        return True
    return '@' in email and '.' in email

def add_contact(contacts):
    clear_screen()
    display_header("➕ ADD NEW CONTACT")
    
    # Get and validate name
    while True:
        name = input("Enter name (required): ").strip()
        if name:
            # Check for duplicate names
            if any(c.name.lower() == name.lower() for c in contacts):
                print("⚠️ A contact with this name already exists!")
                choice = input("Do you want to continue anyway? (yes/no): ").lower()
                if choice not in ['yes', 'y']:
                    continue
            break
        else:
            print("❌ Name cannot be empty. Please try again.")
    
    # Get and validate phone
    while True:
        phone = input("Enter phone number (required): ").strip()
        if validate_phone(phone):
            break
        else:
            print("❌ Invalid phone number. Please enter at least 10 digits.")
    
    # Get optional fields
    email = input("Enter email (optional): ").strip()
    while email and not validate_email(email):
        print("❌ Invalid email format. Please enter a valid email or leave empty.")
        email = input("Enter email (optional): ").strip()
    
    address = input("Enter address (optional): ").strip()
    
    # Create and add contact
    new_contact = Contact(name, phone, email, address)
    contacts.append(new_contact)
    
    if save_contacts(contacts):
        print(f"\n✅ Contact '{name}' added successfully!")
        new_contact.display_details()
    else:
        print("❌ Failed to save contact.")
    
    input("\nPress Enter to continue...")

def display_contact_list(contacts):
    """Display contact list without asking for details"""
    if not contacts:
        print("No contacts found.")
        return []
    
    # Sort contacts alphabetically
    sorted_contacts = sorted(contacts, key=lambda x: x.name.lower())
    
    print(f"Total contacts: {len(contacts)}\n")
    print("INDEX | NAME                          | PHONE")
    print("-" * 60)
    
    for i, contact in enumerate(sorted_contacts, 1):
        print(f"{i:5} | {contact.name:<30} | {contact.phone}")
    
    return sorted_contacts

def view_contacts(contacts):
    clear_screen()
    display_header("📖 CONTACT LIST")
    
    if not contacts:
        print("No contacts found. Add some contacts first!")
        input("\nPress Enter to continue...")
        return
    
    sorted_contacts = display_contact_list(contacts)
    
    print("\n" + "-" * 60)
    choice = input("Enter contact number to view details (or 0 to go back): ").strip()
    
    if choice.isdigit():
        index = int(choice)
        if index == 0:
            return
        if 1 <= index <= len(sorted_contacts):
            clear_screen()
            sorted_contacts[index - 1].display_details()
            input("\nPress Enter to continue...")

def search_contact(contacts):
    clear_screen()
    display_header("🔍 SEARCH CONTACTS")
    
    if not contacts:
        print("No contacts available to search.")
        input("\nPress Enter to continue...")
        return
    
    print("Search by:")
    print("1. Name")
    print("2. Phone")
    print("3. Email")
    print("4. Back to Main Menu")
    
    search_type = input("\nChoose option (1-4): ").strip()
    
    if search_type == '4':
        return
    
    query = input("\nEnter search term: ").strip().lower()
    
    if search_type == '1':
        results = [c for c in contacts if query in c.name.lower()]
    elif search_type == '2':
        results = [c for c in contacts if query in c.phone]
    elif search_type == '3':
        results = [c for c in contacts if query in c.email.lower()]
    else:
        print("❌ Invalid option.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    display_header(f"🔍 SEARCH RESULTS ({len(results)} found)")
    
    if not results:
        print("No matching contacts found.")
    else:
        for i, contact in enumerate(results, 1):
            contact.display_summary(i)
        
        print("\n" + "-" * 60)
        choice = input("Enter contact number to view details (or 0 to go back): ").strip()
        
        if choice.isdigit():
            index = int(choice)
            if index == 0:
                return
            if 1 <= index <= len(results):
                clear_screen()
                results[index - 1].display_details()
    
    input("\nPress Enter to continue...")

def update_contact(contacts):
    clear_screen()
    display_header("✏️ UPDATE CONTACT")
    
    if not contacts:
        print("No contacts available to update.")
        input("\nPress Enter to continue...")
        return
    
    # Display contacts and get selection
    print("Select a contact to update:\n")
    sorted_contacts = display_contact_list(contacts)
    
    try:
        choice = input("\nEnter contact number to update (or 0 to cancel): ").strip()
        
        if not choice.isdigit():
            print("❌ Please enter a valid number.")
            input("\nPress Enter to continue...")
            return
            
        index = int(choice)
        
        if index == 0:  # User entered 0
            return
            
        if 1 <= index <= len(sorted_contacts):
            contact = sorted_contacts[index - 1]
            original_contacts_index = contacts.index(contact)
            
            clear_screen()
            display_header(f"✏️ UPDATE CONTACT: {contact.name}")
            contact.display_details()
            
            print("\nLeave field empty to keep current value.")
            print("-" * 40)
            
            # Get updated values
            new_name = input(f"\nNew name [{contact.name}]: ").strip()
            new_phone = input(f"New phone [{contact.phone}]: ").strip()
            new_email = input(f"New email [{contact.email}]: ").strip()
            new_address = input(f"New address [{contact.address}]: ").strip()
            
            # Validate phone if changed
            if new_phone and not validate_phone(new_phone):
                print("❌ Invalid phone number. Update cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Validate email if changed
            if new_email and not validate_email(new_email):
                print("❌ Invalid email format. Update cancelled.")
                input("\nPress Enter to continue...")
                return
            
            # Update only changed fields
            updates_made = False
            if new_name and new_name != contact.name:
                contact.name = new_name
                updates_made = True
            
            if new_phone and new_phone != contact.phone:
                contact.phone = new_phone
                updates_made = True
            
            if new_email != contact.email:
                contact.email = new_email
                updates_made = True
            
            if new_address != contact.address:
                contact.address = new_address
                updates_made = True
            
            if updates_made:
                contact.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Update the contact in the original list
                contacts[original_contacts_index] = contact
                if save_contacts(contacts):
                    print(f"\n✅ Contact updated successfully!")
                    contact.display_details()
                else:
                    print("❌ Failed to save changes.")
            else:
                print("\nℹ️ No changes made.")
        else:
            print("❌ Invalid contact number.")
    
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    
    input("\nPress Enter to continue...")

def delete_contact(contacts):
    clear_screen()
    display_header("🗑️ DELETE CONTACT")
    
    if not contacts:
        print("No contacts available to delete.")
        input("\nPress Enter to continue...")
        return
    
    # Display contacts and get selection
    print("Select a contact to delete:\n")
    sorted_contacts = display_contact_list(contacts)
    
    try:
        choice = input("\nEnter contact number to delete (or 0 to cancel): ").strip()
        
        if not choice.isdigit():
            print("❌ Please enter a valid number.")
            input("\nPress Enter to continue...")
            return
            
        index = int(choice)
        
        if index == 0:  # User entered 0
            return
            
        if 1 <= index <= len(sorted_contacts):
            contact = sorted_contacts[index - 1]
            original_contacts_index = contacts.index(contact)
            
            clear_screen()
            display_header(f"🗑️ DELETE CONTACT")
            contact.display_details()
            
            confirm = input(f"\n⚠️ Are you SURE you want to delete '{contact.name}'? (yes/no): ").strip().lower()
            
            if confirm in ['yes', 'y']:
                deleted_contact = contacts.pop(original_contacts_index)
                if save_contacts(contacts):
                    print(f"\n✅ Contact '{deleted_contact.name}' deleted successfully!")
                else:
                    print("❌ Failed to save changes. Contact not deleted.")
                    contacts.insert(original_contacts_index, deleted_contact)  # Restore contact
            else:
                print("❌ Deletion cancelled.")
        else:
            print("❌ Invalid contact number.")
    
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    
    input("\nPress Enter to continue...")

def display_statistics(contacts):
    clear_screen()
    display_header("📊 CONTACT BOOK STATISTICS")
    
    total = len(contacts)
    print(f"Total contacts: {total}")
    
    if total > 0:
        with_email = sum(1 for c in contacts if c.email)
        with_address = sum(1 for c in contacts if c.address)
        
        print(f"Contacts with email: {with_email} ({with_email/total*100:.1f}%)")
        print(f"Contacts with address: {with_address} ({with_address/total*100:.1f}%)")
        
        # Find most recent updates
        recent_contacts = sorted(contacts, key=lambda x: x.updated_at, reverse=True)[:3]
        print("\n🕒 Recently updated contacts:")
        for contact in recent_contacts:
            print(f"  • {contact.name} (updated: {contact.updated_at})")
    
    input("\nPress Enter to continue...")

def main():
    clear_screen()
    print("\n" + "🌟" * 30)
    print("       WELCOME TO CONTACT BOOK")
    print("🌟" * 30)
    
    contacts = load_contacts()
    print(f"📂 Loaded {len(contacts)} contacts from storage.\n")
    input("Press Enter to continue...")
    
    while True:
        clear_screen()
        print("\n" + "=" * 60)
        print("📒 MAIN MENU")
        print("=" * 60)
        print("1. ➕ Add Contact")
        print("2. 📖 View All Contacts")
        print("3. 🔍 Search Contact")
        print("4. ✏️ Update Contact")
        print("5. 🗑️ Delete Contact")
        print("6. 📊 View Statistics")
        print("7. 🚪 Exit")
        print("=" * 60)
        
        choice = input("\nChoose an option (1-7): ").strip()
        
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            view_contacts(contacts)
        elif choice == '3':
            search_contact(contacts)
        elif choice == '4':
            update_contact(contacts)
        elif choice == '5':
            delete_contact(contacts)
        elif choice == '6':
            display_statistics(contacts)
        elif choice == '7':
            clear_screen()
            print("\n" + "=" * 60)
            print("Thank you for using Contact Book!")
            print("All data has been saved to 'contacts.json'")
            print("=" * 60)
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-7.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n⚠️ An unexpected error occurred: {e}")
        print("Please report this issue.")