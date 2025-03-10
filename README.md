# Web scraping project
This is a project I created during my internship. As a business development manager, I need to be on the lookout for new leads, new relationships that I can build with potential sponsors and donors. These leads can either be sourced based on principle (such as building relationships through the 1% For The Planet network) or based on location (connecting with new people in the locale of the organization's headquarters). A local Chamber of Commerce directory is a great resource for the latter. This is one of the web-scraping projects I created, targeting the North Shore of Massachusetts. The contacts and names discovered were arranged into a csv file. Here is the link to the member directory that I scraped: "https://www.northshorechamber.org/members/". I then cleaned and formatted the resulting data to prepare the file for assignemnts that I tasked my interns with. I will now explain my process for building the code step-by-step.

1.) **Importing Libraries**: I imported Playwright, Pandas, Subprocess, and Time, all are self explanatory except Subprocess. I had to use that to run Playwright because even though I had playwright installed, I got an error message courtesy of the playwright team stating that I might have installed it too recently for it to properly run. 

2.) **Defining the 'scrape_chamber' function**: This is the bulk of the project, I will go over each step of this function. I start with defining it obviously, and I put a limit argument for testing purposes, following that, I create an empty list named 'data'. For testing, I create a variable named 'profilecount' which is assigned a value of 0 (to begin with).

3.) **Playwright and directory website**: Next, I launch playwright, then create an isolated browsing session to avoid data contamination. The session then navigates to the chamber of commerce members page. The browser is run in headless mode.

4.) **Accessing the business category list**: A length function is assigned to the 'category_count' variable that contains a "page.query_selector_all" command which looks for all instances of the specificed css selector that corresponds to all the category tiles. This figure will be used in print statements for tracking progress when I run the code, example: "print(f"total categories: {category_count}"). A for loop then runs " for index in range(1, category_count + 1): " that iterates over each category of businesses. As a new category is being scraped, a print statement is called to update progress, " print(f"processing category {index}/{category_count}") ".

5.) **Accessing the business list**: A css selector for each individual category tile is isolated ("body > div.wrapper > main > section:nth-child(2) > div.container > section.member-cats > div > div:nth-child({index}) > a"), note the 'index' variable that allows every category tile to be accessed. After accessing a category with a '.click()' command, a "page.wait_for_selector("body > div.wrapper > main > section.mt-60.mb-100 > div.container") " is called to wait for the list of all business tiles to fully load. Then these businesses tiles are counted and iterated over by calling a "page.query_selector_all" function and the for loop : "for biz_index, business in enumerate(businesses, start=1):". 'biz_index' and 'businesses' variables are used in print statements for the sake of clarity in the same way for the category tiles, "print(f"processing business {biz_index}/{len(businesses)} in category {index}")". An if statement "if profilecount >= limit:", will print a message, close the browser, save data, and exit the function once the specified limit is reached.

6.) **Accessing and scraping each profile**: Similar to the category list, a dynamic indexed selector (using biz_index) helps iterate over each business tile. The tile is clicked and then waits for the business profile page to fully load with " page.wait_for_selector("body > div.wrapper > main > section > div") ". Then css selectors for all relevant information is isolated and assigned to appropriately named variables, such as 'name' and 'email'. Extracted text value are cleaned with the .split() function, for example "name1 = name.inner_text().replace("Contact Name: ", "").strip() if name else None".

7.) **Refining names and appending to 'data' list**: A parse_name() function is passed to break up 'name1' into first, middle, and last names that will be sorted into their respective columns in the resulting excel file. "data.append({" stores a dictionary in the list 'data' for each loop cycle, the dictionary includes the previously mentioned data points (names, email, website, phone). After this, the 'profilecount' is incremented by 1. I will go more in depth about the 'parse_name(full_name)' function in the next step.

8.) **'parse_name(full_name)' function**: This function splits the full name text into first, last, middle name, and title. A .split() functions puts all these individual parts into a list assigned to 'name_parts'. 'first_name' is assigned 'name_parts[0], while the 'last_name' is assigned 'name_parts[-1]' (the last element). The title and middle name is initialized as 'none' because it is not a common occurence. If any of the specified titles in the set match, the 2nd to last element of the list becomes the last name, but if there is only one element in the list, then there is no last name "else None". an if statement accounts for middle initital conditions that have a period by "len(name_parts[1]) in (1, 2) and name_parts[1][0].isalpha()", which ensures it is a middle initial, and that the first character is a letter. The if statement is concluded with a return command that returns a dictionary with the extracted name parts: first, last, middle, title.

8.) **Returning to the category list**: using the 'page.go_back()' function, once all business profiles are scraped, the browser returns to the category list page to access the next category. Once it is done with all categories, the browser is closed and 'data' is saved to a csv, more on this in the next step.

9.) **Saving the data and time statements**: I want to save this data in an excel or csv in a specific destination on my computer, but first, I call the function "def save_data(data):", to save the data to a csv file, I then convert 'data' into a dataframe with "df = pd.DataFrame(data)". I then assign the specific filepath to a variable I called 'csvfile', from which I then convert the dataframe to a csv with "df.to_csv(csvfile, index=False)". For the sake of clarity, I track the time. I call the primary function 'scrape_chamber', in between the start time and end time statements. Finally an elapsed time statement is added, and a minutes and seconds variable for an easier reading of the print statement that reports the elapsed time.

Thank you for reading.
