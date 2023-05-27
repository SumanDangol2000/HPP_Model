from bs4 import BeautifulSoup
import requests
import csv

# website = 'https://gharsansarnepal.com/buy-properties-in-nepal?page={}'
website = 'https://gharsansarnepal.com/category/home-for-sale-in-kathmandu/buy?page={}'

important_data = ["Posted On", "Pillar Size", "Tank Capacity", "Road Size", "Road Type", "Built On", "Land Area",
                  "House Area", "Beds", "Living", "Kitchen", "Bathrooms", "Property Face Direction", "Parking Space"]

file = open("data.csv", 'a')
data_writer = csv.writer(
    file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
data_writer.writerow(["Title", "Location", "Price",  "Posted On", "Pillar Size", "Tank Capacity", "Road Size", "Road Type", "Built On", "Land Area",
                      "House Area", "Beds", "Living", "Kitchen", "Bathrooms", "Property Face Direction", "Parking Space", "Amenities"])
file.close()

for page_number in range(1, 27):

    # create empty variable:
    _title = ""
    _location = ""
    _price = ""
    data_to_write = [""] * len(important_data)
    _amenities = []

    # generate Website variable
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

    # Links are now extracted.

    for link in links:
        print()
        print("-"*10)
        print("Opening Link..", link)
        print("-"*10)
        print()
        home_web_data = requests.get(link, headers=headers)
        home_data = BeautifulSoup(home_web_data.text, 'html.parser')

        _title = home_data.find('div', 'banner-title').text.strip()
        _location = home_data.find('div', 'overview-sub-title').text.strip()
        _price = home_data.find('div', 'banner-sub-title').text.strip()
        print(_title, " ", _location, " ", _price)

        detailed_information = home_data.find_all(
            'div', 'contact-list')[-1]
        details = detailed_information.find_all('a', href=True)
        # print(len(details))

        # title, location, price,  Posted On, Pillar Size, Tank Capacity, Road Type, Built On , Land Area ,
        # House Area, Beds, Living, Kitchen, Bathrooms, Property Face Direction, Parking Space, amenities

        # data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # data_writer.writerow([title, location, price])

        # List comprehension
        # details = [" ".join(detail.text.strip().split()) for detail in details]
        # print(details)
        data = {}

        for detail in details:
            detail = " ".join(detail.text.strip().split())
            detail_list = detail.split(":")
            data[detail_list[0].strip().title()] = detail_list[1].strip()

        for index, datum in enumerate(important_data):
            try:
                data_to_write[index] = data[datum]
            except:
                print("Key", datum, "does not exist!")
        # print(data)
        # print(data_to_write)

        amenities = home_data.find_all('div', 'amenities')
        amenities = amenities[0].text.strip().split("\n")
        amenities = [x.strip()
                     for x in amenities if x != 'Amenities' and x != '']
        # print(amenities)

        header_data = [_title, _location, _price]
        file = open("data.csv", 'a')
        data_writer = csv.writer(
            file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writable_data = header_data+data_to_write
        # print(type(writable_data))
        writable_data.append(amenities)
        # print(writable_data)

        # print(write_data)
        data_writer.writerow(writable_data)
        print("Wrote data successfully")
        print("-"*10)
        file.close()
