from bs4 import BeautifulSoup
import os
import re
import shutil

not_allowed_photo_types = ["pory", "siedlisko", "wysyp zarodników",
                     "blue boxes - individual measurements, green star - average"]
not_allowed_file_substrings = ["znalezisko", "mikro", "root"]
relative_path_to_data = ".././MyGrzybiarzeData/AnalyseMushroomDataset/"

def find_mushroom_photo_types(array_of_file_paths):
    num_of_type_count = 10
    map_of_repeated_types = {}
    map_of_all_types = {}
    for file_path in array_of_file_paths:
        with open(file_path, 'rb') as f:
            contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        td = soup.find("td", {"class": "foto-podpis-duzy"})
        if td:
            if td.text[0].isalpha():  # isaplha jest na wypadek dat zamiast opisu
                mush_type = td.text.split(';')[0]
                if mush_type in map_of_all_types.keys():
                    map_of_all_types[mush_type] += 1
                    if map_of_all_types[mush_type] > num_of_type_count:
                        map_of_repeated_types[mush_type] = file_path
                else:
                    map_of_all_types[mush_type] = 1
    return map_of_repeated_types


def store_all_mushroom_files():
    array_of_file_paths = []
    path_directory = relative_path_to_data + "grzyby/htm/"
    for foldername in os.listdir(path_directory):
        path_directory_mushrooms = os.path.join(path_directory, foldername)
        if os.path.isdir(path_directory_mushrooms):
            for filename in os.listdir(path_directory_mushrooms):
                is_not_allowed_filename = any(
                    ext in filename for ext in not_allowed_file_substrings)
                if filename[-4:] == ".htm" and not is_not_allowed_filename:
                    path_file_mushroom = os.path.join(
                        path_directory_mushrooms, filename)
                    array_of_file_paths.append(path_file_mushroom)
    return array_of_file_paths


def copy_photos(array_of_file_paths):
    for path_to_file in array_of_file_paths:
        with open(path_to_file, 'rb') as f:
            contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        copy_species_photo(soup)
        copy_edibility_photo(soup)

def copy_edibility_photo(soup):
    species_base_path = relative_path_to_data + "./chosen_data/edibility/"

    path_relative_species = soup.find(
        "div", {"class": "foto2-tytul"}).a.get("href")[14:]
    path_to_species = relative_path_to_data + "grzyby/gatunki/" + path_relative_species
    is_edible = check_edibility(path_to_species)
    image_path = soup.find("img").get("src")[11:]
    if is_edible == True:
        target_folder_path = species_base_path + "edible"
        copy_file(target_folder_path, image_path)
    elif is_edible == False:
        target_folder_path = species_base_path + "not_edible"
        copy_file(target_folder_path, image_path)


def check_edibility(path_to_species):
    with open(path_to_species, 'rb') as f:
        contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    main_block_divs = soup.find_all("div", {"class": "opis-modul"})
    for block in main_block_divs:
        if block.find("a").get("name") == "WARTOSC":
            value_description = block.find("div", {"class": "opis-tekst"}).text
            if "jadalny" in value_description.lower():
                return True
            else:
                return False
    return None

def copy_species_photo(soup):
    species_base_path = relative_path_to_data + "chosen_data/species/"

    description = soup.find("td", {"class": "foto-podpis-duzy"}).text
    if find_wrong_description(description):
        return

    species_name = find_species(soup)
    image_path = soup.find("img").get("src")[11:]
    target_folder_path = species_base_path + species_name
    copy_file(target_folder_path, image_path)

def copy_file(target_folder_path, image_path):
    image_base_path = relative_path_to_data + "grzyby/foto/"

    if not os.path.exists(target_folder_path):
        os.mkdir(target_folder_path)
    if not os.path.exists(target_folder_path + image_path):
        shutil.copy(image_base_path + image_path, target_folder_path)

def find_species(soup):
    name_div = soup.find("div", {"class": "foto2-tytul"})

    latin_name = name_div.find("span", {"class": "name-latin"}).text
    
    national_name= ""
    national_name_block = name_div.find("span", {"class": "nazwy-narodowe"})
    if national_name_block:
        national_name = "-" + national_name_block.text[3:]
    full_name = latin_name + national_name
    return full_name
    

def find_wrong_description(description):
    photo_has_not_allowed_type = any(
        not_allowed_word in description for not_allowed_word in not_allowed_photo_types)
    if photo_has_not_allowed_type:
        return True

    regexp = re.compile("x\d\d")
    microscope_photo = regexp.search(description)
    if microscope_photo:
        return True

    return False


array_of_file_paths = store_all_mushroom_files()
copy_photos(array_of_file_paths)
