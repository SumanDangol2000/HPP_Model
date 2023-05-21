from bs4 import BeautifulSoup
import requests
import csv

#website = 'https://gharsansarnepal.com/buy-properties-in-nepal?page={}'
website = 'https://gharsansarnepal.com/category/home-for-sale-in-kathmandu/buy?page={}'

# for page_number in range(1, 2):
for page_number in range(1, 26):
    
    website_address = website.format(page_number)
    headers = {
        'User-Agent': 'insomnia/2023.1.0',
    }

    web_data = requests.get(website_address, headers=headers)
    soup = BeautifulSoup(web_data.text, 'html.parser')
    mydivs = soup.find_all("div", "explore-item-title")

    links = []

    for div in mydivs:
        anchor = div.find_all('a', href=True)
        links.append(anchor[0]['href'])

    # #Links are now extracted.
    # file = open("data.csv", 'a')
    # data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # data_writer.writerow(["Title", "Location", "Price",  "Posted On", "Pillar Size", "Tank Capacity", "Road Type", "Built On" , "Land Area" ,
    #                       "House Area", "Beds", "Living", "Kitchen", "Bathrooms", "Property Face Direction", "Parking Space", "Amenities"])
    for link in links:
        print()
        print("-"*10)
        print("Opening Link..", link)
        print("-"*5)
        print()
        home_web_data = requests.get(link, headers=headers)
        home_data = BeautifulSoup(home_web_data.text, 'html.parser')

        title = home_data.find('div', 'banner-title').text.strip()
        location = home_data.find('div', 'overview-sub-title').text.strip()
        price = home_data.find('div', 'banner-sub-title').text.strip()
        print(title, " ", location, " ", price)
        detailed_information = home_data.find_all(
            'div', 'contact-list')[-1]
        details = detailed_information.find_all('a', href=True)
        detail_list = []
        
        # title, location, price,  Posted On, Pillar Size, Tank Capacity, Road Type, Built On , Land Area ,
        # House Area, Beds, Living, Kitchen, Bathrooms, Property Face Direction, Parking Space, amenities 
        
        

        #data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # data_writer.writerow([title, location, price])
        for detail in details:
                i=1
                while i <= len(details):
                    print(' '.join(detail.text.strip().split()[i]))

                    # pass
        
        amenities = home_data.find_all('div', 'amenities')
        #print(amenities)
        print(' '.join(amenities[0].text.strip().split()[1:]))

        # data_writer.writerow([title, location, price,  Posted On, Pillar Size, Tank Capacity, Road Type, Built On , Land Area ,
        # House Area, Beds, Living, Kitchen, Bathrooms, Property Face Direction, Parking Space, amenities ])
        