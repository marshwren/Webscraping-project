from playwright.sync_api import sync_playwright
import pandas as pd
import subprocess
import time
subprocess.run(["playwright", "install"])
def scrape_chamber(limit=2000):
    data = []
    profilecount = 0
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context()
        page=context.new_page()

        #going to directory website
        page.goto("https://www.northshorechamber.org/members/")

        #getting a count of all categories
        category_count=len(
            page.query_selector_all("body > div.wrapper > main > section:nth-child(2) > div.container > section.member-cats > div > div")
        )
        print(f"total categories: {category_count}")

        for index in range(1, category_count + 1):
            print(f"processing category {index}/{category_count}")
            categoryselector=f"body > div.wrapper > main > section:nth-child(2) > div.container > section.member-cats > div > div:nth-child({index}) > a"
            categorytile=page.query_selector(categoryselector)
            categorytile.click()

            #waiting for page to load
            page.wait_for_selector("body > div.wrapper > main > section.mt-60.mb-100 > div.container")

            #get all business tiles
            businesses=page.query_selector_all("body > div.wrapper > main > section.mt-60.mb-100 > div.container > div > div")
            for biz_index, business in enumerate(businesses, start=1):
                if profilecount >= limit:
                    print(f"scraped {profilecount} profiles, test complete")
                    browser.close()
                    save_data(data)
                    return

                print(f"processing business {biz_index}/{len(businesses)} in category {index}")
                businesscss = f"body > div.wrapper > main > section.mt-60.mb-100 > div.container > div > div:nth-child({biz_index})"
                business_tile = page.query_selector(businesscss)
                business_tile.click()
                #waiting for profile to load
                #page.wait_for_selector("body > div.wrapper > main > section > div")
                page.wait_for_load_state("load")

                #css selectors
                name= page.query_selector("div.member-contact-info.mb-40 > p:nth-child(1)")
                address= page.query_selector("div.member-contact-info.mb-40 > p:nth-child(2)")
                phone= page.query_selector("div.member-contact-info.mb-40 > p:nth-child(3)")
                website= page.query_selector("div.member-contact-info.mb-40 > p:nth-child(4) > a")
                email= page.query_selector("div.member-contact-info.mb-40 > div > a")

                #cleaning the extracted info
                name1 = name.inner_text().replace("Contact Name: ", "").strip() if name else None
                address1 = address.inner_text().replace("Address: ", "").strip() if address else None
                phone1 = phone.inner_text().replace("Phone: ", "").strip() if phone else None
                website1 = website.get_attribute("href") if website else None
                email1 = email.get_attribute("href").replace("mailto:", "").strip() if email else None
                #print(f"extracted {name1}, {email1}")

                #parse the name into components
                name_parts = parse_name(name1)
                #add data to list
                data.append({
                    "Full Name": name1,
                    **name_parts,
                    "Email": email1,
                    "Phone": phone1,
                    "Website": website1,
                    "Address": address1})
                profilecount += 1
                #back to business catalog
                page.go_back()
                page.wait_for_selector("body > div.wrapper > main > section.mt-60.mb-100 > div.container > div > div")
            #back to category catalog
            page.go_back()
            page.wait_for_selector(
                "body > div.wrapper > main > section:nth-child(2) > div.container > section.member-cats > div > div")

        #close browser
        browser.close()
        save_data(data)
        print(f"scraping complete, total profiles scraped: {profilecount}")
def parse_name(full_name):
    if not full_name:
        return {"First Name": None, "Middle Initial": None, "Last Name": None, "Title": None}

    #splitting the names
    name_parts=full_name.split()
    first_name=name_parts[0]
    last_name=name_parts[-1]
    middle=None
    title=None
    #check for suffix
    if last_name.lower() in {"jr.", "sr.", "iii", "ii", "cpa", "md", "esq", "cmp", "dmd"}:
        title=last_name
        last_name=name_parts[-2] if len(name_parts) > 1 else None
    #checking for middle
    if len(name_parts) > 2 and len(name_parts[1]) in (1, 2) and name_parts[1][0].isalpha():
        middle=name_parts[1]
    return {
        "First": first_name,
        "Last": last_name,
        "Middle": middle,
        "Title": title}
def save_data(data):
    df=pd.DataFrame(data)
    csvfile="C:/Users/---/---/---.csv"
    df.to_csv(csvfile, index=False)
    print(f"Data saved to csv file.")
start_time=time.time()
scrape_chamber(limit=2000)
end_time=time.time()
elapsed_time=end_time-start_time
minutes=int(elapsed_time // 60)
seconds=int(elapsed_time % 60)
print(f"scraping completed in {minutes} minutes and {seconds} seconds")