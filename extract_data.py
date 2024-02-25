#support file to bbtn.py; makes the static/report.html
import json, os
def find_path(json_obj, target_value, path=None):
    if path is None:
        path = []

    # If the current JSON object is a dictionary
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_path = path + [key]
            if value == target_value:
                return new_path
            elif isinstance(value, (dict, list)):
                found_path = find_path(value, target_value, new_path)
                if found_path:
                    return found_path

    # If the current JSON object is a list
    elif isinstance(json_obj, list):
        for index, item in enumerate(json_obj):
            new_path = path + [index]
            if item == target_value:
                return new_path
            elif isinstance(item, (dict, list)):
                found_path = find_path(item, target_value, new_path)
                if found_path:
                    return found_path
    return None


def parse_slice(slice_str):
    
    parts = slice_str.split(":")
    start = int(parts[0]) if parts[0] else None
    end = int(parts[1]) if parts[1] else None
    return slice(start, end)

def get_elements_from_path_with_deep_slices(json_obj, path):
    def recursive_get(element, subpath):
        if not subpath:
            return [element] if element is not None else []

        key = subpath[0]
        next_subpath = subpath[1:]

        # Handle slice notation in subpath
        if isinstance(key, str) and ":" in key:
            if isinstance(element, list):
                slice_obj = parse_slice(key)
                sliced_elements = element[slice_obj]
                results = []
                for item in sliced_elements:
                    results.extend(recursive_get(item, next_subpath))
                return results
            else:
                return []

        # Handle direct key or index access
        elif isinstance(element, list):
            results = []
            for idx, item in enumerate(element):
                if isinstance(key, int) and idx == key:
                    # Direct index match in list
                    results.extend(recursive_get(item, next_subpath))
                elif isinstance(item, dict):
                    # Proceed if key is in dict regardless of direct index
                    temp_result = recursive_get(item.get(key, None), next_subpath)
                    if temp_result:
                        results.extend(temp_result)
            return results
        elif isinstance(element, dict):
            next_element = element.get(key, None)
            return recursive_get(next_element, next_subpath)
        else:
            return []

    return recursive_get(json_obj, path)


    
def get_elements_from_path_with_slice(json_obj, path):
    
    element = json_obj
    for key in path:
        if isinstance(element, list) and isinstance(key, str) and ":" in key:
            slice_obj = parse_slice(key)
            # Apply the slice to the list
            element = element[slice_obj]
        elif isinstance(element, list) and isinstance(key, str):
            # If the next path item is to be applied to each element in the list
            new_elements = []
            for item in element:
                try:
                    new_elements.append(item[key])
                except (KeyError, TypeError):
                    continue  # Skip items that do not have the key
            element = new_elements
        else:
            # Directly access the key or index
            element = element[key]
    return element

            
# Example usage
if __name__ == "__main__":
    # Load JSON data
    with open('response_cms.json', 'r') as file:
        json_data = json.load(file)
 
"""
    #this allows to find addesses and test for json data in response_cms.json

    target ="THE HEALTH CARE AUTHORITY FOR BAPTIST HEALTH"
    path = find_path(json_data, target)
    print("Path to the target value:", path)
    
    path =['eob_data', 'entry', 1, 'resource', 'contained', 0, 'name']
    elements = get_elements_from_path_with_slice(json_data, path)
    print("Elements at the given path:", elements)
    
    path =['eob_data', 'entry', '0:100', 'resource', 'contained', 0, 'name']
    elements = get_elements_from_path_with_deep_slices(json_data, path)
    print("Elements at the given path:", elements)"""
    
#coverage: ['coverage_data', 'entry', '0:3', 'resource', 'id']
#subscriberid ['coverage_data', 'entry', '0:3', 'resource', 'subscriberId']

#IP or opt ['eob_data', 'entry', '0:100', 'resource', 'id']
#site/ hospital ['eob_data', 'entry', '0:100', 'resource', 'contained', 0, 'name']
#state ['eob_data', 'entry', '0:100', 'resource', 'item', '1:100', 'locationAddress', 'state']



#start ['eob_data', 'entry', '0:10', 'resource', 'billablePeriod', 'start']
#end ['eob_data', 'entry', '0:10', 'resource', 'billablePeriod', 'end']
#diagnosis ['eob_data', 'entry', '0:100', 'resource', 'diagnosis', '0:10', 'diagnosisCodeableConcept', 'coding', '0:1', 'display']
#amount ['eob_data', 'entry', '0:100', 'resource', 'item', '0:100', 'adjudication', '0:100', 'amount', 'value']
#payment ['eob_data', 'entry', '0:100', 'resource', 'payment', 'amount', 'value']


# Assuming get_elements_from_path_with_deep_slices is already defined as per previous discussion
"""
def extract_information(json_obj):
    headings = get_elements_from_path_with_deep_slices(json_obj, ['eob_data', 'entry', '0:100', 'resource', 'id'])
    print(headings)
    locations = get_elements_from_path_with_deep_slices(json_obj, ['eob_data', 'entry', '0:100', 'resource', 'contained', 0, 'name'])
    print(locations)
    start_dates = get_elements_from_path_with_deep_slices(json_obj, ['eob_data', 'entry', '0:100', 'resource', 'billablePeriod', 'start'])
    end_dates = get_elements_from_path_with_deep_slices(json_obj, ['eob_data', 'entry', '0:10', 'resource', 'billablePeriod', 'end'])
    diagnoses = get_elements_from_path_with_deep_slices(json_obj, ['eob_data', 'entry', '0:100', 'resource', 'diagnosis', '0:10', 'diagnosisCodeableConcept', 'coding', '0:1', 'display'])
    costs = get_elements_from_path_with_deep_slices(json_obj, ['eob_data', 'entry', '0:100', 'resource', 'payment', 'amount', 'value'])
    print(costs)

    # Return a list of dictionaries for easier HTML generation
    return [
        {
            "heading": headings,
            "location": locations,
            "date_range": f"{start_dates} to {end_dates}",
            "diagnosis": diagnoses,
            "cost": costs
        }
        for heading, start, end, diagnosis, cost in zip(headings, start_dates, end_dates, diagnoses, costs)
    ]"""


def extract_information(json_obj):
    # Determine the range based on the actual length of 'entry' if possible
    entries_length = len(json_obj.get('eob_data', {}).get('entry', []))
    all_info = []

    for i in range(entries_length):
        # Directly build the path list for each attribute
        heading_path = ['eob_data', 'entry', i, 'resource', 'id']
        location_path = ['eob_data', 'entry', i, 'resource', 'contained', 0, 'name']
        start_date_path = ['eob_data', 'entry', i, 'resource', 'billablePeriod', 'start']
        end_date_path = ['eob_data', 'entry', i, 'resource', 'billablePeriod', 'end']
        diagnosis_path = ['eob_data', 'entry', i, 'resource', 'diagnosis', '1:100', 'diagnosisCodeableConcept', 'coding', '0:2', 'display']
        cost_path = ['eob_data', 'entry', i, 'resource', 'payment', 'amount', 'value']

        heading = get_elements_from_path_with_deep_slices(json_obj, heading_path)
        location = get_elements_from_path_with_deep_slices(json_obj, location_path)
        start_date = get_elements_from_path_with_deep_slices(json_obj, start_date_path)
        end_date = get_elements_from_path_with_deep_slices(json_obj, end_date_path)
        diagnosis = get_elements_from_path_with_deep_slices(json_obj, diagnosis_path)
        cost = get_elements_from_path_with_deep_slices(json_obj, cost_path)

        # Only add info if there's a heading
        formatted_diagnosis = '<br>'.join(diagnosis[0:10]) if diagnosis else "Unknown"
        formatted_cost = "$" + str(cost[0:2]) if cost else "Unknown"
        if heading:
            all_info.append({
                "heading": heading[0] if heading else "Unknown",
                "location": location[0] if location else "Unknown",
                "date_range": f"{start_date[0] if start_date else 'Unknown'} to {end_date[0] if end_date else 'Unknown'}",
                "diagnosis": formatted_diagnosis,
                "cost": formatted_cost
            })

    return all_info


def generate_html(data):
    html_content = "<html><head><title>Report</title></head><body>"
    html_content += "<h1>Report Details</h1>"
    for item in data:
        html_content += f"<div><h2>{item['heading']}</h2>"
        html_content += f"<p>Location: {item['location']}</p>"
        html_content += f"<p>Date Range: {item['date_range']}</p>"
        html_content += f"<p>Diagnosis: {item['diagnosis']}</p>"
        html_content += f"<p>Cost: {item['cost']}</p></div>"
    html_content += "</body></html>"
    return html_content

# Load JSON data
with open('response_cms.json', 'r') as file:
    json_data = json.load(file)

# Extract information
extracted_info = extract_information(json_data)

# Generate HTML
html = generate_html(extracted_info)

# Display or save the HTML content
#print(html)  # For demonstration, this will print the HTML to the console
# To save to a file, you could use:
os.makedirs('static', exist_ok=True)
with open('static/report.html', 'w') as html_file:
     html_file.write(html)


